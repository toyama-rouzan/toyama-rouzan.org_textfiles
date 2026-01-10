#!/usr/bin/perl



# フルパス
eval{ $path1 = `pwd`; };
if ($@ || !$path1) { $path1 = 'error'; }

print "Content-type: text/html\n\n";
print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<title>$ver</title></head>
<body bgcolor="#FFFFFF" text="#000000">
<h3>この「ディレクトリ」のフルパスは以下のとおりです。</h3>

<P>
<DL>
<DT>サーバー内フルパス
<DD><font color="#0000A0" size="+1"><tt>$path1</tt></font><br><br>

</div>
</body>
</html>
EOM

exit;






