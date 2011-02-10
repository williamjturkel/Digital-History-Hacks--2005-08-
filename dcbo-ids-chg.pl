# dcbo-ids-chg.pl
# 21 jan 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Uses entries in the online Dictionary of Canadian Biography
# to determine how biography categories ('Aboriginal', 'Accountant', etc.)
# have changed over time.  Output into CSV file for analysis with
# spreadsheet: volume numbers are columns, category ids are rows.
#
# LWP code adapted from
#   Burke, Perl & LWP (O'Reilly 2002), pp. 27-28, 96-97.
# Max subroutine from
#   Schwartz & Phoenix, Learning Perl, 3rd ed (O'Reilly 2001), pp. 65.

use LWP;

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

# To speed up processing, the codes expected by the DCB search FORM
# have already been scraped.

# This goes into Data6 of the search FORM
my %volumes = (
    '01' => '1000-1700',
    '02' => '1701-1740',
    '03' => '1741-1770',
    '04' => '1771-1800',
    '05' => '1801-1820',
    '06' => '1821-1835',
    '07' => '1836-1850',
    '08' => '1851-1860',
    '09' => '1861-1870',
    '10' => '1871-1880',
    '11' => '1881-1890',
    '12' => '1891-1900',
);

# This goes into Data3 of the search FORM
my %categories = (
    '35716' => 'Philanthropists and Soc...',
    '35681' => 'Business',
    '35712' => 'Legal Professions',
    '35719' => 'Accountants',
    '35720' => 'Archivists',
    '35723' => 'Curators',
    '35713' => 'Fur Trade',
    '35704' => 'Slaves',
    '35726' => 'Librarians',
    '35698' => 'Surveyors',
    '35718' => 'Sports and recreation',
    '35674' => 'Agriculture',
    '35697' => 'Scientists',
    '35696' => 'Religion',
    '35691' => 'Miscellaneous',
    '35676' => 'Armed Forces',
    '35683' => 'Engineers',
    '35709' => 'Interpreters and Transl...',
    '35728' => 'Police',
    '35689' => 'Mariners',
    '35694' => 'Office Holders',
    '35711' => 'Labourers and Labour Or...',
    '35680' => 'Blacks',
    '35695' => 'Politicians',
    '35679' => 'Authors',
    '35677' => 'Artisans',
    '35721' => 'Arts and Entertainment',
    '35722' => 'Communications',
    '35710' => 'Inventors',
    '35730' => 'Social Scientists',
    '35707' => 'Criminals',
    '35708' => 'Aboriginal people',
    '35682' => 'Education',
    '35684' => 'Explorers',
    '35690' => 'Medicine',
    '35675' => 'Architects',     
);

# We need to keep the category keys in the right order.
my @catarray = sort {$categories{$a} cmp $categories{$b}} (keys %categories);

# This will be a hash of arrays.
my %categorycount;

# For each volume (Volumes 1, 3, 9, 10 aren't coded for categories)
foreach my $vol ('02', '04', '05', '06', '07', '08', '11', '12') {

# For each different category, return count of matching biographies.
foreach my $id (@catarray) {
    # Give the user some feedback about progress.
    print "Vol: " . $vol . "\tCat: " . $id . "\n";
    # Get the page.
    my ($content, $message, $is_success) = do_POST(
        $doc_url,
        [ 'Data3' => $id,
          'Data4' => '1',
          'Data6' => $vol ],
        );
    die "Error $message\n"
        unless $is_success;
    my $tmpcontent = $content;
    # Sometimes there are no matching biographies.
    if ($tmpcontent =~ m{<TD CLASS="STANTXT">Your search criteria has no matching biographies}) {
        # $categorycount{$id} = 0;
        push @{ $categorycount{$id} }, "0";
    }
    else {
        $content =~ m{<TD CLASS="STANTXT"><B>([0-9,]+)</B> biography\(ies\) are available using your current search criteria}is;
        my $tmp = $1;
        # Remove commas from numbers in the thousands.
        $tmp =~ s/\,//;
        # $categorycount{$id} = $tmp;
        push @{ $categorycount{$id} }, $tmp;
    }
    # Be considerate to their server.
    sleep 2;
}
}

# Now output the .CSV file
open(OUTPUT, ">ids-chg.csv");

# Output count.
foreach my $key (@catarray) {
    # print OUTPUT $key . "," . $categories{$key} . "," . $categorycount{$key} . "\n";
    print OUTPUT $key . "," . $categories{$key} . "," . join(",", @{ $categorycount{$key} }) . "\n";
}

# Close the file.
close(OUTPUT);
