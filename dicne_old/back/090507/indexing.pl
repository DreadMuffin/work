#!/usr/bin/perl -s

### init

$initdir = "/users/scratch/dicne/data"; # path for dicne-initdir
chdir($initdir); # make sure we are in initdir, the presumed location for data

#### mapping of datasets
# search through data, using /usr/local/dicom/bin/./dcmdump all_files_in_data |grep "{tag}"
# series-tag: (0020,000e), CPR-number: (0010,0020), patient's name (0010,0010), series time (0008,0031).

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
			open (DCMDUMP, "/usr/local/dicom/bin/./dcmdump $file +P 0008,0031 +P 0010,0010 +P 0010,0020 +P 0020,000e -s
			|");
			while (<DCMDUMP>) {
			$_ =~ /\[(.+)\]/;
			push(@header,$1); # @header is now 4N, and [nN, (1+n)N, (2+n)N, (3+n)N] equals [series, CPR, name, time]
			$header_path_tmp = `pwd`;
			chop($header_path_tmp);		
			push(@header_path,$header_path_tmp); # @header_path is now 4N, and all equals path of corrosponding @header
			}
			close DCMDUMP;
		}
	}
	return 0;
}

#####################

### /recursive

### Initiate recursive mapping-sub
&dir_list;

### Prints

#foreach (@filelist) {
#	print "$_\n";
#}

#print "\n";
#
#foreach (@dirlist) {
#	print "$_\n";
#}
#
#print "\n";

### /Prints

#### conversion of datasets

# with the complete header, we can sort those out that are recurring and put the rest in @series, %name and %id

# define initial series
@series = $header[0];
$id{"$series[$#series]"} = "$header[1]";
$name{"$series[$#series]"} = "$header[2]";
$path{"$series[$#series]"} = "$header_path[0]";
$time{"$series[$#series]"} = "$header[3]";

## loop through @header, defining unique series and drawing out relevant information

for ($i = 0; $i < (scalar @header)/4; $i++) {
	if ($header[$i*4] ne $series[$#series]) {
		my $found = 0;
		foreach (@series){
			if ($header[$i*4] eq $_) {
				$found = 1;
			}
		}
		unless ($found == 1) {		
			$series[$#series+1] = $header[$i*4];
			$id{"$series[$#series]"} = "$header[$i*4+1]";
			$name{"$series[$#series]"} = "$header[$i*4+2]";
			$path{"$series[$#series]"} = "$header_path[$i*4]";
			$time{"$series[$#series]"} = "$header[$i*4+3]";
		}
	}
}

### Prints

#print "De samlede serier\n";
#foreach (@series) {
#	print "$_\n";
#}
#print "ScalarHeader er " . scalar @header . "\n";
#print "ScalarSeries er " . scalar @series . "\n";
#print "ValuesPath er " . values(%path) . "\n";
#print "KeysPath er " . keys(%path) . "\n";
#

### troublesome output-form for use in perl

foreach (@series) {
	$id_ph =	$id{"$_"};
	print "$id_ph| ";
	$name_ph =	$name{"$_"};
	print "$name_ph| ";
	print "$_| ";
	$path_ph =	$path{"$_"};
	print "$path_ph| ";
	$time_ph =	$time{"$_"};
	print "$time_ph| ";
	}

### /Prints

#### assumptions

# every scanned directory contains only one series
# dcm2mnc -dname X - X must be defines as string with no sub-/
