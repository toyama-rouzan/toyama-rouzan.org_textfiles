#!/usr/bin/perl

#┌─────────────────────────────────
#│ TOPICS BOARD : check.cgi - 2013/06/02
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

# 外部ファイル取込み
require './init.cgi';
my %cf = init();

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
<li>Perlバージョン : $]
EOM

# ログファイル
if (-f $cf{logfile}) {
	print "<li>ログファイルパス : OK\n";
	if (-r $cf{logfile} && -w $cf{logfile}) {
		print "<li>ログパーミッション : OK\n";
	} else {
		print "<li>ログパーミッション : NG\n";
	}
} else {
	print "<li>ログファイルパス : NG\n";
}

# 画像ディレクトリ
if (-d $cf{imgdir}) {
	print "<li>アップロードディレクトリパス : OK\n";
	if (-r $cf{imgdir} && -w $cf{imgdir} && -x $cf{imgdir}) {
		print "<li>アップロードディレクトリのパーミッション : OK\n";
	} else {
		print "<li>アップロードディレクトリのパーミッション : NG\n";
	}
} else {
	print "<li>アップロードディレクトリパス : NG\n";
}

# テンプレート
my @tmpl = qw|bbs error find|;
foreach (@tmpl) {
	if (-e "$cf{tmpldir}/$_.html") {
		print "<li>テンプレート( $_.html ) : OK\n";
	} else {
		print "<li>テンプレート( $_.html ) : NG\n";
	}
}

# Image-Magick動作確認
eval { require Image::Magick; };
if ($@) {
	print "<li>Image-Magick動作: NG\n";
} else {
	print "<li>Image-Magick動作: OK\n";
}

print <<EOM;
</ul>
</body>
</html>
EOM
exit;

