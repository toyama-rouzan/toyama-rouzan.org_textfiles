#!/usr/bin/perl

#┌─────────────────────────────────
#│ JOYFUL NOTE : check.cgi - 2014/03/08
#│ copyright (c) KentWeb, 1997-2015
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

# 外部ファイル取込み
require './init.cgi';
my %cf = set_init();

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

# データファイル
my %log = (
	logfile => 'ログファイル',
	nofile  => '過去ログ記事ファイル',
	cntfile => 'カウントファイル',
	);
foreach ( keys(%log) ) {
	if (-f $cf{$_}) {
		print "<li>$log{$_}パス : OK\n";
		if (-r $cf{$_} && -w $cf{$_}) {
			print "<li>$log{$_}パーミッション : OK\n";
		} else {
			print "<li>$log{$_}パーミッション : NG\n";
		}
	} else {
		print "<li>$log{$_}パス : NG\n";
	}
}

# 画像ディレクトリ
if (-d $cf{imgdir}) {
	print "<li>アップロードディレクトリパス : OK\n";
	if (-r $cf{imgdir} && -w $cf{imgdir} && -x $cf{imgdir}) {
		print "<li>アップロードディレクトリパーミッション : OK\n";
	} else {
		print "<li>アップロードディレクトリパーミッション : NG\n";
	}
} else {
	print "<li>アップロードディレクトリパス : NG\n";
}

# テンプレート
foreach (qw(bbs find note error msg album res past edit topic topic2)) {
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

