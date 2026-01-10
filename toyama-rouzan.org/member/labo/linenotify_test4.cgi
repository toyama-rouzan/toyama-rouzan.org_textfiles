#!/usr/bin/perl


use strict;
use CGI::Carp qw(fatalsToBrowser);
use warnings;
use lib "./lib";
use LWP::UserAgent;
use Encode;

require './lib/lineapi.pl';

my $LINE_API_TOKEN_MyLabo1 = "1h073TNY63u245Qouu3YeJXC8rSppM3bjOhCtSlAkPv";

my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime;
my $message = "テストメッセージ($hour:$min $sec)";

my $result = line_push_message($LINE_API_TOKEN_MyLabo1,$message);

print <<EOM;
Content-type: text/html; charset=shift_jis

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>LINE notify test</title>
</head>
<body>
<pre>
EOM

print "result status:$result";

print <<EOM;
</pre>
</body>
</html>
EOM

exit;

