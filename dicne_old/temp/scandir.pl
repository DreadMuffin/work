#!/usr/bin/perl -s

$dir = `pwd`;

sub DirList {
	undef @locallist;
	my @locallist = `ls`;
	for (@locallist) {	
		chop $_;	
		if (-d $_){
			unless (grep($_, @dirlist)){
				print "Der var et direktorie: $_ hed det\n";			
				$dir = shift;
				print "Dir is $dir\n";				
				push(@dirlist,$dir);
				print "Dirlist : @dirlist\n";
				chdir $_;
				&DirList;		
			}
		} else {
			print "$_ er ikke et dir\n";
		}
		
	}
}
#####################

### /recursive
&DirList;

print "@dirlist\n";