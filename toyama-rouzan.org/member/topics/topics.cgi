#!/usr/bin/perl

#┌─────────────────────────────────
#│ TOPICS BOARD : topics.cgi - 2013/06/02
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);
use lib "./lib";
use CGI::Minimal;

# 設定ファイル認識
require "./init.cgi";
my %cf = init();

# データ受理
CGI::Minimal::max_read_size($cf{maxdata});
my $cgi = CGI::Minimal->new;
error('容量オーバー') if ($cgi->truncated);
my %in = parse_form($cgi);

# 処理分岐
if ($in{mode} eq 'find') { find_log(); }
bbs_list();

#-----------------------------------------------------------
#  記事表示
#-----------------------------------------------------------
sub bbs_list {
	# ページ数
	my $pg = $in{pg} || 0;

	# データ認識
	my ($i,@log);
	open(IN,"$cf{logfile}") or error("open err: $cf{logfile}");
	while(<IN>) {
		$i++;
		next if ($i < $pg + 1);
		next if ($i > $pg + $cf{pg_max});

		push(@log,$_);
	}
	close(IN);

	# 繰越ボタン作成
	my $pg_btn = make_pgbtn($i,$pg);

	# テンプレート読み込み
	open(IN,"$cf{tmpldir}/bbs.html") or error("open err: bbs.html");
	my $tmpl = join('', <IN>);
	close(IN);

	# テンプレート分割
	my ($head,$loop,$foot) = $tmpl =~ /(.+)<!-- loop_begin -->(.+)<!-- loop_end -->(.+)/s
			? ($1,$2,$3) : error("テンプレート不正");

	# 文字置換
	for ($head, $foot) {
		s/!bbs_title!/$cf{bbs_title}/g;
		s/!([a-z]+_cgi)!/$cf{$1}/g;
		s/!page_btn!/$pg_btn/g;
		s/!homepage!/$cf{homepage}/g;
	}

	# ヘッダ表示
	print "Content-type: text/html; charset=shift_jis\n\n";
	print $head;

	# 記事展開
	foreach (@log) {
		my ($no,$date,$sub,$com,$e1,$w1,$h1,$e2,$w2,$h2,$e3,$w3,$h3,$tag,$att,$tube) = split(/<>/);
		if ($tag == 1) {
			$com = tag($com);
			$com =~ s/\t/\n/g;
		} elsif ($cf{autolink}) {
			$com = auto_link($com);
			$com =~ s/\t/<br>/g;
		}

		# YouTube
		my $clip;
		if ($att eq 't') {
			$clip = tag($tube) if ($tube);

		# UPファイル
		} else {
			$clip = attach($no,$e1,$w1,$h1,$e2,$w2,$h2,$e3,$w3,$h3);
		}
		$clip &&= "<p>$clip</p>";

		# 文字置換
		my $tmp = $loop;
		$tmp =~ s/!date!/$date/g;
		$tmp =~ s/!subject!/$sub/g;
		$tmp =~ s/!comment!/$com/g;
		$tmp =~ s/<!-- clip -->/$clip/g;
		print $tmp;
	}

	# フッタ
	footer($foot);
}

#-----------------------------------------------------------
#  ワード検索
#-----------------------------------------------------------
sub find_log {
	# 条件
	$in{cond} =~ s/\D//g;

	# 検索条件プルダウン
	my %op = (1 => 'AND', 0 => 'OR');
	my $op_cond;
	foreach (1,0) {
		if ($in{cond} eq $_) {
			$op_cond .= qq|<option value="$_" selected>$op{$_}\n|;
		} else {
			$op_cond .= qq|<option value="$_">$op{$_}\n|;
		}
	}

	# 検索実行
	my @log = search($in{word},$in{cond}) if ($in{word} ne '');

	# テンプレート
	open(IN,"$cf{tmpldir}/find.html") or error("open err: find.html");
	my $tmpl = join('', <IN>);
	close(IN);

	# テンプレート分割
	my ($head,$loop,$foot) = $tmpl =~ /(.+)<!-- loop_begin -->(.+)<!-- loop_end -->(.+)/s
			? ($1,$2,$3) : error("テンプレート不正");

	for ($head, $foot) {
		s/!bbs_cgi!/$cf{bbs_cgi}/g;
		s/<!-- op_cond -->/$op_cond/;
		s/!word!/$in{word}/;
	}

	# ヘッダ部
	print "Content-type: text/html; charset=shift_jis\n\n";
	print $head;

	# ループ部
	foreach (@log) {
		my ($no,$date,$sub,$com,$e1,$w1,$h1,$e2,$w2,$h2,$e3,$w3,$h3,$tag,$att,$tube) = split(/<>/);
		if ($tag == 1) {
			$com = tag($com);
		} elsif ($cf{autolink}) {
			$com = auto_link($com);
		}

		# YouTube
		my $clip;
		if ($att eq 't') {
			$clip = tag($tube) if ($tube);

		# UPファイル
		} else {
			$clip = attach($no,$e1,$w1,$h1,$e2,$w2,$h2,$e3,$w3,$h3);
		}
		$clip &&= "<p>$clip</p>";

		my $tmp = $loop;
		$tmp =~ s/!subject!/$sub/g;
		$tmp =~ s/!date!/$date/g;
		$tmp =~ s/!comment!/$com/g;
		$tmp =~ s/<!-- clip -->/$clip/g;
		print $tmp;
	}

	# フッタ部
	footer($foot);
}

#-----------------------------------------------------------
#  検索実行
#-----------------------------------------------------------
sub search {
	my ($word,$cond) = @_;

	# コード変換
	if ($cf{conv_code} == 1) {
		require './lib/Jcode.pm';
		$in{word} = Jcode->new($in{word})->sjis;
	}

	# キーワードを配列化
	$word =~ s/　/ /g;
	my @wd = split(/\s+/,$word);

	# キーワード検索準備（Shift-JIS定義）
	my $ascii = '[\x00-\x7F]';
	my $hanka = '[\xA1-\xDF]';
	my $kanji = '[\x81-\x9F\xE0-\xFC][\x40-\x7E\x80-\xFC]';

	# 検索処理
	my @log;
	open(IN,"$cf{logfile}") or error("open err: $cf{logfile}");
	while (<IN>) {
		my ($no,$date,$nam,$eml,$sub,$com,$url,$hos,$pw,$tim) = split(/<>/);

		my $flg;
		foreach my $wd (@wd) {
			if ("$nam $eml $sub $com $url" =~ /^(?:$ascii|$hanka|$kanji)*?\Q$wd\E/i) {
				$flg++;
				if ($cond == 0) { last; }
			} else {
				if ($cond == 1) { $flg = 0; last; }
			}
		}
		next if (!$flg);

		push(@log,$_);
	}
	close(IN);

	# 検索結果
	return @log;
}

#-----------------------------------------------------------
#  ページ繰越ボタン作成
#-----------------------------------------------------------
sub make_pgbtn {
	my ($i,$pg) = @_;

	# ページ繰越定義
	my $next = $pg + $cf{pg_max};
	my $back = $pg - $cf{pg_max};

	# ページ繰越ボタン作成
	my @pg;
	if ($back >= 0 || $next < $i) {
		my $flg;
		my ($w,$x,$y,$z) = (0,1,0,$i);
		while ($z > 0) {
			if ($pg == $y) {
				$flg++;
				push(@pg,qq!<span class="pg-on"><b>$x</b></span>\n!);
			} else {
				push(@pg,qq!<span class="pg-off"><a href="$cf{bbs_cgi}?pg=$y">$x</a></span>\n!);
			}
			$x++;
			$y += $cf{pg_max};
			$z -= $cf{pg_max};

			if ($flg) { $w++; }
			last if ($w >= 5 && @pg >= 10);
		}
	}
	while( @pg >= 11 ) { shift(@pg); }
	my $ret = join('', @pg);
	if ($back >= 0) {
		$ret = qq!<span class="pg-off"><a href="$cf{bbs_cgi}?pg=$back">&lt;</a></span>\n! . $ret;
	}
	if ($next < $i) {
		$ret .= qq!<span class="pg-off"><a href="$cf{bbs_cgi}?pg=$next">&gt;</a></span>\n!;
	}
	$ret;
}

#-----------------------------------------------------------
#  フッター
#-----------------------------------------------------------
sub footer {
	my $foot = shift;

	# 著作権表記（削除・改変禁止）
	my $copy = <<EOM;
<p style="margin-top:2em;text-align:center;font-family:Verdana,Helvetica,Arial;font-size:10px;">
- <a href="http://www.kent-web.com/" target="_top">Topics Board</a> -
</p>
EOM

	if ($foot =~ /(.+)(<\/body[^>]*>.*)/si) {
		print "$1$copy$2\n";
	} else {
		print "$foot$copy\n";
		print "</body></html>\n";
	}
	exit;
}

#-----------------------------------------------------------
#  自動リンク
#-----------------------------------------------------------
sub auto_link {
	my $text = shift;

	$text =~ s/(s?https?:\/\/([\w-.!~*'();\/?:\@=+\$,%#]|&amp;)+)/<a href="$1" target="_blank">$1<\/a>/g;
	return $text;
}

#-----------------------------------------------------------
#  タグ復元
#-----------------------------------------------------------
sub tag {
	local($_) = @_;

	# 変換
	s/&lt;/</g;
	s/&gt;/>/g;
	s/&amp;/&/g;
	s/&quot;/"/g;
	$_;
}

#-----------------------------------------------------------
#  添付表示
#-----------------------------------------------------------
sub attach {
	my $no = shift;
	my (%e,%w,%h);
	($e{1},$w{1},$h{1},$e{2},$w{2},$h{2},$e{3},$w{3},$h{3}) = @_;

	my $ret;
	foreach my $i (1 .. 3) {
		next if (!$e{$i});

		# 画像以外の場合
		if ($e{$i} !~ /^\.(jpg|gif|png)$/) {
			my $size = -s "$cf{imgdir}/$no-$i$e{$i}";
			$size = int(($size / 1024) + 0.5) . 'KB';
			$ret .= qq|[添付]: <a href="$cf{imgurl}/$no-$i$e{$i}" target="_blank">$no-$i$e{$i}</a> ($size)\n|;

		# 画像の場合
		} elsif (-f "$cf{imgdir}/$no-s-$i$e{$i}") {
			$ret .= qq|<a href="$cf{imgurl}/$no-$i$e{$i}" target="_blank"><img src="$cf{imgurl}/$no-s-$i$e{$i}" class="img"></a>|;

		} else {
			my ($w,$h) = resize($w{$i},$h{$i});
			$ret .= qq|<a href="$cf{imgurl}/$no-$i$e{$i}" target="_blank"><img src="$cf{imgurl}/$no-$i$e{$i}" width="$w" height="$h" class="img"></a>|;
		}
	}
	return $ret;
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

