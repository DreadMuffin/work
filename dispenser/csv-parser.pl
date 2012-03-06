#!/usr/bin/perl

use strict;
#use warnings;

my $file = @ARGV[0];
my $line;
my $ext;
my $start = 0;
my @series;
my @lines;
my $res;
my $i;
my $cfg = "config.txt";
my $charge_save;
my $dir = ".";
my @files;
my $cur;
my $max = 0;

open (CFG, $cfg);

if (@lines = <CFG>) {
    $i = $lines[0];
    $charge_save = $lines[1];
}
else {
    $i = 1;
    $charge_save = "";
}

opendir(DIR, $dir) or die("Couldn't get VAL directory listing!\n");

@files = readdir(DIR);
while (@files) {
    $cur = shift(@files);
    $cur =~ /^VAL.(\d*)$/;
    if ($1 > $max) {
        $max = $1;
    }
}

if ($max >= $i) {
    die("Old VAL-files are still in the VAL-directory!\n");
}


my ($customer, $part, $charge, $depotpos, $filldate, $filltime, $activity,
    $volume, $gros, $tare, $net, $product);

# Hardcoded values for legacy reasons
$product = "F18";

open(FILE, $file) or die("File $file not found!\n");

while($line = <FILE>) {
    # We pick out the series-specific information
    if ($line =~ /Lot ID:,([a-zA-Z0-9\-]*),/) {
        if ($1 ne $charge_save) {
            $charge = "$1";
        }
        else {
            print STDOUT "Current series already done, aborting...";
            exit 0;
        }
    };
    # Check for the line after series end
    if($line =~ /Note:/) {
        $start = 0;
    }

    if ($start) {
        @series = split(/,/, $line);
        $ext = sprintf("%03d",$i);
        
        $customer = $series[1];
        $part = $i;
        $depotpos = 1;
        $series[0] =~ /(\S*) (\S*)/;
        $filldate = $1;
        $filltime = $2;
        $series[5] =~ /(.*);/;
        $activity = $1;
        $volume = $series[4];
        $gros = "0 g";
        $tare = "0 g";
        $net = "0 g";

        # Write the data to files of the type VAL.001, VAL.002 etc
        print "Writing to VAL.$ext...\n";
        open(VAL, ">VAL.$ext") or die("Couldn't create file number $i");
        print VAL    "customer:  $customer\n";
        print VAL    "part:      $part\n";
        print VAL    "charge:    $charge\n";
        print VAL    "depotpos:  $depotpos\n";
        print VAL    "filldate:  $filldate\n";
        print VAL    "filltime:  $filltime\n";
        print VAL    "activity:  $activity\n";
        print VAL    "volume:    $volume\n";
        print VAL    "gros:      $gros\n";
        print VAL    "tare:      $tare\n";
        print VAL    "net:       $net\n";
        print VAL    "product:   $product\n";

        $i++;
}

    # Check for the line before the series start
    if($line =~ /Before/) {
        $start = 1;
    }

}

#Create or update the config file
open(CFG, ">$cfg") or die("Couldn't write config file!\n");

print CFG "$i\n";
print CFG "$charge";
