# dcbo-people.pl
# 28 jan 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Given a range of ID numbers, checks each to see if it
# has been downloaded yet, and if not, goes to DCB and
# gets printable version of biography, which is written
# to "ID.html" in Biographies subdirectory.

# Load necessary modules
use WWW::Mechanize;

my $mech = WWW::Mechanize->new( autocheck => 1 );

# Input file
my $infile = 'IDs\dcbo-vol1-ids.txt';
open(INPUT, "<$infile");

# Loop through each ID in the input file
while(<INPUT>) {
    chomp;
    @fields = split /\t/;
    $id = $fields[0];
    
    # Make sure biography hasn't already been downloaded
    if (-e "Biographies\\$id.html")  {
        print "$id already downloaded\n";    
    } else {
        # Open output file
        open(OUTPUT, ">Biographies\\$id.html");
        # Get biography
        $mech->get( "http://www.biographi.ca/EN/ShowBioPrintable.asp?BioId=$id" );
        # Write biography to output file
        print OUTPUT $mech->content;
        # Be considerate of their server
        sleep 2;
    }
}


