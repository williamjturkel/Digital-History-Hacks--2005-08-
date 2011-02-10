# h-reviews.pl
# 12 mar 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
#
# Gets set of all H-Net lists, retrieves the ISBNs
# of reviewed books so they can be submitted to a library
# catalogue to check whether they are in the library
# or not.  (Relatively brittle).

use WWW::Mechanize;
my $mech = WWW::Mechanize->new( autocheck => 1 );

# Get list of H-Net lists to process (from file, if
# it exists, otherwise need to create file).

my @hnetlists = ();
print '-' x 60 . "\n";
print "Getting list of H-Net lists...\n";
print '-' x 60 . "\n";
if (-e 'h-net-lists.txt') {
    print "File of lists exists...\n";
    open(INPUT, "<h-net-lists.txt");
    while(<INPUT>) {
        chomp;
        @fields = split /\t/;
        push @hnetlists, ( $fields[0] );
    }
} else {
    print "Need to create file of lists...\n";
    open(OUTPUT, ">h-net-lists.txt");
    $mech->get( "http://www.h-net.org/lists/" );
    my @links = $mech->find_all_links( );
    for my $link ( @links ) {
        my $url = $link->url_abs;
        my $text = $link->text;
        if($url =~ m|www.h-net.org/~|) {
            push @hnetlists, ( $text );
            print OUTPUT "$text\n";
        }
    }
    print "File of lists created...\n";
}

# Need list of books reviewed for each H-Net list.
# Make sure that file exists, otherwise create it
# from the H-Net reviews search page.

print '-' x 60 . "\n";
print "Getting list of books reviewed on each H-Net list...\n";
print '-' x 60 . "\n";
foreach $k ( @hnetlists ) {
    print "Processing $k\n";
    if (-e "$k.txt") {
        print "File $k.txt exists...\n";
    } else {
        print "File $k.txt needs to be created...\n";
        my $out_file = "$k.txt";
        sleep 2;
        $mech->get( "http://www.h-net.org/reviews/search.html" );
        $mech->success or die "Can't get the search page for $k";
        $mech->form_number( '2' );
        $mech->field( 'publist', $k );
        $mech->click_button( name => 'search' );
        my @links = $mech->find_all_links; 
        open(OUT, ">$out_file") || die "Can't write-open $out_file: $!";
        binmode(OUT);
        for my $link ( @links ) {
            my $url = $link->url_abs;
            if($url =~ m|www.h-net.org/reviews/show|) {
                print OUT "$url\n";
            }
        }
        close(OUT);
        print "Bytes saved: ", -s $out_file, " in $out_file\n";
    }
}

# Need a list of ISBNs for each book reviewed in a
# given list. Make sure that the file exists, or
# create it if necessary by scraping individual
# review pages.

print '-' x 60 . "\n";
print "Getting ISBNs for books reviewed on each H-Net list...\n";
print '-' x 60 . "\n";
foreach $k ( @hnetlists ) {
    print "Processing $k for ISBNs\n";
    if (-e "$k-isbn.txt") {
        print "File $k-isbn.txt exists...\n";
    } else {
        print "File $k-isbn.txt needs to be created...\n";
        my $out_file = "$k-isbn.txt";
        open(OUT, ">$out_file") || die "Can't write-open $out_file: $!";
        binmode(OUT);
        if (-z "$k.txt") {
            print "File $k.txt is empty...\n";
            close(OUT);
            print "Bytes saved: ", -s $out_file, " in $out_file\n";
        } else {
            print "Processing $k.txt to get ISBNs...\n";
            my $in_file = "$k.txt";
            open (IN, "<$in_file");
            while($review = <IN>) {
                sleep 3;
                $mech->get( $review );
                next unless $mech->success;
                my $response = $mech->content;
                if( $response =~ m|http://www.amazon.com/exec/obidos/ASIN/(.*)/| ) {
                    print OUT "$1\n";
                }
            }
            close(IN);
            close(OUT);
            print "Bytes saved: ", -s $out_file, " in $out_file\n";
        }
    }
}
