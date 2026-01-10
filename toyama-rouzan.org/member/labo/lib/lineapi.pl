#┌─────────────────────────────────
#│ LINE APIモジュール : lineapi.pl - 2021/07/04
#│ Copyright (c) Keiichi Yoshioka
#│
#│2024/12/19:LINE Notifyのサービス終了にともない、
#│           代替手段としてLINE公式アカウントとLine Messaging APIを使ったトークルーム送信
#│           line_BusinessAccount_push_message()を追加
#└─────────────────────────────────

use strict;
use warnings;
use lib "./lib";
use LWP::UserAgent;
use Encode;
use JSON::XS;
use URI::Escape;

#LINE Notify APIのURI
my $LINE_NOTIFY_API_URI= 'https://notify-api.line.me/api/notify';

#LINE MessagingAPIのpushコマンドのURI
my $LINE_MESSAGING_API_PUSH_URI = 'https://api.line.me/v2/bot/message/push';


#-----------------------------------------------------------
#  メッセージをトークルームに送信する
# $token : トークルームに対応するアクセストークン
# $message : メッセージ本文(Shift-JIS)
#
# return LINE APIが返すstatus code
#             200: 成功
#             400: リクエストが不正
#             401: アクセストークンが無効
#             500: サーバ内エラーにより失敗
#-----------------------------------------------------------
sub line_push_message {
	my ($token,$message) = @_;

	$message = decode('Shift_JIS', $message);
	$message = encode('UTF-8', $message);

	my $ua = LWP::UserAgent->new;
	my $res = $ua->post(
		$LINE_NOTIFY_API_URI,
		{ message => $message },
		Authorization => "Bearer $token", 
	);
	return $res->code;
}

#-----------------------------------------------------------
#  メッセージをLINE公式アカウント経由でトークルームに送信する
# $channelAccessToken : LINE公式アカウントのチャネルアクセストークン
#                       LINE Developersサイトの公式アカウントごとの設定画面のMessagin APIタブから取得する
# $groupId : トークルームのID
#            メッセージを送信したいトークルームにLINE公式アカウントを招待すると
#            LINE公式アカウントであらかじめ設定したWebHookが呼び出されるので
#            WebHookに登録したプログラムに渡された引数(JSON)を参照するとトークルームのIDが書いてある
# $message : メッセージ本文(Shift-JIS)
#
# return LINE MessagingAPIが返すstatus code
#             200: 成功
#             400: リクエストが不正
#             401: アクセストークンが無効
#             500: サーバ内エラーにより失敗
#-----------------------------------------------------------
sub line_BusinessAccount_push_message {
	my ($channelAccessToken,$groupId,$message) = @_;
   
	my $message_text = decode('Shift_JIS', $message);

	my $message_packet = {
	    to => $groupId,
	    messages => [
	        {
	            type => 'text',
	            text => $message_text
	        }
	    ]
	};

	# HTTPヘッダを設定
	my $headers = [
	    'Content-Type' => 'application/json',
	    'Authorization' => 'Bearer ' . $channelAccessToken
	];

	# UserAgentを作成
	my $ua = LWP::UserAgent->new;

	# JSON::XSでエンコード
	my $json = JSON::XS->new->utf8->encode($message_packet);

	# POSTリクエストを作成
	my $req = HTTP::Request->new(POST => $LINE_MESSAGING_API_PUSH_URI);
	$req->header(@$headers);
	$req->content($json);

	# リクエストを送信
	my $res = $ua->request($req);

	return $res->code;
}

1;
