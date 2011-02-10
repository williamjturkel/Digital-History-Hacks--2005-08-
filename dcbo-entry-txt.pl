# dcbo-entry-txt.pl
# 29 jan 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Given a collection of HTML files for a DCB biography entry
# strip out all of the formatting and return each as a
# plain text file.

# Load necessary modules
use HTML::TokeParser;
use TEXT::Wrap;

# Output formatting
$Text::Wrap::columns = 72;

# Input list of IDs to process
my $infile = 'IDs\dcbo-vol1-ids.txt';
open(INPUT, "<$infile");

# Loop through each ID in the input file
while(<INPUT>) {
    chomp;
    @fields = split /\t/;
    $id = $fields[0];

    # We don't want to process any files we've already
    # done.
    if (-e "Text\\$id.txt") {
        print "Text file for $id already exists\n";
    } else {

        # If the HTML file has been downloaded, process it.
        # Otherwise, print error message and move on to next.
        if (-e "Biographies\\$id.html")  {
            my $stream = HTML::TokeParser->new("Biographies\\$id.html");
            # Since we don't expect FOOBAR in the entry, this should
            # get all of the text.
            my $text = $stream->get_trimmed_text('FOOBAR');
            # We know that it is a DCB entry.
            $text =~ s/^Dictionary of Canadian Biography //;
            # We want to get rid of the inconsistently-used apostrophe
            # which signals another DCB entry.
            $text =~ tr/*//d;
            # Open output file
            open(OUTPUT, ">Text\\$id.txt");
            # Reformat paragraphs
            print OUTPUT Text::Wrap::wrap('', '', $text);
            # print OUTPUT $text;
            close OUTPUT;
        } else {
            print "Can't find HTML file for $id\n"
        }
    
    }
}
close INPUT;