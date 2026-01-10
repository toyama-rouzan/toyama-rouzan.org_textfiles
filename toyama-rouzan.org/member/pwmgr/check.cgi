#!/usr/bin/perl

#┌─────────────────────────────────
#│ PasswordManager : check.cgi - 2013/11/17
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

# 外部ファイル取り込み
require './init.cgi';
my %cf = &init;

print <<EOM;
Content-type: text/html; charset=shift_jis

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>Check Mode</title>
</head>
<body>
<b>Check Mode: [ $cf{version} ]</b>
<ul>
EOM

my %log = (
	pwdfile => 'パスワードファイル',
	memfile => '会員ファイル',
	axsfile => 'アクセスログ',
);
foreach ( keys %log ) {
	# パス
	if (-e $cf{$_}) {
		print "<li>$log{$_}パス : OK\n";

		# パーミッション
		if (-r $cf{$_} && -w $cf{$_}) {
			print "<li>$log{$_}パーミッション : OK\n";
		} else {
			print "<li>$log{$_}パーミッション : NG\n";
		}
	} else {
		print "<li>$log{$_}パス : NG\n";
	}
}

# sendmail
if (-e $cf{sendmail}) {
	print "<li>sendmailパス : OK\n";
} else {
	print "<li>sendmailパス : NG\n";
}

foreach (qw(conf.html error.html message.html mail.txt)) {
	if (-f "$cf{tmpldir}/$_") {
		print "<li>$_位置 : OK\n";
	} else {
		print "<li>$_位置 : NG\n";
	}
}

print <<EOM;
</ul>
</body>
</html>
EOM

exit;

