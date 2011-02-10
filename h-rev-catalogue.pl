# h-rev-catalogue.pl
# 13 mar 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Submit each ISBN in a list to library catalogue
# and scrape results page to figure out if the book
# is in library.

use WWW::Mechanize;
my $mech = WWW::Mechanize->new( autocheck => 1 );

my $hnet = 'Jhistory';
my $in_file = "$hnet-isbn.txt";
my $count = 0; my $have = 0; my $not = 0;

open(INPUT, "<$in_file");
while($isbn = <INPUT>) {
    # sleep 1;
    $count += 1;
    $mech->get( "http://alpha.lib.uwo.ca/" );
    $mech->success or die "Can't get the search page for $isbn";
    $mech->form_number( '1' );
    $mech->field( 'searchtype', 'i' );
    $mech->field( 'searcharg', $isbn );
    $mech->click_button( name => 'search' );
    if ( $mech->content =~ m|class=\"bibInfoLabel\"\>Author| ){
        $have += 1;
    } else {
        $not += 1;
    }
}
print "$hnet, $count, $have, $not\n";



