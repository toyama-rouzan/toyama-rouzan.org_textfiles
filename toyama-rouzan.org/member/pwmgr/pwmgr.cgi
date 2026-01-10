#!/usr/bin/perl

#┌─────────────────────────────────
#│ PasswordManager : pwmgr.cgi - 2013/01/30
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);
use lib "./lib";
use Jcode;

# 設定ファイル認識
require "./init.cgi";
my %cf = &init;

# データ受理
my %in = &parse_form;

# 条件分岐
if ($in{mode} eq "new_user") { &new_user; }
if ($in{mode} eq "chg_user") { &chg_user; }
if ($in{mode} eq "del_user") { &del_user; }
&error("不明なアクセスです");

#-----------------------------------------------------------
#  ユーザ登録
#-----------------------------------------------------------
sub new_user {
	# 発行制限確認
	if ($cf{pwd_regist} > 1) { &error("不正なアクセスです"); }

	# ホスト名を取得
	my $host = &get_host;

	# 入力チェック
	my $err;
	if ($in{name} eq "") { $err .= "名前が入力モレです<br>"; }
	if ($in{eml1} ne $in{eml2}) { $err .= "メールの再度入力が異なります<br>"; }
	if ($in{eml1} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		$err .= "メールの入力内容が不正です<br>";
	}
	if (length($in{id}) < 4 || length($in{id}) > 8) {
		$err .= "ログインIDは4～8文字で入力してください<br>";
	}
	if ($in{id} =~ /\W/) {
		$err .= "ログインIDに英数字以外の文字が含まれています<br>";
	}
	&error($err) if ($err);

	# 不要改行カット
	$in{name} =~ s/<br>//g;

	# IDの重複チェック
	my ($flg,@data);
	open(DAT,"+< $cf{pwdfile}") or &error("open err: $cf{pwdfile}");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		my ($id,$pw) = split(/:/);

		if ($in{id} eq $id) {
			$flg++;
			last;
		}
		push(@data,$_);
	}

	# 重複あり
	if ($flg) {
		close(DAT);
		&error("$in{id}は既に発行済です。他のID名をご指定ください");
	}

	# パスワード発行
	my @wd = (0 .. 9, 'a' .. 'z', 'A' .. 'Z');
	my $pwd;
	srand;
	for (1 .. 8) {
		$pwd .= $wd[int(rand(@wd))];
	}

	# 暗号化
	my $crypt = &encrypt($pwd);

	# 更新
	seek(DAT, 0, 0);
	print DAT @data;
	print DAT "$in{id}:$crypt\n";
	truncate(DAT, tell(DAT));
	close(DAT);

	# 会員ファイル
	open(DAT,">> $cf{memfile}") or &error("write err: $cf{memfile}");
	eval "flock(DAT, 2);";
	print DAT "$in{id}<>$in{name}<>$in{eml1}<><>\n";
	close(DAT);

	# 時間取得
	my $date = &get_time;

	# メール本文読み込み
	open(IN,"$cf{tmpldir}/mail.txt") or &error("open err: mail.txt");
	my $mbody = join('', <IN>);
	close(IN);

	# 文字置き換え
	$mbody =~ s/!name!/$in{name}/g;
	$mbody =~ s/!date!/$date/g;
	$mbody =~ s/!host!/$host/g;
	$mbody =~ s/!email!/$in{eml1}/g;
	$mbody =~ s/!id!/$in{id}/g;
	$mbody =~ s/!pw!/$pwd/g;

	# 本文コード変換
	$mbody = Jcode->new($mbody,'sjis')->jis;

	# 件名BASE64化
	my $msub = Jcode->new("登録の案内",'sjis')->mime_encode;

	# sendmailコマンド
	my $scmd = "$cf{sendmail} -t -i";
	if ($cf{sendm_f}) {
		$scmd .= " -f $in{master}";
	}

	# sendmail送信
	open(MAIL,"| $scmd") or &error("メール送信失敗");
	print MAIL "To: $in{eml1}\n";
	print MAIL "From: $cf{master}\n";
	print MAIL "Cc: $cf{master}\n";
	print MAIL "Subject: $msub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $cf{version}\n\n";
	print MAIL "$mbody\n";
	close(MAIL);

	# 完了メッセージ
	my $ttl = "ご登録ありがとうございました。";
	my $msg = "ログインIDとパスワード情報は以下のアドレスへ送信しました。";
	$msg .= "<p><b>$in{eml1}</b></p>";
	&message($ttl, $msg);
}

#-----------------------------------------------------------
#  パスワード変更
#-----------------------------------------------------------
sub chg_user {
	# 発行制限
	if ($cf{pwd_regist} > 2) { &error("不正なアクセスです"); }

	# ホスト名を取得
	my $host = &get_host;

	# チェック
	my $err;
	if ($in{id} eq "") { $err .= "ログインIDが入力モレです<br>"; }
	if ($in{pw} eq "") { $err .= "旧パスワードが入力モレです<br>"; }
	if ($in{pw1} eq "") { $err .= "新パスワードが入力モレです<br>"; }
	if ($in{pw1} ne $in{pw2}) {	$err .= "新パスワードで再度入力分が異なります<br>";	}
	&error($err) if ($err);

	# 暗号化
	my $newpw = &encrypt($in{pw1});

	# IDチェック
	my ($flg, $crypt, @new);
	open(DAT,"+< $cf{pwdfile}") or &error("open err: $cf{pwdfile}");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		my ($id,$pw) = split(/:/);

		if ($in{id} eq $id) {
			$flg = 1;
			$crypt = $pw;
			$_ = "$id:$newpw\n";
		}
		push(@new,$_);
	}

	if (!$flg) {
		close(DAT);
		&error("ログインID ($in{id}) は存在しません");
	}

	# 照合
	chomp($crypt);
	if (&decrypt($in{pw}, $crypt) != 1) {
		close(DAT);
		&error("パスワードが違います");
	}

	# パスファイル更新
	seek(DAT, 0, 0);
	print DAT @new;
	truncate(DAT, tell(DAT));
	close(DAT);

	# 完了メッセージ
	my $ttl = "パスワード変更完了";
	my $msg = "ご利用をありがとうございました。";
	&message($ttl, $msg);
}

#-----------------------------------------------------------
#  ユーザ削除
#-----------------------------------------------------------
sub del_user {
	# 発行制限
	if ($cf{pwd_regist} > 2) { &error("不正なアクセスです"); }

	# ホスト名を取得
	my $host = &get_host;

	# チェック
	if ($in{id} eq "" || $in{pw} eq "") {
		&error("ID又はパスワードが入力モレです");
	}

	# IDチェック
	my ($flg, $crypt, @new);
	open(DAT,"+< $cf{pwdfile}") or &error("open err: $cf{pwdfile}");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		my ($id,$pw) = split(/:/);

		if ($in{id} eq $id) {
			$flg = 1;
			$crypt = $pw;
			next;
		}
		push(@new,$_) if ($in{job} eq "del");
	}

	if (!$flg) {
		close(DAT);
		&error("ログインID ($in{id}) は存在しません");
	}

	# 照合
	chomp($crypt);
	if (&decrypt($in{pw}, $crypt) != 1) {
		close(DAT);
		&error("パスワードが違います");
	}

	# 実行
	if ($in{job} eq "del") {

		# パスファイル更新
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# 会員ファイル
		my @file;
		open(DAT,"+< $cf{memfile}") or &error("open err: $cf{memfile}");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($id) = split(/<>/);
			next if ($in{id} eq $id);

			push(@file,$_);
		}
		seek(DAT, 0, 0);
		print DAT @file;
		truncate(DAT, tell(DAT));
		close(DAT);

		# 完了メッセージ
		my $ttl = "登録ID削除完了";
		my $msg = "これまでのご利用をありがとうございました。";
		&message($ttl, $msg);

	# 確認画面
	} else {
		&conf_del;
	}
}

#-----------------------------------------------------------
#  ホスト名取得
#-----------------------------------------------------------
sub get_host {
	my $host = $ENV{REMOTE_HOST};
	my $addr = $ENV{REMOTE_ADDR};

	if ($cf{gethostbyaddr} && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	$host ||= $addr;

	my $flg;
	foreach ( split(/\s+/, $cf{denyhost}) ) {
		if (index($host,$_) >= 0) { $flg = 1; last; }
	}
	if ($flg) { &error("現在登録休止中です"); }

	return $host;
}

#-----------------------------------------------------------
#  エラー処理
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
#  完了メッセージ
#-----------------------------------------------------------
sub message {
	my ($ttl,$msg) = @_;

	# テンプレート読み込み
	open(IN,"$cf{tmpldir}/message.html") or &error("open err: message.html");
	my $tmpl = join('', <IN>);
	close(IN);

	# 置き換え
	$tmpl =~ s/!title!/$ttl/g;
	$tmpl =~ s/!message!/$msg/g;
	$tmpl =~ s/!back_url!/$cf{back_url}/g;

	# 著作権表記（削除・改変禁止）
	my $copy = <<EOM;
<p align="center" style="margin-top:3em;font-size:10px;font-family:verdana,helvetica,arial,osaka;">
- <a href="http://www.kent-web.com/" target="_top">PasswordManager</a> -
</p>
EOM

	# 表示
	print "Content-type: text/html; charset=shift_jis\n\n";

	if ($tmpl =~ /(.+)(<\/body[^>]*>.*)/si) {
		print "$1$copy$2\n";
	} else {
		print "$tmpl$copy\n";
		print "</body></html>\n";
	}
	exit;
}

#-----------------------------------------------------------
#  削除確認画面
#-----------------------------------------------------------
sub conf_del {
	open(IN,"$cf{tmpldir}/conf.html") or &error("open err: conf.html");
	my $tmpl = join('', <IN>);
	close(IN);

	$tmpl =~ s/!id!/$in{id}/g;
	$tmpl =~ s/!pw!/$in{pw}/g;
	$tmpl =~ s/!(\w+_cgi)!/$cf{$1}/g;

	print "Content-type: text/html; charset=shift_jis\n\n";
	print $tmpl;
	exit;
}

