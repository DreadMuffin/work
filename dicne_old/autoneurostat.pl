#!/usr/bin/perl -w

# script for running the Neurostat program and creating INC/DEC image
# Author: Andreas Hjortgaard Danielsen <andreas@hjortgaard.net>
#         Rigshospitalet
#         Klinik for Klinisk Fysiologi og Nuklearmedicin
#         PET- og Cyklotronenheden

use strict;
use Getopt::Long;
use Time::localtime;
use Cwd;

# OUTLINE
# - mincextract -signed -short -range 0 32767 -positive_direction image.mnc > image.img
# - copy image.img to NEUROSTAT_DIR/target.img
# - generate NEUROSTAT_DIR/target.hdr
# - run NEUROSTAT_DIR/neurostatrun
# - copy *.tif to temp_dir/
# - run createincdecs
# - result: targetINCDEC.tif

# TODO:
# - extract z-values to get color coding exact
# - write the used database name in QC image
# - make QC image larger by removing black area
# - what to do with patients under 19? Exit or write a warning in the image?
# - set up a daemon
# - Ian's extensions: Check angle after stereo. Group comparison.

sub select_database;
sub generate_header;
sub run_neurostat;
sub create_incdec;
sub generate_colormaps;

sub usage() {
  print STDOUT "Usage: $0 --neurostat_dir=path/to/neurostat --minc_dir=path/to/mincdir --temp_dir=path/to/temp --z=z1 --z=z2, ... --z=zN path/to/mincfile path/to/output\n";
}


MAIN: 
{
  
  my ($mincfile, $output_dir, $outputfile);
  my $database_dir;
  my $database_name;
  my $satlasmrSFMB;
  my @zvalues;
  my $max_z;
  
  # default values
  my $neurostat_dir = ".";
  my $minc_dir = "/usr/bin";
  my $temp_dir = "temp";
  my $hotcm = "inccm.ppm";
  my $coldcm = "deccm.ppm";
  my $image_min = 0;
  my $image_max = 32767;
  my @default_zvalues = (4,5,6,7); 
  
  # used in colormap generation
  # max_temperature: used to cut off extreme white colors. 1 = whole scale
  my $num_colors = 1024;
  my $max_temperature = 0.85;
  
  my $final_image_cols = 1183;
  my $final_image_rows = 625;

  
  if (@ARGV < 2) {
    usage();
    exit(0);
  }
  
  # get directory and z-value options  
  GetOptions('neurostat_dir=s' => \$neurostat_dir,'minc_dir=s' => \$minc_dir, 'temp_dir=s' => \$temp_dir, 'z=i',\@zvalues);
  
  if (!@zvalues) {
    @zvalues = @default_zvalues;
  }
  
  # get input file and output folder
  $mincfile       = $ARGV[0];
  $output_dir     = $ARGV[1];
   
  $database_dir = "$neurostat_dir/iSSP35-NMP-us/3DSSPDBSample";
  
  `cp $neurostat_dir/iSSP35-NMP-us/DosExec/satlasmrSFMB.* $temp_dir`;
  
  if ($mincfile =~ /.*\/(.+).mnc$/) { 
    $outputfile = $1;
  }
  else {
    $outputfile = "targetINCDEC";
  }
  
  # extract image data from Minc file and store as target.img in the neurostat directory
  `$minc_dir/mincextract -signed -short -range $image_min $image_max -positive_direction $mincfile > $temp_dir/target.img`;

  # select correct database, generate image file header, run neurostat and create INC/DEC image
  $database_name = select_database($minc_dir, $database_dir, $temp_dir, $mincfile);
  generate_header($temp_dir);
  run_neurostat($neurostat_dir, $temp_dir);
  
  # change permissions in temporary and output dirs.
  `chmod +rw $temp_dir/*.tif`;
  `chmod +rw $output_dir/*.tif`;
  
  # create INCDEC images for each z-score value
  generate_colormaps($temp_dir, $hotcm, $coldcm, $num_colors, $max_temperature);
  
  # create background images
  if (!(-e "$temp_dir/background.ppm") || !(-e "$temp_dir/background_mr.ppm" )) { 
    generate_backgrounds($final_image_cols,$final_image_rows,"$temp_dir/background.ppm","$temp_dir/background_mr.ppm");
  }
  
  
  foreach (@zvalues) {
    $max_z = $_;
    create_incdec($neurostat_dir, $temp_dir, $hotcm, $coldcm, $max_z);
    insert_labels($temp_dir, $minc_dir, $mincfile, $max_z);
    `cp $temp_dir/targetINCDEC.tif $output_dir/$outputfile\_z$max_z.tif`;
    `cp $temp_dir/targetINCDECMR.tif $output_dir/$outputfile\_MR\_z$max_z.tif`;
  }
  
  
  # copy QC to output folder and add database name
  `cp $temp_dir/targetAP.tif $output_dir/QC.tif`;
  `convert -font helvetica -pointsize 18 -fill white -draw "text 10,110 'Database: $database_name'" $output_dir/QC.tif $output_dir/QC.tif`;
  
  # clean up temp dir
  `rm -f $temp_dir/satlasmr*`;
  `rm -f $temp_dir/target*`;
  `rm -f $temp_dir/tempdb*`;
  
}

# select the correct database
sub select_database {
  
  my $res;
  my $age;
  my $minc_dir      = $_[0];
  my $database_dir  = $_[1];
  my $temp_dir      = $_[2];
  my $mincfile      = $_[3];
  my $db;
  
  
  # retrieve patient age
  $res = `$minc_dir/mincinfo -attvalue patient:age $mincfile`;
  if ($res =~ /0*(\d+)Y/) {
    $age = int($1);
  }
  
  if ($age < 32) {
    print STDOUT "Age: $age\nDatabase: FDG19-34\n";
    `cp $database_dir/3DSSPDBSampleFDG19-34AGLBMNSFM.dat $temp_dir/tempdbGLBMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG19-34AGLBSDSFM.dat $temp_dir/tempdbGLBSDSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG19-34ATHLMNSFM.dat $temp_dir/tempdbTHLMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG19-34ATHLSDSFM.dat $temp_dir/tempdbTHLSDSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG19-34ACBLMNSFM.dat $temp_dir/tempdbCBLMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG19-34ACBLSDSFM.dat $temp_dir/tempdbCBLSDSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG19-34APNSMNSFM.dat $temp_dir/tempdbPNSMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG19-34APNSSDSFM.dat $temp_dir/tempdbPNSSDSFM.dat`;
    $db = "3DSSPDBSampleFDG19-34A";
  } elsif ($age >= 31 && $age < 57) {
    print STDOUT "Age: $age\nDatabase: FDG31-60\n";
    `cp $database_dir/3DSSPDBSampleFDG31-60AGLBMNSFM.dat $temp_dir/tempdbGLBMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG31-60AGLBSDSFM.dat $temp_dir/tempdbGLBSDSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG31-60ATHLMNSFM.dat $temp_dir/tempdbTHLMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG31-60ATHLSDSFM.dat $temp_dir/tempdbTHLSDSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG31-60ACBLMNSFM.dat $temp_dir/tempdbCBLMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG31-60ACBLSDSFM.dat $temp_dir/tempdbCBLSDSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG31-60APNSMNSFM.dat $temp_dir/tempdbPNSMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG31-60APNSSDSFM.dat $temp_dir/tempdbPNSSDSFM.dat`;
    $db = "3DSSPDBSampleFDG31-60A";
  } else {
    print STDOUT "Age: $age\nDatabase: FDG55-91\n";
    `cp $database_dir/3DSSPDBSampleFDG55-91AGLBMNSFM.dat $temp_dir/tempdbGLBMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG55-91AGLBSDSFM.dat $temp_dir/tempdbGLBSDSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG55-91ATHLMNSFM.dat $temp_dir/tempdbTHLMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG55-91ATHLSDSFM.dat $temp_dir/tempdbTHLSDSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG55-91ACBLMNSFM.dat $temp_dir/tempdbCBLMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG55-91ACBLSDSFM.dat $temp_dir/tempdbCBLSDSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG55-91APNSMNSFM.dat $temp_dir/tempdbPNSMNSFM.dat`;
    `cp $database_dir/3DSSPDBSampleFDG55-91APNSSDSFM.dat $temp_dir/tempdbPNSSDSFM.dat`;
    $db = "3DSSPDBSampleFDG55-91A";  
  }
  return $db;
}


# routine for generating a Neurostat image header
sub generate_header {

  my $temp_dir = $_[0];
  
  open(HEADER, ">$temp_dir/target.hdr") or die("Unable to open file target.hdr");

  print HEADER "!data offset in bytes :=0\n";
  print HEADER "!imagedata byte order :=LITTLEENDIAN\n";
  print HEADER "!matrix size [1] :=128\n";
  print HEADER "!matrix size [2] :=128\n";
  print HEADER "!number format :=signed integer\n";
  print HEADER "!number of bytes per pixel :=2\n";
  print HEADER "scaling factor (mm/pixel) [1] :=2.000000\n";
  print HEADER "scaling factor (mm/pixel) [2] :=2.000000\n";
  print HEADER "!pixel scaling value :=32700.000000\n";
  print HEADER "!number of slices :=74\n";
  print HEADER "!slice thickness (mm/pixel) :=4.250000\n";
  print HEADER "!the right brain on the left   :=0\n";
  print HEADER "!the anterior to the posterior :=0\n";
  print HEADER "!the superior to the inferior  :=0\n";
  print HEADER "!END OF HEADER:=\n";

  close HEADER;

}

# run the Neurostat programs to generate individual INC and DEC files
sub run_neurostat {

  my $neurostat_dir = $_[0];
  my $temp_dir = $_[1];
  
  if (!(-e "$temp_dir/target.img") || !(-e "$temp_dir/target.hdr" )) {
    print STDERR "Neurostat run: Target files do not exist in $temp_dir\n";
    exit(1);
  }
  
  # run neurostat programs and generate tifs
  print STDOUT "Stereotactic Image Registration...\n";
  `$neurostat_dir/stereo $temp_dir/target.img $temp_dir/target -o4 -l0 -q1.0 -v-1.0`;  
  print STDOUT "Peak Cortical Pixel Detection...\n";
  `$neurostat_dir/ssploc $temp_dir/targetW.img $temp_dir/targetW -l0`;
  print STDOUT "Peak Cortical Pixel Sampling...\n";
  `$neurostat_dir/sspsmpl $temp_dir/targetW.img $temp_dir/targetWPX.lib $temp_dir/targetW -S1 -q1.0`;
  print STDOUT "3D-SSP Database Comparison...\n";
  `$neurostat_dir/sspcomp $temp_dir/targetWSFM.dat $temp_dir/tempdbGLB $temp_dir/targetWGLB 2 -z5.0 -q1000.0`;
  `$neurostat_dir/sspcomp $temp_dir/targetWSFM.dat $temp_dir/tempdbTHL $temp_dir/targetWTHL 1 -z5.0 -q1000.0`;
  `$neurostat_dir/sspcomp $temp_dir/targetWSFM.dat $temp_dir/tempdbCBL $temp_dir/targetWCBL 3 -z5.0 -q1000.0`;
  `$neurostat_dir/sspcomp $temp_dir/targetWSFM.dat $temp_dir/tempdbPNS $temp_dir/targetWPNS 4 -z5.0 -q1000.0`;
  print STDOUT "Creating TIFF files...\n";
  `$neurostat_dir/cnvttiff $temp_dir/targetAP.img $temp_dir/targetAP 0.0`;
  `$neurostat_dir/cnvttiff $temp_dir/target.img $temp_dir/target 0.0`;
  `$neurostat_dir/cnvttiff $temp_dir/targetS.img $temp_dir/targetS 0.0`;
  `$neurostat_dir/cnvttiff $temp_dir/targetW.img $temp_dir/targetW 0.0`;
  `$neurostat_dir/cnvttiff $temp_dir/targetWSFM.img $temp_dir/targetWSFM 0.0`;
  
}


# create INC/DEC target image
sub create_incdec {

  my $neurostat_dir = $_[0];  
  my $temp_dir      = $_[1];
  my $hotcm         = $_[2];
  my $coldcm        = $_[3];
  my $max_z         = $_[4];
  my $current_dir   = getcwd();
  
  # create tiffs with specified max z-score
  `$neurostat_dir/cnvttiff $temp_dir/targetWGLBZSFM.img $temp_dir/targetWGLBZSFM$max_z $max_z -g1`;
  `$neurostat_dir/cnvttiff $temp_dir/targetWGLBZSFN.img $temp_dir/targetWGLBZSFN$max_z $max_z -g1`;
  `$neurostat_dir/cnvttiff $temp_dir/targetWTHLZSFM.img $temp_dir/targetWTHLZSFM$max_z $max_z -g1`;
  `$neurostat_dir/cnvttiff $temp_dir/targetWTHLZSFN.img $temp_dir/targetWTHLZSFN$max_z $max_z -g1`;
  `$neurostat_dir/cnvttiff $temp_dir/targetWCBLZSFM.img $temp_dir/targetWCBLZSFM$max_z $max_z -g1`;
  `$neurostat_dir/cnvttiff $temp_dir/targetWCBLZSFN.img $temp_dir/targetWCBLZSFN$max_z $max_z -g1`;
  `$neurostat_dir/cnvttiff $temp_dir/targetWPNSZSFM.img $temp_dir/targetWPNSZSFM$max_z $max_z -g1`;
  `$neurostat_dir/cnvttiff $temp_dir/targetWPNSZSFN.img $temp_dir/targetWPNSZSFN$max_z $max_z -g1`;
  `$neurostat_dir/cnvttiff $temp_dir/satlasmrSFMB.img $temp_dir/satlasmrSFMB 0.0 -g1`;
  
  
  print STDOUT "Creating INC/DEC image with maximum $max_z...\n";
  
  # change folder to temp directory
  # set read permission for all tif files
  chdir($temp_dir) or die "$!";
  `chmod +r *.tif`;
  
  # convert tif images to Portable Graymap file 
  `tifftopnm < targetWSFM.tif > targetWSFM.ppm`;
  `tifftopnm < targetWGLBZSFN$max_z.tif > targetGLBINC.pgm`;
  `tifftopnm < targetWGLBZSFM$max_z.tif > targetGLBDEC.pgm`;
  `tifftopnm < targetWTHLZSFN$max_z.tif > targetTHLINC.pgm`;
  `tifftopnm < targetWTHLZSFM$max_z.tif > targetTHLDEC.pgm`;
  `tifftopnm < targetWCBLZSFN$max_z.tif > targetCBLINC.pgm`;
  `tifftopnm < targetWCBLZSFM$max_z.tif > targetCBLDEC.pgm`;
  `tifftopnm < targetWPNSZSFN$max_z.tif > targetPNSINC.pgm`;
  `tifftopnm < targetWPNSZSFM$max_z.tif > targetPNSDEC.pgm`;
  `tifftopnm < targetWPNSZSFM$max_z.tif > targetPNSDEC.pgm`;
  `tifftopnm < satlasmrSFMB.tif > satlasmrSFMB.pgm`;
  
  # convert to Portable Pixmap using the colormaps generated by generate_colormaps
  `pgmtoppm -map inccm.ppm targetGLBINC.pgm > targetGLBINC.ppm`;
  `pgmtoppm -map deccm.ppm targetGLBDEC.pgm > targetGLBDEC.ppm`;
  `pgmtoppm -map inccm.ppm targetTHLINC.pgm > targetTHLINC.ppm`;
  `pgmtoppm -map deccm.ppm targetTHLDEC.pgm > targetTHLDEC.ppm`;
  `pgmtoppm -map inccm.ppm targetCBLINC.pgm > targetCBLINC.ppm`;
  `pgmtoppm -map deccm.ppm targetCBLDEC.pgm > targetCBLDEC.ppm`;
  `pgmtoppm -map inccm.ppm targetPNSINC.pgm > targetPNSINC.ppm`;
  `pgmtoppm -map deccm.ppm targetPNSDEC.pgm > targetPNSDEC.ppm`;
  `pgmtoppm black-white satlasmrSFMB.pgm > satlasmrSFMB.ppm`;
  
  # create masks for compositing 
  `ppmcolormask black targetGLBINC.ppm > GLB_alphamask`;
  `ppmcolormask black targetTHLINC.ppm > THL_alphamask`;
  `ppmcolormask black targetCBLINC.ppm > CBL_alphamask`;
  `ppmcolormask black targetPNSINC.ppm > PNS_alphamask`;
  
  # compose INC and DEC images
  `pnmcomp -alpha=GLB_alphamask targetGLBINC.ppm < targetGLBDEC.ppm > targetGLBINCDEC.ppm`;
  `pnmcomp -alpha=THL_alphamask targetTHLINC.ppm < targetTHLDEC.ppm > targetTHLINCDEC.ppm`;
  `pnmcomp -alpha=CBL_alphamask targetCBLINC.ppm < targetCBLDEC.ppm > targetCBLINCDEC.ppm`;
  `pnmcomp -alpha=PNS_alphamask targetPNSINC.ppm < targetPNSDEC.ppm > targetPNSINCDEC.ppm`; 

  # crop images and add margin
  `pnmcrop -black targetWSFM.ppm | pnmmargin -black 10 > targetWSFM_crop.ppm`;
  `pnmcrop -black targetGLBINCDEC.ppm | pnmmargin -black 10 > targetGLBINCDEC_crop.ppm`;
  `pnmcrop -black targetTHLINCDEC.ppm | pnmmargin -black 10 > targetTHLINCDEC_crop.ppm`;
  `pnmcrop -black targetCBLINCDEC.ppm | pnmmargin -black 10 > targetCBLINCDEC_crop.ppm`;
  `pnmcrop -black targetPNSINCDEC.ppm | pnmmargin -black 10 > targetPNSINCDEC_crop.ppm`;
  `pnmcrop -black satlasmrSFMB.ppm | pnmmargin -black 10 | pnmpad -right=1 -top=1 > satlasmrSFMB_crop.ppm`;
  
  # compose MR image on top of targets with transparency 0.5
  `ppmmix 0.5 satlasmrSFMB_crop.ppm targetGLBINCDEC_crop.ppm > targetGLBINCDEC_MR.ppm`;
  `ppmmix 0.5 satlasmrSFMB_crop.ppm targetTHLINCDEC_crop.ppm > targetTHLINCDEC_MR.ppm`;
  `ppmmix 0.5 satlasmrSFMB_crop.ppm targetCBLINCDEC_crop.ppm > targetCBLINCDEC_MR.ppm`;
  `ppmmix 0.5 satlasmrSFMB_crop.ppm targetPNSINCDEC_crop.ppm > targetPNSINCDEC_MR.ppm`;
  
  # concatenate images top-down
  `pnmcat -black -topbottom targetGLBINCDEC_crop.ppm targetTHLINCDEC_crop.ppm > targetGLBTHL.ppm`;
  `pnmcat -black -topbottom targetCBLINCDEC_crop.ppm targetPNSINCDEC_crop.ppm > targetCBLPNS.ppm`;
  `pnmcat -black -topbottom targetGLBTHL.ppm targetCBLPNS.ppm > targetGLBTHLCBLPNS.ppm`;
  `pnmcat -black -topbottom targetWSFM_crop.ppm targetGLBTHLCBLPNS.ppm > targetALL.ppm`;
  
  `pnmcat -black -topbottom targetGLBINCDEC_MR.ppm targetTHLINCDEC_MR.ppm > targetGLBTHL_MR.ppm`;
  `pnmcat -black -topbottom targetCBLINCDEC_MR.ppm targetPNSINCDEC_MR.ppm > targetCBLPNS_MR.ppm`;
  `pnmcat -black -topbottom targetGLBTHL_MR.ppm targetCBLPNS_MR.ppm > targetGLBTHLCBLPNS_MR.ppm`;
  `pnmcat -black -topbottom satlasmrSFMB_crop.ppm targetGLBTHLCBLPNS_MR.ppm > targetMR.ppm`;
  
  # add color bars and adjust image to fit the background
  `pnmmargin -black 30 targetALL.ppm | pnmcrop -bottom > targetALLb.ppm`;
  `pnmcat -black -leftright -jbottom targetALLb.ppm colorbars.ppm > targetINCDEC.ppm`;
  
  # add color bars and adjust image to fit the background with MR
  `pnmmargin -black 30 targetMR.ppm | pnmcrop -bottom > targetMRb.ppm`;
  `pnmcat -black -leftright -jbottom targetMRb.ppm colorbars.ppm > targetINCDECMR.ppm`;
  
  # adjust the final image for background composition
  `pnmcrop -black targetINCDEC.ppm > targetINCDEC_crop.ppm`;
  `pnmmargin -black 80 targetINCDEC_crop.ppm > border_targetINCDEC.ppm`;
  
  `pnmcrop -black targetINCDECMR.ppm > targetINCDECMR_crop.ppm`;
  `pnmmargin -black 80 targetINCDECMR_crop.ppm > border_targetINCDECMR.ppm`;
  
  # compose with the background image (containing captions)
  `ppmcolormask black background.ppm > backgroundmask`;
  `pnmcomp -alpha=backgroundmask background.ppm < border_targetINCDEC.ppm > targetINCDEC.ppm`;
  
  `ppmcolormask black background_mr.ppm > backgroundmrmask`;
  `pnmcomp -alpha=backgroundmrmask background_mr.ppm < border_targetINCDECMR.ppm > targetINCDECMR.ppm`;
  
  `pnmtotiff < targetINCDEC.ppm > targetINCDEC.tif`;
  `pnmtotiff < targetINCDECMR.ppm > targetINCDECMR.tif`;
  
  # clean up
  `rm backgroundmask`;
  `rm backgroundmrmask`;
  `rm border_target*.ppm`;
  `rm target*.ppm`;
  `rm target*.pgm`;
  `rm *_alphamask`;
  
  # return to current folder
  chdir($current_dir) or die "$!";

}


# insert labels to the final TIF image
sub insert_labels {

  my $temp_dir  = $_[0];
  my $minc_dir  = $_[1];
  my $mincfile  = $_[2];
  my $max_z     = $_[3];
  my $current_dir   = getcwd();
  
  my $font = "helvetica";
  my $fontsize = "20";
  my $vert_jump = 97;
  my $vert_pos;
  my $horz_pos;
  
  my $min_z;
  my $steps;
  my $stepsize;
  my $zval;
  my $pos_step;
  my $max_pos;
  my $min_pos;
  my $zval_pos;
  
  my ($res, $ID, $name, $age, $sex, $acq_date, $acq_time, $tm, $current_datetime);
  
  #extract ID, age, sex, study time and current time
  $ID = `$minc_dir/mincinfo -attvalue patient:identification $mincfile`;
  
  $res = `$minc_dir/mincinfo -attvalue patient:full_name $mincfile`;
  if ($res =~ /([a-zA-Z]+)\^([a-zA-Z\ \_]+)/) {
    $name = "$1,$2";
  } else {
    $name = $res;
  }
  
  $res = `$minc_dir/mincinfo -attvalue patient:age $mincfile`;
  if ($res =~ /0*(\d+)Y/) {
    $age = int($1);
  } else {
    $age = $res;
  }
  
  $res = `$minc_dir/mincinfo -attvalue patient:sex $mincfile`;
  if ($res =~ /([a-zA-Z]+)\W*/) {
    $sex = "$1";
  } else {
    $sex = $res;
  }
  
  $res = `$minc_dir/mincinfo -attvalue acquisition:start_time $mincfile`;
  if ($res =~ /^(\d{4})(\d{2})(\d{2})/) {
    $acq_date = "$1/$2/$3";
  } else {
    $acq_date = "";
  }
  
  $res = `$minc_dir/mincinfo -attvalue acquisition:acquisition_time $mincfile`;
  if ($res =~ /^(\d{2})(\d{2})/) {
    $acq_time = "$1:$2";
  } else {
    $acq_time = $res;
  }
  
  
  $tm = localtime;
  $current_datetime = sprintf("%d/%02d/%02d %02d:%02d",$tm->year+1900, ($tm->mon)+1, $tm->mday, $tm->hour, $tm->min);
  
  # use convert command to draw text (views, database names)
  print STDOUT "Inserting labels...\n";
  
  
  chdir($temp_dir) or die "$!";
  
  # draw study specific text (ID, date, z-values)
  
  # z-values
  $fontsize = 16;
  $min_z = 1;
  $steps = 4;
  $stepsize = ($max_z-$min_z)/($steps-1);
  
  # INC z-values
  $horz_pos = 1110;
  $max_pos = 156;
  $min_pos = 336;
  $zval = sprintf("%.2f",$max_z);
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$max_pos '$zval'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$max_pos '$zval'" targetINCDECMR.tif targetINCDECMR.tif`;
  $zval = sprintf("%.2f",$min_z);
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$min_pos '$zval'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$min_pos '$zval'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  $pos_step = ($max_pos-$min_pos)/($steps-1);
  $zval = sprintf("%.2f",$min_z + $stepsize);
  $zval_pos = $min_pos + $pos_step;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$zval_pos '$zval'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$zval_pos '$zval'" targetINCDECMR.tif targetINCDECMR.tif`;
  $zval = sprintf("%.2f",$min_z + 2*$stepsize);
  $zval_pos = $min_pos + 2*$pos_step;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$zval_pos '$zval'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$zval_pos '$zval'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  # DEC z-values
  $min_pos = 365;
  $max_pos = 545;
  $zval = sprintf("%.2f",$max_z);
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$max_pos '$zval'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$max_pos '$zval'" targetINCDECMR.tif targetINCDECMR.tif`;
  $zval = sprintf("%.2f",$min_z);
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$min_pos '$zval'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$min_pos '$zval'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  $pos_step = ($max_pos-$min_pos)/($steps-1);
  $zval = sprintf("%.2f",$min_z + $stepsize);
  $zval_pos = $min_pos + $pos_step;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$zval_pos '$zval'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$zval_pos '$zval'" targetINCDECMR.tif targetINCDECMR.tif`;
  $zval = sprintf("%.2f",$min_z + 2*$stepsize);
  $zval_pos = $min_pos + 2*$pos_step;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$zval_pos '$zval'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$zval_pos '$zval'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  # misc info (ID, age, database)
  
  $fontsize = 18;
  $vert_pos = 600;
  $horz_pos = 80;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'ID: $ID'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'ID: $ID'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  $vert_pos = 620;
  $horz_pos = 80;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Name: $name'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Name: $name'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  $vert_pos = 600;
  $horz_pos = 460;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Age: $age'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Age: $age'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  $vert_pos = 620;
  $horz_pos = 460;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Sex: $sex'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Sex: $sex'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  $vert_pos = 600;
  $horz_pos = 725;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Acquisition date: $acq_date'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Acquisition date: $acq_date'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  $vert_pos = 620;
  $horz_pos = 725;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Acquisition time: $acq_time'" targetINCDEC.tif targetINCDEC.tif`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Acquisition time: $acq_time'" targetINCDECMR.tif targetINCDECMR.tif`;
  
  # return to current folder
  chdir($current_dir) or die "$!";

}

# generate the color maps used for making the INC/DEC image
sub generate_colormaps {
  
  my $temp_dir        = $_[0];
  my $hotcm           = $_[1];
  my $coldcm          = $_[2];
  my $num_colors      = $_[3];
  my $max_temperature = $_[4];
  my $current_dir   = getcwd();
  
  # the maximum temperature allowed (in percentage)
  # used to cut off extreme white colors
  my $init_num_colors = int(($num_colors/$max_temperature)/3)+1;
  
  chdir($temp_dir) or die "$!";
  
  print STDOUT "Generating colormaps...\n";
  
  # create a gray ramp and convert to pixmap
  # hot (black-red-yellow-white)
  `pgmramp -tb 30 $init_num_colors > colormap.pgm`;
  `pgmtoppm black-red colormap.pgm > blackred.ppm`;
  `pgmtoppm red-yellow colormap.pgm > redyellow.ppm`;
  `pgmtoppm yellow-white colormap.pgm > yellowwhite.ppm`;
  `pnmcat -topbottom blackred.ppm redyellow.ppm > blackyellow.ppm`;
  `pnmcat -topbottom blackyellow.ppm yellowwhite.ppm > hot.ppm`;

  # cold (black-blue-cyan-white)
  `pgmtoppm black-blue colormap.pgm > blackblue.ppm`;
  `pgmtoppm blue-cyan colormap.pgm > bluecyan.ppm`;
  `pgmtoppm cyan-white colormap.pgm > cyanwhite.ppm`;
  `pnmcat -topbottom blackblue.ppm bluecyan.ppm > blackcyan.ppm`;
  `pnmcat -topbottom blackcyan.ppm cyanwhite.ppm > cold.ppm`;
  
  # cut off extreme white
  `pnmcut -height $num_colors hot.ppm > hot_cut.ppm`;
  `pnmcut -height $num_colors cold.ppm > cold_cut.ppm`;
  
  # create colormap
  `pnmcolormap -sort all hot_cut.ppm > $hotcm`;
  `pnmcolormap -sort all cold_cut.ppm > $coldcm`;

  # create color bars for result image
  `pnmflip -topbottom hot_cut.ppm > hotflip.ppm`;
  `pnmcat -black -topbottom hotflip.ppm cold_cut.ppm > colorbar.ppm`; 
  `pnmscale -xsize 10 -ysize 400 colorbar.ppm > colorbars.ppm`;

  # clean up
  `rm colormap.pgm`;
  `rm blackred.ppm redyellow.ppm yellowwhite.ppm blackyellow.ppm hot.ppm hot_cut.ppm`;
  `rm blackblue.ppm bluecyan.ppm cyanwhite.ppm blackcyan.ppm cold.ppm cold_cut.ppm`;
  `rm hotflip.ppm colorbar.ppm`;
  
  # return to current folder
  chdir($current_dir) or die "$!";
}

# generate background images with constant labels
# make black PPM images of the given size and insert texts 
sub generate_backgrounds {
  
  my $cols      = $_[0];
  my $rows      = $_[1];
  my $bg_file   = $_[2];
  my $bgmr_file = $_[3];
  my ($i,$j);
  
  my $font = "helvetica";
  my $fontsize = "20";
  my $vert_jump = 97;
  my $vert_pos;
  my $horz_pos;
  
  print STDOUT "Creating background images...\n";
  
  # initialize PPM image headers
  open (BACKGROUND,'>:raw',"$bg_file") or die("Unable to open file $bg_file");
  print BACKGROUND "P6\n";
  print BACKGROUND "# created by Andreas Hjortgaard Danielsen's automatic Neurostat program\n";
  print BACKGROUND "$cols $rows\n";
  print BACKGROUND "255\n";
  
  for ($i=0;$i<$rows;$i++) {
    for ($j=0;$j<$cols;$j++) {
      print BACKGROUND pack("C",0); # red
      print BACKGROUND pack("C",0); # green
      print BACKGROUND pack("C",0); # blue
    }
  } 
  close BACKGROUND;
  
  open (BACKGROUND_MR,'>:raw',"$bgmr_file") or die("Unable to open file $bgmr_file");
  print BACKGROUND_MR "P6\n";
  print BACKGROUND_MR "# created by Andreas Hjortgaard Danielsen's automatic Neurostat program\n";
  print BACKGROUND_MR "$cols $rows\n";
  print BACKGROUND_MR "255\n";
  
  for ($i=0;$i<$rows;$i++) {
    for ($j=0;$j<$cols;$j++) {
      print BACKGROUND_MR pack("C",0); # red
      print BACKGROUND_MR pack("C",0); # green
      print BACKGROUND_MR pack("C",0); # blue
    }
  } 
  close BACKGROUND_MR;
  
  
  # title
  $fontsize = 22;
  $vert_pos = 20;
  $horz_pos = 470;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'PET FDG Neurostat'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'PET FDG Neurostat'" $bgmr_file $bgmr_file`;
  
  # views
  $vert_pos = 72;
  $horz_pos = 85;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'RT.LAT'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'RT.LAT'" $bgmr_file $bgmr_file`;
  $horz_pos = 215;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'LT.LAT'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'LT.LAT'" $bgmr_file $bgmr_file`;
  $horz_pos = 355;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'SUP'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'SUP'" $bgmr_file $bgmr_file`;
  $horz_pos = 485;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'INF'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'INF'" $bgmr_file $bgmr_file`;
  $horz_pos = 610;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'ANT'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'ANT'" $bgmr_file $bgmr_file`;
  $horz_pos = 730;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'POST'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'POST'" $bgmr_file $bgmr_file`;
  $horz_pos = 850;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'RT.MED'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'RT.MED'" $bgmr_file $bgmr_file`;
  $horz_pos = 980;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'LT.MED'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'LT.MED'" $bgmr_file $bgmr_file`;
  
  
  # left-right
  $fontsize = 16;
  $vert_pos = 160;
  $horz_pos = 340;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'L'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'L'" $bgmr_file $bgmr_file`;
  $horz_pos = 400;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'R'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'R'" $bgmr_file $bgmr_file`;
  
  $horz_pos = 465;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'R'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'R'" $bgmr_file $bgmr_file`;
  $horz_pos = 525;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'L'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'L'" $bgmr_file $bgmr_file`;
  
  $horz_pos = 595;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'R'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'R'" $bgmr_file $bgmr_file`;
  $horz_pos = 655;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'L'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'L'" $bgmr_file $bgmr_file`;
  
  $horz_pos = 725;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'L'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'L'" $bgmr_file $bgmr_file`;
  $horz_pos = 785;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'R'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'R'" $bgmr_file $bgmr_file`;
  
 
  # database names
  $fontsize = 20;
  $horz_pos = 30;
  $vert_pos = 120;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'MRI'" $bgmr_file $bgmr_file`;
  $vert_pos = $vert_pos + $vert_jump;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'GLB'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'GLB'" $bgmr_file $bgmr_file`;
  $vert_pos = $vert_pos + $vert_jump;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'THL'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'THL'" $bgmr_file $bgmr_file`;
  $vert_pos = $vert_pos + $vert_jump;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'CBL'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'CBL'" $bgmr_file $bgmr_file`;
  $vert_pos = $vert_pos + $vert_jump;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'PNS'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'PNS'" $bgmr_file $bgmr_file`;
  
  # z colorbars
  $fontsize = 20;
  $horz_pos = 1092;
  $vert_pos = 135;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Z'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'Z'" $bgmr_file $bgmr_file`;
  
  $fontsize = 16;
  $horz_pos = 1110;
  $vert_pos = 130;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'INC'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'INC'" $bgmr_file $bgmr_file`;
  $vert_pos = 580;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'DEC'" $bg_file $bg_file`;
  `convert -font $font -pointsize $fontsize -fill white -draw "text $horz_pos,$vert_pos 'DEC'" $bgmr_file $bgmr_file`;
  
  
}

