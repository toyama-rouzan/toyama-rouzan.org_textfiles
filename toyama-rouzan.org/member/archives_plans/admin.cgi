#!/usr/bin/perl

#┌─────────────────────────────────
#│ UP-LOADER : admin.cgi - 2019/12/15
#│ copyright (c) kentweb, 1997-2019
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);
use lib "./lib";
use CGI::Minimal;

# 設定ファイル認識
require "./init.cgi";
my %cf = set_init();

# データ受理
CGI::Minimal::max_read_size($cf{maxdata});
my $cgi = CGI::Minimal->new;
error('容量オーバー') if ($cgi->truncated);
my %in = parse_form($cgi);

# 認証
check_passwd();

# 管理モード
if ($in{mode_data}) { mode_data(); }
if ($in{mode_dlog}) { mode_dlog(); }
mode_data();

#-----------------------------------------------------------
#  データ画面画面
#-----------------------------------------------------------
sub mode_data {
	# 削除処理
	if ($in{del} && $in{no}) {
		
		# 削除情報
		my %del;
		for ( $cgi->param('no') ) { $del{$_}++; }
		
		# 削除情報をマッチング
		my @log;
		open(DAT,"+< $cf{logfile}") or error("open err: $cf{logfile}");
		eval "flock(DAT,2);";
		while (<DAT>) {
			my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host,$fnam) = split(/<>/);
			
			if (defined $del{$no}) {
				unlink("$cf{upldir}/$rand/$fnam.$ex");
				rmdir("$cf{upldir}/$rand");
				next;
			}
			push(@log,$_);
		}
		seek(DAT,0,0);
		print DAT @log;
		truncate(DAT,tell(DAT));
		close(DAT);
		
		# カウントファイル削除
		my @log;
		open(DAT,"+< $cf{cntfile}") or error("open err: $cf{cntfile}");
		eval "flock(DAT,2);";
		while(<DAT>) {
			my ($no,undef) = split(/:/);
			next if (defined $del{$no});
			push(@log,$_);
		}
		# 更新
		seek(DAT,0,0);
		print DAT @log;
		truncate(DAT,tell(DAT));
		close(DAT);
	
	# パス変更
	} elsif ($in{rename}) {
		if (!$in{no}) { error('変更するファイル名にチェックを入れてください'); }
		
		# ファイル名変更
		file_rename();
	}
	
	# 画面表示
	header("データ画面","js");
	menu_btn();
	print <<"EOM";
<div id="main">
<div id="ttl">■ データ管理</div>
<ul>
<li>チェックボタンをチェックして実行ボタンを押します。
<li>ファイルへの直接リンクを避けるため、ファイルの「パス変更」を行うことができます。
</ul>
<form action="$cf{admin_cgi}" method="post" name="allchk">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="mode_data" value="1">
<div id="ope-btn">
<input type="submit" name="del" value="削除" class="btn" onclick="return confirm('削除しますか？');">
<input type="submit" name="rename" value="パス変更" class="btn">
</div>
<table class="form-tbl">
<tr>
	<th><input type="button" onclick="allcheck();" value="全選択"></th>
	<th>アップ日時</th>
	<th>ファイル名</th>
	<th>サイズ</th>
</tr>
EOM

	open(IN,"$cf{logfile}") or error("open err: $cf{logfile}");
	while (<IN>) {
		my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host,$fnam) = split(/<>/);
		
		print qq|<td class="ta-c"><input type="checkbox" name="no" value="$no"></td>|;
		print qq|<td>$date</td>|;
		print qq|<td><a href="$cf{uplurl}/$rand/$fnam.$ex" target="_blank">$fnam.$ex</a></td>|;
		print qq|<td class="ta-r">$size</td></tr>\n|;
	}
	close(IN);
	
	print <<EOM;
</table>
</form>
</div>
EOM
	footer();
}

#-----------------------------------------------------------
#  DLログ画面
#-----------------------------------------------------------
sub mode_dlog {
	my %fnam;
	open(IN,"$cf{logfile}") or error("open err: $cf{logfile}");
	while (<IN>) {
		my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host,$fnam) = split(/<>/);
		
		if (length($fnam) > $cf{file_max}) { $fnam = substr($fnam,0,$cf{file_max}) . '..'; }
		$fnam{$no} = "$fnam.$ex";
	}
	close(IN);
	
	# 画面表示
	header("DLログ閲覧");
	menu_btn();
	print <<"EOM";
<div class="body">
<div id="ttl">■ DLログ閲覧</div>
<table class="form-tbl">
<tr>
	<th>内容</th>
	<th>日時</th>
	<th>ファイル</th>
	<th>ホスト情報</th>
</tr>
EOM

	my %job = (dl => 'DL成功', err => '認証ミス');
	open(IN,"$cf{dlfile}") or error("open err: $cf{dlfile}");
	while (<IN>) {
		my ($job,$num,$date,$host) = split(/<>/);
		
		print qq|<tr><td class="ta-c">$job{$job}</td>|;
		print qq|<td>$date</td>|;
		print qq|<td class="grn">$fnam{$num}</td>|;
		print qq|<td>$host</td></tr>\n|;
	}
	close(IN);
	
	print <<EOM;
</table>
</div>
EOM
	footer();
}

#-----------------------------------------------------------
#  ファイル名変更
#-----------------------------------------------------------
sub file_rename {
	# 対象ファイル
	my %ren;
	for ( $cgi->param('no') ) { $ren{$_}++; }
	
	# データ更新
	my ($i,@log);
	open(DAT,"+< $cf{logfile}") or error("open err: $cf{logfile}");
	eval "flock(DAT,2);";
	while (<DAT>) {
		my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host,$fnam) = split(/<>/);
		
		if (defined $ren{$no}) {
			# 乱数作成
			my $new = make_rand();
			
			# リネーム
			rename("$cf{upldir}/$rand/$fnam.$ex","$cf{upldir}/$new/$fnam.$ex");
			
			# フォーマット
			$i++;
			$_ = "$no<>$date<>$mime<>$ex<>$new<>$com<>$del<>$lock<>$size<>$host<>$fnam<>\n";
		}
		push(@log,$_);
	}
	seek(DAT,0,0);
	print DAT @log;
	truncate(DAT,tell(DAT));
	close(DAT);
	
	# 完了
	message("$i個のファイルパス名を変更しました");
}

#-----------------------------------------------------------
#  HTMLヘッダー
#-----------------------------------------------------------
sub header {
	my ($ttl,$js) = @_;

	print <<EOM;
Content-type: text/html; charset=utf-8

<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<style>
body { font-size:90%; padding:0; margin:0; background:#FFF8C2; font-family:'Hiragino Kaku Gothic ProN','ヒラギノ角ゴ ProN W3',Meiryo,メイリオ,Osaka,'MS PGothic',arial,helvetica,sans-serif; }
#head { background:#A99770; color:#fff; padding:3px 6px; font-weight:bold; }
#body { display:table; width:100%; }
#menu { display:table-cell; width:180px;}
#main { display:table-cell; padding:0 1em; }
#foot { background:#A99770; clear:both; }
#ttl { font-weight:bold; color:#FF934B; border-bottom:1px solid #FF934B; padding:2px; margin-bottom:1em; }
.form-tbl { border-collapse:collapse; margin:1em 0; }
.form-tbl th, .form-tbl td { border:1px solid #666; padding:4px 8px; }
.form-tbl th { background:#eee; }
.form-tbl td { background:#fff; }
.menu-btn { border-collapse:collapse; width:150px; margin:1em auto; }
.menu-btn th { border:1px solid #A99770; background:#fff; padding:4px 2px; height:38px; }
.menu-btn input { width:120px; }
#login { width:400px; margin:3em auto; text-align:center; }
#login fieldset { padding:2em; }
#login input[type="password"] { width:190px; padding:3px; }
#login input[type="submit"] { width:50px; height:27px; }
img.icon { vertical-align:middle; }
#note { border:1px dotted #333; padding:6px; width:650px; background:#fff; }
#note p { margin:0 0 10px 6px; color:#2f7b37; font-weight:bold; }
#msg { border:1px dotted #333; padding:1em; width:500px; background:#fff; text-align:center; border-radius:6px; margin-top:2em; }
#msg p { color:green; }
#err { border:1px dotted red; padding:1em; width:400px; background:#fff; text-align:center; border-radius:6px; margin:3em; color:red; }
#ope-btn input { width:90px; }
.ta-c { text-align:center; }
.ta-r { text-align:right; }
.grn { color:#008942; }
</style>
EOM

	js_boxchk() if ($js eq 'js');

	print <<EOM;
<title>$ttl</title>
</head>
<body>
<div id="head"><img src="$cf{cmnurl}/star.png" alt="star" class="icon"> UPLOADER 管理画面 :: </div>
<div id="body">
EOM
}

#-----------------------------------------------------------
#  javascriptチェック
#-----------------------------------------------------------
sub js_boxchk {
	print <<'EOM';
<script>
function allcheck() {
	var check = document.getElementsByName('no');
	
    var cnt = check.length;
	for ( var i = 0; i < cnt; i++ ) {
		if (check.item(i).checked) {
			check.item(i).checked = false;
		} else {
			check.item(i).checked = true;
		}
	}
}
</script>
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
<form action="$cf{admin_cgi}" method="post">
<div id="login">
	<fieldset><legend> password </legend>
		<input type="password" name="pass">
		<input type="submit" value="認証">
	</fieldset>
</div>
</form>
<script>self.document.forms[0].pass.focus();</script>
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
<div class="ta-c">
<hr width="350">
<h3>ERROR!</h3>
<p class="err">$msg</p>
<hr width="350">
<p><input type="button" value="前画面に戻る" onclick="history.back()"></p>
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
<div class="ta-c" style="margin-top:3em;">
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
		mode_data => 'データ管理',
		mode_dlog => 'DLログ閲覧',
	);
	
	print <<EOM;
<div id="menu">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<table class="menu-btn">
EOM

	foreach (qw(mode_data mode_dlog)) {
		if ($in{$_}) {
			print qq|<tr><th><input type="submit" name="$_" value="$menu{$_}" disabled></th></tr>\n|;
		} else {
			print qq|<tr><th><input type="submit" name="$_" value="$menu{$_}"></th></tr>\n|;
		}
	}
	
	print <<EOM;
<tr>
	<th><input type="button" value="一般画面に戻る" onclick="window.open('$cf{upload_cgi}','_top')"></th>
</tr><tr>
	<th><input type="button" value="ログオフ" onclick="window.open('$cf{admin_cgi}','_top')"></th>
</tr>
</table>
</form>
</div>
EOM
}

#-----------------------------------------------------------
#  フッター
#-----------------------------------------------------------
sub footer {
	print <<EOM;
<div class="foot">
</div>
</body>
</html>
EOM
	exit;
}

