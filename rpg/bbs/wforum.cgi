#!/usr/bin/perl

#┌─────────────────────────────────
#│ Web Forum v4.07 <wforum.cgi> (2002/09/27)
#│ Copyright(C) KENT WEB 2002
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#============#
#  基本設定  #
#============#

# 外部ファイル取込み
require './jcode.pl';
require './fold.pl';
require './wf_init.cgi';

#============#
#  設定完了  #
#============#

# 基本処理を定義
&decode;
&axs_check;
if ($mode eq "msgview") { &msgview; }
elsif ($mode eq "allread") { &allread; }
elsif ($mode eq "newsort") { &newsort; }
elsif ($mode eq "usr_del") { &usr_del; }
elsif ($mode eq "usr_edt") { &usr_edt; }
elsif ($mode eq "find") { &find; }
elsif ($mode eq "past") { &past_view; }
elsif ($mode eq "check") { &check; }
&list_view;


#--------------#
#  リスト表示  #
#--------------#
sub list_view {
	&header;
	print "<div align=\"center\">\n";

	# タイトル部
	if ($t_img) {
		print "<img src=\"$t_img\" alt=\"$title\" width=\"$t_w\" height=\"$t_h\">\n";
	} else {
		print "<B style=\"font-size:$t_point;color:$t_color\">$title</B>\n";
	}

	print "<hr width='90%'>\n",
	"[<a href=\"$home\" target=\"_top\">もどる</a>]\n",
	"[<a href=\"#msg\">新規投稿</a>]\n";

	if ($in{'list'} ne "new") {
		print "[<a href=\"$script?list=new\">新規順表\示</a>]\n";
	} else {
		print "[<a href=\"$script?list=tree\">ツリー表\示</a>]\n";
	}
	print "[<a href=\"$script?mode=newsort&page=$page\">新着記事</a>]\n",
	"[<a href=\"$note\">留意事項</a>]\n",
	"[<a href=\"$script?mode=find&page=$page&list=$in{'list'}\">ワード検索</a>]\n";

	print "[<a href=\"$script?mode=past\">過去ログ</a>]\n" if ($pastkey);
#	print "[<a href=\"search/\">過去ログ</a>]\n";
	print "[<a href=\"$admin\">管理用</a>]\n",
	"<hr width='90%'><table><tr><td>\n",
	"<li>$new_time時間以内の記事は $newmark で表\示されます。</li><br>\n";

	if ($in{'list'} eq "new") {
		print "<li>以下は新規投稿順のリスト表\示です。</li><br>\n";
	} else {
		print "<li>ツリー先頭部の $treehead をクリックすると関連記事を一括表\示します。</li><br>\n";
	}
	print "</td></tr></table></div>\n";

	# ログを開く
	if ($in{'list'} eq "new") { &ListNewOpen; }
	else { &ListTreeOpen; }

	# ページ移動フォーム
	&move_list;

	# メッセージ投稿フォ－ムを表示
	&msg_form;

	# 著作権表示（削除しないで下さい）
	print "<P><div align='center' style='font-size:9pt'><!-- $ver -->\n",
	"- <a href='http://www.kent-web.com/' target='_top'>Web Forum</a> -\n",
	"</div>\n</body></html>\n";
	exit;
}

#--------------------#
#  リストツリー表示  #
#--------------------#
sub ListTreeOpen {
	local($no,$reno,$lx,$sub,$email,$url,$name,$dat,$msg,$t,$h,$pw,$w,$oya);

	# 時間取得
	$time = time;

	if ($mode ne "past") { print "<DL>\n"; }
	print "<UL>\n";

	$i=0;
	$x=0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	if ($mode ne "past") { $top = <IN>; }
	while (<IN>) {
		($no,$reno,$lx,$sub,$email,$url,$name,$dat,$msg,$t,$h,$pw,$w,$oya) = split(/<>/);
		if ($reno == 0) { $i++; }
		if ($i < $page + 1) { next; }
		if ($i > $page + $p_tree) { next; }

		while ($x > $lx) { print "</UL>\n"; $x--; }
		while ($x < $lx) { print "<UL>\n"; $x++; }

		if ($reno == 0) { while ($x > 0) { print "</UL>\n"; $x--; } }

		# 所定時間以内の投稿は[NEWマーク]表示
		if ($time - $t > $new_time * 3600) { $newsign = ""; }
		else { $newsign = $newmark; }

		# 記事タイトル長調整
		$sub = &cut_subject($sub);

		# 過去記事
		if ($mode eq "past") {
			print "<LI><a href=\"$script?mode=allread&pastlog=$in{'pastlog'}&no=$oya&page=$page&act=past\#$no\">$sub</a> - <b>$name</b> $dat <font color=\"$no_color\">No\.$no</font> $newsign\n";
		# 削除記事
		} elsif ($pw eq 'DEL') {
			if ($lx == 0) {
				print "<P><DT><a href=\"$script?mode=allread&no=$no&page=$page\">$treehead</a> - ";
				print "$sub - $dat <font color=\"$no_color\">No\.$no</font>\n";
			} else {
				print "<LI>$sub - $dat <font color=\"$no_color\">No\.$no</font>\n";
			}
		# レス記事
		} elsif ($lx != 0) {
			print "<LI><a href=\"$script?no=$no&reno=$reno&oya=$oya&mode=msgview&page=$page\">$sub</a> - <b>$name</b> $dat <font color=\"$no_color\">No\.$no</font> $newsign\n";

		# 親記事
		} else {
			print "<P><DT><a href=\"$script?mode=allread&no=$no&page=$page\">$treehead</a> - ";
			print "<a href=\"$script?no=$no&reno=$reno&oya=$oya&mode=msgview&page=$page\">$sub</a> - <b>$name</b> $dat <font color=\"$no_color\">No\.$no</font> $newsign\n";
		}

	}
	close(IN);
	while ($x > 0) { print "</UL>\n"; $x--; }
	print "</UL>\n";
	if ($mode ne "past") { print "</DL>\n"; }
}

#--------------------#
#  リスト新着順表示  #
#--------------------#
sub ListNewOpen {
	local($no,$reno,$xl,$sub,$email,$url,$name,$date,$msg,$tim,$h,$pw,$wrap,$oya);

	# 時間取得
	$time = time;

	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$reno,$xl,$sub,$email,$url,$name,$date,$msg,$tim,$h,$pw,$wrap,$oya) = split(/<>/);
		$cnt{$no} = $tim;
		$rno{$no} = $reno;
		$dat{$no} = $date;
		$nam{$no} = $name;
		$sub{$no} = $sub;
		$oya{$no} = $oya;
	}
	close(IN);

	print "<UL>\n";

	# ソート処理
	$i=0;
	$x=0;
	$p_tree *= 3;
	foreach (sort { ($cnt{$b} <=> $cnt{$a}) } keys(%cnt)) {
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $p_tree) { next; }

		# 所定時間以内の投稿は[NEWマーク]表示
		if ($time - $cnt{$_} > $new_time * 3600) { $newsign = ""; }
		else { $newsign = $newmark; }

		if ($sub{$_} eq '<s>投稿者削除</s>') {
			print "<LI>$sub{$_} - $dat{$_} <font color=\"$no_color\">No\.$_</font> $newsign\n";
		} else {
			print "<LI><a href=\"$script?no=$_&reno=$rno{$_}&oya=$oya{$_}&mode=msgview&list=new\">$sub{$_}</a> - <b>$nam{$_}</b> $dat{$_} <font color=\"$no_color\">No\.$_</font> $newsign\n";
		}
	}
	print "</UL>\n";
}

#----------------------#
#  メッセージ内容表示  #
#----------------------#
sub msgview {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$lt,$ho,$pw,$wrap,$oya,$sml,$v_dat,$v_nam,$v_eml,$v_url,$v_msg,$v_tim,$v_sub,$v_wrp,$v_sml,$date);

	$flag=0;
	@new=();
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$lt,$ho,$pw,$wrap,$oya,$sml) = split(/<>/);
		if ($in{'oya'} == $oya) { push(@new,$_); }
		elsif ($flag && $in{'oya'} != $oya) { last; }
		if ($in{'no'} == $no) {
			$flag=1;
			$v_dat = $dat;
			$v_nam = $nam;
			$v_eml = $eml;
			$v_url = $url;
			$v_msg = $msg;
			$v_tim = $lt;
			$v_sub = $sub;
			$v_wrp = $wrap;
			$v_sml = $sml;
		}
	}
	close(IN);

	# レスメッセージ
	$res_msg = "\n&gt; $v_msg";
	$res_msg =~ s/<br>/\r&gt; /g;

	# レスタイトル
	$res_sub = $v_sub;
	if ($res_sub =~ /^Re\^(\d+)\:(.*)/) {
		$renum = $1 + 1;
		$res_sub = "Re\^$renum\:$2";
	}
	elsif ($res_sub =~ /^Re\:(.*)/) { $res_sub = "Re\^2:$1"; }
	else { $res_sub = "Re: $res_sub"; }

	# HTMLを出力
	&header;
	print "<div align=\"center\">\n";
	if ($t_img) {
		print "<img src=\"$t_img\" alt=\"$title\" width=\"$t_w\" height=\"$t_h\">\n";
	} else {
		print "<B style=\"font-size:$t_point;color:$t_color\">$title</B>\n";
	}

	print "<hr width='90%'>\n",
	"[<a href=\"$script?page=$page&list=$in{'list'}\">記事リスト</a>]\n",
	"[<a href=\"$script?mode=newsort\">新着記事</a>]\n",
	"[<a href=\"$script?mode=find\">ワード検索</a>]\n";
	print "[<a href=\"$script?mode=past\">過去ログ</a>]\n" if ($pastkey);
#	print "[<a href=\"search/\">過去ログ</a>]\n";
	print "[<a href=\"$admin\">管理用</a>]<hr width='90%'></div>\n";

	# 引用部色変更
	if ($refcolor) {
		$v_msg =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
	}

	# 自動リンク
	if ($autolink) { &auto_link($v_msg); }

	# PREタグ
	if ($v_wrp eq 'pre') {
		$v_msg =~ s/<br>/\n/g;
		$v_msg = "<pre>$v_msg</pre>";
	}

	# 投稿日時
	$date = &get_time($v_tim);

	print "<P><table cellspacing=0>\n",
	"<tr><td>タイトル</td>",
	"<td>： <b><font color=\"$sub_color\">$v_sub</font></b></td></tr>\n",
	"<tr><td>投稿日</td><td>： $date</td></tr>\n",
	"<tr><td>投稿者</td><td>： <b>$v_nam</b> ";
	if ($v_eml && $v_sml eq '0') {
		print "&nbsp; &lt;<a href=\"mailto:$v_eml\" class=num>$v_eml</a>&gt;";
	}
	print "</td></tr>\n";
	if ($v_url) {
		print "<tr><td>参照先</td><td>： ",
		"<a href=\"http://$v_url\" target=\"_blank\">",
		"http://$v_url</a></td></tr>\n" 
	}
	print "</table><blockquote>$v_msg</blockquote><P>\n";

	if (@new > 1) {
		print "<hr width='95%'><b style='text-indent:18'>- 関連一覧ツリー</b>\n",
		"（$treehead をクリックするとツリー全体を一括表\示します）<br>\n";

		$x=0;
		print "<UL>\n";
		foreach (@new) {
			($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$lt,$ho,$pw,$wrap,$oya,$sml) = split(/<>/);
			while ($x > $lx) { print "</UL>\n"; $x--; }
			while ($x < $lx) { print "<UL>\n"; $x++; }

			# 記事タイトル長調整
			$sub = &cut_subject($sub);

			if ($lx != 0) {
				print "<LI><a href=\"$script?no=$no&reno=$re&oya=$oya&mode=msgview&page=$page\">$sub</a> - <B>$nam</B> $dat ";
			} else {
				print "<a href=\"$script?mode=allread&no=$no&page=$page\">$treehead</a> - <a href=\"$script?no=$no&reno=$re&oya=$oya&mode=msgview&page=$page\">$sub</a> - <B>$nam</B> $dat";
			}

			if ($in{'no'} == $no) {
				print "<font color=\"$sub_color\"><B>No\.$no</B></font>\n";
			} else {
				print "<font color=\"$no_color\">No\.$no</font>\n";
			}
		}
		while ($x > 0) { print "</UL>\n"; $x--; }
		print "</UL>\n";
	}

	# 返信フォーム
	&msg_form;
	print "</body>\n</html>\n";
	exit;
}

#----------------#
#  一括表示機能  #
#----------------#
sub allread {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wrap,$oya,$sml,$date);

	# HTMLを出力
	&header;
	print <<"EOM";
[<a href="$script?page=$page&mode=$in{'act'}">リストへもどる</a>]<br>
<table width="100%"><tr><th bgcolor="#004080">
<font color="#FFFFFF">一括表\示</font></th></tr></table>
EOM
	# 過去ログの場合
	if ($in{'act'} eq "past") {
		# ログファイルを定義
		if ($in{'pastlog'}) {
			$count = $in{'pastlog'};
		} else {
			open(NO,"$nofile") || &error("Open Error : $nofile");
			$count = <NO>;
			close(NO);
		}
		$logfile = sprintf("%s%04d\.cgi", $pastdir,$count);
	}

	# 親記事を出力
	$x=0;
	print "<UL>\n";
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN> if ($in{'act'} ne "past");
	$flag=0;
	while (<IN>) {
		($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wrap,$oya) = split(/<>/);
		if ($in{'no'} == $oya) {
			$flag=1;
			push(@new,$_);

			while ($x > $lx) { print "</UL>\n"; $x--; }
			while ($x < $lx) { print "<UL>\n"; $x++; }

			# 記事タイトル長調整
			$sub = &cut_subject($sub);

			if ($pw eq 'DEL') {
				print "<LI>$sub - $dat <font color=\"$no_color\">No\.$no</font>\n";
			} else {
				print "<LI><a href=\"#$no\">$sub</a> - <B>$nam</B> $dat <font color=\"$no_color\">No\.$no</font>\n";
			}
		}
		elsif ($flag && $in{'no'} != $oya) { last; }
	}
	close(IN);
	while ($x > 0) { print "</UL>\n"; $x--; }
	print "</UL><div align='center'>\n";

	foreach (@new) {
		($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wrap,$oya,$sml) = split(/<>/);
		if ($pw eq 'DEL') { next; }

		# 自動リンク
		if ($autolink) { &auto_link($msg); }

		# 引用部色変更
		if ($refcolor) {
			$msg =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
		}
		# 図表モード
		if ($wrap eq 'pre') {
			$msg =~ s/<br>/\n/g;
			$msg = "<pre>$msg</pre>";
		}

		$date = &get_time($t);
		print "<a name=\"$no\"></a>\n",
		"<table border=1 width='95%' cellpadding=5>\n",
		"<tr><td bgcolor=\"$tbl_color\"><table cellspacing=0>",
		"<tr><td>タイトル</td><td>： ",
		"<font color=\"$sub_color\"><b>$sub</b></font></td></tr>\n",
		"<tr><td>記事No</td><td>： <b>$no</b></td></tr>\n",
		"<tr><td>投稿日</td><td>： $date</td></tr>\n",
		"<tr><td>投稿者</td><td>： <b>$nam</b> ";
		if ($eml && $sml eq '0') {
			print "&nbsp; &lt;<a href=\"mailto:$eml\" class=num>$eml</a>&gt;";
		}
		print "</td></tr>\n";
		if ($url) {
			print "<tr><td>参照先</td><td>： ",
			"<a href=\"http://$url\" target=\"_blank\">",
			"http://$url</a></td></tr>\n";
		}
		print "</table><blockquote>$msg</blockquote>\n";
		if ($in{'act'} ne "past") {
			print "<div align=right>\n",
			"<form action=\"$script\#msg\" method=\"POST\">\n",
			"<input type=hidden name=mode value=msgview>\n",
			"<input type=hidden name=reno value=\"$re\">\n",
			"<input type=hidden name=no value=\"$no\">\n",
			"<input type=hidden name=oya value=\"$oya\">\n",
			"<input type=hidden name=page value=\"$page\">\n",
			"<input type=submit value=\"返信する\"></form></div>\n";
		}
		print "</td></tr></table><br>\n";
	}
	print "</div>\n</body>\n</html>\n";
	exit;
}

#--------------------#
#  新着順ソート表示  #
#--------------------#
sub newsort {
	local($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$tim,$ho,$pw,$wrp,$oya,$sml,$date);

	&header;
	print <<"EOM";
[<a href="$script?page=$page">リストへもどる</a>]
<table width="100%"><tr><th bgcolor="#004080">
<font color="white">新着記事</font></th></tr></table>
<br><div align="center">
EOM
	# 記事展開
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$tim,$ho,$pw,$wrp,$oya,$sml) = split(/<>/);
		if ($pw eq 'DEL') { next; }
		if ($autolink) { &auto_link($msg); }

		# 連想配列化
		$cnt{$no} = $tim;
		$nam{$no} = $nam;
		$eml{$no} = $eml;
		$url{$no} = $url;
		$rno{$no} = $re;
		$sub{$no} = $sub;
		$oya{$no} = $oya;
		$msg{$no} = $msg;
		$wrp{$no} = $wrp;
		$sml{$no} = $sml;
	}
	close(IN);

	# ソート処理
	$i=0;
	foreach (sort { ($cnt{$b} <=> $cnt{$a}) } keys(%cnt)) {
		$i++;
		if ($i > $sortcnt) { last; } # ループを抜ける

		# 引用部色変更
		if ($refcolor) {
			$msg{$_} =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
		}
		# PRE機能
		if ($wrp{$_} eq "pre") {
			$msg{$_} =~ s/<br>/\n/g;
			$msg{$_} = "<pre>$msg{$_}</pre>";
		}

		$date = &get_time($cnt{$_});

		print "<table border=1 width='95%' cellpadding=5>\n",
		"<tr><td bgcolor=\"$tbl_color\">\n",
		"<table cellspacing=0>",
		"<tr><td>タイトル</td><td>： ",
		"<font color=\"$sub_color\"><b>$sub{$_}</b></font></td></tr>",
		"<tr><td>記事No</td><td>： <b>$_</b> &nbsp;&nbsp;",
		"[<a href=\"$script?mode=allread&no=$oya{$_}\">関連記事</a>]</td></tr>\n",
		"<tr><td>投稿日</td><td>： $date</td></tr>\n",
		"<tr><td>投稿者</td><td>： <b>$nam{$_}</b> ";
		if ($eml{$_} && $sml{$_} eq '0') {
			print "&nbsp; &lt;<a href=\"mailto:$eml{$_}\" class=num>",
			"$eml{$_}</a>&gt;";
		}
		print "</td></tr>\n";
		if ($url{$_}) {
			print "<tr><td>参照先</td><td>： ",
			"<a href=\"http://$url{$_}\" target=\"_blank\">",
			"http://$url{$_}</a></td></tr>\n";
		}
		print "</table><blockquote>$msg{$_}</blockquote>\n",
		"<div align=right>\n",
		"<form action=\"$script\#msg\" method=\"POST\">\n",
		"<input type=hidden name=mode value=msgview>\n",
		"<input type=hidden name=reno value=\"$rno{$_}\">\n",
		"<input type=hidden name=no value=\"$_\">\n",
		"<input type=hidden name=oya value=\"$oya{$_}\">\n",
		"<input type=hidden name=page value=\"$page\">\n",
		"<input type=submit value=\"返信する\"></div></form>\n",
		"</td></tr></table><br>\n";
	}
	print "</div>\n</body>\n</html>\n";
	exit;
}

#------------------#
#  投稿フォーム部  #
#------------------#
sub msg_form {
	# クッキーを取得
	local($cname, $cmail, $curl, $cpwd, $cpv, $csmail) = &get_cookie;

	# 修正時
	if ($_[0] eq "edt") {
		($type,$cname,$cmail,$curl,$csmail,$res_sub,$res_msg,$wrap) = @_;
		if (!$wrap) { $wrap='soft'; }
		print "[<a href=\"javascript:history.back()\">戻る</a>]\n",
		"<h3>修正フォーム</h3>\n",
		"<form action=\"$script\" method=\"POST\">\n",
		"<input type=hidden name=mode value=\"usr_edt\">\n",
		"<input type=hidden name=action value=\"edit\">\n",
		"<input type=hidden name=pwd value=\"$in{'pwd'}\">\n",
		"<input type=hidden name=no value=\"$in{'no'}\">\n";
	# 返信時
	} elsif ($mode eq 'msgview') {
		$wrap='soft';
		print "<hr width='95%'><a name=\"msg\"></a>\n",
		"<b style='text-indent:18'>- 返信フォーム</b>\n",
		"（この記事に返信する場合は下記フォームから投稿して下さい）<br>\n",
		"<form action=\"$regist\" method=\"POST\">\n",
		"<input type=hidden name=mode value=\"form\">\n",
		"<input type=hidden name=page value=\"$page\">\n",
		"<input type=hidden name=action value=\"res_msg\">\n",
		"<input type=hidden name=no value=\"$in{'no'}\">\n",
		"<input type=hidden name=oya value=\"$in{'oya'}\">\n";
	# 新規時
	} else {
		$wrap='soft';
		print "<hr width='95%'><P><a name=\"msg\"></a><div align='center'>\n",
		"<b><big>メッセージをどうぞ・・</big></b></a></div>\n",
		"<P><form action=\"$regist\" method=\"POST\">\n",
		"<input type=hidden name=mode value=\"form\">\n",
		"<input type=hidden name=page value=\"$page\">\n",
		"<input type=hidden name=no value=\"new\">\n";
	}

	print "<blockquote><table border=0 cellspacing=0 cellpadding=1>\n",
	"<tr><td nowrap><b>おなまえ</b></td>",
	"<td><input type=text name=name size=28 value=\"$cname\"></td></tr>\n",
	"<tr><td nowrap><b>Ｅメール</b></td>",
	"<td><input type=text name=email size=28 value=\"$cmail\"> ",
	"<select name=smail>\n";

	@sm = ('表示', '非表示');
	if ($csmail eq "") { $csmail=0; }
	foreach (0, 1) {
		if ($csmail == $_) {
			print "<option value=\"$_\" selected>$sm[$_]\n";
		} else {
			print "<option value=\"$_\">$sm[$_]\n";
		}
	}

 	print "</select></td></tr>\n",
	"<tr><td nowrap><b>タイトル</b></td>",
	"<td><input type=text name=sub size=38 value=\"$res_sub\"></td></tr>\n",
	"<tr><td colspan=2><b>メッセージ</b>&nbsp;&nbsp;&nbsp;";

	@w1 = ('手動改行', '強制改行', '図表モード');
	@w2 = ('soft', 'hard', 'pre');
	foreach (0 .. 2) {
		if ($wrap eq $w2[$_]) {
			print "<input type=radio name=wrap value=\"$w2[$_]\" checked>$w1[$_]\n";
		} else {
			print "<input type=radio name=wrap value=\"$w2[$_]\">$w1[$_]\n";
		}
	}

	# プレビューのチェック
	if ($cpv eq "on") { $checked = "checked"; }

	print "<br><textarea name=message rows=10 cols=62 wrap=soft>$res_msg</textarea>",
	"</td></tr><tr><td nowrap><b>ＵＲＬ</b></td>",
	"<td><input type=text name=url size=58 value=\"http://$curl\"></td></tr>\n";

	if ($_[0] eq "edt") {
		print "<tr><td></td><td><input type=submit value=' 記事を修正する '></td>\n",
		"</tr></table></form></blockquote>\n";
	} else {
		print <<"EOM";
<tr>
  <td nowrap><b>パスワード</b></td>
  <td><input type=password name=pwd size=8 value="$cpwd" maxlength=8>
	(英数字で8文字以内)</td>
</tr>
<tr>
  <td></td>
  <td><input type=submit value=" 記事を投稿する ">
	 &nbsp; <input type=checkbox name=pview value="on" $checked>プレビュー</td>
</tr>
</table>
</form>
</blockquote>
<hr width="95%">
<div align="center"><form action="$script" method="POST">
<input type=hidden name=page value="$page">
<font color="$sub_color">
- 以下のフォームから自分の投稿記事を修正・削除することができます -</font><br>
処理 <select name=mode>
<option value="usr_edt">修正
<option value="usr_del">削除</select>
記事No <input type=text name=no size=4>
パスワード <input type=password name=pwd size=6>
<input type=submit value="送信"></form>
<hr width="95%"></div>
EOM
	}
}

#----------------#
#  記事修正処理  #
#----------------#
sub usr_edt {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$lt,$ho,$pw,$wrp,$oya,$sml,$res);

	# フォーム内容のチェック
	$in{'no'} =~ s/\D//g;
	if ($in{'no'} eq '' || $in{'pwd'} eq '')
		{ &error("記事NOまたはパスワードの記入モレがあります"); }

	if ($in{'action'} eq "edit") {
		# 入力チェック
		&chk_form;

		# ロック処理
		&lock if ($lockkey);
	}

	$flag=0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	while (<IN>) {
		chop;
		($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$lt,$ho,$pw,$wrp,$oya,$sml,$res) = split(/<>/);
		if ($in{'no'} == $no) {
			$pw2 = $pw;
			$flag=1;
			if ($in{'action'} ne "edit") { last; }
			else { $_ = "$no<>$re<>$lx<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$dat<>$in{'message'}<>$lt<>$ho<>$pw<>$in{'wrap'}<>$oya<>$in{'smail'}<>$res<>"; }
		}
		if ($in{'action'} eq "edit") { push(@new,"$_\n"); }
	}
	close(IN);
	if (!$flag) { &error("該当の記事が見当たりません"); }
	if ($pw2 eq "") { &error("パスワードが設定されていません"); }
	$check = &decrypt($in{'pwd'}, $pw2);
	if ($check ne "yes") { &error("パスワードが違います"); }

	@wrap1 = ('手動改行', '強制改行', '図表モード');
	@wrap2 = ('soft', 'hard', 'pre');

	if ($in{'action'} eq "edit") {
		unshift(@new,$top);
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		print OUT @new;
		close(OUT);

		&unlock if ($lockkey);

		if ($in{'url'}) { $in{'url'} = "http://$in{'url'}"; }
		if ($in{'wrap'} eq "pre") { $in{'message'} = "<pre>$in{'message'}</pre>"; }
		if ($refcolor) {
			$in{'message'} =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
		}
		foreach (0 .. 2) {
			if ($wrap2[$_] eq $in{'wrap'}) { $wp=$_; last; }
		}
		if ($in{'smail'} == 1) { $in{'email'} = '非表示'; }

		&header;
		print "<h4>- 以下のとおり修正が完了しました -</h4>\n";
		print "<table><tr><td>名前</td><td>： $in{'name'}</td></tr>\n";
		print "<tr><td>e-mail</td><td>： $in{'email'}</td></tr>\n";
		print "<tr><td>タイトル</td><td>： $in{'sub'}</td></tr>\n";
		print "<tr><td>URL</td><td>： $in{'url'}</td></tr>\n";
		print "<tr><td valign=top>記事</td><td>：<P>$in{'message'}</td></tr>\n";
		print "</table><form action=\"$script\">\n";
		print "<input type=submit value='リストに戻る'></form>\n";
		print "</body>\n</html>\n";
		exit;
	}

	$msg =~ s/<br>/\r/g;
	&header;
	&msg_form("edt",$nam,$eml,$url,$sml,$sub,$msg,$wrp);
	print "</body></html>\n";
	exit;
}

#----------------#
#  記事削除処理  #
#----------------#
sub usr_del {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$tim,$ho,$pw,$wr,$oya,$sml,$res,$date);

	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	# フォーム内容のチェック
	$in{'no'} =~ s/\D//g;
	if ($in{'no'} eq '' || $in{'pwd'} eq '')
		{ &error("記事NOまたはパスワードの記入モレがあります"); }

	# 確認画面
	if ($in{'keyno'} eq "") {
		$flag=0;
		open(IN,"$logfile") || &error("Open Error : $logfile");
		$top = <IN>;
		while (<IN>) {
			($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml,$res) = split(/<>/);
			if ($in{'no'} == $no) { $flag=1; last; }
		}
		close(IN);
		if (!$flag) { &error("該当の記事は見当たりません"); }
		if ($pw eq "") { &error("この記事（No $in{'no'}）は削除キーが設定されていません"); }
		# 照合
		$match = &decrypt($in{'pwd'}, $pw);
		if ($match ne "yes") { &error("削除キーが違います"); }

		if ($url) { $url = "http://$url"; }
		&header;
		print "<div align='center'><h3>以下の記事を本当に削除しますか？</h3>\n",
		"<table border=1 bgcolor=\"$tbl_color\" cellpadding=10 width='80%'>",
		"<tr><td><table>\n",
		"<tr><td>記事No</td><td>： <b>$no</b></td></tr>\n",
		"<tr><td>投稿日</td><td>： $dat</td></tr>\n",
		"<tr><td>投稿者</td><td>： <b>$nam</b></td></tr>\n";
		print "<tr><td>E-Mail</td><td>： $eml</td></tr>\n" if ($eml && $sml eq '0');
		print "<tr><td>ＵＲＬ</td><td>： $url</td></tr>\n" if ($url);
		print "<tr><td>タイトル</td><td>： 
			<font color=\"$sub_color\"><b>$sub</b></font></td></tr>",
		"</table></td></table>\n",
		"<P><table><tr><td>\n",
		"<form action=\"$script\" method=POST>\n",
		"<input type=hidden name=mode value=usr_del>\n",
		"<input type=hidden name=no value=\"$in{'no'}\">\n",
		"<input type=hidden name=pwd value=\"$in{'pwd'}\">\n",
		"<input type=hidden name=keyno value=\"$re\">\n",
		"<input type=submit value='本当に削除する'></td></form>\n",
		"<td width=15></td><td><form>",
		"<input type=button value='キャンセルする' onClick=\"history.back()\">",
		"</td></form></tr></table></div>\n",
		"</body>\n</html>\n";
		exit;
	}

	# ロック開始
	&lock if ($lockkey);

	# ログを読み込む
	$new=();
	$flag=0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	while (<IN>) {
		chop;
		($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$tim,$ho,$pw,$wr,$oya,$sml,$res) = split(/<>/);

		if ($in{'no'} == $no) {
			if ($pw eq "") { $flag=2; last; }
			$match = &decrypt($in{'pwd'}, $pw);
			if ($match ne "yes") { $flag=3; last; }
			else { $flag=1; }

			if ($res == 0) { next; }
			$_ = "$no<>$re<>$lx<><s>投稿者削除</s><><><>(削除)<>$dat<>(投稿者により削除されました)<>$tim<>$ho<>DEL<>$wr<>$oya<>$sml<>$res<>";
		} elsif ($no == $in{'keyno'}) {
			if ($res > 0) { $res--; }
			$_ = "$no<>$re<>$lx<>$sub<>$eml<>$url<>$nam<>$dat<>$msg<>$tim<>$ho<>$pw<>$wr<>$oya<>$sml<>$res<>";
		}
		push(@new,"$_\n");
	}
	close(IN);

	if ($flag == 0) { &error("該当記事は見つかりません"); }
	elsif ($flag == 2) { &error("パスワードが設定されていません"); }
	elsif ($flag == 3) { &error("パスワードが違います"); }

	# ログを更新
	unshift(@new,$top);
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# ロック解除
	&unlock if ($lockkey);

	# リスト表示部にもどる
	&list_view;
}

#------------------#
#  クッキーを取得  #
#------------------#
sub get_cookie {
	local($key, $val, *cook);

	$cook = $ENV{'HTTP_COOKIE'};
	foreach (split(/;/, $cook)) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}
	@cook = split(/<>/, $cook{'WEBFORUM'});
	return @cook;
}

#----------------------#
#  パスワード照合処理  #
#----------------------#
sub decrypt {
	local($inpw, $logpw) = @_;
	local($salt, $key, $check);

	$salt = $logpw =~ /^\$1\$(.*)\$/ && $1 || substr($logpw, 0, 2);
	$check = "no";
	if (crypt($inpw, $salt) eq $logpw || crypt($inpw, '$1$' . $salt) eq $logpw)
		{ $check = "yes"; }
	return $check;
}

#----------------#
#  検索フォーム  #
#----------------#
sub find {
	&header;
	print <<"EOM";
[<a href="$script?page=$page&list=$in{'list'}">リストに戻る</a>]
<table width="100%"><tr><th bgcolor="#004080">
  <font color="#FFFFFF">キーワード検索</font></th></tr></table>
<P><a name="SEARCH"></a>
<UL>
<LI>検索したい<b>キーワード</b>を入力し、検索条件を選択して「検索」を押してください。
<LI>複数のキーワードを入力するときは、<b>半角スペース</b>で区切って下さい。
<form action="$script" method="POST">
<input type=hidden name=mode value="find">
<input type=hidden name=list value="$in{'list'}">
キーワード：<input type=text name=word size=35 value="$in{'word'}">
条件：<select name="cond">
EOM
	foreach ('AND', 'OR') {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select> 表\示：<select name=view>\n";
	foreach (10,15,20,25,30) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_件\n";
		} else {
			print "<option value=\"$_\">$_件\n";
		}
	}
	print "</select> <input type=submit value=' 検索 '></form></UL>\n";

	# ワード検索の実行と結果表示
	if ($in{'word'} ne "") { &search; }

	print "</body>\n</html>\n";
	exit;
}

#----------------#
#  検索処理実行  #
#----------------#
sub search {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml,$date,$back,$next);

	# 入力内容を整理
	$in{'word'} =~ s/　/ /g;
	@wd = split(/\s+/, $in{'word'});

	# ロック処理：サーバ負荷を考慮し多重起動回避のため
	&lock if ($lockkey);

	# ファイルを読み込み
	@new=();
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN> if ($mode ne "past");
	while (<IN>) {
		$flag=0;
		foreach $wd (@wd) {
			if (index($_,$wd) >= 0) {
				$flag=1;
				if ($in{'cond'} eq 'OR') { last; }
			} else {
				if ($in{'cond'} eq 'AND') { $flag=0; last; }
			}
		}
		if ($flag) { push(@new,$_); }
	}
	close(IN);

	# 検索終了
	$count = @new;
	print "検索結果：<b>$count</b>件\n";
	if ($in{'page'} eq '') { $in{'page'} = 0; }
	$end_data = @new - 1;
	$page_end = $in{'page'} + $in{'view'} - 1;
	if ($page_end >= $end_data) { $page_end = $end_data; }

	# キーワードをURLエンコード
	$enwd = &url_enc($in{'word'});

	$next = $page_end + 1;
	$back = $in{'page'} - $in{'view'};

	if ($back_line >= 0) {
		print "[<a href=\"$script?mode=$mode&page=$back&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">前の$in{'view'}件</a>]\n";
	}
	if ($page_end ne "$end_data") {
		print "[<a href=\"$script?mode=$mode&page=$next&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">次の$in{'view'}件</a>]\n";
	}

	# ヒットした記事を表示
	print "<hr>\n";
	foreach ($in{'page'} .. $page_end) {
		($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml) = split(/<>/, $new[$_]);

		if ($w eq "pre") {
			$msg =~ s/<br>/\r/g;
			$msg = "<pre>$msg</pre>";
		}
		if ($autolink) { &auto_link($msg); }
		if ($refcolor) {
			$msg =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
		}
		$date = &get_time($t);
		print "<table cellspacing=0>\n",
		"<tr><td>タイトル</td><td>： ",
		"<font color=\"$sub_color\"><b>$sub</b></font></td></tr>\n",
		"<tr><td>記事No</td><td>： <b>$no</b> &nbsp;&nbsp;";
		if ($in{'pastlog'}) {
			print "[<a href=\"$script?mode=allread&no=$oya&pastlog=$in{'pastlog'}&act=past\">関連記事</a>]</td></tr>\n";
		} else {
			print "[<a href=\"$script?mode=allread&no=$oya\">関連記事</a>]</td></tr>\n";
		}
		print "<tr><td>投稿日</td><td>： $date</td></tr>\n",
		"<tr><td>投稿者</td><td>： <b>$nam</b> ";
		if ($eml && $sml eq '0') {
			print "&nbsp; &lt;<a href=\"maito:$eml\" class=num>$eml</a>&gt;";
		}
		print "</td></tr>\n";
		if ($ur) {
			print "<tr><td>参照先</td><td>： ",
			"<a href=\"http://$url\" target=\"_blank\">",
			"http://$url</a></td></tr>\n";
		}
		print "</table><blockquote>$msg</blockquote><hr>\n";
	}
	if ($count) {
		print "<a href=\"#SEARCH\">▲TOP</a>\n";
	}
	if ($back_line >= 0) {
		print "[<a href=\"$script?mode=$mode&page=$back&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">前の$in{'view'}件</a>]\n";
	}
	if ($page_end ne $end_data) {
		print "[<a href=\"$script?mode=$mode&page=$next&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">次の$in{'view'}件</a>]\n";
	}

	# ファイルロック解除
	&unlock if ($lockkey);
}

#--------------#
#  自動リンク  #
#--------------#
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(http\:\/\/[\w\.\~\-\/\?\&\=\;\#\:\%\+\@]+)/$1<a href=\"$2\" target=\"_blank\">$2<\/a>/g;
}

#----------------#
#  過去ログ表示  #
#----------------#
sub past_view {
	open(IN,"$nofile") || &error("Open Error : $nofile");
	$pastno = <IN>;
	close(IN);
	$pastno = sprintf("%04d", $pastno);
	if (!$in{'pastlog'}) { $in{'pastlog'} = $pastno; }

	&header;
	print <<"EOM";
[<a href="$script?">掲示板に戻る</a>]
<table width="100%"><tr><th bgcolor="#004080">
  <font color="#FFFFFF">過去ログ [ $in{'pastlog'} ]</font></th></tr></table>
<P><a name="SEARCH"></a>
<form action="$script" method="POST">
<input type=hidden name=mode value=past>
<table cellpadding=0 cellspacing=0>
<tr><td>過去ログ：<select name=pastlog>
EOM

	$pastkey = $pastno;
	while ($pastkey > 0) {
		$pastkey = sprintf("%04d", $pastkey);
		if ($in{'pastlog'} eq "$pastkey") {
			print "<option value=\"$pastkey\" selected>P $pastkey\n";
		} else {
			print "<option value=\"$pastkey\">P $pastkey\n";
		}
		$pastkey--;
	}
	print "</select>\n<input type=submit value='移動'></td></form>\n";
	print "<td width=40></td><td>\n";
	print "<form action=\"$script\" method=GET>\n";
	print "<input type=hidden name=mode value=past>\n";
	print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
	print "ワード検索：<input type=text name=word size=30 value=\"$in{'word'}\">\n";
	print "条件：<select name=cond>\n";

	foreach ('AND', 'OR') {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select> 表\示：<select name=view>\n";
	if ($in{'view'} eq "") { $in{'view'} = $p_tree; }
	foreach (10,15,20,25,30) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_件\n";
		} else {
			print "<option value=\"$_\">$_件\n";
		}
	}
	print "</select> <input type=submit value='検索'>",
	"</td></form></tr></table><hr>\n";

	# ファイルを定義
	$logfile = "$pastdir$in{'pastlog'}\.cgi";

	# ワード検索処理
	if ($in{'word'} ne "") {
		&search;
		print "</body>\n</html>\n";
		exit;
	}

	&ListTreeOpen('past');
	&move_list;
	print "</body>\n</html>\n";
	exit;
}

#----------------------#
#  記事タイトル長調整  #
#----------------------#
sub cut_subject {
	# 制限長に満たないものは戻す
	if (length($_[0]) <= $sub_length) { return $_[0]; }

	# カット処理
	($_[0], $folded) = &fold($_[0], $sub_length);
	$_[0] .= '..';

	return $_[0];
}

#----------------------#
#  ページ移動フォーム  #
#----------------------#
sub move_list {
	local($next, $back);

	$next = $page + $p_tree;
	$back = $page - $p_tree;
	print "<P><table cellpadding=0 cellspacing=0><tr>\n";
	if ($back >= 0) {
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n" if ($in{'pastlog'} ne "");
		print "<input type=hidden name=page value=\"$back\">\n";
		print "<input type=hidden name=mode value=\"past\">\n" if ($mode eq 'past');
		print "<input type=hidden name=list value=\"$in{'list'}\">\n";
		print "<input type=submit value=\"前ページ\"></td></form>\n";
	}
	if ($next < $i) {
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n" if ($in{'pastlog'} ne "");
		print "<input type=hidden name=page value=\"$next\">\n";
		print "<input type=hidden name=mode value=\"$mode\">\n" if ($mode eq 'past');
		print "<input type=hidden name=list value=\"$in{'list'}\">\n";
		print "<input type=submit value=\"次ページ\"></td></form>\n";
	}
	print "<td width=10></td><td class=num>";

	# ページ移動ボタン表示
	$x=1;
	$y=0;
	while ($i > 0) {
		if ($page eq $y) { print "<b>[$x]</b>\n"; }
		elsif ($in{'pastlog'} ne "") {
			print "[<a href=\"$script?page=$y&list=$in{'list'}&mode=past&pastlog=$in{'pastlog'}\">$x</a>]\n";
		} else {
			print "[<a href=\"$script?page=$y&list=$in{'list'}\">$x</a>]\n";
		}
		$x++;
		$y = $y + $p_tree;
		$i = $i - $p_tree;
	}
	print "</td></tr></table><br>\n";
}

#-----------------#
#  URLエンコード  #
#-----------------#
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#------------------#
#  チェックモード  #
#------------------#
sub check {
	&header;
	print "<h2>Check Mode</h2>\n<UL>\n";

	# ログ
	print "<LI>ログパス：";
	if (-e $logfile) {
		print "OK\n";
		# パーミッション
		print "<LI>ログパーミッション：";
		if (-r $logfile && -w $logfile) { print "OK\n"; }
		else { print "NG → $logfile\n"; }
	} else {
		print "NG → $logfile\n";
	}

	# ロックディレクトリ
	print "<LI>ロック形式：";
	if ($lockkey == 0) { print "設定なし\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }

		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<LI>ロックディレクトリ：$lockdir\n";

		if (-d $lockdir) { print "<LI>ロックディレクトリのパス：OK\n"; }
		else { print "<LI>ロックディレクトリのパス：NG → $lockdir\n"; }

		if (-r $lockdir && -w $lockdir && -x $lockdir) {
			print "<LI>ロックディレクトリのパーミッション：OK\n";
		} else {
			print "<LI>ロックディレクトリのパーミッション：NG → $lockdir\n";
		}
	}

	# 過去ログ
	print "<LI>過去ログ：";
	if ($pastkey == 0) { print "設定なし\n"; }
	else {
		print "設定あり\n";

		# NOファイル
		if (-e $nofile) {
			print "<LI>NOファイルパス：OK\n";
			if (-r $nofile && -w $nofile) { print "<LI>NOファイルパーミッション：OK\n"; }
			else { print "<LI>NOファイルパーミッション：NG → $nofile\n"; }
		} else { print "<LI>NOファイルのパス：NG → $nofile\n"; }

		# ディレクトリ
		if (-d $pastdir) {
			print "<LI>過去ログディレクトリパス：OK\n";
			if (-r $pastdir && -w $pastdir && -x $pastdir) {
				print "<LI>過去ログディレクトリパーミッション：OK\n";
			} else {
				print "<LI>過去ログディレクトリパーミッション：NG → $pastdir\n";
			}
		} else { print "<LI>過去ログディレクトリのパス：NG → $pastdir\n"; }
	}

	print "</body></html>\n";
	exit;
}

__END__

