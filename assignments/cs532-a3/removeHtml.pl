use strict;
use warnings;

# read an entire file
use File::Slurp;
# remove html
use HTML::Restrict;
# get base filename
use File::Basename;
#get current working directory
use Cwd;

#get directory paths
my $htmlDir = cwd();
my $pdir="$htmlDir/processed";
$htmlDir = "$htmlDir/html";

# set up html remove 
# strip all enclosed tags etc and trim 
my $hr = HTML::Restrict->new(
strip_enclosed_content => [ 'script', 'style', 'head' ],
trim => 1
);


# open the directory contianing the html files
opendir(DIR, $htmlDir) or die $!;
# loop through the files
while(my $file = readdir(DIR)){
    # I want only files not . or ..
    next unless (-f "$htmlDir/$file");
    print "$file\n";
    # get text of file and remoce html
    my $text = read_file( "$htmlDir/$file" );
    my $cleaned = $hr->process( $text );
    # attempt to remove none word or space characters i.e html quote characters
    $cleaned =~ s/[^\w\s]+//g;
    my $base = basename($file,".html");
#    print $file;
#    print "$cleaned\n"; 
    my $pfile="$pdir/$base.processed";
#    print "$pfile\n";
    open(my $out, ">>",$pfile) or die $!;
    print $out $cleaned;
    close($out);
}
close(DIR);
