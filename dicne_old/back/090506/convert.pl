#!/usr/bin/perl -w

# converts all .dcm files in data to mnc, and puts these in $initdir/conv
# converts all .mnc files in conv to nii/analyze/short, and names these conv/niiconv

# load the parameters outputted from dicne.php

use CGI;

my $cgi = new CGI;
print $cgi->header('text/html');

@check = $cgi->param('check');

@path = $cgi->param('path');

@series = $cgi->param('series');

@resample = $cgi->param('resample');

foreach (@check) {
	print "Foelgende check er valgt: $_<br>";
}

print "<br>";

foreach (@path) {
	print "Foelgende path er outputtet: $_<br>";
}

print "<br>";

foreach (@series) {
	print "Foelgende serie er outputtet: $_<br>";
}

print "<br>";

foreach (@resample) {
	print "Foelgende resamples er valgt: $_<br>";
}

print "<br>";

## run through @check, converting on the go

## somewhere in here, fit a resampling loop which checks if the index of resample fits check,
## and if true, resample mnc. before converting to nii

# note - converted files are placed in conv dir at guest/~

@c = ("x","y","z"); # defined for use in resample-loop
$chk_cnt = 0;

foreach (@check) {
	print "<br>check er: $_<br>";
	print "path er: $path[$_]<br>";
	print "serie er: $series[$_]<br>";
	$dcm2mnc_out = `ssh guest\@goya2 /usr/local/mni/bin/dcm2mnc -clobber $path[$_]/*.dcm -dname conv -fname $series[$_] .`;
	$series[$_] =~ s/^.//; # remove unwanted space at the beginning of $series[$chk], but only for [1+] as there is no /n in front of first series	
	# if-loop resamples in case defined	
	$chk = $_;
	foreach (@resample) {
	print "Resample er |$_|<br>";
		if ($_ == $check[$chk_cnt]) {
		print "Check er |$check[$chk_cnt]|<br>";
			# loop for all dimensions, and draw out resampling value		
			foreach $co (@c) {
				$space_string = $co . "space";
				$space = `ssh guest\@goya2 /usr/local/mni/bin/mincinfo -dimlength $space_string ~guest/conv/$series[$chk].mnc`;
				$space_rel = $space/128; # the relation pix_old/pix_new
				$step = `ssh guest\@goya2 /usr/local/mni/bin/mincinfo -attvalue $space_string:step ~guest/conv/$series[$chk].mnc`;
				$step_new = $step * $space_rel;
				push (@steps_new, $step_new);			
				print "Her er |" . $space . "|<br>";
				print "Her er |" . $step . "|<br>";
				chop ($step);
				chop ($space);
			}
			# $space is currently for zspace, and $step is currently for zstep 	
		 	$mincresample_out = `ssh guest\@goya2 /usr/local/mni/bin/mincresample -clobber -nelements 128 128 $space -step $steps_new[0] $steps_new[1] $step ~guest/conv/$series[$chk].mnc ~guest/conv/resample.mnc`;
			# it is not possible to overwrite directly in mincresample, therefore placeholder resample.mnc is created
			$mincresample_overwrite = `ssh guest\@goya2 /bin/mv -f ~guest/conv/resample.mnc ~guest/conv/$series[$chk].mnc`;	 	
		 	undef (@steps_new);
		}	
	}	
	$mnc2nii_out = `ssh guest\@goya2 /usr/local/mni/bin/mnc2nii -analyze -short ~guest/conv/$series[$_].mnc ~guest/conv/$series[$_]`;
	$chk_cnt++;
}

## move data from ~guest/conv/* to /users/scratch/dicne/conv/
$mv_final = `ssh guest\@goya2 /bin/mv -f ~guest/conv/* /users/scratch/dicne/conv/`;
