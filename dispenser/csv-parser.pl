#!/usr/bin/perl

use strict;
#use warnings;

my @inputfiles = @ARGV;
my $file;
my $line;
my $ext;
my $start = 0;
my @series;
my @lines;
my $res;
my $i = 1;
my $charge_save;
my $dir = "/users/scratch/dispenser";
my @files;
my $cur;
my $max = 0;


sub csv_parser {
    if (not @inputfiles) {
        print "Need at least one filename as argument, exiting...\n";
        exit 0
    }

    while (@inputfiles) {

        $file = shift(@inputfiles);

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
                $series[0] =~ /(\d{2}).(\d{2}).\d{2}?(\d{2}) (\d{2}).(\d{2}).(\d{2})/;
                $filldate = "$1.$2.$3";
                $filltime = "$4:$5:$6";
                $series[5] =~ /(.*);/;
                $activity = $1;
                $volume = $series[4];
                $gros = "0 g";
                $tare = "0 g";
                $net = "0 g";


                # This was the quickest way to do it...
                # do (an inefficient) linear search in order to find an 
                # extension not taken, so files are not overwritten.
                # This should be ok as the files are moved away fast.
                STAT:
                if (stat("VAL.$ext")) {
                    $ext++;
                    goto STAT;
                }

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

    }
}1;
