#!/usr/bin/perl

#┌─────────────────────────────────
#│ Web Forum v4.07 <wf_regi.cgi> (2002/09/27)
#│ Copyright(C) KENT WEB 2002
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#------------#
#  基本設定  #
#------------#

# 外部ファイル取り込み
require './jcode.pl';
require './fold.pl';
require './wf_init.cgi';

#------------#
#  設定完了  #
#------------#

&decode;
&axs_check;
if ($mode eq "regist") { &regist; }
elsif ($mode eq "form" && $in{'pview'} ne "on") { &regist; }
elsif ($mode eq "form" && $in{'pview'} eq "on") { &preview; }
&error('不明な処理です');

#----------------#
#  書き込み処理  #
#----------------#
sub regist {
	local($count,$ango,$date);

	# 入力チェック
	&chk_form;

	# ロック処理
	&lock if ($lockkey);

	# ログファイル読み込み
	open(IN,"$logfile") || &error("Open Error : $logfile");
	@lines = <IN>;
	close(IN);

	# カウントファイルをアップ
	$count = shift(@lines);
	$count =~ s/\n//;
	if ($count % 9999) { $count++; } else { $count=1; }

	# 二重投稿の禁止
	$flag=0;
	foreach (@lines) {
		local(@f) = split(/<>/);
		if ($in{'name'} eq $f[6] && $in{'message'} eq $f[8]) { $flag=1; last; }
	}
	if ($flag) { &error("二重投稿は禁止です"); }

	# クッキーを発行
	&set_cookie;

	# パスワード暗号化
	if ($in{'pwd'} ne "") { $ango = &encrypt($in{'pwd'}); }

	# 時間を取得
	$times = time;
	$date = &get_time($times, "log");

	## --- 親記事の場合
	if ($in{'no'} eq 'new') {
		unshift (@lines,"$count<>no<>0<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$date<>$in{'message'}<>$times<>$host<>$ango<>$in{'wrap'}<>$count<>$in{'smail'}<>0<>\n");
		@new = @lines;
	}
	## --- レス記事の場合
	else {
		## ツリーソート「あり」
	 	if ($top_sort) {
			@new=();
			@tmp=();
			$flag=0;
			foreach (@lines) {
				chop;
				($no,$reno,$lx,$t,$e,$u,$n,$d,$m,$tm,$h,$a,$w,$OYA,$smail,$res) = split(/<>/);
				if ($bot_res && $flag == 1 && $lx2 > $lx && $OYA == $in{'oya'}) {
					$flag=2;
					push(@new,"$count<>$in{'no'}<>$lx2<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$date<>$in{'message'}<>$times<>$host<>$ango<>$in{'wrap'}<>$in{'oya'}<>$in{'smail'}<>0<>\n");
				}
				# 同一ツリーの記事を @new に配列分割（直レス）
				if ($no == $in{'no'}) {
					$res++;
					push(@new,"$no<>$reno<>$lx<>$t<>$e<>$u<>$n<>$d<>$m<>$tm<>$h<>$a<>$w<>$OYA<>$smail<>$res<>\n");
				}
				# 同一ツリーの記事を @new に配列分割
				elsif ($in{'oya'} == $OYA) { push(@new,"$_\n"); }
				# 別ツリーの記事を @tmp に配列分割
				else { push(@tmp,"$_\n"); }

				if ($no == $in{'no'}) {
					$flag=1;
					$lx2 = $lx + 1;
					if (!$bot_res) {
						push(@new,"$count<>$in{'no'}<>$lx2<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$date<>$in{'message'}<>$times<>$host<>$ango<>$in{'wrap'}<>$in{'oya'}<>$in{'smail'}<>0<>\n");
					}
				}
			}
			if ($bot_res && $flag != 2) {
				push(@new,"$count<>$in{'no'}<>$lx2<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$date<>$in{'message'}<>$times<>$host<>$ango<>$in{'wrap'}<>$in{'oya'}<>$in{'smail'}<>0<>\n");
			}
			# 配列最終結合
			push(@new,@tmp);
		}
		## ツリーソート「なし」
		else {
			@new=();
			$flag=0;
			foreach (@lines) {
				chop;
				($no,$reno,$lx,$t,$e,$u,$n,$d,$m,$tm,$h,$a,$w,$OYA,$smail,$res) = split(/<>/);
				if ($bot_res && $flag == 1 && $lx2 > $lx && ($reno ne $in{'no'} || $OYA != $in{'oya'})) {
					$flag=2;
					push(@new,"$count<>$in{'no'}<>$lx2<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$date<>$in{'message'}<>$times<>$host<>$ango<>$in{'wrap'}<>$in{'oya'}<>$in{'smail'}<>0<>\n");
				}

				# 直親記事
				if ($no == $in{'no'}) {
					$res++;
					push(@new,"$no<>$reno<>$lx<>$t<>$e<>$u<>$n<>$d<>$m<>$tm<>$h<>$a<>$w<>$OYA<>$smail<>$res<>\n");
				} else { push(@new,"$_\n"); }

				if ($no == $in{'no'}) {
					$flag=1;
       					$lx2 = $lx + 1;
					if (!$bot_res) {
       						push (@new,"$count<>$no<>$lx2<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$date<>$in{'message'}<>$times<>$host<>$ango<>$in{'wrap'}<>$in{'oya'}<>$in{'smail'}<>0<>\n");
					}
				}
			}
			if ($bot_res && $flag != 2) {
				push(@new,"$count<>$in{'no'}<>$lx2<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$date<>$in{'message'}<>$times<>$host<>$ango<>$in{'wrap'}<>$in{'oya'}<>$in{'smail'}<>0<>\n");
			}
	    	}
	}
	# 最大記事数処理
	@PAST=();
	if (@new > $max) {
		foreach (0 .. $#new) {
			# 最終尾ファイルを配列から抜き出し過去ログ配列へ
			local($p_file) = pop(@new);
			push(@PAST,$p_file) if ($pastkey);

			local($no,$reno,$lx) = split(/<>/, $p_file);
			if ($#new+1 <= $max && $reno eq 'no') {
				last;
			}
		}
	}
	# ログを更新
	unshift(@new,"$count\n");
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# 過去ログ処理
	if (@PAST) { &pastlog; }

	# ファイルロック解除
	&unlock if ($lockkey);

	# メール通知
	if ($mailing == 2) { &mail_to; }
	elsif ($mailing == 1 && $in{'email'} ne $mailto) { &mail_to; }

	# 投稿後画面
	&after;
}

#------------------#
#  プレビュー画面  #
#------------------#
sub preview {
	# 入力チェック
	&chk_form;

	if ($in{'smail'} == 1) { $email = '非表示'; }
	else { $email = $in{'email'}; }

	&header;
	print <<"EOM";
<font color="$t_color"><big><b>- 以下の内容でメッセージを投稿します -</b></big></font>
<form action="$regist" method="POST">
<input type=hidden name=mode value="regist">
<input type=hidden name=pwd value="$in{'pwd'}">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=email value="$in{'email'}">
<input type=hidden name=url value="$in{'url'}">
<input type=hidden name=sub value="$in{'sub'}">
<input type=hidden name=oya value="$in{'oya'}">
<input type=hidden name=pview value="$in{'pview'}">
<input type=hidden name=smail value="$in{'smail'}">
<input type=hidden name=page value="$page">
EOM
	if ($in{'action'} eq "res_msg") {
		print "<input type=hidden name=no value=\"$in{'no'}\">\n";
		print "<input type=hidden name=action value=\"res_msg\">\n";
	} else {
		print "<input type=hidden name=no value=\"new\">\n";
	}
	$in{'message'} =~ s/<br>/\r/g;
	if ($in{'url'}) { $in{'url'} = "http://$in{'url'}"; }

	print <<"EOM";
<table>
<tr>
  <td><b>タイトル</b></td>
  <td>： <font color="$sub_color"><B>$in{'sub'}</B></font></td>
</tr>
<tr>
  <td><b>投稿者</b></td>
  <td>： <B>$in{'name'}</B></td>
</tr>
<tr>
  <td><b>Ｅメール</b></td>
  <td>： $email</td>
</tr>
<tr>
  <td><b>URL</b></td>
  <td>： $in{'url'}</td>
</tr>
</table>
EOM
	@w1 = ('手動改行', '強制改行', '図表モード');
	@w2 = ('soft', 'hard', 'pre');
	foreach (0 .. 2) {
		if ($in{'wrap'} eq $w2[$_]) {
			print "<input type=radio name=wrap value=\"$w2[$_]\" checked>$w1[$_]\n";
		} else {
			print "<input type=radio name=wrap value=\"$w2[$_]\">$w1[$_]\n";
		}
	}

	print <<"EOM";
<br><textarea cols=62 rows=12 name=message wrap="soft">$in{'message'}</textarea>
<P><input type=submit value="メッセージを投稿する"></form>
<P>[<A HREF="javascript:history.back()">投稿フォームに戻る</A>]
</body>
</html>
EOM
	exit;
}

#------------------------#
#  書きこみ後メッセージ  #
#------------------------#
sub after {
	if ($in{'url'}) { $in{'url'} = "http://$in{'url'}"; }

	# ツリートップ移動処理の場合は書き込み後はトップページ
	if ($top_sort) { $page = 0; }

	# 引用色
	if ($refcolor) {
		$in{'message'} =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
	}

	# 図表モード
	if ($in{'wrap'} eq "pre") {
		$in{'message'} =~ s/<br>/\n/g;
		$in{'message'} = "<pre>$in{'message'}</pre>";
	}
	if ($in{'smail'} == 1) { $in{'email'} = '非表示'; }

	&header;
	print <<"EOM";
<center>
<b style="font-size:12pt;color:$sub_color">正常に書きこみが完了しました</b>
<P><table border=1 cellpadding=10 width="90%">
<tr><td bgcolor="$tbl_color">
<table>
<tr>
  <td>タイトル</td><td>： <b style="color:$sub_color">$in{'sub'}</b></td>
</tr>
<tr>
  <td>投稿者</td><td>： <b>$in{'name'}</b></td>
</tr>
<tr>
  <td>e-mail</td><td>： $in{'email'}</td>
</tr>
<tr>
  <td>参照先</td><td>： $in{'url'}</td>
</tr>
</table>
<br><br>
<blockquote>
$in{'message'}
</blockquote>
</td></tr></table>
<P><form action="$script" method="POST">
<input type=hidden name=page value="$page">
<input type=submit value="リストにもどる">
</form>
</center>
</body>
</html>
EOM
	exit;
}

#--------------#
#  メール送信  #
#--------------#
sub mail_to {
	local($msg, $date2, $mail_sub, $mail_body);

	# メールタイトル
	$mail_sub = "[$count] $in{'sub'}";

	# メール本文のタグ・改行を復元
	$msg = $in{'message'};
	$msg =~ s/<br>/\n/g;
	$msg =~ s/&lt;/</g;
	$msg =~ s/&gt;/>/g;
	$msg =~ s/&quot;/"/g;
	$msg =~ s/&amp;/&/g;

	if ($in{'url'}) { $in{'url'} = "http://$in{'url'}"; }
	$date2 = &get_time($times);

	# メール本文
	$mail_body = <<"EOM";
------------------------------------------------------------
投稿時間：$date2
ホスト名：$host
ブラウザ：$ENV{'HTTP_USER_AGENT'}

投稿者名：$in{'name'}
Ｅメール：$in{'email'}
タイトル：$in{'sub'}
ＵＲＬ  ：$in{'url'}
コメント：

$msg
------------------------------------------------------------
EOM
	# JISコード変換
	&jcode'convert(*mail_sub, 'jis', 'sjis');
	&jcode'convert(*mail_body, 'jis', 'sjis');

	# sendmail起動
	if ($in{'email'} eq "") { $in{'email'} = $mailto; }
	open(MAIL,"| $sendmail -t") || &error("メール送信に失敗しました");
	print MAIL "To: $mailto\n";
	print MAIL "From: $in{'email'}\n";
	print MAIL "Subject: $mail_sub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	print MAIL $mail_body;
	close(MAIL);
}

#------------------#
#  クッキーの発行  #
#------------------#
sub set_cookie {
	local($gmt, $cook, @t, @m, @w);
	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	$cook = "$in{'name'}<>$in{'email'}<>$in{'url'}<>$in{'pwd'}<>$in{'pview'}<>$in{'smail'}";
	print "Set-Cookie: WEBFORUM=$cook; expires=$gmt\n";
}

#----------------------#
#  パスワード暗号処理  #
#----------------------#
sub encrypt {
	local($inpw) = $_[0];
	local(@char, $salt, $encrypt);

	@char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $char[int(rand(@char))] . $char[int(rand(@char))];
	$encrypt = crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
	return $encrypt;
}

#----------------#
#  過去ログ生成  #
#----------------#
sub pastlog {
	local($past_flag)=0;

	# 過去ログファイルを定義
	open(NO,"$nofile") || &error("Open Error : $nofile");
	$num = <NO>;
	close(NO);
#	$num = sprintf("%04d", $num);
#	$pastfile = "$pastdir$num\.cgi";
	$pastfile = sprintf("%s%04d\.cgi", $pastdir,$num);

	# 過去ログを開く
	open(IN,"$pastfile") || &error("Open Error : $pastfile");
	@data = <IN>;
	close(IN);

	# 規定の行数をオーバーすると次ファイルを自動生成
	if ($#data > $max_line) {
		$past_flag=1;

		# カウントファイル更新
		$num++;
		open(NO,">$nofile") || &error("Write Error : $nofile");
		print NO $num;
		close(NO);
#		$num = sprintf("%04d", $num);
#		$pastfile = "$pastdir$num\.cgi";
		$pastfile = sprintf("%s%04d\.cgi", $pastdir,$num);
		@data=();
	}

	foreach (@PAST) { unshift(@data,$_); }

	# 過去ログを更新
	open(OUT,">$pastfile") || &error("Write Error : $pastfile");
	print OUT @data;
	close(OUT);

	if ($past_flag) { chmod(0666, $pastfile); }
}

__END__

