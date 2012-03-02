#!/usr/bin/perl

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
	print "Foelgende serie er valgt: $_<br>";
}

print "<br>";

foreach (@path) {
	print "Foelgende path er outputtet: $_<br>";
}

print "<br>";

foreach (@series) {
	print "Foelgende serie er outputtet: $_<br>";
}

print "<br><br>";

## run through @check, converting on the go

foreach (@check) {
	print "check er: $_<br>";
	print "path er: $path[$_]<br>";
	print "serie er: $series[$_]<br><br>";
	$dcm2mnc_out = `ssh guest@goya2 /usr/local/mni/bin/dcm2mnc $path[$_]/*.dcm -dname ./conv -fname $series[$_] .`;
	$mnc2nii_out = `ssh guest@goya2 /usr/local/mni/bin/mnc2nii -analyze -short conv/$series[$_].mnc conv/$series[$_]`;
}














