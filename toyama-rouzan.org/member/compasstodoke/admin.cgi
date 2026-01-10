#!/usr/bin/perl

#┌─────────────────────────────────
#│ JOYFUL NOTE : admin.cgi - 2019/11/03
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
cgi_err('容量オーバー') if ($cgi->truncated);
my %in = parse_form($cgi);

# 認証
check_passwd();

# 管理モード
admin_art();

#-----------------------------------------------------------
#  記事管理
#-----------------------------------------------------------
sub admin_art {
	# 修正フォーム
	if ($in{job} eq "edit" && $in{no}) {
		
		my @log;
		open(DAT,"$cf{logfile}") or cgi_err("open err: $cf{logfile}");
		my $top = <DAT>;
		while (<DAT>) {
			my ($no,$reno,$date,$name,$eml,$sub,$com,$url,$host,$pw,$col,$ext,$w,$h,$chk) = split(/<>/);
			
			if ($in{no} == $no) {
				@log = ($name,$eml,$sub,$com,$url,$col,$ext);
				last;
			}
		}
		close(DAT);
		
		if (@log == 0) { cgi_err("該当記事は存在しません"); }
		
		# 修正フォーム
		edit_form(@log);
	
	# 修正実行
	} elsif ($in{job} eq "edit2") {
		
		# 入力値補正
		if ($in{url} eq 'http://') { $in{url} = ''; }
		$in{sub} ||= '無題';
		
		# データオープン
		my @data;
		open(DAT,"+< $cf{logfile}") or cgi_err("open err: $cf{logfile}");
		eval "flock(DAT,2);";
		my $top = <DAT>;
		while (<DAT>) {
			my ($no,$reno,$date,$name,$eml,$sub,$com,$url,$host,$pw,$col,$ex,$w,$h,$chk) = split(/<>/);
			
			if ($no == $in{no}) {
				
				# 添付削除
				if ($in{imgdel}) {
					unlink("$cf{imgdir}/$in{no}$ex");
					unlink("$cf{imgdir}/$in{no}-s$ex") if (-f "$cf{imgdir}/$in{no}-s$ex");
					$ex = $w = $h = '';
				}
				$_ = "$no<>$reno<>$date<>$in{name}<>$in{email}<>$in{sub}<>$in{comment}<>$in{url}<>$host<>$pw<>$in{color}<>$ex<>$w<>$h<>$chk<>\n";
			}
			push(@data,$_);
		}
		
		# 更新
		unshift(@data,$top);
		seek(DAT,0,0);
		print DAT @data;
		truncate(DAT,tell(DAT));
		close(DAT);
	
	# 削除処理
	} elsif ($in{job} eq "dele" && $in{no}) {
		
		# 削除
		my @data;
		open(DAT,"+< $cf{logfile}") or cgi_err("open err: $cf{logfile}");
		eval "flock(DAT,2);";
		my $top = <DAT>;
		while (<DAT>) {
			my ($no,$reno,$date,$name,$eml,$sub,$com,$url,$host,$pw,$col,$ex,$w,$h,$chk) = split(/<>/);
			
			# 削除
			if ($in{no} == $no || $in{no} == $reno) {
				unlink("$cf{imgdir}/$no$ex") if ($ex);
				unlink("$cf{imgdir}/$no-s$ex") if (-f "$cf{imgdir}/$no-s$ex");
				next;
			}
			push(@data,$_);
		}
		
		# 更新
		unshift(@data,$top);
		seek(DAT,0,0);
		print DAT @data;
		truncate(DAT,tell(DAT));
		close(DAT);
	
	# 画像許可
	} elsif ($in{job} eq "perm" && $in{no}) {
		
		# 許可情報をマッチングし更新
		my @data;
		open(DAT,"+< $cf{logfile}") or cgi_err("open err: $cf{logfile}");
		eval "flock(DAT,2);";
		my $top = <DAT>;
		while (<DAT>) {
			my ($no,$reno,$date,$name,$eml,$sub,$com,$url,$host,$pw,$col,$ex,$w,$h,$chk) = split(/<>/);
			
			if ($no == $in{no}) {
				if ($chk == 1) { $chk = 0; } else { $chk = 1; }
				$_ = "$no<>$reno<>$date<>$name<>$eml<>$sub<>$com<>$url<>$host<>$pw<>$col<>$ex<>$w<>$h<>$chk<>\n";
			}
			push(@data,$_);
		}
		
		# 更新
		unshift(@data,$top);
		seek(DAT,0,0);
		print DAT @data;
		truncate(DAT,tell(DAT));
		close(DAT);
	}
	
	# 管理を表示
	header("管理画面");
	print <<EOM;
<div id="body">
<div class="ta-r">
<form action="$cf{bbs_cgi}">
<input type="submit" value="&lt; 掲示板">
</form>
</div>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<p>処理を選択して送信ボタンを押してください。</p>
処理：
<select name="job">
<option value="edit">編集
<option value="dele">削除
EOM

	if ($cf{img_check}) {
		print qq|<option value="perm">許可\n|;
	}

	print <<EOM;
</select>
<input type="submit" value="送信する">
EOM

	open(IN,"$cf{logfile}") or cgi_err("open err: $cf{logfile}");
	my $top = <IN>;
	while (<IN>) {
		my ($no,$reno,$date,$name,$eml,$sub,$com,$url,$host,$pw,$col,$ex,$w,$h,$chk) = split(/<>/);
		$name = qq|<a href="mailto:$eml">$name</a>| if ($eml);
		
		if (!$reno) {
			print qq|<div class="main">|;
		} else {
			print qq|<div class="sub">|;
		}
		
		print qq|<input type="radio" name="no" value="$no">[$no]\n|;
		print qq|<b class="sub">$sub</b> 名前：<b>$name</b> 日時：$date\n|;
		if ($ex) {
			print qq|[<a href="$cf{imgurl}/$no$ex" target="_blank">添付</a>]\n|;
			if ($cf{img_check}) {
				if ($chk == 1) {
					print qq|[<span class="grn">承認済</span>]\n|;
				} else {
					print qq|[<span class="red">未承認</span>]\n|;
				}
			}
		}
		print qq|[$host]\n|;
		print qq|<div class="com">| . strcutbytes_utf8($com,100) . qq|</div>\n|;
		print qq|</div>\n|;
	}
	close(IN);
	
	print <<EOM;
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  修正フォーム
#-----------------------------------------------------------
sub edit_form {
	my ($name,$eml,$sub,$com,$url,$col,$ext) = @_;
	$com =~ s|<br( /)?>|\n|g;
	$url ||= 'http://';
	
	my @col = split(/\s+/,$cf{colors});
	my $color;
	foreach (0 .. $#col) {
		if ($col == $_) {
			$color .= qq|<input type="radio" name="color" value="$_" checked>|;
		} else {
			$color .= qq|<input type="radio" name="color" value="$_">|;
		}
		$color .= qq|<span style="color:$col[$_]">■</span>\n|;
	}
	
	header("管理モード &gt; 修正フォーム");
	print <<EOM;
<div id="body">
<div class="ta-r">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="&lt; 戻る">
</form>
</div>
<div class="ttl">■ 編集フォーム</div>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="job" value="edit2">
<input type="hidden" name="no" value="$in{no}">
<table class="form-tbl">
<tr>
	<th>名前</th>
	<td><input type="text" name="name" value="$name" size="30"></td>
</tr><tr>
	<th>E-mail</th>
	<td><input type="text" name="email" value="$eml" size="30"></td>
</tr><tr>
	<th>件名</th>
	<td><input type="text" name="sub" value="$sub" size="40"></td>
</tr><tr>
	<th>コメント</th>
	<td><textarea name="comment" cols="50" rows="6">$com</textarea></td>
EOM

	if ($ext) {
		print qq|</tr><tr>\n|;
		print qq|<th>添付</th><td>\n|;
		print qq|[<a href="$cf{imgurl}/$in{no}$ext" target="_blank">添付</a>]&nbsp;\n|;
		print qq|<input type="checkbox" name="imgdel" value="1">削除</td>\n|;
	}
	
	print <<EOM;
</tr><tr>
	<th>URL</th>
	<td><input type="text" name="url" value="$url" size="50"></td>
</tr><tr>
	<th>文字色</th>
	<td>$color</td>
</tr>
</table>
<input type="submit" value="送信する">
</form>
</div>
</body>
</html>
EOM
	exit;
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
		cgi_err("認証できません");
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
#  HTMLヘッダー
#-----------------------------------------------------------
sub header {
	my $ttl = shift;
	
	print <<EOM;
Content-type: text/html; charset=utf-8

<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
body { font-size:90%; padding:0; margin:0; background:#FFF8C2; font-family:Verdana,"MS PGothic",Osaka,Arial,sans-serif; }
div.ttl { color:#2b0000; border-bottom:1px solid #2b0000; font-weight:bold; padding:4px; margin:1em 0; }
.red { color:red; }
.grn { color:green; }
.form-tbl { border-collapse:collapse; margin:1em 0; }
.form-tbl th, .form-tbl td { border:1px solid #666; padding:8px; }
.form-tbl th { background:#E7E8F2; }
.form-tbl td { background:#fff; }
.ta-r { text-align:right; }
b.sub { color:green; }
div.com { color:#804000; font-size:12px; margin-left:2em; }
div.main { border-top:1px dotted gray; padding:6px; margin-top:6px; }
div.sub { margin-left:3em; padding:6px; }
#login { width:400px; margin:3em auto; text-align:center; }
#login fieldset { padding:2em; }
#login input[type="password"] { width:190px; padding:3px; }
#login input[type="submit"] { width:50px; height:27px; }
#head { background:#A99770; color:#fff; padding:3px; font-weight:bold; }
#body { padding:6px; }
</style>
<title>$ttl</title>
</head>
<body>
<div id="head"> :: JoyfulNote 管理画面 :: </div>
EOM
}

#-----------------------------------------------------------
#  エラー画面
#-----------------------------------------------------------
sub cgi_err {
	my $err = shift;
	
	header("ERROR");
	print <<EOM;
<div align="center">
<hr width="350">
<h3>ERROR!</h3>
<p class="red">$err</p>
<hr width="350">
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  文字カット for UTF-8
#  [quote] http://linkage.white-void.net/development/server/perl-utf8-strcut.html
#-----------------------------------------------------------
sub strcutbytes_utf8 {
	my ($src,$maxlen) = @_;
	$src =~ s/[\t\n]//g;
	$src =~ s|<br( /)?>|\n|g;
	
	my $srclen = length($src);
	my $srcpos = 0;
	while($srcpos < $srclen) {
		my $character = substr($src, $srcpos, 1);
		my $value = ord($character);
		if($value < 0x80) { # ASCII characters
			$srcpos++;
			next;
		}
		my $width = 6;
		$width = 5 if ($value < 0xFC);
		$width = 4 if ($value < 0xF8);
		$width = 3 if ($value < 0xF0);
		$width = 2 if ($value < 0xE0);
		my $nextpos = $srcpos + $width;
		last if($nextpos > $maxlen);
		last if($nextpos > $srclen); # sequence is incomplete
		$srcpos = $nextpos;
	}
	return substr($src, 0, $srcpos);
}

