#!/usr/bin/perl

#API実装モジュール化版

use strict;
use CGI::Carp qw(fatalsToBrowser);
use warnings;
use lib "./lib";

require './lib/lineapi.pl';

# LINE公式アカウントのアクセストークンを設定

#AccessToken:富山勤労者山岳会 イベント案内
my $access_token = 'NFR4a4n1jRObTVpKbHs+WXbmETIdDJkprbAU2jVSKXjXCAPZ4dpU8W6Rxon9kwyxzLljyIWBVtFGDpC/wssxYr2KqcCa05c7j7bE0Vne34WvASNembW41KS44uWg2X43UXZ4uhdupyjs/oa6u8ybzAdB04t89/1O/w1cDnyilFU=';

# AccessToken:富山勤労者山岳会 事務局
#my $access_token = '3y5GFJZdOZOcPrDFT7FV02cx14XDBm9/GoDV9qKmE3QKSVt+Mat5BDbPZdUQbLzDQWlTxMc/MGwkkKcNdITWxhhPzhu57GsoxG4ia4qu7hvMAvtMpNV4wkg3yBAb+DFPuKSrDs5t36SP7o9CdHD9rwdB04t89/1O/w1cDnyilFU=';


# グループIDを設定
#GroupID:よしおかけい:第1実験室
#my $group_id = 'Cec27d2bf38acb6ab1a89e87ea0bde1db';

#GroupID:富山労山おむすび会
my $group_id = 'C5a2397090383e4bd01a4098bf3139622';

# 送信するメッセージを設定

my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime;
my $message = "LINE Messaging APIテストメッセージ($hour:$min $sec)";

my $result = line_BusinessAccount_push_message($access_token,$group_id,$message);


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

print "result status:$result";


print <<EOM;
</pre>
</body>
</html>
EOM

exit;

