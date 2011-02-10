# dcbo-features.pl
# 4 feb 2006
#
# wj turkel
# http://digitalhistoryhacks.blogspot.com
#
# Given a collection of plaintext biography files
# and a feature space, output a spreadsheet of
# feature vectors.

# Need this to strip out accented characters
require Encode;
use Unicode::Normalize;

# Input feature file and build feature hash
my $featurefile = 'Concordance\dcbo-vol1-features.txt';
my %features = ();
open(FEATURES, $featurefile) || die("Could not open feature file.\n");
@raw_data = <FEATURES>;
close(FEATURES);
foreach $f (@raw_data) {
    $f =~ s/\n$//g;
    $features{$f} = '0';
}
my @sortkeys = sort keys (%features);

# Print feature names to output file
my $outfile = 'dcbo-vol1-featurespace.csv';
open(OUTPUT, ">$outfile");
print OUTPUT "\"ID\"";
foreach $k (@sortkeys) {
    print OUTPUT ',' . "\"" . $k . "\"";
}

# Now we want to loop through all of the text bios
# we have already downloaded and calculate a feature
# vector for each one...

# Input list of IDs to process
my $idsfile = 'IDs\dcbo-vol1-ids.txt';
open(IDSFILE, "<$idsfile") || die("Could not open IDs file.\n");

# Loop through each ID in the file of IDs to process
while(<IDSFILE>) {
    chomp;
    @fields = split /\t/;
    $id = $fields[0];

    # Input biography file
    my $infile = "Text\\$id.txt";
    open(INPUT, "<$infile") || die("Couldn't open input file $infile.\n");
    
    my $inline;
    while ($inline = <INPUT> ) {
    
        # Clean up the input line... 
        # Strip out accented characters   
        for ( $inline ) {
            $_ = Encode::decode( 'iso-8859-1', $_ );  
            $_ = NFD( $_ );   
            s/\pM//g;
            s/[^\0-\x80]//g;
        }
        # Convert to all caps
        $inline = uc $inline;
        # Remove punctuation
        $inline =~ s/[,;:!\?\.\"]{1,}//g;
        $inline =~ s/[\(\)&'’”`“]{1,}//g;
        # Remove final -S
        $inline =~ s/S\s+/ /g;
        # Remove dates
        $inline =~ s/[0-9]+//g;
        
        # Check each word in the input line and
        # hash it if it is a feature
        @inarray = split /\s+/, $inline;
        foreach $word (@inarray) {
            # If a more sophisticated representation is needed
            # the hash can be incremented here
            $features{$word} = '1' if exists $features{$word};
        }
    }
    
    # Output each feature vector to CSV file we are creating
    print OUTPUT "\n" . "\"$id\"";
    foreach $k (@sortkeys) {
        print OUTPUT ',', $features{$k};
    }
    
    # Prepare for next pass
    close(INPUT);
    foreach $f (@sortkeys) {
        $features{$f} = '0';
    }
}
close(OUTPUT);
close(IDSFILE);