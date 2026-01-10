#!/usr/bin/perl

# ↑先頭のパスはプロバイダによって異なります
###########################################################################
# Miniりすと ver4.01（2002/12/6公開）
# すくりぷと by けぃ(K-ji)
#
# 設置法や詳細は、readme.txtを参照してください（おまけつきなので^^）
# デザイン設定は、style.cssを編集してください。このstyle.cssは、niftyの
# ようなCGI専用サーバーではURLを変える必要があるので注意してください。
#
###########################################################################
$ver = 'v4.01';	# バージョン情報

#--------------------------------
# 重要な設定
#--------------------------------
# マスターパスワード(半角英数、4～8文字)
# このパスワードで、管理画面と全ての人の内容編集画面に入室できます
$m_pass = '0123';

# 名前は誰でも追加できるようにする？(0=no 1=yes) [0は管理人のみ追加可能]
$addname = 0;

# トップページで表示する順番
# 0 ： 番号の小さい順（1,2,3・・・）で表示
# 1 ： 最新更新日順（名前が追加・修正されたら、一番上にもってくる）
$topsort = 0;

# 上で$topsort=1（Yes）にした時のみ、登録する名前の最大数を設定できます（番号順に表示する時には、この機能を使うと考えにくいため）
# 最大数を超えると、"最も最終更新日の古い名前"が削除されます。登録の多い大規模HP向け（1000件越すようだと重くなると思うんで）
$maxlist = 0;		# 0の場合は、この機能を使いません

# 訪問者が名前を追加できる時に、追加する位置(番号)を自由にする(0=no 1=yes) 
$free_add = 0;

# 戻り先のURL。「http://～」でもOK
$modoru = "../index.html";	# ""にすれば「戻る」のリンク自体表示されなくなります

# 項目の名前（必要ないときは''にしてください。入力フォーム自体表示されなくなります）
$mail_name = '';		# メール
$url_name = '';		# ＵＲＬ
$gazou = '';	# 画像を貼り付ける項目

# 画像貼り付けは・・・(0：ver3.xのようにURLを記入する方式 1:アップロード方式)
$uptype = 1;

# 一般の入力項目の設定。同様の形式($koumoku[項目番号] = '項目名';)でいくつでも追加できます。
$koumoku[1] = 'ニックネーム';		# 項目1
$koumoku[2] = '納入状況';			# 項目2
$koumoku[3] = '納入日';		# 項目3
$koumoku[4] = '';			# 項目4
$koumoku[5] = '';			# 項目5
$koumoku[6] = '';			# 項目6
$koumoku[7] = '';			# 項目7
$koumoku[8] = '';	# 項目8
$koumoku[9] = '';		# 項目9
$koumoku[10] = '';		# 項目10
$koumoku[11] = '';		# 項目11
$koumoku[12] = '';# 項目12
$koumoku[13] = '';			# 項目13
$koumoku[14] = '';			# 項目14


#----------------------------------
# トップページに表示する項目の設定
#----------------------------------
# トップページに表示したい項目番号を、「,」区切りで書く。小さい順じゃなくてもOK
@show=(1,2,3);	# ←初期設定だと項目1と6と5の順に、左から表示されます

# ↑で指定した各項目の幅（width=○○の部分)。
@width=(200,80,80);	# ←初期設定だと項目1が280、項目5と6が50

# 項目以外で、トップページに表示するものの幅。表示しないときには「0」にする
$show_no = 40;		# 「No.」の幅
$show_name = 150;	# 「Name」の幅(これだけは必ず表示するので、0にしないでください)
$show_url = 0;		# 「URL」の幅
$show_mail = 0;	# 「Mail」の幅
$show_img = 0;		# 「画像の有無」の幅
$show_lastup = 0;	# 「最終更新日」の幅

# 最終更新日を色付きで表示するのは、何時間前までに投稿・修正があったとき？
# 0にすれば、この機能は働きません。
$new_time  = 0;

# トップページでメールやURL、画像の有無を表示する時のマーク
# アイコンを使いたくないときは、「$urllink ='[Web]';」や「$maillink = '[Mail]';」とすればOK
# 逆に、画像があるときのマークにアイコンを使うこともできます。 ＞Web,Mailを見本に
$urllink ='<img src="web.gif" border=0 width=15 height=15 alt="Home">';		# Web
$maillink ='<img src="mail.gif" border=0 width=15 height=12 alt="Mail">';	# Mail
$imglink = '★';								# 画像がある場合の表示


#----------------------------------
# プルダウン項目の設定
#----------------------------------
# プルダウン選択式にしたい項目番号を、「,」区切りで書く。
@select = (2); # ←これだと項目5と項目6

# プルダウンの内容なんですけど、見りゃ分かると思います（←適当だなぁ）
# 同じような書式で、いくらでも追加できます。ちなみに無記入の場合を考えて、1個目は「''」にしておくことをオススメします。
$sel[2] = ['','納入済'];		# 項目5のプルダウン設定

# 検索の時に、プルダウンの項目を使うようにする?(0=no 1=yes) 
$psearch = 1;

# プルダウン項目の1つ目が「''」でない場合、空の検索ができなくなってしまうのでその時は$emptyを1にしてください。
$empty = 0;


#----------------------------------
# その他、項目に関する詳細設定
#----------------------------------
# 入力必須にする項目の設定（URLと画像の項目以外は必須にできるはず）
$checkmail = 0;		# メールの記入を必須にする(0=no 1=yes) 
$checkcom = 0;		# コメントの入力を必須にする(0=no 1=yes)
@check=();		# 入力を必須にする項目番号を記入。例：@check=(1,5,11);

# 文字数制限したい項目を記入。書式は↓の通り
# $lim[制限したい項目番号] = 制限したい文字数（全角換算）
$lim[1] = 50;		# 項目1を25文字に制限。次の行以下にどんどん追加できます。
$lim[3] = 10;

#--------------------------------
# 一般設定（重要そうなものほど、上にもってきました）
#--------------------------------
# トップページで、1つのテーブルに$max人表示し、そのテーブルを$max_table個表示する
# つまりデフォルトでは1ページに25×2=50人表示されます
$max = 25;	# テーブル1つあたりの人数
$max_table = 2;	# 1ページに表示するテーブルの数

# 同じ名前が登録されるのを…(0=認めない 1=認める)
# view機能を利用するときには、0を推奨します(view機能についてはreadmeを参照)
$checkname = 0;

# index.htmlを作成する(0=no 1=yes)
# この機能をONにした場合は、index.htmlにリンクを張ります
$makeindex = 0;

# フォームメール機能を使用する(0=no 1=yes)。Sendmailが使える場合のみです
# この機能を使うと、登録者はメールアドレスを非公開のままメールを受け取ることができます
$formmail = 0;

# 管理ページ以外から登録・修正があったとき、管理人にお知らせメールを送る（Sendmailが使える場合のみ）
$adminmail = 0;			# 0：送らない  1：新規投稿の場合のみ  2：修正の時のみ 3：新規投稿と修正の時
$mailfor = 'xxxx@xxx.xxx';	# 送り先メールアドレス。送らないときは変更の必要無し
$mailfrom = 'Formmail';		# 差出人欄に表示するアドレス。これは変更しなくてもOK

# タグ利用の設定(0:全て不可 1:コメント欄のみ可 2:全ての項目で許可)
$usetag = 0;

# タグ許可のとき、次の危険なタグは使用不能にする。
@errtag = ('table','script','meta','form','!--','embed','html','body','tr','td','th','noscript','style');

# コメント欄にURLが入力されたとき、自動リンクする
$autolink = 0;

# 詳細表示ページで、書き込んだ人のHost情報も表示する(0=no 1=yes)
$show_host = 0;

# 訪問者が入力したURLに飛ぶときは・・・0:同じ窓で表示 1:別窓表示
$target = 1;

# 日付は年まで取得する？(0=月まで 1=年まで) 
$getyear = 0;

# 詳細表示ページで、前後のNoの人へのリンクを表示するするか？
#  (0=表示しない 1=上部にのみ表示 2=下部にのみ表示 3=上下に表示) 
$numlink = 0;

# 曜日の表示法。変更例→ @wday_array = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');　←こんな感じ
@wday_array = ('日','月','火','水','木','金','土');

# 登録者が自分で削除を行った場合の設定
# 0：削除自体不可能にする(削除フォーム非表示)
# 1：完全削除（再登録は不可能になるが、ログは軽くなる）
# 2：欠番状態にする（再登録可）
# 3：1と2で選択可
$deltype = 2;

# 項目入力フォームと、コメント入力フォームの幅
$item_wid = 30;		# 項目入力フォーム
$com_wid = 60;		# コメント入力フォーム

# データベース風に使う場合は、$namaeを「情報」や「データ」としてもいいかも。
# スクリプト中の「名前」とという単語をすべて置きかえます。
$namae = '氏名';

# 背景画像の設定(http://～でOK)
$background = '';


#--------------------------------
# ファイル・フォルダへのパス設定
#--------------------------------
# cgi-lib.plへのパス（同じフォルダならこのまま）
require './cgi-lib.pl';

# jcode.plへのパス（同じフォルダならこのまま）
$jcodepath = './jcode.pl';

# tool.cgiへのパス（同じフォルダならこのまま）
$uppath = './tool.cgi';

# sendmailへのパス（フォームメール機能を利用する場合のみ）
$sendmail="";

# 外部スタイルシートへのパス
$stylepath = './style.css';

# このスクリプトの名前
$cgipath = './list.cgi';

# データファイル名
$datapath = "./data/data.csv";

# アップロードされた画像を保存するフォルダ（最後に「/」をつける）
$imgdir = './img/';


#--------------------------------
# タイトルの設定
#--------------------------------
# タイトル
$main_title = '年会費納入状況';

# タイトルに画像を使いたい場合は以下を設定
$t_img= '';			# タイトル画像をURLで指定
$twid = 135;			# 　〃　の横幅(ピクセル指定)
$thei = 80;			# 　〃　の縦幅(　〃　)


#--------------------------------
# セキュリティ関連の設定
#--------------------------------
# アクセス制限機能の設定。（0：使わない 1:下で指定するホストを禁止 2:下で指定するホスト「以外」を禁止）
# 2は「大学からのみアクセス可能」なんて時に使えるかもしれません。でも、本格的にアクセス制限するなら.htaccessを。
$usedeny = 0;
@deny = ("xxx.xxx.com","123.456.789.*","");	# 対象のホスト名（IPアドレス）

# アクセス制限に引っ掛かる場合は・・・(0:名簿の閲覧自体禁止 1:閲覧はできるけど投稿できない)
$denytype = 0;

# アクセス制限に引っ掛かった場合のコメント。
$denycom = '現在利用できません';

# 他サイトから投稿を排除する場合には、設置URLを記入(http://～)。ただし、他サイトでない場合も
# 「HTTP_REFERER」を取得できない訪問者は書き込めなくなるので、荒らされでもしない限り指定しないのが無難。
$base_url = '';

# 投稿形式(POST or GET)。アップロード機能を使うときは必ずPOSTに。
$method = 'POST';


#--------------------------------
# サーバーに依存しそうな設定
#--------------------------------
# 以下の設定は、基本的に「1」でよいのですが、サーバーによっては使用できません。
# 設置はできるけど、名前の追加・編集時にうまくいかない時には「0」にしてみてください。

# 書き込み時にファイルをロックする (0=ロックしない 1=symlink関数でロック 2=open関数でロック)
$locktype = 0;

# ファイルロックをする場合、ロックファイル名とロックに使用するディレクトリ
$lockfile = "list.loc";		# ロックファイル名
$lockdir = "lock/";		# ロックファイルディレクトリ（パーミッションは777or755）

# パスワードを暗号化する(0=no 1=yes)
$encode = 1;

# Location機能を使って、2重投稿を防止する(0=no 1=yes)
$location = 1;

# BIGLOBEなど、CGI専用サーバーで画像アップロード機能を使う時、
# 上で指定した画像保存フォルダ($imgdir)のURLを、http://～で記入する
$imgdir2 = '';		# 通常は空のままでOK

#--------------------------------
# 利用者へのコメントの設定
#--------------------------------
# トップ上部のコメント(タグ使用OK。以下は例の文章)
$com = <<EOM;
<small>
■ 名前をクリックすると、詳細が表\示されます。<BR>
■ $new_time時間以内に追加・更新された名前は、日付が<span class=new>色つき</span>で表\示されます
</small>
EOM
# ↑は消しちゃダメです


# 新規登録ページ上部のコメント(タグ使用OK。以下は例の文章)
$com2 = <<EOM;
※$namaeと初期パスワードを入力して「$namaeの追加」をクリックしてください。
EOM
# ↑は消しちゃダメです


# フォームメールから送られたメールの、上部コメント
# できれば、設置URLなどを書いてあげましょう
$mailmes = <<EOM;
このメールは、$main_titleのフォームメールから送られたものです。
EOM
# ↑は消しちゃダメです


#--------------------------------
# アップロード機能の設定
#--------------------------------
# この機能をOFFにするには、「重要な設定」にて「 $gazou = '';」 にします
# アップできる画像形式は、.gif、.jpg、.jpeg、.pngです。

# 投稿できる画像のデータサイズ → 例 : 102400 = 100KB
$cgi_lib'maxdata = 102400;

# 画像ファイルの最大表示の大きさ（単位：ピクセル）
# → これを超える画像は縮小表示します。縮小が嫌な場合は、9999にでもしてください^^;
$MaxW = 380;	# 横幅
$MaxH = 380;	# 縦幅


# ===================== 設定完了 ===================== #
# -------------------------------- #
# ここから下は、プログラム本体です #
# -------------------------------- #
&decode;
$lockfile = "$lockdir$lockfile";		# ロックファイルを定義
if(!$imgdir2){ $imgdir2 = $imgdir; }		# CGI専用サーバーでの利用を考慮
if($usedeny && !$denytype){ &host_check; }	# アクセス制限

if($mode eq "") { &index; }
elsif ($mode eq "show") { &show; }
elsif ($mode eq "view") { &show; }

require "$uppath";	# 滅多に使わないサブルーチン入れ読み込み
if ($mode eq "add") { &add; }
elsif ($mode eq "find") { &find; }
elsif ($mode eq "addform") { &form; }
elsif ($mode eq "editform"){ &form; }
elsif ($mode eq "send_form") { &send_form; }
elsif ($mode eq "admin") { &admin; }
elsif ($mode eq "edit"){ &edit; }
elsif ($mode eq "c_pass") { &edit; }
elsif ($mode eq "c_img") { &edit; }
elsif ($mode eq "c_name") { &edit; }
elsif ($mode eq "del") { &edit; }
elsif ($mode eq "download") { &download; }
elsif ($mode eq "send") { &send; }
elsif ($mode eq "make") { &make; }
elsif ($mode eq "remake") { &remake; }
else{ &index; }
exit;


# ------------------ #
# トップページの表示 #
# ------------------ #
sub index{
&head; $head_flag = 1;

# タイトル表示
print "<div align=\"center\">\n";
if($t_img eq ""){ print"<div class=title>$main_title</div>\n"; }
else{ print "<img src=\"$t_img\" width=$twid height=$thei>\n"; }

# メニュー表示
print "<hr width=30\%>\n";
if($addname){print "[<A HREF=\"$cgipath?mode=addform\">新規登録</A>]　";}
print "[<A HREF=\"$cgipath?mode=find\">検索</A>]";
if($modoru){ print"　[<A HREF=\"$modoru\">戻る</A>]\n"; }
print "<BR><hr width=30\%>\n";
print"<table><tr><td>$com</td></tr></table>\n";

# インデックス作成ファイルオープン
open(IN,"$datapath") || &error("open");
@LINES = <IN>;
close(IN);

# 名簿の一覧表示
&list;

# 管理ページへの入室フォーム表示
print<<EOM;
<DIV ALIGN="right">
<form action="$cgipath" method="$method">
<input type=hidden name=mode value="admin">
Pass：<input type=password name=mpass size=8 maxlength=8>
<INPUT type="submit" value="管理">
</DIV>
</FORM>
EOM
&foot;
exit;
}


# -------------- #
# 名簿の一覧表示 #
# -------------- #
sub list{
# 時間取得は、○時間前の更新を色付きで表示するときのみ
if($show_lastup && $new_time) { $time = time; }

# URLの飛び方指定
if($target){ $target="_blank"; }
else{ $target="_top"; }

# ソート実行（番号順）
if($sort == 1){
	$sortname = "No.順";
	@LINES = sort { (split(/\,/,$a))[$sort-1] <=> (split(/\,/,$b))[$sort-1] } @LINES;
	if($in{'rev'}){ @LINES = reverse @LINES; }
}

# ソート実行（最終更新日順 or 名前の追加日順）
elsif($sort == 5 || $sort == 7){
	if($sort == 5){ $sortname = "更新日順"; } else { $sortname = "登録日順"; }
	@LINES = sort { (split(/\,/,$b))[$sort-1] <=> (split(/\,/,$a))[$sort-1] } @LINES;
	if($in{'rev'}){ @LINES = reverse @LINES; }
}

# ソート実行(それ以外)。こうしないと、空の項目が先頭に来ちゃうんだよな（－－；
elsif($sort){
	$sortname = "$koumoku[$sort-19]";
	foreach $line(@LINES){
		$sortdata = (split(/\,/,$line))[$sort-1];

		if($sortdata){
			$sortno{$line} = $sortdata;
		}
		else{ push(@temp,$line); }
	}
	# ハッシュソート実行
	@LINES = sort { (uc $sortno{$a} <=> uc $sortno{$b}) || (uc $sortno{$a} cmp uc $sortno{$b})} keys(%sortno);

	if($in{'rev'}){ @LINES = reverse @LINES; }
	# 空の項目は後ろにくっつける
	push(@LINES,@temp);
}

# ソートの見出し表示
print "<form action=\"$cgipath\" method=\"$method\">\n";
if ($in{'mpass'} && $in{'mpass'} eq $m_pass){ print "<input type=hidden name=mode value=\"admin\">\n<input type=hidden name=mpass value=\"$m_pass\">\n"; }
if ($mode eq 'find'){
print "<input type=hidden name=mode value=\"find\">\n";
print "<input type=hidden name=word value=\"$in{'word'}\">\n";
print "<input type=hidden name=cond value=\"$in{'cond'}\">\n";
print "<input type=hidden name=sflag value=\"1\">\n";
if($psearch){
	for($x=1; $x<=$#koumoku; $x++){
		if($in{"item$x"}){ 
		print "<input type=hidden name=item$x value=\"$in{\"item$x\"}\">\n";
		}
	}
}
}
print "<select name=\"sort\">\n";

# ↓なんか、もっといい書き方ありそうだ（汗;
if($sort==1 || (!$sort && !$topsort)){ print "<option value=1 selected>No.順\n"; } else{ print "<option value=1>No.順\n"; }
if($sort==2){ print "<option value=2 selected>$namae\n";} else{ print "<option value=2>$namae\n"; }
if($sort==5 || (!$sort && $topsort)){ print "<option value=5 selected>最終更新日順\n";} else{ print "<option value=5>最終更新日順\n"; }

if($show_mail){
	if($sort==8){ print "<option value=8 selected>Mail\n"; }
	else{ print "<option value=8>Mail\n"; }
}
if($show_url){
	if($sort==10){ print "<option value=10 selected>Web\n"; }
	else{ print "<option value=10>Web\n"; }
}
foreach(@show){
	$sortno = $_ + 19;
	if($sort == $sortno){ print "<option value=$sortno selected>$koumoku[$_]\n"; }
	else{ print "<option value=$sortno>$koumoku[$_]\n"; }
	$x++;
}
if($show_img){
	if($uptype){
		if($sort==12){ print "<option value=12 selected>画像\n"; }
		else{ print "<option value=12>画像\n"; }
	}
	else{
		if($sort==11){ print "<option value=11 selected>画像\n"; }
		else{ print "<option value=11>画像\n"; }
	}
}
print "</select>\n";

if($in{'rev'}){ print "<input type=checkbox name=rev value=1 checked><small>逆順表\示</small>\n"; }
else{ print "<input type=checkbox name=rev value=1><small>逆順表\示</small>\n"; }

print "<input type=\"submit\" value=\"ソ\ート実行\">\n";
print "</form></div>\n";

# テーブル見出し部分の表示(改造するときは、下にもう1箇所あり)
print "<table class=\"table2\" cellpadding=2 align=\"center\">\n<tr class=\"tr1\">";
if($show_no){ print "<td width=$show_no>No.</td>"; }
print "<td width=$show_name>$namae</td>";
if($show_mail){ print "<td width=$show_mail>Mail</td>"; }
if($show_url){ print "<td width=$show_url>Web</td>"; }
$x=0;
foreach(@show){
	$sortno = $_ + 19;
	print"<td width=\"$width[$x]\">$koumoku[$_]";
	$x++;
}
if($show_img){ print "<td width=$show_url>画像</td>"; }
if($show_lastup){print "<td width=$show_lastup>最終更新日</td>"; }
print"</tr>\n";

# テーブル本体部分の表示開始
$i = 0;
$j = 0;
$K = 0;
$flag=0;
$count = $max;
$max_no = $max * $max_table;

$page = $in{'page'};
$start = $page + 1;
$end   = $page + $max_no;
foreach(@LINES){
	if($max && $i == $count){
		$flag=1;
		$count = $count + $max;
	}
	$i++;
	if ($i < $start) { next; }
	elsif($i > $end){ $i = $#LINES + 1; last; }
	$j = $page + 1; # ページの先頭の場合
	if($i == $j){ $flag= 0; }

	$_ =~ s/\s*$//;
	($num,$name,undef,$last_time,$time1,$imgno,undef,$mail,$mailflag,$url,$imgurl,$tail,undef,undef,undef,undef,undef,undef,undef,@item) = split(/,/);
	# 一定量ごとにテーブルを閉じる→見出しの再表示
	if($flag){
		$flag=0;
		print "</table><br>\n";
		print "<table class=\"table2\" cellpadding=2 align=\"center\">\n<tr class=\"tr1\">";
		if($show_no){ print "<td width=$show_no>No.</td>"; }
		print "<td width=$show_name>$namae</td>";
		if($show_mail){ print "<td width=$show_mail>Mail</td>"; }
		if($show_url){ print "<td width=$show_url>Web</td>"; }
		$x=0;
		foreach(@show){
			$sortno = $_ + 19;
			print"<td width=\"$width[$x]\">$koumoku[$_]</td>";
			$x++;
		}
		if($show_img){ print "<td width=$show_url>画像</td>"; }
		if($show_lastup){print "<td width=$show_lastup>最終更新日</td>"; }
		print "</tr>\n";
	}

	# 本体表示部分を改造したい場合はここから下
	if($K){ print"<tr class=\"tr2\">"; $K=0; }
	else{ print"<tr class=\"tr3\">"; $K=1; }
	
	if($show_no){ print"<td>$num</td>"; }
	if($name){ print"<td width=$show_name><a href=\"$cgipath?id=$num&mode=show\">$name</a></td>";}
	else{print"<td><a href=\"$cgipath?id=$num&mode=show\">---</a></td>";}

	# メール表示
	if($show_mail){
		if($mail && !$mailflag){ print"<td><a href=\"mailto:$mail\">$maillink</a></td>" }
		elsif($mail && $mailflag && $formmail){ print"<td><a href=\"$cgipath?id=$num&mode=send_form\">$maillink</a></td>" }
		else{ print "<td>－</td>" }
	}

	# ホームページへのリンク表示
	if($show_url){
		if($url){ print"<td><a href=\"http://$url\" target=\"$target\">$urllink</a></td>" }
		else{ print "<td>－</td>" }

	}

	# 項目表示
	$x=0;
	foreach(@show){
		if($item[$_-1] eq ''){print"<td width=\"$width[$x]\">－</td>";}
		else{print"<td width=\"$width[$x]\">$item[$_-1]</td>";}
		$x++;
	}

	# 画像の有無チェック
	if($show_img){
		if($uptype){
			if($tail){ print"<td><a href=\"$imgdir2$imgno$tail\">$imglink</a></td>" }
			else{ print "<td>－</td>" }
		}
		else{
			if($imgurl){ print"<td><a href=\"$imgurl\">$imglink</a></td>" }
			else{ print "<td>－</td>" }
		}
	}

	# 前回の更新時間を表示
	if($show_lastup){
		if($last_time eq ''){ print"<td>－</td>"; }
		else{
			# $new_time時間以内に更新があったら色付きで
			if ($new_time && ($time - $time1) < $new_time*3600) { $last_time = "<span class=\"new\">$last_time</span>"; }
			print"<td><small>$last_time</small></td>";
		}
	}
	print"</tr>\n";
}
print"</table>\n";

# 他ページへのリンク表示
if($#LINES >= $max * $max_table){
	print "<div align=\"center\">\n";
	print "<form action=\"$cgipath\" method=\"$method\">\n";
	if ($in{'mpass'} && $in{'mpass'} eq $m_pass){ print "<input type=hidden name=mode value=\"admin\">\n<input type=hidden name=mpass value=\"$m_pass\">\n"; }
	if ($mode eq 'find'){
	print "<input type=hidden name=mode value=\"find\">\n";
	print "<input type=hidden name=word value=\"$in{'word'}\">\n";
	print "<input type=hidden name=cond value=\"$in{'cond'}\">\n";
	print "<input type=hidden name=sflag value=\"1\">\n";
	if($psearch){
		for($x=1; $x<=$#koumoku; $x++){
			if($in{"item$x"}){ 
			print "<input type=hidden name=item$x value=\"$in{\"item$x\"}\">\n";
			}
		}
	}
	}
	print "<input type=hidden name=sort value=\"$sort\">\n";
	print "<input type=hidden name=rev value=\"$in{'rev'}\">\n";
	print "<select name=page>";
	$x=1;
	$y=0;
	while ($i > 0) {
		if ($page == $y) { print "<option value=$y selected>ページ$x\n"; }
		else { print "<option value=$y>ページ$x\n"; }
		$x++;
		$y = $y + $max_no;
		$i = $i - $max_no;
	}
	print "</select>\n";
	print "<input type=\"submit\" value=\"ページ移動\">\n";
	print "</form></div>\n";
}
}

# -------------- #
# 詳細表示ページ #
# -------------- #
sub show{
&head; $head_flag=1;

if($target){ $target="_blank"; }
else{ $target="_top"; }
$id = $in{'id'};
$flag = 0;

if($makeindex){ print "□ <a href=\"index.html\">BACK</a>\n"; }
else{ print "□ <a href=\"$cgipath\">BACK</a>\n"; }
print "<center>\n";

open (IN,"$datapath") || &error('open');
while(<IN>){
	if($mode eq 'view'){
		if((split(/,/))[1] ne $in{'name'}){ next; }
	}
	else {
		if((split(/,/))[0] != $in{'id'}){ next; }
	}

	# データが見つかった時は、改行をはずして全項目を読み込みましょう
	$_ =~ s/\s*$//;
	($num,$name,$pass,$last_time,$time1,$imgno,$host,$mail,$mailflag,$url,$imgurl,$tail,$imgw,$imgh,$imgflag,$comment,undef,undef,undef,@item) = split(/,/);
	if($mode eq 'view'){ $id = $num; }

	# 欠番フォーム
	if(!$name){ 
print <<EOM;
<br><br>
<b>この$namaeは削除されたため、現在はデータがありません。<br><br>
削除前のパスワードか管理用パスワードで、$namaeを再登録できます。</b>
<form action="$cgipath" method="$method">
<input type=hidden name=id value="$num">
<input type="hidden" name="mode" value="c_name">
新しい$namae：<INPUT name="name" size="15">　パスワード：<input type=password name=pass size=8 maxlength=8>　<input type="submit" value="再登録する">
</form>
</center>
EOM
if($numlink){
	my($a,$b);
	$a = $id - 1; $b = $id + 1;
	print "<div align=center>\n";
	print "<a href=\"$cgipath?mode=show&id=$a\">[←Back]</a> &nbsp; [No.$num] &nbsp; <a href=\"$cgipath?mode=show&id=$b\">[Next→]</a>\n";
	print "</div>\n";
}
&foot;
exit;
	}

	print "<TABLE WIDTH=\"95%\" CELLPADDING=\"2\">\n";
	print "<TR><TD class=\"name\">$name</TD></TR>\n";
	if($last_time){ 
		if($show_host && $host){$last_time = "$last_time <BR>Host：$host"}
		print "<TR><TD align=\"right\"><SMALL><I>Last Update：$last_time</I></SMALL></TD></TR>";
	}
	if(!$last_time && $show_host && $host){print "<TR><TD align=\"right\"><SMALL><I>Host：$host</I></SMALL></TD></TR>";}
	print "</TABLE>\n<BR>\n";
	if($last_time){
		# 画像自動リンク
		if($gazou && !$uptype && $imgurl){ $imgurl =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<IMG SRC=\"$2\">/g; }

		# 前後Noへのリンク表示
		if($numlink == 1 || $numlink == 3){
			my($a,$b);
			$a = $id - 1; $b = $id + 1;
			print "<div align=center>\n";
			print "<a href=\"$cgipath?mode=show&id=$a\">[←Back]</a> &nbsp; [No.$num] &nbsp; <a href=\"$cgipath?mode=show&id=$b\">[Next→]</a>\n";
			print "</div>\n";
		}
		# 項目表示開始
		print "<TABLE BORDER=\"0\" CELLPADDING=\"3\">\n";
		if($mail_name && $mail && !$mailflag && $formmail){print "<TR><TD class=\"left\">$mail_name</TD><TD class=\"right\"><A HREF=\"mailto:$mail\">$mail</A> &nbsp;<small>（<A HREF=\"$cgipath?id=$id&mode=send_form\">メール送信フォーム</A>）</small></TD></TR>\n";}
		elsif($mail_name && $mail && !$mailflag && !$formmail){print "<TR><TD class=\"left\">$mail_name</TD><TD class=\"right\"><A HREF=\"mailto:$mail\">$mail</A></TD></TR>\n";}
		elsif($mail_name && $mail && $mailflag && $formmail){print "<TR><TD class=\"left\">$mail_name</TD><TD class=\"right\"><A HREF=\"$cgipath?id=$id&mode=send_form\">メール送信フォームへ</A></TD></TR>\n";}
		if($url_name && $url){print "<TR><TD class=\"left\">$url_name</TD><TD class=\"right\"><A HREF=\"http://$url\" target=\"$target\">http://$url</A></TD></TR>\n";}
		for($x=0;$x<$#koumoku;$x++){
			if($koumoku[$x+1] && $item[$x]){print "<TR><TD class=\"left\">$koumoku[$x+1]</TD><TD class=\"right\">$item[$x]</TD></TR>\n";}
		}

		# 画像表示
		if($gazou && !$uptype && $imgurl){ print "<TR><TD class=\"left\">$gazou</TD><TD class=\"right\">$imgurl</TD></TR>\n" }
		if($gazou && $tail){
			if($imgflag){ $tail ="<a href=\"$imgdir2$imgno$tail\"><img src=\"$imgdir2$imgno$tail\" border=0 width=$imgw height=$imgh alt=\"$imgno$tail\"></a>"; }
			else{ $tail ="<img src=\"$imgdir2$imgno$tail\" border=0 width=$imgw height=$imgh alt=\"$imgno$tail\">"; }
			print "<TR><TD class=\"left\">$gazou</TD><TD class=\"right\">$tail</TD></TR>\n";
		}
		print "</TABLE>\n<BR><BR>\n\n\n";

		# コメント部分表示開始
		if($comment){
			print "<TABLE CELLSPACING=\"0\"><TR><TD class=\"com1\">　▼Comment</TD></TR>\n";
			print "<TR><TD class=\"com2\">\n";
			print "<TABLE WIDTH=\"98%\"><TR><TD class=\"com3\">$comment</TD></TR></TABLE>\n";
			print "</TD></TR></TABLE><BR>\n";
		}

		# 前後Noへのリンク表示
		if($numlink == 2 || $numlink == 3){
			my($a,$b);
			$a = $id - 1; $b = $id + 1;
			print "<div align=center>\n";
			print "<a href=\"$cgipath?mode=show&id=$a\">[←Back]</a> &nbsp; [No.$num] &nbsp; <a href=\"$cgipath?mode=show&id=$b\">[Next→]</a>\n";
			print "</div>\n";
		}
	}
	# 最終更新日がないのは、管理人が名前だけ登録したとき
	else{
		print "<br>\n<b>現在データは登録されていません。</b>";
		if($numlink){
			my($a,$b);
			$a = $id - 1; $b = $id + 1;
			print "<br><br><div align=center>\n";
			print "<a href=\"$cgipath?mode=show&id=$a\">[←Back]</a> &nbsp; [No.$num] &nbsp; <a href=\"$cgipath?mode=show&id=$b\">[Next→]</a>\n";
			print "</div>\n";
		}
	}
	$flag = 1;
	last;
}
close (IN);

if(!$flag){ &error('notfound'); }

print<<EOM;
<DIV ALIGN="right">
<form action="$cgipath" method="$method">
<input type=hidden name=mode value="editform">
<input type=hidden name=id value="$id">
Pass：<input type=password name=pass size=8 maxlength=8>
<INPUT type="submit" value="内容の編集">
</DIV>
</FORM>
</CENTER>
EOM
&foot;
exit;
}


# ------------ #
# デコード処理 #
# ------------ #
sub decode{
&ReadParse;
if(%in){ require "$jcodepath"; }
while (($key,$val) = each %in) {
	if ($key ne "upfile") {
		&jcode'convert(*val, "sjis", "", "z");

		# タグ処理
		# 全て許可
   		if($usetag == 2) {
			if($in{'kill_tag'} && $key eq "comment"){
				$val =~ s/</&lt;/g;
				$val =~ s/>/&gt;/g;
				$val =~ s/\"/&quot;/g;
			}
			foreach ( @errtag ){
				if ($value =~ /<$_(.|\n)*>/i) {	 &error("利用できないタグが含まれています"); }
			}
		}
		else {
			# コメントのみタグ許可
			if($usetag == 1 && $key eq "comment"){
				if($in{'kill_tag'}){
					$val =~ s/</&lt;/g;
					$val =~ s/>/&gt;/g;
					$val =~ s/\"/&quot;/g;
				}
				else{
					foreach ( @errtag ){
					if ($value =~ /<$_(.|\n)*>/i) {	 &error("利用できないタグが含まれています");	}
					}
				}
			}
			# 全て不可
			else{
				$val =~ s/</&lt;/g;
				$val =~ s/>/&gt;/g;
				$val =~ s/\"/&quot;/g;
			}
		}

		# 区切り文字の”,”があれば"，”に変換
		$val =~ s/\,/，/g;

		# 改行処理
		if ($key eq "comment") {
			$val =~ s/\r\n/<br>/g;
			$val =~ s/\r/<br>/g;
			$val =~ s/\n/<br>/g;
		}
		else {
			$val =~ s/\r//g;
			$val =~ s/\n//g;
		}

		if($autolink && $key eq "comment"){
			$val =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target='_blank'>$2<\/a>/g;
		}
	}
	$in{$key} = $val;
}
$mode = $in{'mode'};
$sort = $in{'sort'};
$in{'url'} =~ s/^http\:\/\///;
}


# ------------ #
# アクセス制限 #
# ------------ #
sub host_check{
	&gethost;
	if($usedeny == 2){ $flag = 0; }
	foreach (@deny) {
		if(!$_){ next; }
		if ($new_host =~ /$_/i) {
			if($usedeny == 1){ &error("$denycom"); }
			elsif($usedeny == 2){ $flag = 1; last; }
		}
	}
	if($usedeny == 2 && !$flag){ &error("$denycom"); }
}


# ------------ #
# HTMLヘッダー #
# ------------ #
sub head{
print "Content-type: text/html; charset=Shift_JIS\n\n";
print <<EOM;
<html>
<head>
<link rel=stylesheet type=text/css href="$stylepath">
<title>$main_title</title>
</head>
EOM
if($background){ print"<body background=\"$background\">\n"; }
else{ print"<body>\n"; }
}


# -------------- #
# HTMLフッターー #
# -------------- #
sub foot{
# 著作権表示です
print <<EOM
</body>
</html>
EOM
}


# ---------------- #
# ホスト名・IP取得 #
# ---------------- #
sub gethost{
$addr = $ENV{'REMOTE_ADDR'};
$new_host = $ENV{'REMOTE_HOST'};
if ($new_host eq '' || $new_host eq $addr) {$new_host = gethostbyaddr(pack('C4',split(/\./,$addr)),2) || $addr;}
}


# ---------- #
# エラー処理 #
# ---------- #
sub error {
	if ($_[0] ne "lock"){ unlink($lockfile); }	# ロックファイル削除
	if($_[0] eq "open"){ $errmes = "$datapathを開けません"; }
	elsif($_[0] eq "badpass"){ $errmes = "パスワードが違います"; }
	elsif($_[0] eq "no_pass"){ $errmes = "パスワードの入力は必須です"; }
	elsif($_[0] eq "length"){ $errmes = "「$koumoku[$x]」は全角$lim[$x]文字以下にしてください"; }
	elsif($_[0] eq "lock"){ $errmes = "同時アクセスのため、書き込みを中断しました"; }
	elsif($_[0] eq "notfound"){ $errmes = "該当するデータが見つかりません"; }
	else{ $errmes = "$_[0]"}

	if(!$head_flag){ &head; }
	print "<center>ERROR! - $errmes<br><br>\n";
	print "<a href=\"javascript:history.back()\"><b>Back</b></a></center><br>\n";
	&foot;
exit;
}
