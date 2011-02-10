# dcbo-minmax-dists.pl
# 8 feb 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Given a file of distances between every
# biography in a multidimensional feature
# space, output files of pairs that are
# unusually close or unusually distant.

my ($id, $dist, @fields, %distances);

# Open the distance file
my $distances = 'dcbo-vol1-distances.txt';
open(INPUT, "<$distances") || die "Couldn't open distance file.";

# Read contents into hash table
while(<INPUT>) {
    chomp;
    @fields = split /,/;
    $id = shift @fields;
    # $id =~ s/\"//g;
    $dist = shift @fields;
    $distances{$id} = $dist;
}

my $outminfile = 'dcbo-vol1-min-dists.txt';
my $outmaxfile = 'dcbo-vol1-max-dists.txt';
open(OUTMIN, ">$outminfile");
open(OUTMAX, ">$outmaxfile");
my @sortidpairs = sort keys (%distances);
foreach $k (@sortidpairs) {
    if ($distances{$k} >= 0.8) {
        print OUTMAX "$k," . $distances{"$k"} . "\n";
    } elsif (($distances{$k} <= 0.05) && ($distances{$k} > 0)) {
        print OUTMIN "$k," . $distances{"$k"} . "\n";
    }
}

close(INPUT);
close(OUTMIN);
close(OUTMAX);



