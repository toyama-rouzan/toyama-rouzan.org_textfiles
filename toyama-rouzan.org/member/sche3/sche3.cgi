#!/usr/bin/perl

###############################################
#   sche3.cgi
#      V3.0 (2010.8.26)
#                     Copyright(C) CGI-design
###############################################

require './cgi-lib.pl';

$script = 'sche3.cgi';
$base = './schedata';				#データ格納ディレクトリ
$nofile = "$base/no.txt";			#記事番号
$opfile = "$base/option.txt";
$cgi_lib'maxdata = 5120000;			#入力最大容量（byte）

@week = ('日','月','火','水','木','金','土');
@mdays = (31,28,31,30,31,30,31,31,30,31,30,31);

open (IN,"$opfile") || &error("OPEN ERROR");	$opdata = <IN>;		close IN;
if (!$opdata) {
	$pass = &crypt('cgi');
	chmod(0666,$opfile);	open (OUT,">$opfile") || &error("OPEN ERROR");
	print OUT "$pass<>Schedule<><><>$base<>$base<>#fafaf5,#000000,#c00000,#a8c7a8,#c9e0de,#ffffff,#ff0000,#0000ff,#ffffdd<>200";
	close OUT;
	chmod(0666,$nofile);
}

### メイン処理 ###
&ReadParse;
while (($n,$val) = each %in) {
	if ($n eq 'img') {next;}
	$val =~ s/&/&amp;/g;	$val =~ s/</&lt;/g;		$val =~ s/>/&gt;/g;		$val =~ s/"/&quot;/g;	$val =~ s/\r\n|\r|\n/<br>/g;
	$in{$n} = $val;
}
$mode = $in{'mode'};
$logyear = $in{'year'};
$logmon = $in{'mon'};
$logday = $in{'day'};

open (IN,"$opfile") || &error("OPEN ERROR");
($pass,$title,$home,$bg_img,$savedir,$loaddir,$colors,$max_wh) = split(/<>/,<IN>);
close IN;
($bg_color,$text_color,$title_color,$frame_color,$subbg_color,$combg_color,$hol_color,$sat_color,$today_color) = split(/,/,$colors);
@wcolor = ($hol_color,$text_color,$text_color,$text_color,$text_color,$text_color,$sat_color);

($sec,$min,$hour,$nowday,$nowmon,$nowyear) = localtime;
$nowyear += 1900;
$nowmon++;

if (!$logyear) {$logyear = $nowyear; $logmon = $nowmon; $logday = $nowday;}
$logfile = "$base/$logyear$logmon.txt";

if ($mode eq 'admin') {&admin;} else {&main;}

print "</center></body></html>\n";
exit;

###
sub header {
	print "Content-type: text/html\n\n";
	print "<html><head><META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=Shift_JIS\">\n";
	print "<title>$title</title><link rel=\"stylesheet\" type=\"text/css\" href=\"$loaddir/style.css\"></head>\n";
	$head = 1;
}

###
sub main {
	&header;
	print "<body background=\"$bg_img\" bgcolor=\"$bg_color\" text=\"$text_color\"><center>\n";
	print "<table width=98%><tr><td width=60 valign=top>";
	if ($home) {print "<a href=\"$home\">HOME</a>";}
	print "</td><td align=center><font color=\"$title_color\" size=\"+1\"><b>$title</b></font></td><td width=60 align=right><a href=\"$script?mode=admin\">[管理]</a></td></tr></table>\n";

	$mon = $logmon - 1;
	if ($mon < 1) {$mon = 12; $year = $logyear - 1;} else {$year = $logyear;}
	print "<table width=93%><tr><td width=60><b>$logyear年</b></td><td align=center><a href=\"$script?year=$year&mon=$mon\"><img src=\"$loaddir/back.gif\" border=0></a>　　　<font size=\"+2\"><b>$logmon月</b></font>　　　";
	$mon = $logmon + 1;
	if (12 < $mon) {$mon = 1; $year = $logyear + 1;} else {$year = $logyear;}
	print "<a href=\"$script?year=$year&mon=$mon\"><img src=\"$loaddir/next.gif\" border=0></a></td><td width=60></td></tr></table>\n";
	&cal;
	# 次の行は著作権表示ですので削除しないで下さい。#
	print "<a href=\"http://cgi-design.net\" target=\"_blank\">CGI-design</a>\n";
}

###
sub cal {
	@data = ();
	%data = ();
	if (-e $logfile) {
		open (IN,"$logfile") || &error("OPEN ERROR");
		while (<IN>) {
			($no,$day,$sub,$com,$imgt) = split(/<>/);
			if ($com || $imgt) {$sub = "<a href=\"#$no\">$sub</a>";}
			$data{$day} .= "<br>$sub";
			push (@data,$_);
		}
		close IN;
	}
	$mdays = $mdays[$logmon - 1];
	if ($logmon == 2 && $logyear % 4 == 0) {$mdays = 29;}

	print "<table width=95% bgcolor=\"$combg_color\" bordercolor=\"$frame_color\" border=1 cellspacing=0 cellpadding=4 style=\"border-collapse: collapse;\">\n";
	print "<tr bgcolor=\"$subbg_color\" align=center>\n";
	for (0 .. 6) {print "<td width=14%><font color=\"$wcolor[$_]\"><b>$week[$_]</b></font></td>\n";}
	print "</tr>\n";

	&set_holiday;
	&get_wday($logyear,$logmon,1);
	$w = $n = 0;
	$k = 1;
	for (0 .. 41) {
		if (!$w) {print "<tr valign=top>";}
		if ($wday <= $_ && $k <= $mdays) {
			$wcolor = $wcolor[$w];
			if (2007 <= $logyear) {
				if ($w == 1) {$n++;}
				&get_holiday;
				if ($holiday) {$wcolor = $wcolor[0];}
			}
			if ($logyear eq $nowyear && $logmon eq $nowmon && $k eq $nowday) {$bc = " bgcolor=\"$today_color\"";} else {$bc = '';}
			if ($k < 10) {$day = "&nbsp;$k";} else {$day = $k;}
			print "<td$bc height=90><font color=\"$wcolor\" size=\"+1\"><b>$day</b></font>$data{$k}</td>\n";
			$pro[$k] = "$w,$wcolor";
			$k++;
		} else {
			print "<td></td>";
		}
		$w++;
		if ($w == 7) {
			print "</tr>\n";
			if ($mdays < $k) {last;}
			$w = 0;
		}
	}
	print "</table><br><br>\n";

	foreach (@data) {
		($no,$day,$sub,$com,$imgt,$imgw,$imgh) = split(/<>/);
		if (!$mode && !$com && !$imgt) {next;}
		$com =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href="$2" target="_blank">$2<\/a>/g;
		($w,$wcolor) = split(/,/,$pro[$day]);

		print "<a name=\"$no\"></a><table width=700 bgcolor=\"$subbg_color\" cellspacing=2 cellpadding=0>\n";
		print "<tr><td height=20>　 $logyear年$logmon月$day日<font color=\"$wcolor\">($week[$w])</font>　　<b>$sub</b></td><td align=right>";
		if ($mode eq 'admin') {print "<input type=submit name=$no value=\"修正\">";}
		print "</td></tr>\n";
		print "<tr><td bgcolor=\"$combg_color\" colspan=2><table width=100% cellspacing=8><tr><td>\n";
		if ($imgt) {
			$imgfile = "$loaddir/$no.$imgt";
			print "<a href=\"$imgfile\" target=\"_blank\"><img src=\"$imgfile\" width=$imgw height=$imgh border=0 hspace=8 vspace=2 align=left></a>\n";
		}
		print "$com</td></tr></table></td></tr></table>\n";
		print "<table width=700 cellpadding=0><tr><td align=right><a href=\"#\">▲top</a></td></tr></table>\n";
	}
}

###
sub set_holiday {
	$def = 0.242194*($logyear-1980)-int(($logyear-1980)/4);
	$spr = int(20.8431+$def);
	$aut = int(23.2488+$def);
	%hod = ('0101','元日','0211','建国記念の日',"03$spr",'春分の日','0429','昭和の日','0503','憲法記念日','0504','みどりの日','0505','こどもの日',"09$aut",'秋分の日','1103','文化の日','1123','勤労感謝の日','1223','天皇誕生日');
	%how = ('12','成人の日','73','海の日','93','敬老の日','102','体育の日');
}

###
sub get_holiday {
	$sm = sprintf("%02d%02d",$logmon,$k);
	$holiday = $hod{$sm};
	if ($holiday && !$w) {$hflag = 1;}
	if (!$holiday && $w == 1) {$holiday = $how{"$logmon$n"};}
	if (!$holiday && $hflag) {$holiday = '振替休日'; $hflag = 0;}
	if (($logyear eq '2009' || $logyear eq '2015') && $sm eq '0922') {$holiday = '国民の休日';}
}

###
sub get_wday {
	($y,$m,$d) = @_;
	if ($m < 3) {$y--; $m+=12;}
	$wday = ($y+int($y/4)-int($y/100)+int($y/400)+int((13*$m+8)/5)+$d)%7;
}

###
sub admin {
	&header;
	print "<body><center>\n";
	$inpass = $in{'pass'};
	if ($inpass eq '') {
		print "<table width=97%><tr><td><a href=\"$script\">Return</a></td></tr></table>\n";
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

	print "<table width=95% bgcolor=\"#8c4600\"><tr><td>　<a href=\"$script\"><font color=\"#ffffff\"><b>Return</b></font></a></td>\n";
	print "<form action=\"$script\" method=POST><td align=right>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=submit value=\"記事編集\">\n";
	print "<input type=submit name=set value=\"基本設定\"></td></form><td width=10></td></tr></table><br>\n";

	if ($in{'set'}) {&setup;} else {&edtin;}
}

###
sub edtin {
	if ($in{'newwrt'}) {&newwrt;}
	elsif ($in{'edtwrt'}) {&edtwrt;}
	elsif ($in{'delwrt'}) {&delwrt;}

	&in_form;
	print "<hr width=700>記事を修正、削除する場合は「修正」をクリックして下さい。<br><br>\n";
	print "<table width=93%><tr><td width=60><b>$logyear年</b></td>\n";
	$mon = $logmon - 1;
	if ($mon < 1) {$mon = 12; $year = $logyear - 1;} else {$year = $logyear;}
	print "<form action=\"$script\" method=POST><td align=right>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=year value=\"$year\">\n";
	print "<input type=hidden name=mon value=\"$mon\">\n";
	print "<input type=image src=\"$loaddir/back.gif\"></td></form>\n";
	print "<td width=100 align=center><font size=\"+2\"><b>$logmon月</b></font></td>\n";
	$mon = $logmon + 1;
	if (12 < $mon) {$mon = 1; $year = $logyear + 1;} else {$year = $logyear;}
	print "<form action=\"$script\" method=POST><td>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=year value=\"$year\">\n";
	print "<input type=hidden name=mon value=\"$mon\">\n";
	print "<input type=image src=\"$loaddir/next.gif\"></td></form><td width=60></td></tr></table>\n";

	print "<table cellspacing=0 cellpadding=0><tr><form action=\"$script\" method=POST><td>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=year value=\"$logyear\">\n";
	print "<input type=hidden name=mon value=\"$logmon\">\n";
	print "<input type=hidden name=edt value=\"1\"></td></tr></table>\n";
	&cal;
	print "</form>\n";
}

###
sub in_form {
	print "<form action=\"$script\" method=POST enctype=\"multipart/form-data\">\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";

	print "<table bgcolor=\"#e6e4ce\" cellspacing=8><tr><td><table cellspacing=1 cellpadding=0>\n";
	print "<tr><td>日付&nbsp;</td><td>";
	if ($in{'edt'}) {
		open (IN,"$logfile") || &error("OPEN ERROR");
		while (<IN>) {
			($no,$day,$sub,$com) = split(/<>/);
			if ($in{$no}) {last;}
		}
		close IN;
		print "<input type=hidden name=no value=\"$no\">\n";
		print "<input type=hidden name=year value=\"$logyear\">\n";
		print "<input type=hidden name=mon value=\"$logmon\">\n";
		$com =~ s/<br>/\r/g;
		print "&nbsp;<b>$logyear年$logmon月$day日</b>";
	} else {
		print "<select name=year>\n";
		for (2010 .. $nowyear+1) {
			if ($_ eq $logyear) {$sel = ' selected';} else {$sel = '';}
			print "<option value=\"$_\"$sel>$_</option>\n";
		}
		print "</select>年 <select name=mon>\n";
		for (1 .. 12) {
			if ($_ eq $logmon) {$sel = ' selected';} else {$sel = '';}
			print "<option value=\"$_\"$sel>$_</option>\n";
		}
		print "</select>月 <select name=day>\n";
		for (1 .. 31) {
			if ($_ eq $logday) {$sel = ' selected';} else {$sel = '';}
			print "<option value=\"$_\"$sel>$_</option>\n";
		}
		print "</select>日";
		$sub = $com = '';
	}
	print "</td></tr>\n";
	print "<tr><td>題名</td><td><input type=text size=60 name=sub value=\"$sub\" style=\"ime-mode:active;\"></td></tr>\n";
	print "<tr><td valign=top><br>内容</td><td><textarea cols=80 rows=20 name=com style=\"ime-mode:active;\">$com</textarea></td></tr>\n";
	print "<tr><td>画像</td><td><input type=file size=60 name=img></td></tr>\n";
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
	&img("$savedir/$no",'img');
	$newdata = "$no<>$logday<>$in{'sub'}<>$in{'com'}<>$type<>$width<>$height<>\n";

	if (-e $logfile) {
		@new = ();
		$flag = 0;
		open (IN,"$logfile") || &error("OPEN ERROR");
		while (<IN>) {
			($no,$day) = split(/<>/);
			if (!$flag && $logday < $day) {push(@new,$newdata); $flag = 1;}
			push(@new,$_);
		}
		close IN;
		if (!$flag) {push(@new,$newdata);}
		open (OUT,">$logfile") || &error("OPEN ERROR");		print OUT @new;			close OUT;
	} else {
		open (OUT,">$logfile") || &error("OPEN ERROR");		print OUT $newdata;		close OUT;		chmod(0666,$logfile);
	}
}

###
sub edtwrt {
	&img("$savedir/$in{'no'}",'img');
	@new = ();
	open (IN,"$logfile") || &error("OPEN ERROR");
	while (<IN>) {
		($no,$day,$sub,$com,$imgt,$imgw,$imgh) = split(/<>/);
		if ($no eq $in{'no'}) {
			if ($type) {$imgt = $type; $imgw = $width; $imgh = $height;}
			push(@new,"$no<>$day<>$in{'sub'}<>$in{'com'}<>$imgt<>$imgw<>$imgh<>\n");
		} else {push(@new,$_);}
	}
	close IN;
	open (OUT,">$logfile") || &error("OPEN ERROR");		print OUT @new;		close OUT;
}

###
sub delwrt {
	@new = ();
	open (IN,"$logfile") || &error("OPEN ERROR");
	while (<IN>) {
		($no,$day,$sub,$com,$imgt) = split(/<>/);
		if ($no eq $in{'no'}) {if ($imgt) {unlink "$savedir/$no.$imgt";}} else {push(@new,$_);}
	}
	close IN;
	open (OUT,">$logfile") || &error("OPEN ERROR");		print OUT @new;		close OUT;
}

###
sub setup {
	if ($in{'wrt'}) {
		if ($in{'newpass'} ne '') {$pass = &crypt($in{'newpass'});}
		$title = $in{'title'};
		$home = $in{'home'};		$bg_img = $in{'bg_img'};
		$savedir = $in{'savedir'};	$loaddir = $in{'loaddir'};
		$colors = $in{'colors'};	$colors =~ s/\0/,/g;
		$max_wh = $in{'max_wh'};

		open (OUT,">$opfile") || &error("OPEN ERROR");
		print OUT "$pass<>$title<>$home<>$bg_img<>$savedir<>$loaddir<>$colors<>$max_wh";
		close OUT;
	}
	print "下記に入力後、「設定する」を押して下さい。<br><br>\n";
	print "<form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=set value=\"1\">\n";
	print "<input type=submit name=wrt value=\"設定する\"><br><br>\n";

	print "<table bgcolor=\"#dddddd\" cellspacing=10><tr><td><table cellspacing=1 cellpadding=0>\n";
	print "<tr><td><b>タイトル</b></td><td><input type=text size=60 name=title value=\"$title\"></td></tr>\n";
	print "<tr><td><b>ホームURL</b></td><td><input type=text size=60 name=home value=\"$home\"></td></tr>\n";
	print "<tr><td><b>壁紙</b></td><td><input type=text size=60 name=bg_img value=\"$bg_img\"></td></tr>\n";
	print "<tr><td><b>画像格納ディレクトリ</b></td><td><input type=text size=60 name=savedir value=\"$savedir\"></td></tr>\n";
	print "<tr><td><b>画像読出ディレクトリ</b></td><td><input type=text size=60 name=loaddir value=\"$loaddir\"></td></tr>\n";

	print "<tr><td></td><td><a href=\"$loaddir/color.htm\" target=\"_blank\">カラーコード</a></td></tr>\n";
	@name = ('基本背景色','基本文字色','タイトル','枠色','見出し背景色','記事背景色','休日','土曜日','本日背景色');
	@colors = split(/,/,$colors);
	for (0 .. $#name) {
		print "<tr><td><b>$name[$_]</b></td><td><table cellspacing=0 cellpadding=0><tr>\n";
		print "<td><input type=text size=10 name=colors value=\"$colors[$_]\" style=\"ime-mode:inactive;\"></td>\n";
		print "<td width=5></td><td width=80 bgcolor=\"$colors[$_]\"></td></tr></table></td></tr>\n";
	}
	print "<tr><td><b>画像表\示</b></td><td><input type=text size=4 name=max_wh value=\"$max_wh\" style=\"text-align:right; ime-mode:disabled;\">px</td></tr>\n";
	print "<tr><td><b>パスワード変更</b></td><td><input type=password size=10 maxlength=8 name=newpass> （英数8文字以内）</td></tr>\n";
	print "</table></td></tr></table></form>\n";
}

###
sub img {
	$type=$width=$height=$big=$mac='';
	$imgdata = $in{"$_[1]"};
	if (!$imgdata) {return;}

	foreach (@in) {
		if (/$_[1]/ and /Content-Type:(.+)/i) {
			if ($1 =~ /image\/.*jpeg/i) {$type = 'jpg';}
			elsif ($1 =~ /image\/gif/i) {$type = 'gif';}
			elsif ($1 =~ /image\/.*png/i) {$type = 'png';}
		}
		if (/application\/x-macbinary/i) {$mac = 1;}
	}
	if (!$type) {&error("このファイルはアップロードできません");}

	if ($mac) {
		$leng = substr($imgdata,83,4);
		$leng = unpack("%N",$leng);
		$imgdata = substr($imgdata,128,$leng);
	}
	$img_file = "$_[0].$type";
	open (IMG,">$img_file") || &error("$img_fileファイルを作成できません");
	binmode IMG;
	print IMG $imgdata;
	close IMG;
	chmod (0666,$img_file);

	($t,$width,$height) = &getImageSize("$img_file");
	if (!$width || !$height) {&error("ファイルを認識できません");}

	if ($max_wh && ($max_wh < $width || $max_wh < $height)) {
		if ($height < $width) {$height = int($height * $max_wh / $width); $width = $max_wh;}
		else {$width = int($width * $max_wh / $height); $height = $max_wh;}
		$big = 1;
	}
}

#=========================================
# Get Image Pixel Size.（出典：stdio-902）
#=========================================
sub getImageSize {
	local($file_name) = @_;
	local($head);

	return if (!open IMG, $file_name);
	binmode IMG;
	read IMG, $head, 8;
	if ($head eq "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a") {
		local($width, $height);
		if (read(IMG, $head, 4) != 4 || read(IMG, $head, 4) != 4 || $head ne 'IHDR') {
			close IMG;
			return "PNG", 0;
		}
		read IMG, $head, 8;
		close IMG;
		$width = unpack "N", substr($head, 0, 4);
		$height = unpack "N", substr($head, 4, 4);
		return "PNG", $width, $height;
	}
	$head = substr $head, 0, 3;
	if ($head eq "\x47\x49\x46") {
		local($head, $width, $height);
		seek IMG, 6, 0;
		read IMG, $head, 4;
		close IMG;
		($width, $height) = unpack "vv", $head;
		return "GIF", $width, $height;
	}
	$head = substr $head, 0, 2;
	if ($head eq "\xff\xd8") {
		local($head, $width, $height, $w1, $w2, $h1, $h2, $l1, $l2, $length);
		seek IMG, 2, 0;
		while (read IMG, $head, 1) {
			last if ($head eq "");
			if ($head eq "\xff") {
				$head = getc IMG;
				if ($head =~ /^[\xc0-\xc3\xc5-\xcf]$/) {
					seek IMG, 3, 1;
					last if (read(IMG, $head, 4) != 4);
					close IMG;
					($h1, $h2, $w1, $w2) = unpack "C4", $head;
					$height = $h1 * 256 + $h2;
					$width  = $w1 * 256 + $w2;
					return "JPG", $width, $height;
				} elsif ($head eq "\xd9" || $head eq "\xda") {
					last;
				} else {
					last if (read(IMG, $head, 2) != 2);
					($l1, $l2) = unpack "CC", $head;
					$length = $l1 * 256 + $l2;
					seek IMG, $length - 2, 1;
				}
			}
		}
		close IMG;
		return "JPG", 0;
	}
	return 0;
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
