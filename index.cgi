#!/usr/bin/perl

use WWW::Mechanize;
use JSON -support_by_pp;
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

#Your thermostat IP
$therm="192.168.77.10";
#
 
fetch_json("http://$therm/tstat");

if($json_hash->{tmode} == 0) {
 $mode=OFF; 
} elsif($json_hash->{tmode} == 1) {
 $mode="<font color=red>Heat</font>";
} elsif($json_hash->{tmode} == 2) {
 $mode="Cool";
} elsif($json_hash->{tmode} == 3) {
 $mode="Auto Select";
}

if($json_hash->{tstate} == 0) {
 $state="Idle";
} elsif($json_hash->{tstate} == 1) {
 $state="<font color=red>Running / Heating</font>";
} elsif($json_hash->{tstate} == 2) {
 $state="<font color=blue>Running / Cooling</font>";
}

if($json_hash->{override} == 0) {
 $override=Off;
} elsif($json_hash->{override} == 1) {
 $override="<font color=red>On</font>";
}

if($json_hash->{hold} == 0) {
 $hold="Not enabled";
} elsif($json_hash->{hold} == 1) {
 $hold="<font color=red>Enabled</font>";
}

print header;

print "<body bgcolor=lightgrey>";

print "<b>Current temperature is:</b><br><table border=2 bgcolor=white cellpadding=10><tr><td><font size=10 color=blue><b>$json_hash->{temp}</b></font></td></tr></table><br>";
print "<b>Heater temperature is set to:</b><br><table border=2 bgcolor=white cellpadding=10><tr><td><font size=10 color=orange><b>$json_hash->{t_heat}</b></font></td></tr></table><br>";
print "<table border=2 bgcolor=white cellpadding=10><tr><td><pre>";
print "Current mode is:      $mode<br>";
print "Current state is:     $state<br>";
print "Temperature hold is:  $hold<br>";
print "Override is:          $override<br>";
print "Current time is:      $json_hash->{time}->{hour}:$json_hash->{time}->{minute}";
print "</pre></td></tr></table><br>";

print "<TABLE bgcolor=\"white\" border=\"2\" cellpadding=\"25\"><TR><TD>
	<h4>Heater control panel:</h4>
        <FORM action=\"change.cgi\" method=\"get\">
	<h5>New Temperature:</h5>
	<SELECT name=\"settemp\" size=\"1\">
	   <OPTION value=\"\" selected>No Change</option>
	   <OPTION value=\"65\">65</option>
	   <OPTION value=\"66\">66</option>
	   <OPTION value=\"67\">67</option>
	   <OPTION value=\"68\">68</option>
	   <OPTION value=\"69\">69</option>
	   <OPTION value=\"70\">70</option>
	   <OPTION value=\"71\">71</option>
	   <OPTION value=\"72\">72</option>
	   <OPTION value=\"73\">73</option>
	   <OPTION value=\"74\">74</option>
	   <OPTION value=\"75\">75</option>
	   <OPTION value=\"76\">76</option>
	   <OPTION value=\"77\">77</option>
	</SELECT>
        <h5>Hold Temp (will not change during normal schedule):</h5>
        <INPUT type=radio name=\"hold\" value=\"yes\">Hold Temp<br>
        <INPUT type=radio name=\"hold\" value=\"no\">Do Not Hold Temp<br>
        <h5>Master Power:</h5>
        <INPUT type=radio name=\"mode\" value=\"off\">Heater OFF<br>
        <INPUT type=radio name=\"mode\"  value=\"heat\">Heater ON<br> 
	<br><br>
        <INPUT type=submit value=\"Submit\">
        </FORM></TD></TR></TABLE>"
;

sub fetch_json
{
  my ($json_url) = @_;
  my $browser = WWW::Mechanize->new();
  $browser->get( $json_url );
  my $content = $browser->content();
  my $json = new JSON;
  $json_hash = $json->allow_nonref->utf8->relaxed->escape_slash->loose->allow_singlequote->allow_barekey->decode($content);
  return $json_hash;        
}

