#########################################################################
#
# 画像のアップロードなど、滅多に使われないサブルーチン入れ。
# 画像アップロードについては、KENTさんのCGIを参考にしまくってます。
# もちろん、自分でも努力したのですが・・・。連絡してないので心が痛いです。
#
##########################################################################

# ---------- #
# 検索ページ #
# ---------- #
sub find{
&head; $head_flag = 1;
if($makeindex){print "□ <a href=\"index.html\">BACK</a>\n";}
else{print "□ <a href=\"$cgipath\">BACK</a>\n";}

print "<CENTER>\n";
print <<EOM;
<table width="100%" border="0"><tr><td class="midashi">検索</td></tr></table>
<form action="$cgipath" method="$method">
<input type=hidden name=mode value="find">
<input type=hidden name=sflag value="1">
<table><tr><td align=right>キーワード：</td><td><input type=text name=word size=35 value="$in{'word'}"></td></tr>
EOM

# プルダウン検索
if($psearch){
	for($x=1; $x<=$#koumoku; $x++){
		if($x == $select[$y]){
			print"<TR><TD ALIGN=\"RIGHT\">$koumoku[$x]：</TD><TD><select name=\"item$x\">";
			if($empty){print "<option value=\"\">"}
			foreach $str(@{$sel[$x]}){
				if($str eq $in{"item$x"}){ print"<option value=\"$str\" selected>$str"; }
				else{ print"<option value=\"$str\">$str"; }
			}
		$y++;
		print"</select>\n"
		}
	}
}

print "<tr><td align=right>検索条件</td><td>";
if($in{'cond'} ne 'or'){
print "<input type=radio name=cond value=\"and\" checked>AND \n";
print "<input type=radio name=cond value=\"or\">OR</td></tr>\n";
}
else{
print "<input type=radio name=cond value=\"and\">AND \n";
print "<input type=radio name=cond value=\"or\" checked>OR</td></tr>\n";
}
print<<EOM;
<tr><th colspan=2><input type=submit value="検索">
<input type=reset value="リセット"></th></tr>
</table>
</form>
EOM

# ワード検索の実行と結果表示
if ($in{'sflag'}){

$cond = $in{'cond'};
$word = $in{'word'};
$word =~ s/　/ /g;
$word =~ s/\t/ /g;
@pairs = split(/ /,$word);

# ファイルを読み込み
open(DB,"$datapath") || &error('open');
while(<DB>) 
{
	$flag = 0;
	# プルダウン項目を比較
	for($x=0; $x<=$y; $x++){
		if($in{"item$select[$x]"}){
			$pulldata = (split(/\,/))[$select[$x]+18];
			if($in{"item$select[$x]"} eq $pulldata){
				if ($cond eq 'or') { $flag = 2; last; }
				$flag= 1;
			}
			else {
			if ($cond eq 'and'){ $flag = 3; last; }
			}
		}
	}

	# ワード部分を比較
	if(!$flag || $flag==1){
		foreach $pair (@pairs){
			if (index($_,$pair) >= 0){
				$flag = 1;
				if ($cond eq 'or') { last; }
			}
			else {
				if ($cond eq 'and'){ $flag = 3; last; }
			}
		}
	}
	if ($flag == 1 || $flag == 2) { push(@LINES,$_); }
}
close(DB);

$count = @LINES;
print "<hr width=90\%><b>検索結果：$count件</b>\n";
# 名簿の表示
&list;
}

print <<EOM;
<br></center>
EOM
&foot;
exit;
}


# ------------------------ #
# 名前の追加・修正フォーム #
# ------------------------ #
sub form{
if($in{'mpass'}){if($in{'mpass'} ne $m_pass){ &error('badpass');}}
# 管理人が禁止してるのに、名前を追加しようとする奴は…
if($mode eq "addform" && !$addname && $in{"mpass"} ne $m_pass){ &error('不正なアクセスです'); }

&head; $head_flag = 1;
if($makeindex){print "□ <a href=\"index.html\">BACK</a>\n";}
else{print "□ <a href=\"$cgipath\">BACK</a>\n";}

# 入力必須項目のボタン作成
$che = "<span class=check>*</span>";

if($mode eq "editform"){
	$bname = "保存して終了";
	open (IN,"$datapath") || &error('open');
	$flag = 0;
	while(<IN>){
		if($usetag){$_ =~ s/\"/&quot;/g;}
		if($in{'id'} eq (split(/,/))[0]){
			$flag = 1;
			$lastdata = $_;
			if($in{'mpass'}){	# 管理ページからの編集
				if($in{'mpass'} ne $m_pass){ close (IN); &error('badpass'); }
			}
			else{
				$pw = $in{'pass'};	# 入力された生パスは$pwへ
				$u_pass = (split(/,/,$lastdata))[2];
				# 暗号化をしている場合
				if($encode){$in{'pass'} = crypt($in{'pass'},$in{'pass'});}
				if($in{'pass'} ne "$u_pass" && $pw ne "$m_pass"){ close (IN); &error('badpass'); }
			}
			last;
		}
	}
	close (IN);
	if(!$flag){ &error("notfound");}
	($num,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail,$imgw,$imgh,$imgflag,$comment,undef,undef,undef,@item) = split(/,/,$lastdata);
	$comment =~ s/<br>/\n/g;
	if($autolink){ $comment =~ s/(.*)((<a href[\s\w\=\#\"\'\:\/\-\~\.\>\+\?\&\=\@\%\;\#]+)>(.*)(<\/a>))/$1$4/ig;}
print <<EOM;
<TABLE align=center WIDTH="90%"><TR><TD class="name">$name</TD></TR></TABLE>
<BR><BR>
<table width=580 align=center>
<tr><td><span class="bold">▼入力項目の編集</span></td></tr>
EOM
}

else{
$bname = "$namaeの追加";
if($in{'mpass'} eq $m_pass){ $passdata = "<input type=hidden name=mpass value=\"$m_pass\">"; }
print <<EOM;
<TABLE WIDTH="100%" BORDER="0"><TR><TD class="midashi">新規登録</TD></TR></TABLE>
<BR>
<table align=center width=580>
<tr><td><span class="bold">▼$namaeの追加</span></td></tr>
<tr><td>$com2</td></tr>
<tr><td align=center><FORM action="$cgipath" method="$method" enctype=\"multipart/form-data\"><INPUT type="hidden" name="mode" value="add">$passdata
$che$namae：<INPUT name="name" size="15"> &nbsp;$che初期パスワード：<input type=password name="pass" size=8 maxlength=8>&nbsp;
EOM

# 番号選択
if($free_add || $in{'mpass'}){
	open(IN,"$datapath") || &error("open");
	@LINES = <IN>;
	close(IN);
	$x = 0;
	foreach(@LINES){
		$tempno = (split(/,/))[0];
		if($x < $tempno){ $x = $tempno; }
	}
	$x++;
	print "No.<select name=\"add_no\">\n";
	for ($i=1; $i<=$x; $i++){
		if($x == $i){print "<option value=\"$i\" selected>$i\n";}
		else{print "<option value=\"$i\">$i\n";}
	}
	print "</select> &nbsp;";
}
print <<EOM;
</td></tr>
</TABLE>
<hr width=580>
<table width=580 align=center>
EOM
}

# 以下は共通部分
if($usetag == 2){print "<tr><td>※「$che」マークがついている項目は入力必須です。タグは全ての項目に使用できます。</td></tr>\n";}
elsif($usetag == 1){print "<tr><td>※「$che」マークがついている項目は入力必須です。タグはコメント欄にのみ使用できます。</td></tr>\n";}
else{print "<tr><td>※「$che」マークがついている項目は入力必須です。タグは使用できません。</td></tr>\n";}
if($mail_name && $formmail){print "<tr><td>※メールアドレスを非公開にしても、フォームメールからメールを受け取ることができます。</td></tr>\n";}
# 文字数制限処理
if($#lim){
	print "<tr><td>※文字数制限は、すべて全角文字で換算されます。</td></tr>\n";
	for($x=1; $x<=$#koumoku; $x++){
	if($lim[$x]){$limit[$x]="<SMALL>（$lim[$x]字以内）</SMALL>";}
	}
}
print "</table>\n";

if($mode eq "editform"){
if($in{'mpass'}){ $passdata = "<input type=hidden name=mpass value=\"$m_pass\">"; }
else{ $passdata = "<input type=hidden name=pass value=\"$pw\">"; }
print <<EOM;
<form action="$cgipath" method="$method">
<input type=hidden name=mode value="edit">
<input type=hidden name=id value="$num">
$passdata
EOM
}

$y = 0; $z = 0;
print "<TABLE BORDER=\"0\" CELLPADDING=\"3\" align=center>\n";
if($mode eq "editform"){print"<TR><TD ALIGN=\"RIGHT\">$che$namae：</TD><TD><INPUT name=\"name\" size=$item_wid value=\"$name\"></TD></TR>\n";}

if($mail_name){
	if($checkmail){$che = "<span class=check>*</span>";}
	else{ $che = ""; }
	print"<TR><TD ALIGN=\"RIGHT\">$che$mail_name：</TD><TD><INPUT name=\"mail\" size=$item_wid value=\"$mail\">";
	if($formmail && !$mailflag){ print "&nbsp;<input type=checkbox name=\"mailflag\" value=1>非公開</TD></TR>\n"}
	elsif($formmail && $mailflag){ print "&nbsp;<input type=checkbox name=\"mailflag\" value=1 checked>非公開</TD></TR>\n"}
	else{ print "</TD></TR>\n" }
}
if($url_name){print"<TR><TD ALIGN=\"RIGHT\">$url_name：</TD><TD><INPUT name=\"url\" size=$item_wid value=\"http://$url\"></TD></TR>\n";}
for($x=1; $x<=$#koumoku; $x++){
	if($x == $check[$z]){ $che = "<span class=check>*</span>"; $z++; }
	else{ $che = ""; }
	if($x == $select[$y]){
		print"<TR><TD ALIGN=\"RIGHT\">$che$koumoku[$x]$limit[$x]：</TD><TD><select name=\"item$x\">";
		foreach $str(@{$sel[$x]}){
			if($str eq $item[$x-1]){ print"<option value=\"$str\" selected>$str"; }
			else{ print"<option value=\"$str\">$str"; }
		}
		$y++;
		print"</select>\n"
	}
	elsif($koumoku[$x]){
		print"<TR><TD ALIGN=\"RIGHT\">$che$koumoku[$x]$limit[$x]：</TD><TD><INPUT name=\"item$x\" size=$item_wid value=\"$item[$x-1]\"></TD></TR>\n";
	}
}

if($gazou && !$uptype){
	print"<TR><TD ALIGN=\"RIGHT\">画像URL(http://～)：</TD><TD><input name=imgurl size=$item_wid value=$imgurl ></TD></TR>\n";
}
if($mode eq "addform" && $gazou && $uptype){
	print"<TR><TD ALIGN=\"RIGHT\">アップロード画像：</TD><TD><input type=file name=upfile size=$item_wid></TD></TR>\n";
}
print "</TABLE><br><div align=center>\n";

if($checkcom){ $che = "<span class=check>*</span>"; }
else{ $che = ""; }
print"$che コメントがあれば書き込んでください \n";
if($usetag){print "<input type=checkbox name=kill_tag value=\"1\">：タグ無効\n";}

print <<EOM;
<BR>
<textarea cols=$com_wid rows=10 name=comment>$comment</textarea><BR><BR>
<input type=submit value="$bname">　<input type=reset value="リセット">
</FORM>
</div>
EOM

if($mode eq "editform"){
# アップロードするファイルの変更・削除フォーム
if($gazou && $uptype){
print<<EOM;
<br><CENTER><HR WIDTH="580">
<FORM action="$cgipath" method="$method" enctype=\"multipart/form-data\">
<table width=580 align="center">
<tr><td><span class=bold>▼アップロードするファイルの変更・削除</span></td></tr>
EOM
if($tail){
	print "<tr><td>※現在、<b>すでにファイルがアップロードされています</b>。</td></tr>\n";
	print "<tr><td>※新しくファイルをアップロードすると、<b>前のファイルに上書き保存</b>されます。</td></tr>\n"; 
	print "<tr><td>※ファイルの削除のみ行う時は、空のまま送信ボタンを押してください。</td></tr>\n";
	}
else{
	print "<tr><td>※現在ファイルはアップロードされていません。</td></tr>\n";
	print "<tr><td>※アップロードを行う時は、ファイルを指定して送信ボタンを押してください。</td></tr>\n"; 

}

print<<EOM;
</table>
<input type=hidden name=mode value="c_img">
<input type=hidden name=id value="$num">
$passdata
<input type=file name=upfile size=35> &nbsp;
<INPUT type="submit" value="送信">
</FORM></CENTER>
EOM
}


# 情報削除フォーム
if($deltype){
print<<EOM;
<CENTER>
<form action="$cgipath" method="$method">
<table width=580 align="center">
<tr><td><span class="bold">▼データの削除</span></td></tr>
EOM
if($deltype == 1 || $deltype == 2){ print "<tr><td>＊確認ボタンにチェックを入れ、実行ボタンを押してください</td></tr>\n"; }
else{
	print "<tr><td>＊処理を選択して、実行ボタンを押してください</td></tr>\n";
	print "<tr><td>＊『欠番処理』の場合は削除前のパスワードで$namaeを再登録できます。</td></tr>\n";
}
if($deltype == 2){ print "<tr><td>＊削除をしても削除前のパスワードで$namaeの再登録できます。</td></tr>\n"; }
print<<EOM;
</table>
<input type=hidden name=mode value="del">
<input type=hidden name=id value=\"$num\">
$passdata
EOM

if($deltype == 3){
	print "<select name=deltype>\n";
	print "<option value=0>処理を選んでください\n";
	print "<option value=1>・完全削除\n";
	print "<option value=2>・欠番処理\n";
	print "</select>\n";
}
else{
	print "確認：<input type=checkbox name=deltype value=$deltype>\n";
}

print<<EOM;
<INPUT type="submit" value=" 実行 ">
</FORM><HR WIDTH="580"></CENTER>
EOM
}
}
&foot;
exit;
}


# ---------- #
# 日付を取得 #
# ---------- #
sub jikan{
$ENV{'TZ'} = "JST-9";
$time = time;
(undef,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
if ($year > 50) { $year += 1900; } else{ $year += 2000; }
if($getyear){ $jikan = sprintf("%04d/%02d/%02d(%s) %02d:%02d",$year,$mon +1,$mday,$wday_array[$wday],$hour,$min,); }
else{ $jikan = sprintf("%02d/%02d(%s) %02d:%02d",$mon +1,$mday,$wday_array[$wday],$hour,$min,); }
}


# ------------------ #
# メール送信フォーム #
# ------------------ #
sub send_form{
# 名前取得
open (IN,"$datapath") || &error('open');
$flag = 0;
while(<IN>){
	if((split(/,/))[0] == $in{'id'}){
		$name = (split(/,/))[1];
		$flag = 1;
		last;
	}
}
close (IN);
if(!$formmail){ &error("不正なアクセスです"); }
elsif(!$flag){ &error('そのIDは見つかりません'); }

&head; $head_flag = 1;
print <<EOM;
<div align=center><br>以下は<b>$name</b>さん宛てのメールフォームです</div>
<form action="$cgipath" method="post">
<input type="hidden" name="mode" value="send">
<input type="hidden" name="id" value="$in{'id'}">
<table align=center border="0" cellpadding="2" cellspacing="2">
<tr>
<td class="mail">名前（必須）：</td>
<td><input type="text" name="name" size="40"></td>
</tr>
<tr>
<td class="mail">メールアドレス（必須）：</td>
<td><input type="text" name="mail" size="40"></td>
</tr>
<tr>
<td class="mail">タイトル（必須）：</td>
<td><input type="text" name="sub" size="40"></td>
</tr>
<tr>
<td class="mail">メッセージ：</td>
<td><textarea name="comment" cols="50" rows="9" wrap="soft"></textarea></td>
</tr>
<tr>
<td colspan="2" align="center"><input type="submit" value="メール送信"> <input type="reset" value="リセット"></td>
</tr>
</table>
EOM
&foot;
exit;
}


# ---------- #
# メール送信 #
# ---------- #
sub send{

# メールアドレス取得
open (IN,"$datapath") || &error('file');
$flag = 0;
while(<IN>){
	if((split(/,/))[0] == $in{'id'}){
		$mailto = (split(/,/))[7];
		$flag = 1;
		last;
	}
}
close (IN);

# 入力チェック
if(!$flag){ &error('そのIDは見つかりません'); }
elsif(!$mailto || !$formmail){ &error('不正なアクセスです'); }
elsif(!$in{'mail'}){ &error('メールアドレスの入力は必須です'); }
elsif(!$in{'sub'}){ &error('タイトルの入力は必須です'); }
elsif(!$in{'name'}){ &error('名前の入力は必須です'); }

$in{'comment'} =~ s/<br>/\n/g;
# メール作成＆送信
$com = <<EOM;
From: $in{'mail'}
To: $mailto
Subject: $in{'sub'}
MIME-Version: 1.0
Content-type: text/plain; charset=ISO-2022-JP
-----------------------------
$mailmes
Name : $in{'name'}
Mail : $in{'mail'}
-----------------------------
$in{'comment'}
EOM

&jcode'convert(*com,"jis");
if (!open(MAIL, "|$sendmail -t")) { &error("Sendmailのパスが間違っているか、利用できないサーバーです"); };
print MAIL $com;
close(MAIL);

# 送信後の画面表示
&head; $head_flag = 1;
print "<center>\n";
print <<EOM;
<table width="100%" border="0"><tr><td class="midashi">メール送信完了</td></tr></table>
<BR>
<span class=bold>メッセージを送信しました。</span><br><br>
<a href="$cgipath">[Back]</a>
</cetner>
EOM
exit;
}


# -------------------------- #
# 管理人へお知らせメール送信 #
# -------------------------- #
sub send_admin{

# 入力チェック
$in{'comment'} =~ s/<br>/\n/g;
# メール作成＆送信
$com = <<EOM;
From: $mailfrom
To: $mailfor
Subject: $main_titleお知らせメール
MIME-Version: 1.0
Content-type: text/plain; charset=ISO-2022-JP
EOM
if($mode eq "edit"){ $com .= "No.$in{'id'} の $in{'name'} さんが内容の編集をしました\n" }
else{ $com .= "No.$in{'add_no'} に $in{'name'} さんが新規投稿しました\n" }

if($in{'mail'}){ $com .= "Mail : $in{mail}\n" }
if($in{'url'}){ $com .= "URL : http\:\/\/$in{url}\n" }
for($x=1; $x<$#koumoku; $x++){ 
	if($in{"item$x"}){ $com .= "$koumoku[$x] : $in{\"item$x\"}\n"; }
	}
if($in{'upfile'} || $imgurl){ $com .= "画像 : 有り\n"; }
if($in{'comment'}){ $com .= "\nComment :\n$in{\"comment\"}\n"; }

&jcode'convert(*com,"jis");
if (!open(MAIL, "|$sendmail -t")) { &error("Sendmailのパスが間違っているか、利用できないサーバーです"); };
print MAIL $com;
close(MAIL);
}


# ---------------- #
# ログファイル出力 #
# ---------------- #
sub download{
if($in{'mpass'} ne $m_pass){ &error(badpass); }
print "Content-type: text/download\n\n";
open (IN,"$datapath") || &error('file');
@LINES = <IN>;
close (IN);

# ログファイルをそのまま出力
if($in{'type'} eq "backup"){
	foreach(@LINES){
		print "$_";
	}
}

# XML形式で出力
elsif($in{'type'} eq "xml"){
	@LINES = sort { (split(/\,/,$a))[$sort-1] <=> (split(/\,/,$b))[$sort-1] } @LINES;
	print "<?xml version = '1.0' encoding = 'Shift_JIS'?>\n";
	print "<list>\n";
	foreach(@LINES){
		($num,$name,undef,undef,undef,undef,undef,$mail,undef,$url,undef,undef,undef,undef,undef,undef,undef,undef,undef,@item) = split(/,/);
		if($name){
			print"  <no num=\"$num\">\n";
			print"    <name>$name</name>\n";
			if($mail_name && $mail) {print"    <mail>$mail</mail>\n"; }
			if($url_name && $web) {print"    <web>$web</web>\n"; }
			for($x=1; $x <= $#koumoku; $x++){
				if($item[$x-1]){ print "      <item$x>$item[$x-1]</item$x>\n"; }
			}
			print"  </no>\n";
		}
	}
	print "</list>\n";
}

# 項目のみをCSV出力
elsif($in{'type'} eq "csv"){
	@LINES = sort { (split(/\,/,$a))[$sort-1] <=> (split(/\,/,$b))[$sort-1] } @LINES;
	for($x=0;$x<$#koumoku;$x++){
		$itemdata .= "$koumoku[$x+1],";
	}
	print "番号,$namae,メール,URL,$itemdata\n";
	foreach(@LINES){
		$itemdata = "";
		($num,$name,undef,undef,undef,undef,undef,$mail,undef,$url,undef,undef,undef,undef,undef,undef,undef,undef,undef,@item) = split(/,/);
		for($x=0;$x<$#koumoku;$x++){
			$itemdata .= "$item[$x],";
		}
		print "$num,$name,$mail,$url,$itemdata\n";
	}
}
exit;
}


# ---------- #
# 名前の追加 #
# ---------- #
sub add{

# 記入漏れをチェック
if($in{'name'} eq ''){ &error('名前の入力は必須です'); }
if($in{'pass'} eq ''){ &error('no_pass'); }
if($in{'mpass'} && $in{'mpass'} ne $m_pass){ &error('badpass'); }

# ユーザーによる登録の場合のみ入力チェック
if(!$in{'mpass'}){
	if($show_mail && $checkmail && !$in{'mail'}){ &error("メールの入力は必須です") } 
	if($checkcom && $in{'comment'} eq ''){ &error('コメントの入力は必須です'); }
	foreach(@check){ if(!$in{"item$_"}){ &error("『$koumoku[$_]』の入力は必須です")} }
}

# 書き込み元のURLチェック
if($base_url){ &url_check; }

# ホストチェック（アクセス制限）
if($usedeny && $denytype){ &host_check; }

# 項目の長さチェック
for($x=1; $x<=$#koumoku; $x++){
	if ($lim[$x] && length($in{"item$x"}) > $lim[$x] * 2){ &error('length'); }
	$itemdata .= "$in{\"item$x\"},";
}

# 時間を取得
&jikan;

# ユーザーが名前を追加したときのみホスト名取得
if(!$in{'mpass'}){ &gethost; }
else{ $new_host = "";}

# パスワード暗号化
if($encode){$in{'pass'} = crypt($in{'pass'},$in{'pass'});}

# ファイルロック開始
if ($locktype) { &lock; }

open (IN,"$datapath") || &error('open');
@new = <IN>;
close (IN);

# 名前の重複チェックとカウント取得(No.指定が無い時)
if($#new || !$in{'add_no'}){
	$count = 0;
	foreach(@new){
		($tempno,$tempname) = split(/,/);
		if(!$checkname && $tempname eq $in{'name'}){ &error("その$namaeはすでに登録されています"); }
		if($count < $tempno){ $count = $tempno; }
	}
	$count++;
}

# ファイル添付処理
if ($in{'upfile'}) { $imgno = $time; &UpFile; }

# 挿入番号の指定が無い場合
if(!$in{'add_no'}){
	if($topsort){ unshift(@new,"$count,$in{'name'},$in{'pass'},$jikan,$time,$time,$new_host,$in{'mail'},$in{'mailflag'},$in{'url'},$in{'imgurl'},$tail,$W,$H,$imgflag,$in{'comment'},0,0,0,$itemdata\n");}
	else{ push(@new,"$count,$in{'name'},$in{'pass'},$jikan,$time,$time,$new_host,$in{'mail'},$in{'mailflag'},$in{'url'},$in{'imgurl'},$tail,$W,$H,$imgflag,$in{'comment'},0,0,0,$itemdata\n");}
	$in{'add_no'} = $count;
}

# 挿入場所指定。後からくっつけた機能なので、ちょっと無理あり^^；
else{
	$flag=0;
	foreach $line(@new){
		$line =~ s/\s*$//;
		($num,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail2,$imgw,$imgh,$imgflag2,$comment,undef,undef,undef,@item) = split(/,/,$line);
		# 挿入番号より小さい場合
		if($num < $in{'add_no'}){
			push (@LINES,"$line\n");
		}
		# トップソートしない場合は、同じor大きな番号を見つけた時点で挿入
		elsif(!$flag){
			if(!$topsort){ push(@LINES,"$in{'add_no'},$in{'name'},$in{'pass'},$jikan,$time,$time,$new_host,$in{'mail'},$in{'mailflag'},$in{'url'},$in{'imgurl'},$tail,$W,$H,$imgflag,$in{'comment'},0,0,0,$itemdata\n");}
			$itemdata2 = "";
			for($x=0;$x<$#koumoku;$x++){ $itemdata2 .= "$item[$x],"; }
			$num++;
			push(@LINES,"$num,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail2,$imgw,$imgh,$imgflag2,$comment,0,0,0,$itemdata2\n");
			$flag = 1;
		}
		# 挿入番号より大きい場合
		else{
			$itemdata2 = "";
			for($x=0;$x<$#koumoku;$x++){ $itemdata2 .= "$item[$x],"; }
			$num++;
			push(@LINES,"$num,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail2,$imgw,$imgh,$imgflag2,$comment,0,0,0,$itemdata2\n");
		}
	}
if(!$flag && !$topsort){ push(@LINES,"$in{'add_no'},$in{'name'},$in{'pass'},$jikan,$time,$time,$new_host,$in{'mail'},$in{'mailflag'},$in{'url'},$in{'imgurl'},$tail,$W,$H,$imgflag,$in{'comment'},0,0,0,$itemdata\n"); }
if($topsort){ unshift(@LINES,"$in{'add_no'},$in{'name'},$in{'pass'},$jikan,$time,$time,$new_host,$in{'mail'},$in{'mailflag'},$in{'url'},$in{'imgurl'},$tail,$W,$H,$imgflag,$in{'comment'},0,0,0,$itemdata\n");}
@new = @LINES;
}

# 登録数が規定数を超えた場合
if($maxlist && $topsort && $#new >= $maxlist){
	# 念のため、1回の処理では100件まで
	for($x=0; $x<100; $x++){
		if($#new < $maxlist){ last; }
		$popdata = pop(@new);
		(undef,undef,undef,undef,undef,$imgno,undef,undef,undef,undef,undef,$tail2) = split(/,/,$popdata);
		if($tail2){ unlink("$imgdir$imgno$tail2"); }
	}
}

# 書き込み処理
open (OUT,">$datapath") || &error('open');
print OUT (@new);
close (OUT);

# HTML更新
if($makeindex){ &make; }

# お知らせメール送信
if(($adminmail == 1 || $adminmail == 3) && !$in{'mpass'}){ &send_admin; }

# ロック解除
if(-e $lockfile){ unlink($lockfile); }

# 2重投稿対策
if($in{'mpass'}){ &admin; }
elsif($location){ 
	if($makeindex){ print "Location: ./index.html\n\n"; }
	else{ print "Location: $cgipath\n\n"; }
}
else{ &index; }
}


# ---------- #
# 内容の編集 #
# ---------- #
sub edit{
if($in{'mpass'}){
	if($in{'mpass'} ne $m_pass){ &error('badpass'); }
}
elsif($in{'pass'} eq ''){ &error(no_pass); }

if($mode eq "c_pass"){
	if($in{'pass1'} eq ''){&error(no_pass);}
	elsif($in{'pass2'} eq ''){&error(no_pass);}
	elsif($in{'pass1'} ne $in{'pass2'}){&error("2つのパスワードは同じものを入力してください");}

	# パスワード暗号化
	if($encode){$in{'pass1'} = crypt($in{'pass1'},$in{'pass1'});}
}
elsif($mode eq "edit"){
	# 記入漏れチェック
	if($in{'name'} eq ''){&error('名前の入力は必須です');}
	if($checkcom && $in{'comment'} eq ''){ &error('コメントの入力は必須です'); }
	if($show_mail && $checkmail && !$in{'mail'}){&error("メールの入力は必須です")} 
	foreach(@check){ if(!$in{"item$_"}){ &error("『$koumoku[$_]』の入力は必須です")} }
}

# 書き込み元のURLチェック
if($base_url){ &url_check; }

# 時間を取得
&jikan;

# ホスト名取得
&gethost;

# ファイルロック開始
if ($locktype) { &lock; }

open (IN,"$datapath") || &error('open');
@LINES = <IN>;
close (IN);

$flag = 0;
foreach $line(@LINES){
	# 名前の重複チェック
	if(!$checkname && ($mode eq "edit" || $mode eq "c_name")){
		if((split(/,/,$line))[1] eq $in{'name'}){
			if((split(/,/,$line))[0] != $in{'id'}){ &error("その$namaeはすでに登録されています"); }
		 }
	}

	if((split(/,/,$line))[0] == $in{'id'}){
		$flag = 1;
		$itemdata = "";
		# 該当する番号の場合は、改行をはずして全データ読み込み
		$line =~ s/\s*$//;
		($num,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail2,$imgw,$imgh,$imgflag2,$comment,undef,undef,undef,@item) = split(/,/,$line);

		if(!$in{'mpass'}){
			$pw = $in{'pass'};
			if($encode){$in{'pass'} = crypt($in{'pass'},$in{'pass'});}
			if($in{'pass'} ne "$pass" && $pw ne "$m_pass"){ close (IN); &error('badpass'); }
		}
		
		# 通常の修正
		if($mode eq "edit"){
			# 項目の長さチェック
			for($x=1; $x<=$#koumoku; $x++){
				if ($lim[$x] && length($in{"item$x"}) > $lim[$x] * 2){ &error('length'); }
				$itemdata .= "$in{\"item$x\"},";
			}

			if($topsort){
				unshift(@new,"$num,$in{'name'},$pass,$jikan,$time,$imgno,$new_host,$in{'mail'},$in{'mailflag'},$in{'url'},$in{'imgurl'},$tail2,$imgw,$imgh,$imgflag2,$in{'comment'},0,0,0,$itemdata\n");
			}
			else{
				push(@new,"$num,$in{'name'},$pass,$jikan,$time,$imgno,$new_host,$in{'mail'},$in{'mailflag'},$in{'url'},$in{'imgurl'},$tail2,$imgw,$imgh,$imgflag2,$in{'comment'},0,0,0,$itemdata\n");
			}
			next;
		}

		for($x=0;$x<$#koumoku;$x++){ $itemdata .= "$item[$x],"; }
		# パスワード変更の場合
		if($mode eq "c_pass"){
			push(@new,"$num,$name,$in{'pass1'},$last_time,$time1,$imgno,$new_host,$mail,$mailflag,$url,$imgurl,$tail2,$imgw,$imgh,$imgflag2,$comment,0,0,0,$itemdata\n");
		}

		# データの削除・欠番処理の場合
		elsif($mode eq "del"){
			if($in{'deltype'} == 1){ 
				if($tail2){ unlink("$imgdir$imgno$tail2"); }
				next;
			}
			elsif($in{'deltype'} == 2){
				if($tail2){ unlink("$imgdir$imgno$tail2"); }
				push(@new,"$num,,$pass,,,$imgno,\n");
			}
			else{ 
				if($deltype == 3){ &error('処理を選択してください'); }
				else { &error('確認ボタンにチェックを入れてください'); }
			}
		}

		# ファイルのアップロードの場合
		elsif($mode eq "c_img"){
			require "$uppath";
			if($tail2){ unlink("$imgdir$imgno$tail2"); }	# 以前のファイルを削除
			if ($in{'upfile'}) { &UpFile; }
			if($topsort){ unshift(@new,"$num,$name,$pass,$jikan,$time,$imgno,$new_host,$mail,$mailflag,$url,$imgurl,$tail,$W,$H,$imgflag,$comment,0,0,0,$itemdata\n"); }
			else{ push(@new,"$num,$name,$pass,$jikan,$time,$imgno,$new_host,$mail,$mailflag,$url,$imgurl,$tail,$W,$H,$imgflag,$comment,0,0,0,$itemdata\n"); }
		}

		# 名前の再登録の場合
		elsif($mode eq "c_name"){
			if($topsort){ unshift(@new,"$num,$in{'name'},$pass,,$time,$imgno,,,,,,,,,,,,,,\n");}
			else{ push(@new,"$num,$in{'name'},$pass,,$time,$imgno,,,,,,,,,,,,,,\n");}
		}
	}
	else{
		if($mode eq "edit"){
			if(!$checkname && (split(/,/))[1] eq $in{'name'}){
				close(IN);
				&error("その$namaeはすでに登録されています");
			}
		}

		if($mode eq "del" && $in{'deltype'} == 1){
			if((split(/,/,$line))[0] > $in{'id'}){
				# 番号を詰める時（汚いソースですこと^^
				$line =~ s/\s*$//;
				($num,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail2,$imgw,$imgh,$imgflag2,$comment,undef,undef,undef,@item) = split(/,/,$line);
				$num--;
				$itemdata = "";
				for($x=0;$x<$#koumoku;$x++){ $itemdata .= "$item[$x],"; }
				push(@new,"$num,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail2,$imgw,$imgh,$imgflag2,$comment,0,0,0,$itemdata\n");
			}
			else { push(@new,$line); }		
		}
		else { push(@new,$line); }
	}
}
if(!$flag){ &error("notfound");}

# 書き込み処理
open (OUT,">$datapath") || &error('open');
print OUT (@new);
close (OUT);

# HTML更新
if($makeindex){ &make; }

# お知らせメール送信
if(($adminmail==2 || $adminmail == 3) && !$in{'mpass'} && $mode eq "edit"){ &send_admin; }

# ロック解除
if(-e $lockfile){ unlink($lockfile); }

if($in{'mpass'}){ &admin; }

if($mode eq "c_pass"){
# 変更したことを表示
&head; $head_flag = 1;
print <<EOM;
<CENTER>
<BIG><B>パスワードを変更しました</B></BIG><BR><BR>
<A HREF="$cgipath">戻る</A>
</CENTER>
EOM
&foot;
exit;
}

elsif($mode eq "del"){
	# 2重投稿対策
	if($location){ 
		if($makeindex){ print "Location: ./index.html\n\n"; }
		else{ print "Location: $cgipath\n\n"; }
	}
	else{ &index; }
}

else{
	# 2重投稿対策
	if($location){ print "Location: $cgipath?id=$in{'id'}&mode=show\n\n"; }
	else{ &show; }
}
}


# ------------ #
# 管理用ページ #
# ------------ #
sub admin{
if($in{'mpass'} eq ''){ &error(no_pass); }
elsif($in{'mpass'} ne $m_pass){ &error(badpass); }

open(IN,"$datapath") || &error("open");
@LINES = <IN>;
close(IN);

&head; $head_flag = 1;
if($makeindex){print "□ <a href=\"index.html\">BACK</a>\n";}
else{print "□ <a href=\"$cgipath\">BACK</a>\n";}
print "<CENTER>\n";

print <<EOM;
<TABLE WIDTH="100%"><TR><TD class="midashi">管理ぺージ</TD></TR></TABLE>

<BR>
<table><tr><td>


<form action="$cgipath" method="$method">
※名簿追加と同時に項目の入力をしたい場合は、↓から登録フォームへ。
<div align=center>
<input type=hidden name="mode" value="addform"><input type=hidden name="mpass" value="$m_pass"><INPUT type="submit" value=" $namaeの追加フォームへ移動 ">
</div>
</td></tr></table>
</form>
<HR WIDTH="60%">
EOM

# 名簿の表示
&list;

print <<EOM;
<HR WIDTH="75%">
<TABLE border=0><TR><TD>

<FORM action="$cgipath" method="$method">
<span class="bold">▼登録内容の編集（名前,パスワード,項目など）</span><BR>
<SMALL>※変更したいNoとを入力して「実行」をクリックすると、編集フォームに行けます。</SMALL><BR>
<INPUT type="hidden" name="mode" value="editform">
<INPUT type="hidden" name="mpass" value="$m_pass">
変更するNo.：<INPUT name="id" size="3">　<INPUT type="submit" value=" 実行 ">
</FORM>

</TD></TR></TABLE>
<HR WIDTH="75%">
</CENTER><BR>
EOM
&foot;
exit;
}


# -------------- #
# index.html作成 #
# -------------- #
sub make{
if($show_lastup && $new_time) { &jikan; }
open(HTML,">index.html");
print HTML "<html>\n<head>\n";
print HTML "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
print HTML "<link rel=stylesheet type=text/css href=\"$stylepath\">\n";
print HTML "<title>$main_title</title>\n";
print HTML "</head>\n";$head_flag = 1;
if($background){ print HTML "<body background=\"$background\">\n"; }
else{ print HTML "<body>\n"; }
print HTML "<div align=\"center\">\n";
if($t_img eq ""){ print HTML "<div class=title>$main_title</div>\n"; }
else{ print HTML "<img src=\"$t_img\" width=$twid height=$thei>\n"; }

print HTML "<hr width=30\%>\n";
if($addname){print HTML "[<A HREF=\"$cgipath?mode=addform\">新規登録</A>]　";}
print HTML "[<A HREF=\"$cgipath?mode=find\">検索</A>]";
if($modoru){ print HTML "　[<A HREF=\"$modoru\">戻る</A>]\n"; }
print HTML "<BR><hr width=30\%>\n";
print HTML "<table><tr><td>$com</td></tr></table>\n";

# インデックス作成ファイルオープン
open(IN,"$datapath") || &error("open");
@LINES = <IN>;
close(IN);

if($target){ $target="_blank"; }
else{ $target="_top"; }

print HTML "<form action=\"$cgipath\" method=\"$method\">\n";
print HTML "<select name=\"sort\">\n";

if(!$topsort){ print HTML "<option value=1 selected>No.順\n"; } else{ print HTML "<option value=1>No.順\n"; }
print HTML "<option value=2 selected>$namae\n";
if($topsort){ print HTML "<option value=5 selected>最終更新日順\n";} else{ print HTML "<option value=5>最終更新日順\n"; }
if($show_mail){ print HTML "<option value=8>Mail\n"; }
if($show_url){ print HTML "<option value=10>Web\n"; }
foreach(@show){
	$sortno = $_ + 19;
	print HTML "<option value=$sortno>$koumoku[$_]\n";
	$x++;
}
if($show_img){ print HTML "<option value=12>画像\n"; }
print HTML "</select>\n";
print HTML "<input type=checkbox name=rev value=1><small>逆順表\示</small>\n";
print HTML "<input type=\"submit\" value=\"ソ\ート実行\">\n";
print HTML "</form></div>\n";

# テーブル見出し部分の表示(改造するときは、下にもう1箇所あり)
print HTML "<table class=\"table2\" cellpadding=2 align=\"center\">\n<tr class=\"tr1\">";
if($show_no){ print HTML "<td width=$show_no>No.</td>"; }
print HTML "<td width=$show_name>$namae</td>";
if($show_mail){ print HTML "<td width=$show_mail>Mail</td>"; }
if($show_url){ print HTML "<td width=$show_url>Web</td>"; }
$x=0;
foreach(@show){
	$sortno = $_ + 19;
	print HTML "<td width=\"$width[$x]\">$koumoku[$_]";
	$x++;
}
if($show_img){ print HTML "<td width=$show_url>画像</td>"; }
if($show_lastup){print HTML "<td width=$show_lastup>最終更新日</td>"; }
print HTML "</tr>\n";

# テーブル本体部分の表示開始
$i = 0;
$K = 0;
$flag=0;
$count = $max;
$max_no = $max * $max_table;
foreach(@LINES){
	if($max && $i == $count){
		$flag=1;
		$count = $count + $max;
	}
	$i++;
	# 改ページ処理
	if($i > $max_no){ $i = $#LINES + 1; last; }
	if($i == 1){ $flag= 0; }

	$_ =~ s/\s*$//;
	($num,$name,undef,$last_time,$time1,$imgno,undef,$mail,$mailflag,$url,$imgurl,$tail,undef,undef,undef,undef,undef,undef,undef,@item) = split(/,/);
	# 一定量ごとにテーブルを閉じる→見出しの再表示
	if($flag){
		$flag=0;
		print HTML "</table><br>\n";
		print HTML "<table class=\"table2\" cellpadding=2 align=\"center\">\n<tr class=\"tr1\">";
		if($show_no){ print HTML "<td width=$show_no>No.</td>"; }
		print HTML "<td width=$show_name>$namae</td>";
		if($show_mail){ print HTML "<td width=$show_mail>Mail</td>"; }
		if($show_url){ print HTML "<td width=$show_url>Web</td>"; }
		$x=0;
		foreach(@show){
			$sortno = $_ + 19;
			print HTML "<td width=\"$width[$x]\">$koumoku[$_]</td>";
			$x++;
		}
		if($show_img){ print HTML "<td width=$show_url>画像</td>"; }
		if($show_lastup){print HTML "<td width=$show_lastup>最終更新日</td>"; }
		print HTML "</tr>\n";
	}

	# 本体表示部分を改造したい場合はここから下
	if($K){ print HTML "<tr class=\"tr2\">"; $K=0; }
	else{ print HTML "<tr class=\"tr3\">"; $K=1; }
	if($show_no){ print HTML"<td>$num</td>"; }
	if($name){ print HTML"<td width=$show_name><a href=\"$cgipath?id=$num&mode=show\">$name</a></td>";}
	else{print HTML "<td><a href=\"$cgipath?id=$num&mode=show\">---</a></td>";}
	if($show_mail){
		if($mail && !$mailflag){ print HTML "<td><a href=\"mailto:$mail\">$maillink</a></td>" }
		elsif($mail && $mailflag){ print HTML "<td><a href=\"$cgipath?id=$num&mode=send_form\">$maillink</a></td>" }
		else{ print HTML "<td>－</td>" }
	}
	if($show_url){
		if($url){ print HTML "<td><a href=\"http://$url\" target=\"$target\">$urllink</a></td>" }
		else{ print HTML "<td>－</td>" }

	}
	$x=0;
	foreach(@show){
		if($item[$_-1] eq ''){print HTML "<td width=\"$width[$x]\">－</td>";}
		else{print HTML "<td width=\"$width[$x]\">$item[$_-1]</td>";}
		$x++;
	}
	if($show_img){
		if($tail){ print HTML "<td><a href=\"$imgdir$imgno$tail\">$imglink</a></td>" }
		else{ print HTML "<td>－</td>" }

	}
	if($show_lastup){
		if($last_time eq ''){ print HTML "<td>－</td>"; }
		else{
			# $new_time時間以内に更新があったら色付きで
			if ($new_time && ($time - $time1) < $new_time*3600) { $last_time = "<span class=\"new\">$last_time</span>"; }
			print HTML "<td><small>$last_time</small></td>";
		}
	}
	print HTML "</tr>\n";
}
print HTML "</table>\n";


# 他ページへのリンク表示
if($#LINES >= $max * $max_table){
	print HTML "<div align=\"center\">\n";
	print HTML "<form action=\"$cgipath\" method=\"$method\">\n";
	print HTML "<select name=page>";
	$x=1;
	$y=0;
	while ($i > 0) {
		if ($page == $y) { print HTML "<option value=$y selected>ページ$x\n"; }
		else { print HTML "<option value=$y>ページ$x\n"; }
		$x++;
		$y = $y + $max_no;
		$i = $i - $max_no;
	}
	print HTML "</select>\n";
	print HTML "<input type=\"submit\" value=\"ページ移動\">\n";
	print HTML "</form></div>\n";
}
print HTML "<DIV ALIGN=\"right\">\n";
print HTML "<form action=\"$cgipath\" method=\"$method\">\n";
print HTML "<input type=hidden name=mode value=\"admin\">\n";
print HTML "Pass：<input type=password name=mpass size=8 maxlength=8>\n";
print HTML "<INPUT type=\"submit\" value=\"Admin\">\n";
print HTML "</DIV>\n</FORM>\n";
print HTML "<DIV ALIGN=\"RIGHT\"><SMALL><A HREF=\"http://minicgi.net/\" target=\"_top\">Miniりすと $ver</A></SMALL></DIV>\n";
print HTML "</body>\n</html>\n";
close(HTML);
if($mode eq "make"){
	if($location){ print "Location: index.html\n\n"; }
	else{ &index; }
}
}


# ------------ #
# 名簿の最適化 #
# ------------ #
sub remake{
if($in{'mpass'} ne $m_pass){ &error(badpass); }
# ファイルロック開始
if($locktype){ &lock; }

open(IN,"$datapath") || &error("open");
@LINES = <IN>;
close(IN);

# ソート実行(それ以外)。こうしないと、空の項目が先頭に来ちゃうんだよな（－－；
foreach $line(@LINES){
	($no,$name) = split(/,/,$line);
	if($name){
		$sortno{$line} = $no;
	}
}
# ハッシュソート実行
@LINES = sort { ($sortno{$a} <=> $sortno{$b}) } keys(%sortno);

$num = 1;
foreach $line(@LINES){
	$line =~ s/\s*$//;
	(undef,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail2,$imgw,$imgh,$imgflag2,$comment,undef,undef,undef,@item) = split(/,/,$line);
	for($x=0; $x<$#koumoku; $x++){ $itemdata .= "$item[$x],"; }
	push(@new,"$num,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail2,$imgw,$imgh,$imgflag2,$comment,0,0,0,$itemdata\n");
	$num++;
	$itemdata = "";
}

# 最新更新日順に並べ替え
if($topsort){ @new = sort { (split(/\,/,$b))[4] <=> (split(/\,/,$a))[4] } @new; }

# 書き込み処理
open (OUT,">$datapath") || &error('open');
print OUT (@new);
close (OUT);

# HTML更新
if($makeindex){ &make; }

# ロック解除
if(-e $lockfile){ unlink($lockfile); }
&admin;
}


# ---------------------------- #
# 他サイトからのアクセスを排除 #
# ---------------------------- #
sub url_check {
	$ref_url = $ENV{'HTTP_REFERER'};
	$ref_url =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if ($ref_url !~ /$base_url/i) { &error("不正なアクセスです"); }
}


# -------------- #
# ファイルロック #
# -------------- #
sub lock {
	# 1分以上経過したロックファイルは削除
	if (-e $lockfile) {
		($locktime) = (stat($lockfile))[9];
		if ($locktime < time - 60) { unlink($lockfile); }
	}

	if($locktype == 1){
		local($retry) = 5;
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error("lock"); }
			sleep(1);
		}
	}
	elsif($locktype == 2){
		$lflag = 0;
		foreach (1 .. 5) {
			unless (-e $lockfile) {
				open(LOCK,">$lockfile") || &error("ロックファイルを作成できません");
				close(LOCK);
				$lflag = 1;
				last;
			} else {
				sleep(1);
			}
		}
		if ($lflag == 0) {
			&error("lock");
		}
	}
}


# ------------------ #
# 画像のアップロード #
# ------------------ #
sub UpFile {
	# 画像処理
	$macbin=0;
	foreach (@in) {
		if ($_ =~ /(.*)Content-type:(.*)/i) { $tail=$2; }
		if ($_ =~ /(.*)upfile=(.*)/i) { $fname=$2; }
		if ($_ =~ /application\/x-macbinary/i) { $macbin=1; }
	}

	$tail =~ s/\r//g;
	$tail =~ s/\n//g;
#	$fname =~ s/\"//g;
	$fname =~ tr/\"\x0D\x0A//d;

	# ファイル形式を認識
	$flag=0;
	if ($tail =~ /image\/gif/i) { $tail=".gif"; $flag=1; }
	if ($tail =~ /image\/jpeg/i) { $tail=".jpg"; $flag=1; }
	if ($tail =~ /image\/pjpeg/i) { $tail=".jpg"; $flag=1; }
	if ($tail =~ /image\/x-png/i) { $tail=".png"; $flag=1; }

	if (!$flag) {
		if ($fname =~ /\.gif$/i) { $tail=".gif"; $flag=1; }
		if (($fname =~ /\.jpe?g$/i)) { $tail=".jpg"; $flag=1; }
		if ($fname =~ /\.png$/i) { $tail=".png"; $flag=1; }
	}
	# アップロード失敗処理
	if(!$flag){ &error("アップロードできないファイル形式です"); }

	$upfile = $in{'upfile'};

	# マックバイナリ対策
	if ($macbin) {
		$length = substr($upfile,83,4);
		$length = unpack("%N",$length);
		$upfile = substr($upfile,128,$length);
	}

	# 添付データを書き込み
	$ImgFile = "$imgdir$imgno$tail";
	open(OUT,"> $ImgFile") || &error("画像のアップロードに失敗しました","lock");
	binmode(OUT);
	binmode(STDOUT);
	print OUT $upfile;
	close(OUT);
	chmod (0666,$ImgFile);

	# 画像サイズ取得
	if ($tail eq ".jpg") { ($W, $H) = &JpegSize($ImgFile); }
	elsif ($tail eq ".gif") { ($W, $H) = &GifSize($ImgFile); }
	elsif ($tail eq ".png") { ($W, $H) = &PngSize($ImgFile); }

	# 画像表示縮小
	$imgflag = 0;
	if ($W > $MaxW || $H > $MaxH) {
		$imgflag=1;
		$W2 = $MaxW / $W;
		$H2 = $MaxH / $H;
		if ($W2 < $H2) { $key = $W2; }
		else { $key = $H2; }
		$W = int ($W * $key) || 1;
		$H = int ($H * $key) || 1;
	}
}


# ---------------- #
#  JPEGサイズ認識  #
# ---------------- #
sub JpegSize {
	local($jpeg) = @_;
	local($t, $m, $c, $l, $W, $H);

	open(JPEG, "$jpeg") || return (0,0);
	binmode JPEG;
	read(JPEG, $t, 2);
	while (1) {
		read(JPEG, $t, 4);
		($m, $c, $l) = unpack("a a n", $t);

		if ($m ne "\xFF") { $W = $H = 0; last; }
		elsif ((ord($c) >= 0xC0) && (ord($c) <= 0xC3)) {
			read(JPEG, $t, 5);
			($H, $W) = unpack("xnn", $t);
			last;
		}
		else {
			read(JPEG, $t, ($l - 2));
		}
	}
	close(JPEG);
	return ($W, $H);
}


# --------------- #
#  GIFサイズ認識  #
# --------------- #
sub GifSize {
	local($gif) = @_;
	local($data);

	open(GIF,"$gif") || return (0,0);
	binmode(GIF);
	sysread(GIF,$data,10);
	close(GIF);

	if ($data =~ /^GIF/) { $data = substr($data,-4); }

	$W = unpack("v",substr($data,0,2));
	$H = unpack("v",substr($data,2,2));
	return ($W, $H);
}


# --------------- #
#  PNGサイズ認識  #
# --------------- #
sub PngSize {
	local($png) = @_;
	local($data);

	open(PNG, "$png") || return (0,0);
	binmode(PNG);
	read(PNG, $data, 24);
	close(PNG);

	$W = unpack("N", substr($data, 16, 20));
	$H = unpack("N", substr($data, 20, 24));
	return ($W, $H);
}

1;
