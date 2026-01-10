#!/usr/bin/perl


use strict;
use CGI::Carp qw(fatalsToBrowser);
use warnings;
use lib "./lib";
use LWP::UserAgent;
use Encode;

my $LINE_API_URI = "https://notify-api.line.me/api/notify";
my $LINE_API_TOKEN = "1h073TNY63u245Qouu3YeJXC8rSppM3bjOhCtSlAkPv";

my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime;
my $message = "テストメッセージ($hour:$min $sec)";
$message = decode('Shift_JIS', $message);
$message = encode('UTF-8', $message);

my $ua = LWP::UserAgent->new;
my $res = $ua->post(
  $LINE_API_URI,
  { message => $message },
  Authorization => "Bearer $LINE_API_TOKEN", # set created auth key
);

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

print $res->content;

print <<EOM;
</pre>
</body>
</html>
EOM

exit;

