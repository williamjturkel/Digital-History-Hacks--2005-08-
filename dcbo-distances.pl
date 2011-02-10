# dcbo-distances.pl
# 8 feb 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Given a spreadsheet of biographies located in
# a multidimensional feature space, return a file
# of distances between each. Simply counts
# features that both bios have in common,
# or both lack.

my ($id, @fields, %vectors, %distances);

# Open the feature spreadsheet
my $featurespace = 'dcbo-vol1-featurespace.csv';
open(INPUT, "<$featurespace") || die "Couldn't open feature space file.";

# Throw away header record
$id = <INPUT>;

# Hash the vector for each biography as a long bit string
while(<INPUT>) {
    chomp;
    @fields = split /,/;
    $id = shift @fields;
    $id =~ s/\"//g;
    $vectors{$id} = join "", @fields;
}
close(INPUT);

# For each ID, measure distance from all remaining IDs.
# We need to process the IDs to create upper triangular
# portion of matrix. The distances are stored in a
# hash table of lowID:highID => distance
my $outfile = 'dcbo-vol1-distances.txt';
open(OUTPUT, ">$outfile");
my @sortids = sort keys (%vectors);
my $lastid = $sortids[-1];
foreach $k (@sortids) {
    for ($j = $k; $j <= $lastid; $j++) {
        $distances{"$k:$j"} = vectdist($k, $j);
        print OUTPUT "$k:$j," . $distances{"$k:$j"} . "\n";
    }
}
close(OUTPUT);

# Subroutine to calculate the distance between
# two feature vectors, normalized to 0..1

sub vectdist {
    my ($id1, $id2) = @_;
    my @id1vect = split "", $vectors{$id1};
    my @id2vect = split "", $vectors{$id2};
    my ($tmp, $max) = (0, scalar(@id1vect));
    for ($i=0; $i < $max; $i++) {
        if ($id1vect[$i] == $id2vect[$i]) {
            $tmp++;
        }
    }
    1 - ($tmp / $max);
}
