#1/usr/bin/perl
use strict;
use warnings;

my $moreTests = 'yes';

chdir '/opt/revend/';

while($moreTests !~ /no?/i) {
    system('python', '/opt/revend/pos.py');
    system('python', '/opt/revend/box.py');
    print "More tests? (yes/no): ";
    $moreTests = <STDIN>;
}

exit 0;
