#!/usr/bin/perl

#┌─────────────────────────────────
#│ Web Forum v4.07 <wf_admin.cgi> (2002/09/27)
#│ Copyright(C) KENT WEB 2002
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#============#
#  設定項目  #
#============#

# 外部ファイル取り込み
require './jcode.pl';
require './wf_init.cgi';

# パスワード (半角英数字で)
$pass = '0915';

#============#
#  設定完了  #
#============#

&decode;
if ($in{'pass'} eq "") { &enter; }
elsif ($mode eq "edit" && $in{'no'}) { &edit; }
elsif ($mode eq "edit2" && $in{'no'}) { &edit2; }
elsif ($mode eq "del" && $in{'no'}) { &del; }
&loglist;

#----------------#
#  ログ閲覧画面  #
#----------------#
sub loglist {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya);

	if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	&header;
	print <<"EOM";
[<a href="$script">戻る</a>]
<UL>
<LI>ツリーの先頭記事を削除すると、ツリーごと一括削除されます。
<form action="$admin" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<select name=mode>
<option value="edit">修正
<option value="del">削除</select>
<input type=submit value="送信する">
</UL>
<DL>
EOM
	$x=0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya) = split(/<>/);
		if ($lx) { $sp="&nbsp;&nbsp;&nbsp;" x $lx; } else { $sp=""; }
		$msg =~ s/<br>/ /g;
		$msg =~ s/</&lt;/g;
		$msg =~ s/>/&gt;/g;
		if (length($msg) > 60) { $msg = substr($msg,0,58); $msg .= '..'; }

		print "<DT>";
		print "<hr>" if ($no == $oya);
		print "$sp<input type=radio name=no value=\"$no\"> <b>$sub</b> ",
		"- <B>$nam</B> $dat ($ho) <font color=green>No\.$no</font>\n";
		"<DD>$sp<span style='font-size:8pt'>$msg</span>\n";

	}
	close(IN);
	print "<DT><hr></DL></form>\n", "</body></html>\n";
	exit;
}

#----------------#
#  記事編集画面  #
#----------------#
sub edit {
	local($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml);

	if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	# ログを開く
	open(IN,"$logfile") || &error("Can't open $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml) = split(/<>/);
		last if ($in{'no'} == $no);
	}
	close(IN);

	$msg =~ s/<br>/\r/g;

	# 編集フォームを出力
	&header;
	print <<"EOM";
[<a href="javascript:history.back()">戻る</a>]
<UL>
<LI>変更したい部分のみ修正し、「送信する」を押してください。
<form action="$admin" method=POST>
<input type=hidden name=mode value="edit2">
<input type=hidden name=no value="$in{'no'}">
<input type=hidden name=pass value="$in{'pass'}">
<table border=0>
<tr>
  <td><B>投稿者</B></td>
  <td><input type=text name=name value="$nam" size=28></td>
</tr>
<tr>
  <td><B>Ｅメール</B></td>
  <td><input type=text name=email value="$eml" size=28>
	<select name=smail>
EOM
	@sm = ('表示', '非表示');
	foreach (0, 1) {
		if ($sml == $_) {
			print "<option value=\"$_\" selected>$sm[$_]\n";
		} else {
			print "<option value=\"$_\">$sm[$_]\n";
		}
	}

	print <<"EOM";
</select></td>
</tr>
<tr>
  <td><B>タイトル</B></td>
  <td><input type=text name=sub value="$sub" size=38></td>
</tr>
<tr>
  <td colspan=2><B>メッセージ</B>
EOM
	@w1 = ('手動改行', '強制改行', '図表モード');
	@w2 = ('soft', 'hard', 'pre');
	foreach (0 .. 2) {
		if ($wr eq $w2[$_]) {
			print "<input type=radio name=wrap value=\"$w2[$_]\" checked>$w1[$_]\n";
		} else {
			print "<input type=radio name=wrap value=\"$w2[$_]\">$w1[$_]\n";
		}
	}

	print <<"EOM";
<br><textarea name=message cols=64 rows=10 wrap=soft>$msg</textarea></td>
</tr>
<tr>
  <td><B>ＵＲＬ</B></td>
  <td><input type=text name=url value="http://$url" size=55></td>
</tr>
</table>
<input type=submit value=" 送信する "><input type=reset value="リセット">
</form>
</UL>
</body>
</html>
EOM
	exit;
}

#----------------#
#  記事編集処理  #
#----------------#
sub edit2 {
	local($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml,$res);

	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	$in{'url'} =~ s/^http\:\/\///;

	# ロック開始
	&lock if ($lockkey);

	# ログを開く
	@new=();
	open(IN,"$logfile") || &error("Open Error : $logfile");
	while (<IN>) {
		chop;
		($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml,$res) = split(/<>/);
		if ($in{'no'} == $no) {
			$_ = "$no<>$re<>$x<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$dat<>$in{'message'}<>$t<>$ho<>$pw<>$in{'wrap'}<>$oya<>$in{'smail'}<>$res<>";
		}
		push(@new,"$_\n");
	}
	close(IN);

	# ログを更新
	unshift(@new,$top);
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# ロック解除
	&unlock if ($lockkey);

	# 初期画面に戻る
	&loglist;
}

#----------------#
#  記事削除処理  #
#----------------#
sub del {
	local($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya);

	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	# ロック開始
	&lock if ($lockkey);

	# ログを開く
	$flag=0;
	@new=();
	open(IN,"$logfile") || &error("Open Error : $logfile","LK");
	$top = <IN>;
	while (<IN>) {
		($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya) = split(/<>/);

		if ($in{'no'} == $no) {
			# 親記事
			if ($no == $oya) {
				$flag=1;
				next;
			# レス記事
			} else {
				next;
			}
		}
		if ($flag && $in{'no'} == $oya) { next; }
		push(@new,$_);
	}
	close(IN);

	# ログを更新
	unshift(@new,$top);
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# ロック解除
	&unlock if ($lockkey);

	# 初期画面に戻る
	&loglist;
}

#------------#
#  入室画面  #
#------------#
sub enter {
	&header;
	print <<"EOM";
<div align="center">
<h4>パスワードを入力してください</h4>
<form action="$admin" method="POST">
<input type=password name=pass size=8>
<input type=submit value=" 認証 "></form>
</div><!-- $ver -->
</body>
</html>
EOM
	exit;
}

__END__

