# dcbo-ids.pl
# 28 jan 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Given a list of people with DCB entries and their ID numbers,
# creates text file with one ID number and name on each line
# written to IDs directory.
#
# To prepare the starting page, go to the DCB and get a list of
# all of the people of interest on one page; save it in Queries
# directory.

# Load necessary modules
use WWW::Mechanize;

my $infile = 'Queries\dcbo-vol1.html';
my $outfile ='IDs\dcbo-vol1-ids.txt';

# Open output file
open(OUTPUT, ">$outfile");

# Starting page
my $mech = WWW::Mechanize->new( autocheck => 1 );
$mech->get( "file:$infile" );

# Get all of the links on the page
my @links = $mech->find_all_links( );

# Strip out IDs and Names
for my $link ( @links ) {
    my $url = $link->url_abs;
    my $text = $link->text;
    
    if($url =~ m/ShowBio\.asp\?BioId=(.*)\&query\=/) {
        print OUTPUT "$1\t$text\n";
    }

}