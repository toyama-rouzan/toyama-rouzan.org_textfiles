#!/usr/bin/perl

#┌─────────────────────────────────
#│ Perl Module Viewer : module.cgi - 2012/05/13
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────
my $ver = 'Perl Module Viewer v1.5';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);
use File::Find;

my @mod;
foreach (@INC) {
	next if ($_ eq '.');
	push(@mod,$_);
}

# HTML出力
&print_html;

# 検索開始
my ($i,@data,@sort);
find(\&dir, @mod);

# ソート
@data = @data[sort { lc $sort[$a] cmp lc $sort[$b] } 0 .. $#sort];

# 結果表示
my $i = 0;
foreach (@data) {
	my ($nam,$pkg,$ver) = split(/\t/);

	$i++;
	my $col = $i % 2 ? 'col1' : 'col2';
	print qq|<tr class="$col"><td class="no">$i</td>\n|;
	print qq|<td class="mod">$nam</td>\n|;
	print qq|<td class="pkg">$pkg</td>\n|;
	print qq|<td class="ver">$ver</td></tr>\n|;
}

#フッター
&print_foot;

#-----------------------------------------------------------
#  検索
#-----------------------------------------------------------
sub dir {
	next if (!/\.pm$/);

	# ファイルパス
	my $fnam = $File::Find::name;

	# モジュール読み込み
	open(IN,"$fnam");
	my $pm = join('',<IN>);
	close(IN);

	# パッケージ/バージョン取得
	my $pkg = $pm =~ /package ([\w\:]+);/ ? $1 : 'unknown';
	my $ver = $pm =~ /VERSION\s*=\s*['"]([\d\.]+)['"];/ ? $1 : '-';

	push(@sort,$_);
	push(@data,"$_\t$pkg\t$ver");
}

#-----------------------------------------------------------
#  HTML出力
#-----------------------------------------------------------
sub print_html {
	print <<EOM;
Content-type: text/html; charset=shift_jis

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
<!--
body { font-family:Verdana,Helvetica,Arial; }
h1 { font-size:130%; }
p { font-size:10px; text-align:center; }
table { border-collapse:collapse; table-layout:fixed; }
td.mod { width:220px; font-size:11px; }
td.pkg { width:460px; font-size:9px; }
td.ver { width:60px; font-size:11px; }
td.no  { width:30px; font-size:11px; text-align:center; }
th,td { border:1px solid #999999; padding:2px; }
.col1 { background:#c4ffe1; }
.col2 { background:#fff; }
-->
</style>
<title>Perlモジュール・ビューワー</title>
</head>
<body>
<h1>$ver</h1>
<table>
<tr>
	<td class="no">No.</td>
	<td class="mod">モジュール名</td>
	<td class="pkg">パッケージ名</td>
	<td class="ver">バージョン</td>
</tr>
EOM
}

#-----------------------------------------------------------
#  フッター出力
#-----------------------------------------------------------
sub print_foot {
	print <<EOM;
</table>
<!-- 著作権表\示（削除不可）-->
<p>- <a href="http://www.kent-web.com/">$ver</a> -</p>
</body>
</html>
EOM
	exit;
}

