# sip-map.pl
# 26 apr 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Given the ISBN of a book, scrapes its SIPs
# (statistically improbable phrases) from Amazon.com
# and plots them with the GraphViz package.
# Outputs a PNG file.

# Load necessary modules
use WWW::Mechanize;
use GraphViz;

# Given an ISBN, get the starting page from Amazon.com
my $startbook = 'Diamond, Guns, Germs and Steel';
my $startisbn = "0393317552";

# Initialize output graph
my $g = GraphViz->new(layout => 'fdp');
$g->add_node($startbook, shape => 'box');

my $start = "http://www.amazon.com/gp/product/" . $startisbn . "/";

my $mech = WWW::Mechanize->new( autocheck => 1 );
$mech->get( $start );

# Extract the SIPs for the starting book

my %sipurls = ();
my @links = $mech->find_all_links( );
    
for my $link ( @links ) {

    my $url = $link->url_abs;
    my $siptext = $link->text;
    
    if($url =~ m/sip_bod/) {
        
        # print "SIP", "\t", $siptext, "\n\n";
        $g->add_node($siptext);
        $g->add_edge($startbook => $siptext);
        
        # Hash the SIP URL and associated SIP to process later
        
        # print "URL", "\t", $url, "\n";
        $sipurl{ $url } = $siptext;
    }
    
}

# Extract the books for each SIP

for my $url ( keys %sipurl ) {
    
    my $siptext = $sipurl{ $url };
    print "URL", "\t", $url, "\n";
    print "SIP", "\t", $siptext, "\n\n";
    
    $mech->get( $url );
    my @furtherlinks = $mech->find_all_links( );
    
    for my $link ( @furtherlinks ) {
        my $newurl = $link->url_abs;
        my $booktext = $link->text;

        if($newurl =~ m/sip_pdp_dp/) {

            # print "SIP", "\t", $siptext, "\n\n";
            $g->add_node($booktext, shape => 'box');
            $g->add_edge($siptext => $booktext);
        }
    }
    
    }

# Create the graph

open(OUTPUT, ">$startisbn.png");
binmode OUTPUT;
print OUTPUT $g->as_png;
close OUTPUT;
