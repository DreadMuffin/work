#!/usr/bin/perl

# converts all .dcm files in data to mnc, and puts these in $initdir/conv
# converts all .mnc files in conv to nii/analyze/short, and names these conv/niiconv
chdir($initdir); # to make sure we are once again in the initdir
foreach (@series) {
	$dcm2mnc_out = `/usr/local/mni/bin/dcm2mnc $path{"$_"}/*.dcm -dname conv -fname $_ .`;
	$mnc2nii_out = `/usr/local/mni/bin/mnc2nii -analyze -short $initdir/conv/$_.mnc $initdir/conv/$_`;
}