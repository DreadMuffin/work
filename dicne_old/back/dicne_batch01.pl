#!/usr/bin/perl -s

#################################################
# dicne - DICom to NEurostat converter program 	#
# developed spring 2009									#
# copyright Mikkel Oeberg, 2009						#
#																#
# version 0.1.5 [alpha]									#
# 27.02.2009												#
#################################################

# TEMP - clean converted files
#remove = `rm -f conv/*`;

### init

$initdir = "/users/scratch/Mikkel/dicne/data"; # path for dicne-initdir
$convdir = $initdir . "/conv"; # path for dicne-convdir
chdir($initdir); # make sure we are in initdir

#### sorting of datasets
# search through data, using /usr/local/dicom/bin/./dcmdump all_files_in_data |grep "{tag}"
# series-tag: (0020,000e), CPR-number: (0010,0020), patient's name (0010,0010).

# this part will be made recursive to map the entire directory

### recursive

sub dir_list
{
	my ($dir) = @_;
	my @files;
	
	if (!opendir(DIR, ".")) {
		return -1;
	}else{
		@files = readdir(DIR);
		closedir(DIR);
	}
	foreach my $file (@files){
		next if $file eq "." || $file eq "..";
		if (-d $file){
			if (chdir($file)){
			push(@dirlist,$file);
				&dir_list($dir eq "" ? $file : "$dir/$file");
				chdir("..");
			}
		}elsif (-f $file){
			push(@filelist,$file);
			
		}
	}
	return 0;
}

#####################

### /recursive

&dir_list;

foreach (@filelist) {
	print "$_\n";
}

print "\n";

foreach (@dirlist) {
	print "$_\n";
}

print "\n";

#####################

# noget foreach $currdir = @dirlist, fyr det hele i headeren og gem $currdir i @header_path
open (DCMDUMP, "/usr/local/dicom/bin/./dcmdump $currdir/*.dcm +P 0010,0010 +P 0010,0020 +P 0020,000e -s
|");
while (<DCMDUMP>) {
$_ =~ /\[(.+)\]/;
push(@header,$1); # @header is now 3N, and [nN, (1+n)N, (2+n)N] equals [series, CPR, name]
push(@header_path,`pwd`); # @header_path is now 3N, and all equals path of corrosponding @header
}
close DCMDUMP;

#####################



### with the complete header, we can sort those out that are recurring and put the rest in @series, %name and %id

# define initial series
@series = $header[0];
$id{"$series[$#series]"} = "$header[1]";
$name{"$series[$#series]"} = "$header[2]";
$path{"$series[$#series]"} = "$header_path[0]";

## loop through @header, defining unique series and drawing out relevant information

for ($i = 0; $i < (scalar @header)/3; $i++) {
	if ($header[$i*3] ne $series[$#series]) 
		{
		$series[$#series+1] = $header[$i*3];
		$id{"$series[$#series]"} = "$header[$i*3+1]";
		$name{"$series[$#series]"} = "$header[$i*3+2]";
		$path{"$series[$#series]"} = "$header_path[$i*3]";
	}
}

### Prints

print "De samlede serier\n";
print "@series\n"; #test
print "ScalarHead er " . scalar @header . "\n";
print "ScalarSeries er " . scalar @series . "\n";
print "ValuesPath er " . values(%path) . "\n";
print "KeysPath er " . keys(%path) . "\n";
print "path[0] is $path{\"$series[0]\"}\n";

### /Prints

# converts all .dcm files in data to mnc, and puts these in conv
# converts all .mnc files in conv to nii/analyze/short, and names these conv/niiconv
foreach (@series) {
	$dcm2mnc_out = `/usr/local/mni/bin/dcm2mnc $currdir/*.dcm -dname conv -fname $_ .`;
	$mnc2nii_out = `/usr/local/mni/bin/mnc2nii -analyze -short $convdir/$_.mnc $convdir/$_`;
}

## history

# 0.1 [alpha] - converts dicom data
# 0.1.5 - converts all available dicom data into seperate analyze-files 
# 0.2 - select specific series to convert 
# 0.3 - user is listed all series, selects some, and these are converted
# 0.4 - validation of data in neurostat
# 0.5 - basic php-interface for listing multiple series
# 0.6 - basic php-interface for selecting a series and executing conversion
# 0.7 [beta] - check-boxes allow selection of multiple series, followed by conversion
# 0.8 [beta] - 
# 0.9 [beta] - 
# 1.0 [release] - initial release

#### Assumptions

# every scanned directory contains only one series
# dcm2mnc -dname X - X must be defines as string with no sub-/
