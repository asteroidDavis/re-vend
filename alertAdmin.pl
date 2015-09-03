#!/usr/bin/perl
use strict;
use warnings;

use Net::SMTP::SSL;
use Config::Simple;
use Data::Dumper;
use WWW::curlmyip;
use Getopt::Long;

#sets up the object for reading the mail config
my $netConfig = new Config::Simple('netConfig.txt');
my $mailOptions = $netConfig->param(-block=>'mail');

#the message contents
my %messageInfo = (
    'message' => '',
    'sender' => $mailOptions{'sender'),
    'mailingList' => $mailOptions('mailingList'),
    'includeIP' => $mailOptions('includeIP'),       #appends the IP to the subject for all true values
    'subject' => '',
);

my %networkInfo = {
    'mailServer' => $mailOptions{'mailServer'},
    'mailServerUser' => $mailOptions{'mailServerUser'},         #the user to authenticate with on the mail server
    'mailServerPassword' => $mailOptions{'mailServerPassword'},  #the password for the mail servers user
}



exit 0;

#gets the message and the subject from the command line
sub getArgs {
    GetOptions(
        'message=s' => \$messageInfo{'message'},
        'subject=s' => \$messageInfo{'subject'},
    );
}

#checks the values of the command line arguments
sub untaint {
    
}



=cut
my $config = new Config::Simple('boxconfig.txt');
my $generalConfig = $config->param(-block=>'general');

#gets the ip so the admin knows which machine is down
my $ip = get_ip();

#gets the email address and authentication info
my $adminEmail = ${$generalConfig}{'admin_email'};
=cut

