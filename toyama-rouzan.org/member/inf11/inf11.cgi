#!/usr/bin/perl

###############################################
#   inf11.cgi
#      V2.0 (2010.9.1)
#                     Copyright(C) CGI-design
###############################################

$script = 'inf11.cgi';
$base = './infdata';				#データ格納ディレクトリ
$inffile = "$base/inf.txt";			#記事
$nofile = "$base/no.txt";			#記事番号
$opfile = "$base/option.txt";

open (IN,"$opfile") || &error("OPEN ERROR");	$opdata = <IN>;		close IN;
if (!$opdata) {
	$pass = &crypt('cgi');
	chmod(0666,$opfile);	open (OUT,">$opfile") || &error("OPEN ERROR");
	print OUT "$pass<>#ffffff,#000000,#c00000";
	close OUT;
	chmod(0666,$inffile);	chmod(0666,$nofile);
}

### メイン処理 ###
if ($ENV{'REQUEST_METHOD'} eq "POST") {read(STDIN,$in,$ENV{'CONTENT_LENGTH'});} else {$in = $ENV{'QUERY_STRING'};}
%in = ();
foreach (split(/&/,$in)) {
	($n,$val) = split(/=/);
	$val =~ tr/+/ /;
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$val =~ s/&/&amp;/g;	$val =~ s/</&lt;/g;		$val =~ s/>/&gt;/g;		$val =~ s/"/&quot;/g;	$val =~ s/\r\n|\r|\n/<br>/g;
	if (defined($in{$n})) {$in{$n} .= "\0$val";} else {$in{$n} = $val;}
}
$mode = $in{'mode'};

open (IN,"$opfile") || &error("OPEN ERROR");	($pass,$colors) = split(/<>/,<IN>);		close IN;
($bg_color,$text_color,$line_color) = split(/,/,$colors);

if ($mode eq 'admin') {&admin;} else {&main;}

print "</body></html>\n";
exit;

###
sub header {
	print "Content-type: text/html\n\n";
	print "<html><head><META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=Shift_JIS\">\n";
	print "<title>Information</title><link rel=\"stylesheet\" type=\"text/css\" href=\"$base/style.css\"></head>\n";
	$head = 1;
}

###
sub main {
	&header;
	print "<body bgcolor=\"$bg_color\" text=\"$text_color\">\n";
	&dsp;
	#次の行は著作権表示ですので削除しないで下さい。#
	print "<center><a href=\"http://cgi-design.net\" target=\"_blank\">CGI-design</a></center>\n";
}

###
sub dsp {
	open (IN,"$inffile") || &error("OPEN ERROR");
	while (<IN>) {
		($no,$year,$mon,$day,$com,$url) = split(/<>/);
		$com =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href="$2" target="_blank">$2<\/a>/g;
		if ($url) {$com = "<a href=\"$url\" target=\"_parent\">$com</a>";}
		if ($mode eq 'admin') {print "<input type=submit name=$no value=\"修正\"> ";}
		print "<b>$year.$mon.$day</b><br>$com<hr size=1 color=\"$line_color\">\n";
	}
	close IN;
}

###
sub admin {
	&header;
	print "<body><center>\n";
	$inpass = $in{'pass'};
	if ($inpass eq '') {
		print "<br><br><br><br><h4>パスワードを入力して下さい</h4>\n";
		print "<form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=password size=10 maxlength=8 name=pass>\n";
		print "<input type=submit value=\" 認証 \"></form>\n";
		print "</center></body></html>\n";
		exit;
	}
	$mat = &decrypt($inpass,$pass);
	if (!$mat) {&error("パスワードが違います");}

	print "<table width=95% bgcolor=\"#8c4600\"><tr><td>　<a href=\"$script?mode=admin\"><font color=\"#ffffff\"><b>Return</b></font></a></td>\n";
	print "<form action=\"$script\" method=POST><td align=right>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=submit value=\"記事編集\">\n";
	print "<input type=submit name=set value=\"基本設定\"></td></form><td width=10></td></tr></table><br>\n";

	if ($in{'set'}) {&setup;} else {&edtin;}

	print "</center>\n";
}

###
sub edtin {
	if ($in{'newwrt'}) {&newwrt;}
	elsif ($in{'edtwrt'}) {&edtwrt;}
	elsif ($in{'delwrt'}) {&delwrt;}

	&in_form;
	print "<hr width=600>修正、削除する場合は「修正」をクリックして下さい。<br><br>\n";
	print "<form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=edt value=\"1\">\n";
	print "<table width=500 cellpadding=0><tr><td>\n";
	&dsp;
	print "</td></tr></table></form>\n";
}

###
sub in_form {
	($sec,$min,$hour,$nowday,$nowmon,$nowyear) = localtime;
	$nowyear += 1900;
	$nowmon++;

	print "<form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	if ($in{'edt'}) {
		open (IN,"$inffile") || &error("OPEN ERROR");
		while (<IN>) {
			($no,$year,$mon,$day,$com,$url) = split(/<>/);
			if ($in{$no}) {last;}
		}
		close IN;
		print "<input type=hidden name=no value=\"$no\">\n";
		$com =~ s/<br>/\r/g;
	} else {
		$year = $nowyear;
		$mon = $nowmon;
		$day = $nowday;
		$com = $url = '';
	}
	print "<table bgcolor=\"#e6e4ce\" cellspacing=8><tr><td><table cellspacing=1 cellpadding=0>\n";
	print "<tr><td>日付</td><td><select name=year>\n";
	for (2010 .. $nowyear+1) {
		if ($_ eq $year) {$sel = ' selected';} else {$sel = '';}
		print "<option value=\"$_\"$sel>$_</option>\n";
	}
	print "</select>年 <select name=mon>\n";
	for (1 .. 12) {
		if ($_ eq $mon) {$sel = ' selected';} else {$sel = '';}
		print "<option value=\"$_\"$sel>$_</option>\n";
	}
	print "</select>月 <select name=day>\n";
	for (1 .. 31) {
		if ($_ eq $day) {$sel = ' selected';} else {$sel = '';}
		print "<option value=\"$_\"$sel>$_</option>\n";
	}
	print "</select>日</td></tr>\n";
	print "<tr><td valign=top><br>内容</td><td><textarea cols=70 rows=6 name=com style=\"ime-mode:active;\">$com</textarea></td></tr>\n";
	print "<tr><td>リンク</td><td><input type=text size=70 name=url value=\"$url\" style=\"ime-mode:inactive;\"></td></tr>\n";
	print "<tr><td></td><td>";
	if ($in{'edt'}) {
		print "<table width=100%><tr><td><input type=submit name=edtwrt value=\"修正する\"></td>\n";
		print "<td width=40 bgcolor=red><input type=submit name=delwrt value=\"削除\"></td></tr></table>\n";
	} else {
		print "<input type=submit name=newwrt value=\"新規登録\">";
	}
	print "</td></tr></table></td></tr></table></form>\n";
}

###
sub newwrt {
	open (IN,"$nofile") || &error("OPEN ERROR"); 		$no = <IN>; 		close IN;
	$no++;
	open (OUT,">$nofile") || &error("OPEN ERROR");		print OUT $no;		close OUT;
	$in{'no'} = $no;
	&edtwrt;
}

###
sub edtwrt {
	$newdata = "$in{'no'}<>$in{'year'}<>$in{'mon'}<>$in{'day'}<>$in{'com'}<>$in{'url'}<>\n";
	$newdate = sprintf("$in{'year'}%02d%02d",$in{'mon'},$in{'day'});
	$flag = 0;
	@new = ();
	open (IN,"$inffile") || &error("OPEN ERROR");
	while (<IN>) {
		($no,$year,$mon,$day) = split(/<>/);
		if ($no eq $in{'no'}) {next;}
		if (!$flag) {
			$date = sprintf("$year%02d%02d",$mon,$day);
			if ($date <= $newdate) {push(@new,$newdata); $flag = 1;}
		}
		push(@new,$_);
	}
	close IN;
	if (!$flag) {push(@new,$newdata);}
	open (OUT,">$inffile") || &error("OPEN ERROR");		print OUT @new;		close OUT;
}

###
sub delwrt {
	@new = ();
	open (IN,"$inffile") || &error("OPEN ERROR");
	while (<IN>) {
		($no) = split(/<>/);
		if ($no ne $in{'no'}) {push(@new,$_);}
	}
	close IN;
	open (OUT,">$inffile") || &error("OPEN ERROR");		print OUT @new;		close OUT;
}

###
sub setup {
	if ($in{'wrt'}) {
		if ($in{'newpass'} ne '') {$pass = &crypt($in{'newpass'});}
		$colors = $in{'colors'};	$colors =~ s/\0/,/g;

		open (OUT,">$opfile") || &error("OPEN ERROR");		print OUT "$pass<>$colors";		close OUT;
	}
	print "下記に入力後、「設定する」を押して下さい。<br><br>\n";
	print "<form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=set value=\"1\">\n";
	print "<input type=submit name=wrt value=\"設定する\"><br><br>\n";

	print "<table bgcolor=\"#dddddd\" cellspacing=10><tr><td><table cellspacing=1 cellpadding=0>\n";
	print "<tr><td></td><td><a href=\"$base/color.htm\" target=\"_blank\">カラーコード</a></td></tr>\n";
	@name = ('基本背景色','基本文字色','区切り線');
	@colors = split(/,/,$colors);
	for (0 .. $#name) {
		print "<tr><td><b>$name[$_]</b></td><td><table cellspacing=0 cellpadding=0><tr>\n";
		print "<td><input type=text size=10 name=colors value=\"$colors[$_]\" style=\"ime-mode:inactive;\"></td>\n";
		print "<td width=5></td><td width=80 bgcolor=\"$colors[$_]\"></td></tr></table></td></tr>\n";
	}
	print "<tr><td><b>パスワード変更</b></td><td><input type=password size=10 maxlength=8 name=newpass> （英数8文字以内）</td></tr>\n";
	print "</table></td></tr></table></form>\n";
}

###
sub crypt {
	@salt = ('a' .. 'z','A' .. 'Z','0' .. '9');
	srand;
	$salt = "$salt[int(rand($#salt))]$salt[int(rand($#salt))]";
	return crypt($_[0],$salt);
}

###
sub decrypt {
	$salt = $_[1] =~ /^\$1\$(.*)\$/ && $1 || substr($_[1],0,2);
	if (crypt($_[0],$salt) eq $_[1] || crypt($_[0],'$1$' . $salt) eq $_[1]) {return 1;}
	return 0;
}

###
sub error {
	if (!$head) {&header; print "<body><center>\n";}
	print "<br><br><br><br><h3>ERROR !!</h3><font color=red><b>$_[0]</b></font>\n";
	print "</center></body></html>\n";
	exit;
}
