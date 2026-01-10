#!/usr/bin/perl

use utf8;
use strict;
use CGI::Carp qw(fatalsToBrowser);
use warnings;
use Net::POP3;

use lib "./lib";
use Jcode;

my $server = 'mail.toyama-rouzan.org';      # メールサーバ名
my $user = 'ml-t0yamar0uzan@toyama-rouzan.org';              # ユーザ名
my $pass = 'tsurugi2999yakushi2926';            # パスワード
my $kcode = "utf-8";               # 表示の際の漢字コード
my $result = "no data";

my $pop = Net::POP3->new($server,SSL => 1,Timeout => 60) || die "pop";
#$pop->user($user) || die "user";
#$pop->pass($pass) || die "pass";
#$pop->login($user,$pass) || die 'login';
$pop->apop($user,$pass) || die 'apop';


print <<EOM;
Content-type: text/html; charset=utf-8

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<title>POP3 テスト</title>
</head>
<body>
<pre>
EOM

print "\nlist()\n";
my $refOfList = $pop->list();
while (my ($name, $value) = each(%$refOfList)) {
	print "MsgNum:$name size:$value bytes\n";
}
print "\nuidl()\n";
my $refOfUIDL = $pop->uidl();
while (my ($name, $value) = each(%$refOfUIDL)) {
	print "MsgNum:$name UIDL:$value\n";
	my $msg = $pop->get($name);
	print "---メッセージ---\n";
	foreach my $line (@$msg){
		print $line;
	}
	print "\n---end---\n";
}



print <<EOM;
</pre>
</body>
</html>
EOM

exit;

