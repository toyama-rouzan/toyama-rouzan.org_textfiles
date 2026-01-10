#!/usr/bin/perl

###############################################
#   view6.cgi
#      V3.1 (2010.8.25)
#                     Copyright(C) CGI-design
###############################################

require './cgi-lib.pl';

$script = 'view6.cgi';
$base = './viewdata';				#データ格納ディレクトリ
$viewfile = "$base/view.txt";		#記事
$opfile = "$base/option.txt";
$cgi_lib'maxdata = 10240000;			#入力最大容量（byte）

open (IN,"$opfile") || &error("OPEN ERROR");	$opdata = <IN>;		close IN;
if (!$opdata) {
	$pass = &crypt('cgi');
	chmod(0666,$opfile);	open (OUT,">$opfile") || &error("OPEN ERROR");
	print OUT "$pass<>PHOTO<><><>$base<>$base<>#869D7D,#000000,#ffffff,#D4D4A6<>160<>5";
	close OUT;
	chmod(0666,$viewfile);
}

###　メイン処理　###
&ReadParse;
while (($n,$val) = each %in) {
	if ($n eq 'img') {next;}
	$val =~ s/&/&amp;/g;	$val =~ s/</&lt;/g;		$val =~ s/>/&gt;/g;		$val =~ s/"/&quot;/g;	$val =~ s/\r\n|\r|\n/<br>/g;
	$in{$n} = $val;
}
$mode = $in{'mode'};

open (IN,"$opfile") || &error("OPEN ERROR");
($pass,$title,$home,$bg_img,$savedir,$loaddir,$colors,$max_wh,$imgcols) = split(/<>/,<IN>);
close IN;
($bg_color,$text_color,$title_color,$com_color) = split(/,/,$colors);
if ($imgcols == 0) {$imgcols = 5;}

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
	print "</td><td align=center><font color=\"$title_color\" size=\"+1\"><b>$title</b></font></td><td width=60></td></tr></table>\n";
	&dsp;
	print "<div align=right><a href=\"$script?mode=admin\">[管理]</a></div>\n";
	# 次の行は著作権表示ですので削除しないで下さい。#
	print "<a href=\"http://cgi-design.net\" target=\"_blank\">CGI-design</a>\n";
}

###
sub dsp {
	$perw = int(100 / $imgcols);
	$k = 0;
	print "<table cellspacing=8 cellpadding=4>\n";
	open (IN,"$viewfile") || &error("OPEN ERROR");
	while (<IN>) {
		($no,$imgt,$imgw,$imgh,$imgb,$sub) = split(/<>/);
		if (!$k) {print "<tr align=center valign=bottom>";}
		if ($mode eq 'admin') {$bc = ' bgcolor="#e2defe"';} else {$bc = '';}
		print "<td width=$perw%$bc>";
		$imgfile = "$loaddir/$no.$imgt";
		$imgsrc = "<img src=\"$imgfile\" width=$imgw height=$imgh border=0 vspace=2>";
		if ($imgb) {print "<a href=\"$imgfile\" target=\"_blank\">$imgsrc</a>";} else {print $imgsrc;}
		print "<br>\n";
		if ($mode eq 'admin') {print "<input type=text size=20 name=sub$no value=\"$sub\"><br><input type=checkbox name=del$no value=\"1\">削除";}
		else {print "<font color=\"$com_color\">$sub</font><br>";}
		print "</td>\n";
		$k++;
		if ($k == $imgcols) {print "</tr>\n"; $k = 0;}
	}
	close IN;
	if ($k) {
		for ($k+1 .. $imgcols) {print "<td width=$perw%></td>";}
		print "</tr>";
	}
	print "</table>\n";
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
	if ($in{'wrt'}) {
		@new = ();
		open (IN,"$viewfile") || &error("OPEN ERROR");
		while (<IN>) {
			($no,$imgt,$imgw,$imgh,$imgb) = split(/<>/);
			if ($in{"del$no"}) {unlink "$savedir/$no.$imgt";}
			else {push(@new,"$no<>$imgt<>$imgw<>$imgh<>$imgb<>$in{\"sub$no\"}<>\n");}
		}
		close IN;

		if ($in{'img'}) {
			($no) = split(/<>/,$new[0]);
			$no++;
			&img("$savedir/$no",'img');
			unshift(@new,"$no<>$type<>$width<>$height<>$big<><>\n");
		}
		open (OUT,">$viewfile") || &error("OPEN ERROR");	print OUT @new;		close OUT;
	}
	print "下記に入力後、「設定する」を押して下さい。<br><br>\n";
	print "<form action=\"$script\" method=POST enctype=\"multipart/form-data\">\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=submit name=wrt value=\"設定する\"><br><br>\n";
	print "<table bgcolor=\"#e6e4ce\" cellspacing=10><tr><td>画像 <input type=file size=60 name=img></td></tr></table><br>\n";
	&dsp;
	print "</form>\n";
}

###
sub setup {
	if ($in{'wrt'}) {
		if ($in{'newpass'} ne '') {$pass = &crypt($in{'newpass'});}
		$title = $in{'title'};
		$home = $in{'home'};		$bg_img = $in{'bg_img'};
		$savedir = $in{'savedir'};	$loaddir = $in{'loaddir'};
		$colors = $in{'colors'};	$colors =~ s/\0/,/g;
		$max_wh = $in{'max_wh'};	$imgcols = $in{'imgcols'};

		open (OUT,">$opfile") || &error("OPEN ERROR");
		print OUT "$pass<>$title<>$home<>$bg_img<>$savedir<>$loaddir<>$colors<>$max_wh<>$imgcols";
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
	@name = ('基本背景色','基本文字色','タイトル','コメント');
	@colors = split(/,/,$colors);
	for (0 .. $#name) {
		print "<tr><td><b>$name[$_]</b></td><td><table cellspacing=0 cellpadding=0><tr>\n";
		print "<td><input type=text size=10 name=colors value=\"$colors[$_]\" style=\"ime-mode:inactive;\"></td>\n";
		print "<td width=5></td><td width=80 bgcolor=\"$colors[$_]\"></td></tr></table></td></tr>\n";
	}
	print "<tr><td><b>画像表\示</b></td><td><input type=text size=4 name=max_wh value=\"$max_wh\" style=\"text-align:right; ime-mode:disabled;\">px　　<input type=text size=3 name=imgcols value=\"$imgcols\" style=\"text-align:right; ime-mode:disabled;\">列</td></tr>\n";
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
