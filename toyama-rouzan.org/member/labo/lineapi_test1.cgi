#!/usr/bin/perl


use strict;
use warnings;
use LWP::UserAgent;
use JSON::XS;
use URI::Escape;
use Encode 'decode';

require './lib/lineapi.pl';

# LINEのアクセストークンを設定(LINE公式アカウント:富山勤労者山岳会 イベント案内)
my $access_token = 'NFR4a4n1jRObTVpKbHs+WXbmETIdDJkprbAU2jVSKXjXCAPZ4dpU8W6Rxon9kwyxzLljyIWBVtFGDpC/wssxYr2KqcCa05c7j7bE0Vne34WvASNembW41KS44uWg2X43UXZ4uhdupyjs/oa6u8ybzAdB04t89/1O/w1cDnyilFU=';

# LINEのエンドポイントURLを設定
my $url = 'https://api.line.me/v2/bot/message/push';

# グループIDを設定(よしおかけい:第1実験室)
my $group_id = 'Cec27d2bf38acb6ab1a89e87ea0bde1db';

# 送信するメッセージを設定

my $message_text='こんにちは、これはグループトークへのメッセージです！';
   $message_text = decode('Shift_JIS', $message_text);

my $message = {
    to => $group_id,
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
    'Authorization' => 'Bearer ' . $access_token
];

# UserAgentを作成
my $ua = LWP::UserAgent->new;

# JSON::XSでエンコード
my $json = JSON::XS->new->utf8->encode($message);

# POSTリクエストを作成
my $req = HTTP::Request->new(POST => $url);
$req->header(@$headers);
$req->content($json);

# リクエストを送信
my $res = $ua->request($req);


print <<EOM;
Content-type: text/html; charset=shift_jis

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>LINE Messaging API test</title>
</head>
<body>
<pre>
EOM

if ($res->is_success) {
    print "メッセージがグループに送信されました！\n";
} else {
    print "エラーが発生しました: " . $res->status_line . "\n";
}

print <<EOM;
</pre>
</body>
</html>
EOM

exit;

