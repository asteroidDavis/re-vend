#!/usr/bin/perl -T
use strict;
use warnings;
use feature qw(switch);
use Net::SMTP::SSL;
use Config::Simple;
use Data::Dumper;
use WWW::curlmyip;

print "Starting box workflow\n";
#clears the path for taint mode
$ENV{PATH} = '';
print "Set ENV{Path} to the empty string\n";

#get the rfid keyboard with a tired hack
my $rfidKeyboard = `/bin/awk \'c&&!--c;/RFID/{c=4};\' /proc/bus/input/devices | /bin/awk \'{print \$4}\'`;
#makes rfid keyboard is an event
$rfidKeyboard = untaint('kbd', $rfidKeyboard);

#checks if a rfid keyboard event  was found
if($rfidKeyboard) {
    $rfidKeyboard = "/dev/input/$rfidKeyboard";
    print "RFID keyboard: $rfidKeyboard\n";
    #lauch box workflow
}
else {
    #sends an email to the admin if no rfid keyboard event is found
    alertAdmin();
}

exit 0;

#sends an email to the admin in the boxconfig.txt file
sub alertAdmin {
    #uses the boxconfig.txt for the box workflows
    my $config = new Config::Simple('boxconfig.txt');
    my $generalConfig = $config->param(-block=>'general');

    #gets the ip so the admin knows which machine is down
    my $ip = get_ip();

    #gets the email address and authentication info
    my $adminEmail = ${$generalConfig}{'admin_email'};
    my $mailPass = ${$generalConfig}{'mail_pass'};
    my $sender = ${$generalConfig}{'mail_sender'};

    #untaints values from the config
    $adminEmail = untaint('email', $adminEmail);
    $sender = untaint('email', $sender);
    $mailPass = untaint('password', $mailPass);
    print "Admin Email: $adminEmail\n";

    #sends the no rfid keyboard report using the zoho smtp server
    my $mailer = Net::SMTP::SSL->new(
        'smtp.zoho.com',
        Port => 465,
        Timeout => 120,
        Debug => 1,
    );
    $mailer->auth($sender, $mailPass);
    $mailer->mail($sender);
    $mailer->to($adminEmail);
    $mailer->data();
    $mailer->datasend("To: $adminEmail\n");
    $mailer->datasend("From: $sender\n");
    $mailer->datasend("Subject: RFID keyboard not found\n");
    $mailer->datasend("\n");
    $mailer->datasend("Oh no. We looked everywhere but the awk hack failed. Make the keyboard work on $ip\n");
    $mailer->dataend();
    $mailer->quit();
}

#untaints a value based on the type. If the type is not recognized the value is emptied
#parameters:
#   $type: The type of value to untaint
#   taintedValue: The value which must be untainted
sub untaint {
    my $type = shift;
    my $taintedValue = shift;
    
    given ($type) {
        when('email') {
            if($taintedValue =~ /^(.*?@.*)$/) {
                $taintedValue = $1;
            }
            else {
                $taintedValue = '';
            }
        }
        when('password') {
            $taintedValue =~ /^(.*)$/;
            $taintedValue = $1;
        }
        when('kbd') {
            if($taintedValue =~ /^(event[0-9]{1,3})$/) {
                $taintedValue = $1;
            }
            else {
                $taintedValue = '';
            }
        }
        default {
            print "Can't untaint $taintedValue\n";
            $taintedValue = '';
        }
    }
    return $taintedValue;
}


