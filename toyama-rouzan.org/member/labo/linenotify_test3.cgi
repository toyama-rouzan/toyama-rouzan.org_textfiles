#!/usr/bin/perl


use strict;
use CGI::Carp qw(fatalsToBrowser);
use warnings;
use Encode;

my $LINE_API_TOKEN = "1h073TNY63u245Qouu3YeJXC8rSppM3bjOhCtSlAkPv";
my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime;
my $message = "テストメッセージ($hour:$min $sec)";

my $command = "php /var/www/vhosts/w872.jpnsv.net/toyama-rouzan.org/member/labo/linenotify_test2.php $LINE_API_TOKEN \"$message\"";

$command = decode('Shift_JIS', $command);
$command = encode('UTF-8', $command);

open my $rs, "$command |";
my @rlist = <$rs>;
close $rs;
my $result = join '', @rlist;

print <<EOM;
Content-type: text/html; charset=shift_jis

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift-jis">
<title>LINE notify test 3-1</title>
</head>
<body>
<pre>
EOM

$command = decode('UTF-8', $command);
$command = encode('Shift_JIS', $command);
print "$command \n";
print "result:$result\n";

print <<EOM;
</pre>
</body>
</html>
EOM

exit;

