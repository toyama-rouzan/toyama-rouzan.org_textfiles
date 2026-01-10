#!/usr/bin/perl

#┌────────────────────────
#│ PasswordManager : admin.cgi - 2013/01/30
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

# 設定ファイル認識
require "./init.cgi";
my %cf = &init;

# データ受理
my %in = &parse_form;

# 認証
&check_passwd;

# 管理モード
if ($in{member_new}) { &member_new; }
if ($in{member_edit}) { &member_edit; }
if ($in{access_log}) { &access_log; }
&menu_html;

#-----------------------------------------------------------
#  メニュー画面
#-----------------------------------------------------------
sub menu_html {
	&header("メニューTOP");

	print <<EOM;
<div class="ttl">■ 管理メニュー</div>
<ul>
<li>選択ボタンを押してください。
<li>アクセスログ集計は別途「SSI + pwlog.cgi」による埋め込みが必要です。
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<table class="tbl-top">
<tr>
	<th>選択</th>
	<th class="w250">処理メニュー</th>
</tr><tr>
	<td><input type="submit" name="member_new" value="選択"></td>
	<td>会員管理（新規登録）</td>
</tr><tr>
	<td><input type="submit" name="member_edit" value="選択"></td>
	<td>会員管理（修正/削除）</td>
</tr><tr>
	<td><input type="button" value="選択" onclick="javascript:window.location='$cf{admin_cgi}'"></td>
	<td>ログアウト</td>
</tr>
</table>
</form>
</ul>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  会員管理（新規）
#-----------------------------------------------------------
sub member_new {
	my ($id,$nam,$eml,$memo) = @_;
	$memo =~ s/<br>/\n/g;

	# 登録実行
	if ($in{job} eq 'new') { &add_data; }

	# 登録フォーム
	&header("会員登録フォーム");
	&back_btn;
	print <<EOM;
<div class="ttl">■ 会員登録フォーム</div>
<ul>
<li>各項目を入力して送信ボタンを押してください。
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
EOM

	if ($in{member_new}) {
		print qq|<input type="hidden" name="member_new" value="1">\n|;
		print qq|<input type="hidden" name="job" value="new">\n|;
	} else {
		print qq|<input type="hidden" name="member_edit" value="1">\n|;
		print qq|<input type="hidden" name="job" value="edit2">\n|;
		print qq|<input type="hidden" name="id" value="$in{id}">\n|;
	}

	print <<EOM;
<table class="tbl-top">
<tr>
	<th>名前</th>
	<td><input type="text" name="name" size="30" value="$nam"></td>
</tr><tr>
	<th>E-mail</th>
	<td><input type="text" name="email" size="30" value="$eml"></td>
</tr><tr>
	<th>ユーザID</th>
EOM

	if ($in{member_new}) {
		print qq|<td><input type="text" name="id" size="20" maxlength="20" style="ime-mode:inactive">\n|;
		print qq|(入力必須。英数字で20文字以内)</td></tr>\n|;
		print qq|<tr><th>パスワード</th>\n|;
		print qq|<td><input type="text" name="pw" size="20" maxlength="20" style="ime-mode:inactive">\n|;
		print qq|(入力必須。英数字で20文字以内)</td></tr>\n|;
	} else {
		print qq|<td><b>$id</b></td></tr>\n|;
	}

	print <<EOM;
<tr>
	<th>備考</th>
	<td><textarea name="memo" cols="30" rows="4">$memo</textarea></td>
</tr>
</table>
<input type="submit" value="送信する">
EOM

	if (!$in{member_new}) { &chg_pwd_form; }

	print <<EOM;
</form>
</ul>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  会員管理（メンテ）
#-----------------------------------------------------------
sub member_edit {
	# ページ定義
	my $pg;
	foreach ( keys(%in) ) {
		if (/^page:(\d+)$/) {
			$pg = $1;
			last;
		}
	}
	$pg ||= 0;

	# 修正フォーム
	if ($in{job_edit} && $in{id}) {

		# PWファイル
		my @log;
		open(IN,"$cf{memfile}") or &err("open err: $cf{memfile}");
		while (<IN>) {
			my ($id,$nam,$eml,$memo) = split(/<>/);

			if ($in{id} eq $id) {
				@log = ($id,$nam,$eml,$memo);
				last;
			}
		}
		close(IN);

		if (@log == 0) { &err("該当のID情報が見当たりません"); }
		&member_new(@log);

	# 修正実行
	} elsif ($in{job} eq "edit2" && !$in{pwchg}) {

		# 会員ファイル
		my @new;
		open(DAT,"+< $cf{memfile}") or &err("open err: $cf{memfile}");
		while (<DAT>) {
			my ($id,$nam,$eml,$memo) = split(/<>/);

			if ($in{id} eq $id) {
				$_ = "$id<>$in{name}<>$in{email}<>$in{memo}<>\n";
			}
			push(@new,$_);
		}
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# パスワード強制変更
	} elsif ($in{pwchg} && $in{pw1} ne '' && $in{pw2} ne '') {

		# チェック
		if ($in{pw1} ne $in{pw2}) { &err("パスワードの再入力が異なります"); }

		# PWを暗号化
		my $pwd = &encrypt($in{pw1});

		# PWファイル
		my @new;
		open(DAT,"+< $cf{pwdfile}") or &err("open err: $cf{pwdfile}");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($id,$pw) = split(/:/);

			if ($in{id} eq $id) { $_ = "$id:$pwd\n"; }

			push(@new,$_);
		}
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# 削除
	} elsif ($in{job_dele} && $in{id}) {

		# 削除情報
		my %del;
		foreach ( split(/\0/, $in{id}) ) {
			$del{$_}++;
		}

		# PWファイル
		my @new;
		open(DAT,"+< $cf{pwdfile}") or &err("open err: $cf{pwdfile}");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($id,undef) = split(/:/);
			next if (defined($del{$id}));

			push(@new,$_);
		}
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# 会員ファイル
		@new = ();
		open(DAT,"+< $cf{memfile}") or &err("open err: $cf{memfile}");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($id) = (split(/<>/))[0];
			next if (defined($del{$id}));

			push(@new,$_);
		}
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);
	}

	# キーワード検索準備（Shift-JIS定義）
	my $ascii = '[\x00-\x7F]';
	my $hanka = '[\xA1-\xDF]';
	my $kanji = '[\x81-\x9F\xE0-\xFC][\x40-\x7E\x80-\xFC]';

	&header("会員管理");
	&back_btn;
	print <<EOM;
<div class="ttl">■ 会員管理</div>
<ul>
<li>処理を選択して送信ボタンを押してください。
</ul>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="member_edit" value="1">
<input type="submit" name="job_edit" value="修正">
<input type="submit" name="job_dele" value="削除">
&nbsp; &nbsp; &nbsp;
<input type="text" name="find" value="$in{find}" size="20">
<input type="submit" name="job_find" value="検索"> （ID又は名前の検索）<br>
<table class="tbl-top">
<tr>
  <th>選択</th>
  <th>ID名</th>
  <th>名前</th>
  <th>備考</th>
</tr>
EOM

	my $i = 0;
	open(IN,"$cf{memfile}") or &err("open err: $cf{memfile}");
	while (<IN>) {
		my ($id,$nam,$eml,$memo) = split(/<>/);

		# 検索のとき
		if ($in{find} ne '' && ($in{job_find} || $pg)) {
			next if ("$id $nam" !~ /^(?:$ascii|$hanka|$kanji)*?\Q$in{find}\E/i);
		}

		$i++;
		next if ($i < $pg + 1);
		next if ($i > $pg + $cf{pageView});

		$nam ||= '名前なし';
		$eml &&= qq|<a href="mailto:$eml">$nam</a>|;
		$memo =~ s/<br>/ /g;

		print qq|<tr><td align="center"><input type="checkbox" name="id" value="$id"></td>|;
		print qq|<td><b>$id</b></td>|;
		print qq|<td>$nam<br></td>|;
		print qq|<td>$memo<br></td></tr>\n|;
	}
	close(IN);

	print <<EOM;
</table>
EOM

	# 繰越ページ
	my $next = $pg + $cf{pageView};
	my $back = $pg - $cf{pageView};

	if ($back >= 0) {
		print qq|<input type="submit" name="page:$back" value="前の$cf{pageView}件">\n|;
	}
	if ($next < $i) {
		print qq|<input type="submit" name="page:$next" value="次の$cf{pageView}件">\n|;
	}

	print <<EOM;
</form>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  アクセスログ集計
#-----------------------------------------------------------
sub access_log {
	# ページ定義
	my $pg;
	foreach ( keys(%in) ) {
		if (/^page:(\d+)$/) {
			$pg = $1;
			last;
		}
	}
	$pg ||= 0;

	&header("アクセスログ集計");
	&back_btn;
	print <<EOM;
<div class="ttl">■ アクセスログ集計</div>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="access_log" value="1">
<input type="submit" name="list" value="一覧">
<input type="submit" name="calc" value="集計">
EOM

	# 集計のとき
	if ($in{calc}) { &calc_aclog; }

	# ログ展開
	my $i = 0;
	open(IN,"$cf{axsfile}") or &err("open err: $cf{axsfile}");
	while (<IN>) {
		$i++;
		next if ($i < $pg + 1);
		last if ($i > $pg + $cf{pageView});

		my ($id,$date,$host,$agent) = split(/<>/);

		print qq|<div class="dot">[ ID ] $id</div>\n|;
		print "[ DATE ] $date<br>\n";
		print "[ HOST ] $host<br>\n";
		print "[ AGENT ] $agent\n";
	}
	close(IN);

	print qq|<div class="dot"></div>\n|;

	# 繰越ページ
	my $next = $pg + $cf{pageView};
	my $back = $pg - $cf{pageView};

	if ($back >= 0) {
		print qq|<input type="submit" name="page:$back" value="前の$cf{pageView}件">\n|;
	}
	if ($next < $i) {
		print qq|<input type="submit" name="page:$next" value="次の$cf{pageView}件">\n|;
	}

	print "</body></html>\n";
	exit;
}

#-----------------------------------------------------------
#  ログ集計
#-----------------------------------------------------------
sub calc_aclog {
	# ログ展開
	my %ac;
	open(IN,"$cf{axsfile}") or &err("open err: $cf{axsfile}");
	while (<IN>) {
		my ($id,$date,$host,$agent) = split(/<>/);

		# アクセス数を数える
		$ac{$id}++;
	}
	close(IN);

	# IDとカウント数を配列化
	my (@id,@ac);
	foreach ( keys(%ac) ) {
		push(@id,$_);
		push(@ac,$ac{$_});
	}

	# ソート
	@id = @id[sort{$ac[$b] <=> $ac[$a]} 0 .. $#ac];

	# 集計テーブル
	print <<EOM;
<table class="tbl-top">
<tr>
	<th nowarp>ID</th>
	<th nowarp>アクセス数</th>
</tr>
EOM

	foreach (@id) {
		print qq|<tr><td>$_</td>|;
		print qq|<td align="right">$ac{$_}</td></tr>\n|;
	}

	print "</table>\n";
	print "</body></html>\n";
	exit;
}

#-----------------------------------------------------------
#  パスワード変更フォーム
#-----------------------------------------------------------
sub chg_pwd_form {
	print <<EOM;
<br><br>
<li>パスワードを変更する場合
<table class="tbl-top">
<tr>
	<th>パスワード</th>
	<td>
		<input type="password" name="pw1" size="20"> （英数字で20文字以内）<br>
		<input type="password" name="pw2" size="20"> （再度入力）
	</td>
</tr>
</table>
<input type="submit" name="pwchg" value="送信する">
EOM
}

#-----------------------------------------------------------
#  パスワード認証
#-----------------------------------------------------------
sub check_passwd {
	# パスワードが未入力の場合は入力フォーム画面
	if ($in{pass} eq "") {
		&enter_form;

	# パスワード認証
	} elsif ($in{pass} ne $cf{password}) {
		&err("認証できません");
	}
}

#-----------------------------------------------------------
#  会員登録フォーム
#-----------------------------------------------------------
sub add_data {
	# チェック
	if ($in{id} eq "" || $in{pw} eq "") {
		&err("ID又はパスワードが未入力です");
	}

	# IDの重複チェック
	my ($flg,@data);
	open(DAT,"+< $cf{pwdfile}") or &err("open err: $cf{pwdfile}");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		my ($id,$pw) = split(/:/);

		if ($in{id} eq $id) {
			$flg++;
			last;
		}
		push(@data,$_);
	}

	if ($flg) {
		close(DAT);
		&err("<b>$in{id}</b>は既に発行済です");
	}

	# 暗号化
	my $crypt = &encrypt($in{pw});

	seek(DAT, 0, 0);
	print DAT @data;
	print DAT "$in{id}:$crypt\n";
	truncate(DAT, tell(DAT));
	close(DAT);

	# 会員ファイル更新
	open(DAT,">> $cf{memfile}") or &err("open err: $cf{memfile}");
	eval "flock(DAT, 2);";
	print DAT "$in{id}<>$in{name}<>$in{email}<>$in{memo}<>\n";
	close(DAT);

	&message("登録を完了しました");
}

#-----------------------------------------------------------
#  入室画面
#-----------------------------------------------------------
sub enter_form {
	&header("入室画面");
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
sub err {
	my $err = shift;

	&header("ERROR!");
	print <<EOM;
<div align="center">
<hr width="350">
<h3>ERROR!</h3>
<p class="err">$err</p>
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

	&header("完了");
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
#  HTMLヘッダ
#-----------------------------------------------------------
sub header {
	my $ttl = shift;

	print <<EOM;
Content-type: text/html; charset=shift_jis

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
<!--
body,th,td { background:#f0f0f0; font-size:80%; }
div.ttl { border-bottom:1px solid #004080; color:#004080; font-weight:bold; padding:3px; }
p.err { color:#dd0000; }
table.tbl-top { border-collapse:collapse; margin:1em 0; }
table.tbl-top th { padding:6px; border:1px solid #333; background:#8cc6ff; }
table.tbl-top td { padding:6px; border:1px solid #333; background:#fff; }
.w250 { width:250px; }
div.dot { border-top:1px dashed #8080c0; margin-top:5px; padding-top:4px; }
-->
</style>
<title>$ttl</title>
</head>
<body>
EOM
}

#-----------------------------------------------------------
#  戻りボタン
#-----------------------------------------------------------
sub back_btn {
	print <<EOM;
<div align="right">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="▲管理TOP">
</form>
</div>
EOM
}

