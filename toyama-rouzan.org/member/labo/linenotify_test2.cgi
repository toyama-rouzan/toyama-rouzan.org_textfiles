#!/usr/bin/perl


use strict;
use CGI::Carp qw(fatalsToBrowser);
use warnings;
use Encode;


print <<EOM;
Content-type: text/html; charset=shift_jis

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>LINE notify test 2</title>
</head>
<body>
<pre>
EOM


print <<EOM;
</pre>
</body>
</html>
EOM

exit;

