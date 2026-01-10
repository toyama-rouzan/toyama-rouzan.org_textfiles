# モジュール宣言/変数初期化
use strict;
my %cf;
#┌─────────────────────────────────
#│ JOYFUL NOTE : init.cgi - 2014/01/05
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────
$cf{version} = 'JoyfulNote v5.2';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────

#===========================================================
# ■ 設定項目
#===========================================================

# 管理者用パスワード
$cf{password} = '0123';

# サムネイル画像を作成する（要：Image::Magick）
# → 縮小画像を自動生成し、画像記事の表示速度を軽くする機能
# 0=no 1=yes
$cf{thumbnail} = 0;

# 掲示板タイトル
$cf{bbs_title} = "たんぽぽ記事投稿専用掲示板";

# アップロードファイル管理者チェック機能 (0=no 1=yes)
# → アップロードファイルは管理者がチェック後表示
$cf{img_check} = 0;

# 最大記事数 (親記事+レス記事も含めた数）
$cf{max} = 50;

# 返信がつくと親記事をトップへ移動 (0=no 1=yes)
$cf{topsort} = 1;

# 画像の位置
# 1 : コメントの下
# 2 : コメントの左（廻り込み）
$cf{image_position} = 1;

# ミニカウンタの設置
# → 0=no 1=テキスト 2=GIF画像
$cf{counter} = 1;

# ミニカウンタの桁数
$cf{mini_fig} = 6;

# テキストのとき：ミニカウンタの色
$cf{cntcol} = "#bb0000";

# GIFカウンタのとき：画像までのディレクトリ
$cf{gif_path} = "./icon";

# カウンタファイル
$cf{cntfile} = './data/count.dat';

# 本体CGIのURL【URLパス】
$cf{bbs_cgi} = './joyful.cgi';

# 書込CGIのURL【URLパス】
$cf{regist_cgi} = './regist.cgi';

# 管理CGIのURL【URLパス】
$cf{admin_cgi} = './admin.cgi';

# ログファイル【サーバパス】
$cf{logfile} = './data/log.cgi';

# アップロードディレクトリ【サーバパス】
$cf{imgdir} = './img';

# アップロードディレクトリ【URLパス】
$cf{imgurl} = "./img";

# テンプレートディレクトリ【サーバパス】
$cf{tmpldir} = './tmpl';

# 戻り先のURL【URLパス】
$cf{homepage} = "../../index.html";

# 文字コード自動判別（0=no 1=yes）
# → フォーム入力の文字コード判別を行う場合
$cf{conv_code} = 0;

# 記事 [タイトル] 部の長さ (全角文字換算)
$cf{sub_len} = 15;

# 同一IPアドレスからの連続投稿時間（秒数）
# → 値を 0 にするとこの機能は無効になります
$cf{wait} = 60;

# １画面当たりの記事表示数 (親記事基準)
# → 順に、スレッド表示、トピック表示、アルバム表示
$cf{max_thread} = 10;
$cf{max_topics} = 20;
$cf{max_albums} = 20;

# メール通知機能
# → 0=no  1=yes
$cf{mailing} = 0;

# メール通知先アドレス（メール通知する場合）
$cf{mailto} = 'xxx@xxx.xxx';

# sendmailのパス（メール通知する場合）
$cf{sendmail} = '/usr/lib/sendmail';

# sendmailの -fコマンドが必要な場合
# 0=no 1=yes
$cf{sendm_f} = 0;

# 文字色の設定（半角スペースで区切る）
$cf{colors} = '#800000 #DF0000 #008040 #0000FF #C100C1 #FF80C0 #FF8040 #000080 #808000';

# URLの自動リンク (0=no 1=yes)
$cf{auto_link} = 1;

# アイコン画像【URLパス】
# → 順に [eメール] [ホームページ]
$cf{ico_mail} = "./icon/mail.gif";
$cf{ico_home} = "./icon/home.gif";

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$cf{gethostbyaddr} = 0;

# アクセス制限（半角スペースで区切る、アスタリスク可）
#  → 拒否ホスト名を記述（後方一致）【例】*.anonymizer.com
$cf{deny_host} = '';
#  → 拒否IPアドレスを記述（前方一致）【例】210.12.345.*
$cf{deny_addr} = '';

# 禁止ワード
# → 投稿時禁止するワードをコンマで区切る
$cf{no_wd} = '';

# 日本語チェック（投稿時日本語が含まれていなければ拒否する）
# 0=No  1=Yes
$cf{jp_wd} = 1;

# URL個数チェック
# → 投稿コメント中に含まれるURL個数の最大値
$cf{urlnum} = 2;

# アップロードを許可するファイル（0=no 1=yes）
$cf{ok_text}  = 1;  # TEXT
$cf{ok_gif}   = 1;  # GIF
$cf{ok_jpeg}  = 1;  # JPEG
$cf{ok_excel} = 1;  # EXCEL
$cf{ok_word}  = 1;  # WORD
$cf{ok_ppt}   = 1;  # POWER POINT
$cf{ok_zip}   = 1;  # ZIP
$cf{ok_pdf}   = 1;  # PDF

# 投稿受理最大サイズ (bytes)
# → 例 : 102400 = 100KB
$cf{maxdata} = 10240000;

# 画像ファイルの最大表示の大きさ（単位：ピクセル）
# → これを超える画像は縮小表示します
$cf{max_img_w} = 250;
$cf{max_img_h} = 150;

# クッキーID名（特に変更しなくてよい）
$cf{cookie_id} = "joyfulbbs";

# -------------------------------------------------------------- #
# [ 以下は「過去ログ」機能を使用する場合の設定 ]
#
# 過去ログ生成
# → 0=no 1=yes
$cf{pastkey} = 0;

# 過去ログ用NOファイル【サーバパス】
$cf{nofile}  = './data/pastno.dat';

# 過去ログのディレクトリ【サーバパス】
# → パスの最後に / をつけない
$cf{pastdir} = './data/past';

# 過去ログ１ファイルの行数
# → この行数を超えると次ページを自動生成します
$cf{pastmax} = 600;

# -------------------------------------------------------------- #
# [ 以下は「画像認証機能」機能を使用する場合の設定 ]
#
# 画像認証機能の使用
# 0 : しない
# 1 : ライブラリ版（pngren.pl）
# 2 : モジュール版（GD::SecurityImage + Image::Magick）→ Image::Magick必須
$cf{use_captcha} = 0;

# 認証用画像生成ファイル【URLパス】
$cf{captcha_cgi} = './captcha.cgi';

# 画像認証プログラム【サーバパス】
$cf{captcha_pl} = './lib/captcha.pl';
$cf{captsec_pl} = './lib/captsec.pl';
$cf{pngren_pl}  = './lib/pngren.pl';

# 画像認証機能用暗号化キー（暗号化/復号化をするためのキー）
# → 適当に変更してください。
$cf{captcha_key} = 'captjoyfulbbs';

# 投稿キー許容時間（分単位）
# → 投稿フォーム表示後、送信ボタンが押されるまでの可能時間。
$cf{cap_time} = 30;

# 投稿キーの文字数
# ライブラリ版 : 4～8文字で設定
# モジュール版 : 6～8文字で設定
$cf{cap_len} = 6;

# 画像/フォント格納ディレクトリ【サーバパス】
$cf{bin_dir} = './lib/bin';

# [ライブラリ版] 画像ファイル [ ファイル名のみ ]
$cf{si_png} = "stamp.png";

# [モジュール版] 画像フォント [ ファイル名のみ ]
$cf{font_ttl} = "tempest.ttf";

#===========================================================
# ■ 設定完了
#===========================================================

# 設定内容を返す
sub init {
	return %cf;
}

#-----------------------------------------------------------
#  フォームデコード
#-----------------------------------------------------------
sub parse_form {
	my $cgi = shift;

	my %in;
	foreach ( $cgi->param() ) {
		my $val = $cgi->param($_);

		if ($_ ne 'upfile') {
			# 無効化
			$val =~ s/&/&amp;/g;
			$val =~ s/</&lt;/g;
			$val =~ s/>/&gt;/g;
			$val =~ s/"/&quot;/g;
			$val =~ s/'/&#39;/g;

			# 改行変換
			$val =~ s/\r\n/<br>/g;
			$val =~ s/\n/<br>/g;
			$val =~ s/\r/<br>/g;
		}

		$in{$_} = $val;
	}
	return %in;
}

#-----------------------------------------------------------
#  エラー画面
#-----------------------------------------------------------
sub error {
	my $err = shift;

	open(IN,"$cf{tmpldir}/error.html") or die;
	my $tmpl = join('', <IN>);
	close(IN);

	$tmpl =~ s/!error!/$err/g;

	print "Content-type: text/html; charset=shift_jis\n\n";
	print $tmpl;
	exit;
}

#-----------------------------------------------------------
#  画像リサイズ
#-----------------------------------------------------------
sub resize {
	my ($w,$h) = @_;

	# 画像表示縮小
	if ($w > $cf{max_img_w} || $h > $cf{max_img_h}) {
		my $w2 = $cf{max_img_w} / $w;
		my $h2 = $cf{max_img_h} / $h;
		my $key;
		if ($w2 < $h2) { $key = $w2; } else { $key = $h2; }
		$w = int ($w * $key) || 1;
		$h = int ($h * $key) || 1;
	}
	return ($w,$h);
}


1;

