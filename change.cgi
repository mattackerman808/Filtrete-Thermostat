#!/usr/bin/perl
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use JSON;

$therm = "192.168.77.10";

$setmode = param('mode');
$settemp = param('settemp');
$sethold = param('hold');

%cmdhash = ();

if ($setmode) {

 if ($setmode eq "off") {
   $cmdhash{tmode} = '0';
 } elsif ($setmode eq "heat") {
   $cmdhash{tmode} = '1';
 } elsif ($setmode eq "cool") {
   $cmdhash{tmode} = '2';
 } elsif ($setmode eq "auto") {
   $cmdhash{tmode} = '3';
 }

}

if ($settemp) {

 $cmdhash{t_heat} = $settemp;

}

if ($sethold) {

 if ($sethold eq "yes") {
   $cmdhash{hold} = '1';
 } elsif ($sethold eq "no") {
   $cmdhash{hold} = '0';
 } 

}

## do work

$postcmd="{";

while (($key, $value) = each(%cmdhash)){
     $postcmd="$postcmd\"$key\":$value,";
}

$postcmd =~ s/,$/}/;

print header;

print "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">
<html>
<head>
<title>Build is ready</title>
<meta http-equiv=\"REFRESH\" content=\"2;url=index.cgi\"></HEAD>
<BODY>
OK, making the change!<br><br>";

print "Executing: $postcmd\n<br><br>";

$result = `curl -s -d \'$postcmd\' http://$therm/tstat`;

print "Result is: $result<br><br>

Taking you back to the control page...

</BODY>
</HTML>
";

