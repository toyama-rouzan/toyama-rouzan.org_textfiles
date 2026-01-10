# モジュール宣言/変数初期化
use strict;

my %cf;
#┌─────────────────────────────────
#│ PasswordManager : init.cgi - 2013/11/17
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────
$cf{version} = 'PasswordManager v3.5';
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
$cf{password} = '8942926';

# 管理アドレス
$cf{master} = 'ysokk1@gmail.com';

# パスワード発行形態
# 1 : ユーザからの発行＆メンテを可能にする
# 2 : 発行は管理者のみ。ユーザはメンテのみ
# 3 : 発行＆メンテは管理者のみ（pwmgr.cgi index.htmlは不要）
$cf{pwd_regist} = 2;

# パスワードファイル【サーバパス】
# → 正確にフルパスを記述すること
$cf{pwdfile} = '/var/www/vhosts/w872.jpnsv.net/toyama-rouzan.org/member/pwmgr/.htpasswd';

# 会員ファイル【サーバパス】
# → 正確にフルパスを記述すること
$cf{memfile} = '/var/www/vhosts/w872.jpnsv.net/toyama-rouzan.org/member/pwmgr/member_dat.cgi';

# アクセスログファイル【サーバパス】
# → 正確にフルパスを記述すること
$cf{axsfile} = '/var/www/vhosts/w872.jpnsv.net/toyama-rouzan.org/member/pwmgr/pwlog_dat.cgi';

# アクセスログの最大数
$cf{log_max} = 300;

# 本体プログラムURL【URLパス】
$cf{pwmgr_cgi} = './pwmgr.cgi';

# 管理プログラムURL【URLパス】
$cf{admin_cgi}  = './admin.cgi';

# テンプレートディレクトリ【サーバパス】
$cf{tmpldir} = './tmpl';

# 戻り先URL【URLパス】
$cf{back_url} = '../index.html';

# １ページ当り会員表示件数
$cf{pageView} = 50;

# sendmailパス【サーバパス】
$cf{sendmail} = '/usr/sbin/sendmail';

# sendmailの -fコマンドが必要な場合
# 0=no 1=yes
$cf{sendm_f} = 0;

# ユーザ登録アクセス制限（半角スペースで区切る）
#  → 拒否するホスト名又はIPアドレスを記述
#  → 記述例 $deny = '.anonymizer.com 211.154.120.';
$cf{denyhost} = '';

# １回当りの最大投稿サイズ (bytes)
$cf{maxdata} = 51200;

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
	my ($buf,%in);
	if ($ENV{REQUEST_METHOD} eq "POST") {
		&error('受理できません') if ($ENV{CONTENT_LENGTH} > $cf{maxdata});
		read(STDIN, $buf, $ENV{CONTENT_LENGTH});
	} else {
		$buf = $ENV{QUERY_STRING};
	}
	foreach ( split(/&/, $buf) ) {
		my ($key,$val) = split(/=/);
		$key =~ tr/+/ /;
		$key =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# 無効化
		$key =~ s/[<>"'&\r\n]//g;
		$val =~ s/&/&amp;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/'/&#39;/g;
		$val =~ s/\r\n/<br>/g;
		$val =~ s/\n/<br>/g;
		$val =~ s/\r/<br>/g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	return %in;
}

#-----------------------------------------------------------
#  crypt暗号
#-----------------------------------------------------------
sub encrypt {
	my $in = shift;

	my @wd = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	my $salt = $wd[int(rand(@wd))] . $wd[int(rand(@wd))];
#	crypt($in, $salt) || crypt ($in, '$1$' . $salt); MD5暗号化を優先 2020/02/05
	crypt ($in, '$1$' . $salt) || crypt($in, $salt);
}

#-----------------------------------------------------------
#  crypt照合
#-----------------------------------------------------------
sub decrypt {
	my ($in, $dec) = @_;

	my $salt = $dec =~ /^\$1\$(.*)\$/ ? $1 : substr($dec, 0, 2);
#	if (crypt($in, $salt) eq $dec || crypt($in, '$1$' . $salt) eq $dec) {
	if (crypt($in, '$1$' . $salt) eq $dec || crypt($in, $salt) eq $dec) {
		return 1;
	} else {
		return 0;
	}
}

#-----------------------------------------------------------
#  時間取得
#-----------------------------------------------------------
sub get_time {
	# タイムゾーン設定
	$ENV{TZ} = "JST-9";

	my ($min,$hour,$mday,$mon,$year) = (localtime(time))[1..5];
	sprintf("%04d/%02d/%02d-%02d:%02d",	$year+1900,$mon+1,$mday,$hour,$min);
}


1;

