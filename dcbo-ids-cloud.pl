# dcbo-ids-cloud.pl
# 15 jan 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Goes to the online Dictionary of Canadian Biography to get the
# number of people in each category ('Aboriginal', 'Accountant', etc.)
# Outputs a tag cloud as HTML.
#
# LWP code adapted from
#   Burke, Perl & LWP (O'Reilly 2002), pp. 27-28, 96-97.
# Tag cloud adapted from
#   Bausch, Yahoo! Hacks (O'Reilly 2006), pp. 203-04.
# Max subroutine from
#   Schwartz & Phoenix, Learning Perl, 3rd ed (O'Reilly 2001), pp. 65.

use LWP;
use LWP::Simple;
use POSIX "floor";

sub max {
    my($max_so_far) = shift @_;
    foreach(@_) {
        if ($_ > $max_so_far) {
            $max_so_far = $_;
        }
    }
    $max_so_far;
}

my $browser;
sub do_POST {
    $browser = LWP::UserAgent->new() unless $browser;
    my $resp = $browser->post(@_);
    return ($resp->content, $resp->status_line, $resp->is_success, $resp)
        if wantarray;
    return unless $resp->is_success;
    return $resp->content;
}

my $doc_url = 'http://www.biographi.ca/EN/Search.asp';

# Create a hash of category IDs and names by scraping base page.
my %categories = ();
my $document = get($doc_url);
while ($document =~ m/<A CLASS="NormalLink" HREF="Javascript:fSubmit\('','','','','([0-9]+)','1','','','','','',''\);">(.*?)<\/A>/g) {
    my ($id, $tmp) = ($1, $2);
    $tmp =~ s/<IMG(.*?)>//;
    $categories{$id} = $tmp;
}

# We need to keep the category keys in the right order.
my @catarray = sort {$categories{$a} cmp $categories{$b}} (keys %categories);

# For each different category, return count of matching biographies.
my %categorycount = ();
foreach my $id (@catarray) {
    my ($content, $message, $is_success) = do_POST(
        $doc_url,
        [ 'Data3' => $id,
          'Data4' => '1' ],
        );
    die "Error $message\n"
        unless $is_success;
    $content =~ m{<TD CLASS="STANTXT"><B>([0-9,]+)</B> biography\(ies\) are available using your current search criteria}is;
    my $tmp = $1;
    $tmp =~ s/\,//;
    $categorycount{$id} = $tmp;
    # Be considerate to their server.
    sleep 2;
}

# Debugging scaffolding: check this output against tag cloud.
print "\n----------------------------\n";
foreach my $key (@catarray) {
    print "key: " . $key . "\tcat: " . $categories{$key} . "\tcnt: " . $categorycount{$key} . "\n";
}
print "\n----------------------------\n";

# Now we send the tag cloud to an HTML file.
open(OUTPUT, ">ID-cloud.html");

# Range of font sizes to use.
my $minfontsize = 12;
my $maxfontsize = 36;

# Get the maximum number of biographies in any category.
my $maxbio = &max(values %categorycount);

# Output the opening HTML tags.
print OUTPUT "<html>\n<head>\n<style>\nbody {\n";
print OUTPUT "\tbackground-color:#fff;\n\tfont-family:Tahoma, Verdana, Arial;\n";
print OUTPUT "\tcolor:#354251;\n}\n.tag{\n\tmargin-bottom: 10px;\n\tpadding: 5px;\n}\n";
print OUTPUT "</style>\n</head>\n<body>\n";
print OUTPUT "<table border=1px width=80% cellpadding=4px align=center>\n<tr>\n<td>\n";

# Print the name of each category in the appropriate sized font.
foreach my $catid (@catarray) {
    my $fontsize = $minfontsize + floor(($maxfontsize-$minfontsize) * ($categorycount{$catid}/$maxbio));        
    print OUTPUT "<span class=\'tag\' style=\'font-size:" . $fontsize . "px\'>" . $categories{$catid} . "</span>\n";
}

# Output the closing HTML tags.
print OUTPUT "</td></tr></table>\n</body>\n</html>\n";

print "Finished processing.\n";