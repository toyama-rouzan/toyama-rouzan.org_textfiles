#!/usr/bin/perl

#┌─────────────────────────────────
#│ KEY SEARCH : admin.cgi - 2013/01/01
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);
use lib "./lib";
use CGI::Simple;

# 設定ファイル認識
require "./init.cgi";
my %cf = init();

# データ受理
$CGI::Simple::DISABLE_UPLOADS = 0;
$CGI::Simple::POST_MAX = $cf{maxdata};
my $cgi = new CGI::Simple;
error('容量オーバー') if ($cgi->cgi_error);
my %in = parse_form($cgi);

# 認証
check_passwd();

# 管理モード
if ($in{mode_data})  { mode_data(); }
if ($in{mode_dllog}) { mode_dllog(); }
mode_data();

#-----------------------------------------------------------
#  データ画面画面
#-----------------------------------------------------------
sub mode_data {
	# 削除処理
	if ($in{del} && $in{no}) {

		my %del;
		foreach ( $cgi->param('no') ) {
			$del{$_}++;
		}

		# 削除情報をマッチング
		my @log;
		open(DAT,"+< $cf{logfile}") or error("open err: $cf{logfile}");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host) = split(/<>/);

			if (defined($del{$no})) {
				unlink("$cf{upldir}/$rand.$ex");
				next;
			}
			push(@log,$_);
		}
		seek(DAT, 0, 0);
		print DAT @log;
		truncate(DAT, tell(DAT));
		close(DAT);

	# ファイル名変更
	} elsif ($in{rename}) {
		if (!$in{no}) { error('変更するファイル名にチェックを入れてください'); }

		# ファイル名変更
		file_rename();
	}

	# 画面表示
	header("データ画面");
	menu_btn();
	print <<"EOM";
<div class="body">
<p class="ttl">■ データ管理</p>
<ul>
<li>チェックボタンをチェックして実行ボタンを押します。
<li>ファイルへの直接リンクを避けるため、「ファイル名の変更」を行うことができます。
</ul>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="mode_data" value="1">
実行ボタン : 
<input type="submit" name="del" value="削除する" class="btn">
&nbsp;
<input type="submit" name="rename" value="ファイル名変更" class="btn">
<dl>
EOM

	open(IN,"$cf{logfile}") or error("open err: $cf{logfile}");
	while (<IN>) {
		my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host) = split(/<>/);

		print qq|<dt><hr><input type="checkbox" name="no" value="$no">|;
		print qq|[<b>$no</b>] 日時：$date &lt;$host&gt;|;
		print qq|<dd>ファイル名 : <a href="$cf{uplurl}/$rand.$ex" target="_blank">$rand.$ex</a> ($size bytes)\n|;
	}
	close(IN);

	print <<EOM;
</dl>
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  DLログ画面
#-----------------------------------------------------------
sub mode_dllog {
	# 画面表示
	header("DLログ閲覧");
	menu_btn();
	print <<"EOM";
<div class="body">
<p class="ttl">■ DLログ閲覧</p>
<ol>
EOM

	my %job = (dl => 'DL成功', err => '認証ミス');
	open(IN,"$cf{dlfile}") or error("open err: $cf{dlfile}");
	while (<IN>) {
		my ($job,$num,$date,$host) = split(/<>/);

		print qq|<li>[$job{$job}] <b>$num</b> - $date &lt;$host&gt;<br>\n|;
	}
	close(IN);

	print <<EOM;
</ol>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  ファイル名変更
#-----------------------------------------------------------
sub file_rename {
	# 対象ファイル
	my %ren;
	foreach ( $cgi->param('no') ) {
		$ren{$_}++;
	}

	# 念のため
	srand;

	# データ更新
	my ($i,@log);
	open(DAT,"+< $cf{logfile}") or error("open err: $cf{logfile}");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host) = split(/<>/);

		if (defined($ren{$no})) {
			# 乱数作成
			my $new = make_rand();

			# リネーム
			rename("$cf{upldir}/$rand.$ex","$cf{upldir}/$new.$ex");

			# フォーマット
			$i++;
			$_ = "$no<>$date<>$mime<>$ex<>$new<>$com<>$del<>$lock<>$size<>$host<>\n";
		}
		push(@log,$_);
	}
	seek(DAT, 0, 0);
	print DAT @log;
	truncate(DAT, tell(DAT));
	close(DAT);

	# 完了
	message("$i個のファイル名を変更しました");
}

#-----------------------------------------------------------
#  HTMLヘッダー
#-----------------------------------------------------------
sub header {
	my $ttl = shift;

	print <<EOM;
Content-type: text/html; charset=shift_jis

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
<!--
body,td,th { font-size:80%; background:#f0f0f0; }
p.ttl { font-weight:bold; color:#004080; border-bottom:1px solid #004080; padding:2px; width:100%; }
p.err { color:#dd0000; }
p.msg { color:#006400; }
table.menu-btn { border-collapse:collapse; width:150px; }
table.menu-btn th { border:1px solid #383872; background:#cccce6; padding:4px; height:38px; }
table.menu-btn input { width:130px; }
div.menu { float:left; width:170px; padding:1.5em; }
div.body { float:left; padding:1.5em; }
input.btn { width:110px; }
-->
</style>
<title>$ttl</title>
</head>
<body>
EOM
}

#-----------------------------------------------------------
#  パスワード認証
#-----------------------------------------------------------
sub check_passwd {
	# パスワードが未入力の場合は入力フォーム画面
	if ($in{pass} eq "") {
		enter_form();

	# パスワード認証
	} elsif ($in{pass} ne $cf{password}) {
		error("認証できません");
	}
}

#-----------------------------------------------------------
#  入室画面
#-----------------------------------------------------------
sub enter_form {
	header("入室画面");
	print <<EOM;
<div align="center">
<form action="$cf{admin_cgi}" method="post">
<table width="380" style="margin-top:50px">
<tr>
	<td height="40" align="center">
		<fieldset><legend>管理パスワード入力</legend><br>
		<input type="password" name="pass" value="" size="20">
		<input type="submit" value=" 認証 "><br><br>
		</fieldset>
	</td>
</tr>
</table>
</form>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  エラー
#-----------------------------------------------------------
sub error {
	my $msg = shift;

	header("ERROR!");
	print <<EOM;
<div align="center">
<hr width="350">
<h3>ERROR!</h3>
<p class="err">$msg</p>
<hr width="350">
<form>
<input type="button" value="前画面に戻る" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  完了メッセージ
#-----------------------------------------------------------
sub message {
	my $msg = shift;

	header("完了");
	print <<EOM;
<div align="center" style="margin-top:3em;">
<hr width="350">
<p class="msg">$msg</p>
<hr width="350">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="管理画面に戻る">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  メニューボタン
#-----------------------------------------------------------
sub menu_btn {
	my %menu = (
		mode_data  => 'データ管理',
		mode_dllog => 'DLログ閲覧',
	);

	print <<EOM;
<div class="menu">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<table class="menu-btn">
EOM

	foreach ( 'mode_data','mode_dllog' ) {
		if ($in{$_}) {
			print qq|<tr><th><input type="submit" name="$_" value="$menu{$_}" disabled></th></tr>\n|;
		} else {
			print qq|<tr><th><input type="submit" name="$_" value="$menu{$_}"></th></tr>\n|;
		}
	}

	print <<EOM;
<tr>
	<th><input type="button" value="一般画面に戻る" onclick=window.open("$cf{upload_cgi}","_top")></th>
</tr><tr>
	<th><input type="button" value="ログオフ" onclick=window.open("$cf{admin_cgi}","_top")></th>
</tr>
</table>
</form>
</div>
EOM
}

