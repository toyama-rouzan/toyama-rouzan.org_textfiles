# モジュール取込/変数初期化
use strict;
my %cf;
#┌─────────────────────────────────
#│ UP-LOADER : init.cgi - 2013/04/14
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────
$cf{version} = 'UP-LOADER v2.6';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────

#===========================================================
# ■ 基本設定
#===========================================================

# 管理用パスワード
$cf{password} = '0123';

# アップロードを許可するファイル（0=no 1=yes）
$cf{ok_text}  = 1;  # TEXT
$cf{ok_gif}   = 1;  # GIF
$cf{ok_jpeg}  = 1;  # JPEG
$cf{ok_excel} = 1;  # EXCEL
$cf{ok_word}  = 1;  # WORD
$cf{ok_ppt}   = 1;  # POWER POINT
$cf{ok_zip}   = 1;  # ZIP
$cf{ok_pdf}   = 1;  # PDF

# １回当りの最大投稿サイズ (Bytes)
# [参考]20480000 = 20MB
$cf{maxdata} = 5120000;

# 本体プログラムURL【URLパス】
$cf{upload_cgi} = './upload.cgi';

# 管理プログラムURL【URLパス】
$cf{admin_cgi} = './admin.cgi';

# ログファイル【サーバパス】
$cf{logfile} = './data/log.cgi';

# DLログファイル【サーバパス】
$cf{dlfile} = './data/dllog.cgi';

# カウントファイル【サーバパス】
$cf{cntfile} = './data/count.dat';

# アップロードディレクトリ【サーバパス】
$cf{upldir} = "./upl";

# アップロードディレクトリ【URLパス】
$cf{uplurl} = "./upl";

# テンプレートディレクトリ【サーバパス】
$cf{tmpldir} = './tmpl';

# DLログ保存最大数（これを超えると自動削除）
$cf{dllog_max} = 300;

# コメント部の最大入力文字数（全角換算で）
$cf{max_com} = 30;

# 記録最大数
# → これを超えると古い順に削除
$cf{log_max} = 200;

# １ページあたりの記事表示件数
$cf{pg_max} = 20;

# MIMEタイプの表示最大文字数
$cf{mime_max} = 25;

# 戻り先URL【URLパス】
$cf{homepage} = "../index.html";

# アイコン画像【URLパス】
# → 順に [ノーマル] [ロック][削除]
$cf{ico_down} = "./icon/down.gif";
$cf{ico_lock} = "./icon/lock.gif";
$cf{ico_del}  = "./icon/del.gif";

# アクセス制限：アップロード時のみ（半角スペースで区切る、アスタリスク可）
#  → 拒否ホスト名を記述（後方一致）【例】*.anonymizer.com
$cf{deny_host} = '';
# → 拒否IPアドレスを記述（前方一致）【例】210.12.345.*
$cf{deny_addr} = '';

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$cf{gethostbyaddr} = 0;

#===========================================================
# ■ 設定完了
#===========================================================

# 設定値を返す
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

		# 無害化
		if ($_ ne 'upfile') {
			$val =~ s/&/&amp;/g;
			$val =~ s/"/&quot;/g;
			$val =~ s/</&lt;/g;
			$val =~ s/>/&gt;/g;
			$val =~ s/'/&#39;/g;
			$val =~ s/[\r\n]//g;
		}
		$in{$_} = $val;
	}
	return %in;
}

#-----------------------------------------------------------
#  乱数発生
#-----------------------------------------------------------
sub make_rand {
	# 使用文字
	my @wd = (0 .. 9, 'a' .. 'z', 'A' .. 'Z', '_');

	# 乱数発生
	my $rand;
	for (1 .. 20) { $rand .= $wd[rand(@wd)]; }

	# 結果を返す
	return $rand;
}


1;

