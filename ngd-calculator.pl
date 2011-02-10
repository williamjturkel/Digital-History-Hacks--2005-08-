#!"C:\Program Files\xampp\perl\bin\perl.exe"
# ngd-calculator.cgi
#
# wjt
# http://history.uwo.ca/faculty/turkel/
#
# 5 aug 2006

use SOAP::Lite;
use CGI;
use POSIX qw(log10);
use List::Util qw(max min);

# Google API developer's key
my $google_key = '<Insert Key Here>';

# Google WSDL
my $google_wsdl = "http://api.google.com/GoogleSearch.wsdl";
# my $google_wsdl = "./GoogleSearch.wsdl";

# start, maxResults, filter, restrict, safeSearch, lr, ie, oe
my @params = (0, 10, 0, '', 0, '', 'utf-8', 'utf-8');

# Do Google search and return count
sub do_search {
    unshift (@params, ($google_key, $_[0]));
    my $result =
        SOAP::Lite
        -> service($google_wsdl)
        -> doGoogleSearch(@params);
    shift @params;
    shift @params;
    return $result->{estimatedTotalResultsCount};
}

# Create the search page
$query = new CGI;
print $query->header;
print $query->start_html('NGD Calculator');
print "<H1>Normalized Google Distance (NGD) Calculator</H1>";

print '<p>';
print 'For information about NGD see Rudi Cilibrasi and Paul Vitanyi, "';
print '<a href="http://www.arxiv.org/PS_cache/cs/pdf/0412/0412098.pdf">';
print 'Automatic Meaning Discovery Using Google</a>."';
print '</p>';

# Print the search box form
print $query->startform;
print '<strong>Enter term 1</strong> ',$query->textfield('term1');
print '<br />';
print '<strong>Enter term 2</strong> ',$query->textfield('term2');
print '<br />';
print $query->submit('form_1','Calculate');
print $query->endform;
print '<br />';

$x = ''; $y = ''; $xy = '';
$x = '+"' . $query->param('term1') . '"';
$y = '+"' . $query->param('term2') . '"';
$xy = $x . " " . $y;

$fx = 1; $fy = 1; $fxy = 1;
$logfx = 0; $logfy = 0; $logfxy = 0; $logm = 0;
$maxlogfxy = 0; $minlogfxy = 0;
$ngd = 0;

# Best guess as of Jan 2006
$m = 11828505634;

if ($x && $y) {

    # Determine frequencies
    $fx = do_search( $x );
    $fy = do_search( $y );
    $fxy = do_search( $xy );
    
    # Determine logarithms
    $logm = log10( $m );
    $logfx = log10( $fx );
    $logfy = log10( $fy );
    $logfxy = log10( $fxy );
    
    # Determine max and min
    @fxy = ($logfx, $logfy);
    $maxlogfxy = max @fxy;
    $minlogfxy = min @fxy;
    
    # Calculate NGD
    $ngd = ($maxlogfxy - $logfxy) / ($logm - $minlogfxy);
    
    print 'NGD(x,y) = ' . $ngd . '<br /><br />';
    
    print 'Term 1: ' . $x . '<br />';
    print 'f(x) = ' . $fx . '<br />';
    print 'log f(x) = ' . $logfx . '<br /><br />';
    
    print 'Term 2: ' . $y . '<br />';
    print 'f(y) = ' . $fy . '<br />';
    print 'log f(y) = ' . $logfy . '<br /><br />';
    
    # print 'max(log f(x),log f(y)) = ' . $maxlogfxy . '<br />';
    # print 'min(log f(x),log f(y)) = ' . $minlogfxy . '<br /><br />';
    
    print 'Intersection: ' . $xy . '<br />';
    print 'f(x,y) = ' . $fxy . '<br />';
    print 'log f(x,y) = ' . $logfxy . '<br /><br />';
    
    print 'M: ' . $m . '<br />';
    print 'log M: ' . $logm . '<br />';
}

print qq{<P><A HREF="http://history.uwo.ca/faculty/turkel">Digital History at Western</A>};
print $query->end_html;
