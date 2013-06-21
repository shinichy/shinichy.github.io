#!/usr/bin/perl

#��������������������������������������������������������������������
#�� Web Forum v4.07 <wforum.cgi> (2002/09/27)
#�� Copyright(C) KENT WEB 2002
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#============#
#  ��{�ݒ�  #
#============#

# �O���t�@�C���捞��
require './jcode.pl';
require './fold.pl';
require './wf_init.cgi';

#============#
#  �ݒ芮��  #
#============#

# ��{�������`
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
#  ���X�g�\��  #
#--------------#
sub list_view {
	&header;
	print "<div align=\"center\">\n";

	# �^�C�g����
	if ($t_img) {
		print "<img src=\"$t_img\" alt=\"$title\" width=\"$t_w\" height=\"$t_h\">\n";
	} else {
		print "<B style=\"font-size:$t_point;color:$t_color\">$title</B>\n";
	}

	print "<hr width='90%'>\n",
	"[<a href=\"$home\" target=\"_top\">���ǂ�</a>]\n",
	"[<a href=\"#msg\">�V�K���e</a>]\n";

	if ($in{'list'} ne "new") {
		print "[<a href=\"$script?list=new\">�V�K���\\��</a>]\n";
	} else {
		print "[<a href=\"$script?list=tree\">�c���[�\\��</a>]\n";
	}
	print "[<a href=\"$script?mode=newsort&page=$page\">�V���L��</a>]\n",
	"[<a href=\"$note\">���ӎ���</a>]\n",
	"[<a href=\"$script?mode=find&page=$page&list=$in{'list'}\">���[�h����</a>]\n";

	print "[<a href=\"$script?mode=past\">�ߋ����O</a>]\n" if ($pastkey);
#	print "[<a href=\"search/\">�ߋ����O</a>]\n";
	print "[<a href=\"$admin\">�Ǘ��p</a>]\n",
	"<hr width='90%'><table><tr><td>\n",
	"<li>$new_time���Ԉȓ��̋L���� $newmark �ŕ\\������܂��B</li><br>\n";

	if ($in{'list'} eq "new") {
		print "<li>�ȉ��͐V�K���e���̃��X�g�\\���ł��B</li><br>\n";
	} else {
		print "<li>�c���[�擪���� $treehead ���N���b�N����Ɗ֘A�L�����ꊇ�\\�����܂��B</li><br>\n";
	}
	print "</td></tr></table></div>\n";

	# ���O���J��
	if ($in{'list'} eq "new") { &ListNewOpen; }
	else { &ListTreeOpen; }

	# �y�[�W�ړ��t�H�[��
	&move_list;

	# ���b�Z�[�W���e�t�H�|����\��
	&msg_form;

	# ���쌠�\���i�폜���Ȃ��ŉ������j
	print "<P><div align='center' style='font-size:9pt'><!-- $ver -->\n",
	"- <a href='http://www.kent-web.com/' target='_top'>Web Forum</a> -\n",
	"</div>\n</body></html>\n";
	exit;
}

#--------------------#
#  ���X�g�c���[�\��  #
#--------------------#
sub ListTreeOpen {
	local($no,$reno,$lx,$sub,$email,$url,$name,$dat,$msg,$t,$h,$pw,$w,$oya);

	# ���Ԏ擾
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

		# ���莞�Ԉȓ��̓��e��[NEW�}�[�N]�\��
		if ($time - $t > $new_time * 3600) { $newsign = ""; }
		else { $newsign = $newmark; }

		# �L���^�C�g��������
		$sub = &cut_subject($sub);

		# �ߋ��L��
		if ($mode eq "past") {
			print "<LI><a href=\"$script?mode=allread&pastlog=$in{'pastlog'}&no=$oya&page=$page&act=past\#$no\">$sub</a> - <b>$name</b> $dat <font color=\"$no_color\">No\.$no</font> $newsign\n";
		# �폜�L��
		} elsif ($pw eq 'DEL') {
			if ($lx == 0) {
				print "<P><DT><a href=\"$script?mode=allread&no=$no&page=$page\">$treehead</a> - ";
				print "$sub - $dat <font color=\"$no_color\">No\.$no</font>\n";
			} else {
				print "<LI>$sub - $dat <font color=\"$no_color\">No\.$no</font>\n";
			}
		# ���X�L��
		} elsif ($lx != 0) {
			print "<LI><a href=\"$script?no=$no&reno=$reno&oya=$oya&mode=msgview&page=$page\">$sub</a> - <b>$name</b> $dat <font color=\"$no_color\">No\.$no</font> $newsign\n";

		# �e�L��
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
#  ���X�g�V�����\��  #
#--------------------#
sub ListNewOpen {
	local($no,$reno,$xl,$sub,$email,$url,$name,$date,$msg,$tim,$h,$pw,$wrap,$oya);

	# ���Ԏ擾
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

	# �\�[�g����
	$i=0;
	$x=0;
	$p_tree *= 3;
	foreach (sort { ($cnt{$b} <=> $cnt{$a}) } keys(%cnt)) {
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $p_tree) { next; }

		# ���莞�Ԉȓ��̓��e��[NEW�}�[�N]�\��
		if ($time - $cnt{$_} > $new_time * 3600) { $newsign = ""; }
		else { $newsign = $newmark; }

		if ($sub{$_} eq '<s>���e�ҍ폜</s>') {
			print "<LI>$sub{$_} - $dat{$_} <font color=\"$no_color\">No\.$_</font> $newsign\n";
		} else {
			print "<LI><a href=\"$script?no=$_&reno=$rno{$_}&oya=$oya{$_}&mode=msgview&list=new\">$sub{$_}</a> - <b>$nam{$_}</b> $dat{$_} <font color=\"$no_color\">No\.$_</font> $newsign\n";
		}
	}
	print "</UL>\n";
}

#----------------------#
#  ���b�Z�[�W���e�\��  #
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

	# ���X���b�Z�[�W
	$res_msg = "\n&gt; $v_msg";
	$res_msg =~ s/<br>/\r&gt; /g;

	# ���X�^�C�g��
	$res_sub = $v_sub;
	if ($res_sub =~ /^Re\^(\d+)\:(.*)/) {
		$renum = $1 + 1;
		$res_sub = "Re\^$renum\:$2";
	}
	elsif ($res_sub =~ /^Re\:(.*)/) { $res_sub = "Re\^2:$1"; }
	else { $res_sub = "Re: $res_sub"; }

	# HTML���o��
	&header;
	print "<div align=\"center\">\n";
	if ($t_img) {
		print "<img src=\"$t_img\" alt=\"$title\" width=\"$t_w\" height=\"$t_h\">\n";
	} else {
		print "<B style=\"font-size:$t_point;color:$t_color\">$title</B>\n";
	}

	print "<hr width='90%'>\n",
	"[<a href=\"$script?page=$page&list=$in{'list'}\">�L�����X�g</a>]\n",
	"[<a href=\"$script?mode=newsort\">�V���L��</a>]\n",
	"[<a href=\"$script?mode=find\">���[�h����</a>]\n";
	print "[<a href=\"$script?mode=past\">�ߋ����O</a>]\n" if ($pastkey);
#	print "[<a href=\"search/\">�ߋ����O</a>]\n";
	print "[<a href=\"$admin\">�Ǘ��p</a>]<hr width='90%'></div>\n";

	# ���p���F�ύX
	if ($refcolor) {
		$v_msg =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
	}

	# ���������N
	if ($autolink) { &auto_link($v_msg); }

	# PRE�^�O
	if ($v_wrp eq 'pre') {
		$v_msg =~ s/<br>/\n/g;
		$v_msg = "<pre>$v_msg</pre>";
	}

	# ���e����
	$date = &get_time($v_tim);

	print "<P><table cellspacing=0>\n",
	"<tr><td>�^�C�g��</td>",
	"<td>�F <b><font color=\"$sub_color\">$v_sub</font></b></td></tr>\n",
	"<tr><td>���e��</td><td>�F $date</td></tr>\n",
	"<tr><td>���e��</td><td>�F <b>$v_nam</b> ";
	if ($v_eml && $v_sml eq '0') {
		print "&nbsp; &lt;<a href=\"mailto:$v_eml\" class=num>$v_eml</a>&gt;";
	}
	print "</td></tr>\n";
	if ($v_url) {
		print "<tr><td>�Q�Ɛ�</td><td>�F ",
		"<a href=\"http://$v_url\" target=\"_blank\">",
		"http://$v_url</a></td></tr>\n" 
	}
	print "</table><blockquote>$v_msg</blockquote><P>\n";

	if (@new > 1) {
		print "<hr width='95%'><b style='text-indent:18'>- �֘A�ꗗ�c���[</b>\n",
		"�i$treehead ���N���b�N����ƃc���[�S�̂��ꊇ�\\�����܂��j<br>\n";

		$x=0;
		print "<UL>\n";
		foreach (@new) {
			($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$lt,$ho,$pw,$wrap,$oya,$sml) = split(/<>/);
			while ($x > $lx) { print "</UL>\n"; $x--; }
			while ($x < $lx) { print "<UL>\n"; $x++; }

			# �L���^�C�g��������
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

	# �ԐM�t�H�[��
	&msg_form;
	print "</body>\n</html>\n";
	exit;
}

#----------------#
#  �ꊇ�\���@�\  #
#----------------#
sub allread {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wrap,$oya,$sml,$date);

	# HTML���o��
	&header;
	print <<"EOM";
[<a href="$script?page=$page&mode=$in{'act'}">���X�g�ւ��ǂ�</a>]<br>
<table width="100%"><tr><th bgcolor="#004080">
<font color="#FFFFFF">�ꊇ�\\��</font></th></tr></table>
EOM
	# �ߋ����O�̏ꍇ
	if ($in{'act'} eq "past") {
		# ���O�t�@�C�����`
		if ($in{'pastlog'}) {
			$count = $in{'pastlog'};
		} else {
			open(NO,"$nofile") || &error("Open Error : $nofile");
			$count = <NO>;
			close(NO);
		}
		$logfile = sprintf("%s%04d\.cgi", $pastdir,$count);
	}

	# �e�L�����o��
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

			# �L���^�C�g��������
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

		# ���������N
		if ($autolink) { &auto_link($msg); }

		# ���p���F�ύX
		if ($refcolor) {
			$msg =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
		}
		# �}�\���[�h
		if ($wrap eq 'pre') {
			$msg =~ s/<br>/\n/g;
			$msg = "<pre>$msg</pre>";
		}

		$date = &get_time($t);
		print "<a name=\"$no\"></a>\n",
		"<table border=1 width='95%' cellpadding=5>\n",
		"<tr><td bgcolor=\"$tbl_color\"><table cellspacing=0>",
		"<tr><td>�^�C�g��</td><td>�F ",
		"<font color=\"$sub_color\"><b>$sub</b></font></td></tr>\n",
		"<tr><td>�L��No</td><td>�F <b>$no</b></td></tr>\n",
		"<tr><td>���e��</td><td>�F $date</td></tr>\n",
		"<tr><td>���e��</td><td>�F <b>$nam</b> ";
		if ($eml && $sml eq '0') {
			print "&nbsp; &lt;<a href=\"mailto:$eml\" class=num>$eml</a>&gt;";
		}
		print "</td></tr>\n";
		if ($url) {
			print "<tr><td>�Q�Ɛ�</td><td>�F ",
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
			"<input type=submit value=\"�ԐM����\"></form></div>\n";
		}
		print "</td></tr></table><br>\n";
	}
	print "</div>\n</body>\n</html>\n";
	exit;
}

#--------------------#
#  �V�����\�[�g�\��  #
#--------------------#
sub newsort {
	local($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$tim,$ho,$pw,$wrp,$oya,$sml,$date);

	&header;
	print <<"EOM";
[<a href="$script?page=$page">���X�g�ւ��ǂ�</a>]
<table width="100%"><tr><th bgcolor="#004080">
<font color="white">�V���L��</font></th></tr></table>
<br><div align="center">
EOM
	# �L���W�J
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$tim,$ho,$pw,$wrp,$oya,$sml) = split(/<>/);
		if ($pw eq 'DEL') { next; }
		if ($autolink) { &auto_link($msg); }

		# �A�z�z��
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

	# �\�[�g����
	$i=0;
	foreach (sort { ($cnt{$b} <=> $cnt{$a}) } keys(%cnt)) {
		$i++;
		if ($i > $sortcnt) { last; } # ���[�v�𔲂���

		# ���p���F�ύX
		if ($refcolor) {
			$msg{$_} =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
		}
		# PRE�@�\
		if ($wrp{$_} eq "pre") {
			$msg{$_} =~ s/<br>/\n/g;
			$msg{$_} = "<pre>$msg{$_}</pre>";
		}

		$date = &get_time($cnt{$_});

		print "<table border=1 width='95%' cellpadding=5>\n",
		"<tr><td bgcolor=\"$tbl_color\">\n",
		"<table cellspacing=0>",
		"<tr><td>�^�C�g��</td><td>�F ",
		"<font color=\"$sub_color\"><b>$sub{$_}</b></font></td></tr>",
		"<tr><td>�L��No</td><td>�F <b>$_</b> &nbsp;&nbsp;",
		"[<a href=\"$script?mode=allread&no=$oya{$_}\">�֘A�L��</a>]</td></tr>\n",
		"<tr><td>���e��</td><td>�F $date</td></tr>\n",
		"<tr><td>���e��</td><td>�F <b>$nam{$_}</b> ";
		if ($eml{$_} && $sml{$_} eq '0') {
			print "&nbsp; &lt;<a href=\"mailto:$eml{$_}\" class=num>",
			"$eml{$_}</a>&gt;";
		}
		print "</td></tr>\n";
		if ($url{$_}) {
			print "<tr><td>�Q�Ɛ�</td><td>�F ",
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
		"<input type=submit value=\"�ԐM����\"></div></form>\n",
		"</td></tr></table><br>\n";
	}
	print "</div>\n</body>\n</html>\n";
	exit;
}

#------------------#
#  ���e�t�H�[����  #
#------------------#
sub msg_form {
	# �N�b�L�[���擾
	local($cname, $cmail, $curl, $cpwd, $cpv, $csmail) = &get_cookie;

	# �C����
	if ($_[0] eq "edt") {
		($type,$cname,$cmail,$curl,$csmail,$res_sub,$res_msg,$wrap) = @_;
		if (!$wrap) { $wrap='soft'; }
		print "[<a href=\"javascript:history.back()\">�߂�</a>]\n",
		"<h3>�C���t�H�[��</h3>\n",
		"<form action=\"$script\" method=\"POST\">\n",
		"<input type=hidden name=mode value=\"usr_edt\">\n",
		"<input type=hidden name=action value=\"edit\">\n",
		"<input type=hidden name=pwd value=\"$in{'pwd'}\">\n",
		"<input type=hidden name=no value=\"$in{'no'}\">\n";
	# �ԐM��
	} elsif ($mode eq 'msgview') {
		$wrap='soft';
		print "<hr width='95%'><a name=\"msg\"></a>\n",
		"<b style='text-indent:18'>- �ԐM�t�H�[��</b>\n",
		"�i���̋L���ɕԐM����ꍇ�͉��L�t�H�[�����瓊�e���ĉ������j<br>\n",
		"<form action=\"$regist\" method=\"POST\">\n",
		"<input type=hidden name=mode value=\"form\">\n",
		"<input type=hidden name=page value=\"$page\">\n",
		"<input type=hidden name=action value=\"res_msg\">\n",
		"<input type=hidden name=no value=\"$in{'no'}\">\n",
		"<input type=hidden name=oya value=\"$in{'oya'}\">\n";
	# �V�K��
	} else {
		$wrap='soft';
		print "<hr width='95%'><P><a name=\"msg\"></a><div align='center'>\n",
		"<b><big>���b�Z�[�W���ǂ����E�E</big></b></a></div>\n",
		"<P><form action=\"$regist\" method=\"POST\">\n",
		"<input type=hidden name=mode value=\"form\">\n",
		"<input type=hidden name=page value=\"$page\">\n",
		"<input type=hidden name=no value=\"new\">\n";
	}

	print "<blockquote><table border=0 cellspacing=0 cellpadding=1>\n",
	"<tr><td nowrap><b>���Ȃ܂�</b></td>",
	"<td><input type=text name=name size=28 value=\"$cname\"></td></tr>\n",
	"<tr><td nowrap><b>�d���[��</b></td>",
	"<td><input type=text name=email size=28 value=\"$cmail\"> ",
	"<select name=smail>\n";

	@sm = ('�\��', '��\��');
	if ($csmail eq "") { $csmail=0; }
	foreach (0, 1) {
		if ($csmail == $_) {
			print "<option value=\"$_\" selected>$sm[$_]\n";
		} else {
			print "<option value=\"$_\">$sm[$_]\n";
		}
	}

 	print "</select></td></tr>\n",
	"<tr><td nowrap><b>�^�C�g��</b></td>",
	"<td><input type=text name=sub size=38 value=\"$res_sub\"></td></tr>\n",
	"<tr><td colspan=2><b>���b�Z�[�W</b>&nbsp;&nbsp;&nbsp;";

	@w1 = ('�蓮���s', '�������s', '�}�\���[�h');
	@w2 = ('soft', 'hard', 'pre');
	foreach (0 .. 2) {
		if ($wrap eq $w2[$_]) {
			print "<input type=radio name=wrap value=\"$w2[$_]\" checked>$w1[$_]\n";
		} else {
			print "<input type=radio name=wrap value=\"$w2[$_]\">$w1[$_]\n";
		}
	}

	# �v���r���[�̃`�F�b�N
	if ($cpv eq "on") { $checked = "checked"; }

	print "<br><textarea name=message rows=10 cols=62 wrap=soft>$res_msg</textarea>",
	"</td></tr><tr><td nowrap><b>�t�q�k</b></td>",
	"<td><input type=text name=url size=58 value=\"http://$curl\"></td></tr>\n";

	if ($_[0] eq "edt") {
		print "<tr><td></td><td><input type=submit value=' �L�����C������ '></td>\n",
		"</tr></table></form></blockquote>\n";
	} else {
		print <<"EOM";
<tr>
  <td nowrap><b>�p�X���[�h</b></td>
  <td><input type=password name=pwd size=8 value="$cpwd" maxlength=8>
	(�p������8�����ȓ�)</td>
</tr>
<tr>
  <td></td>
  <td><input type=submit value=" �L���𓊍e���� ">
	 &nbsp; <input type=checkbox name=pview value="on" $checked>�v���r���[</td>
</tr>
</table>
</form>
</blockquote>
<hr width="95%">
<div align="center"><form action="$script" method="POST">
<input type=hidden name=page value="$page">
<font color="$sub_color">
- �ȉ��̃t�H�[�����玩���̓��e�L�����C���E�폜���邱�Ƃ��ł��܂� -</font><br>
���� <select name=mode>
<option value="usr_edt">�C��
<option value="usr_del">�폜</select>
�L��No <input type=text name=no size=4>
�p�X���[�h <input type=password name=pwd size=6>
<input type=submit value="���M"></form>
<hr width="95%"></div>
EOM
	}
}

#----------------#
#  �L���C������  #
#----------------#
sub usr_edt {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$lt,$ho,$pw,$wrp,$oya,$sml,$res);

	# �t�H�[�����e�̃`�F�b�N
	$in{'no'} =~ s/\D//g;
	if ($in{'no'} eq '' || $in{'pwd'} eq '')
		{ &error("�L��NO�܂��̓p�X���[�h�̋L������������܂�"); }

	if ($in{'action'} eq "edit") {
		# ���̓`�F�b�N
		&chk_form;

		# ���b�N����
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
	if (!$flag) { &error("�Y���̋L������������܂���"); }
	if ($pw2 eq "") { &error("�p�X���[�h���ݒ肳��Ă��܂���"); }
	$check = &decrypt($in{'pwd'}, $pw2);
	if ($check ne "yes") { &error("�p�X���[�h���Ⴂ�܂�"); }

	@wrap1 = ('�蓮���s', '�������s', '�}�\���[�h');
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
		if ($in{'smail'} == 1) { $in{'email'} = '��\��'; }

		&header;
		print "<h4>- �ȉ��̂Ƃ���C�����������܂��� -</h4>\n";
		print "<table><tr><td>���O</td><td>�F $in{'name'}</td></tr>\n";
		print "<tr><td>e-mail</td><td>�F $in{'email'}</td></tr>\n";
		print "<tr><td>�^�C�g��</td><td>�F $in{'sub'}</td></tr>\n";
		print "<tr><td>URL</td><td>�F $in{'url'}</td></tr>\n";
		print "<tr><td valign=top>�L��</td><td>�F<P>$in{'message'}</td></tr>\n";
		print "</table><form action=\"$script\">\n";
		print "<input type=submit value='���X�g�ɖ߂�'></form>\n";
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
#  �L���폜����  #
#----------------#
sub usr_del {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$tim,$ho,$pw,$wr,$oya,$sml,$res,$date);

	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	# �t�H�[�����e�̃`�F�b�N
	$in{'no'} =~ s/\D//g;
	if ($in{'no'} eq '' || $in{'pwd'} eq '')
		{ &error("�L��NO�܂��̓p�X���[�h�̋L������������܂�"); }

	# �m�F���
	if ($in{'keyno'} eq "") {
		$flag=0;
		open(IN,"$logfile") || &error("Open Error : $logfile");
		$top = <IN>;
		while (<IN>) {
			($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml,$res) = split(/<>/);
			if ($in{'no'} == $no) { $flag=1; last; }
		}
		close(IN);
		if (!$flag) { &error("�Y���̋L���͌�������܂���"); }
		if ($pw eq "") { &error("���̋L���iNo $in{'no'}�j�͍폜�L�[���ݒ肳��Ă��܂���"); }
		# �ƍ�
		$match = &decrypt($in{'pwd'}, $pw);
		if ($match ne "yes") { &error("�폜�L�[���Ⴂ�܂�"); }

		if ($url) { $url = "http://$url"; }
		&header;
		print "<div align='center'><h3>�ȉ��̋L����{���ɍ폜���܂����H</h3>\n",
		"<table border=1 bgcolor=\"$tbl_color\" cellpadding=10 width='80%'>",
		"<tr><td><table>\n",
		"<tr><td>�L��No</td><td>�F <b>$no</b></td></tr>\n",
		"<tr><td>���e��</td><td>�F $dat</td></tr>\n",
		"<tr><td>���e��</td><td>�F <b>$nam</b></td></tr>\n";
		print "<tr><td>E-Mail</td><td>�F $eml</td></tr>\n" if ($eml && $sml eq '0');
		print "<tr><td>�t�q�k</td><td>�F $url</td></tr>\n" if ($url);
		print "<tr><td>�^�C�g��</td><td>�F 
			<font color=\"$sub_color\"><b>$sub</b></font></td></tr>",
		"</table></td></table>\n",
		"<P><table><tr><td>\n",
		"<form action=\"$script\" method=POST>\n",
		"<input type=hidden name=mode value=usr_del>\n",
		"<input type=hidden name=no value=\"$in{'no'}\">\n",
		"<input type=hidden name=pwd value=\"$in{'pwd'}\">\n",
		"<input type=hidden name=keyno value=\"$re\">\n",
		"<input type=submit value='�{���ɍ폜����'></td></form>\n",
		"<td width=15></td><td><form>",
		"<input type=button value='�L�����Z������' onClick=\"history.back()\">",
		"</td></form></tr></table></div>\n",
		"</body>\n</html>\n";
		exit;
	}

	# ���b�N�J�n
	&lock if ($lockkey);

	# ���O��ǂݍ���
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
			$_ = "$no<>$re<>$lx<><s>���e�ҍ폜</s><><><>(�폜)<>$dat<>(���e�҂ɂ��폜����܂���)<>$tim<>$ho<>DEL<>$wr<>$oya<>$sml<>$res<>";
		} elsif ($no == $in{'keyno'}) {
			if ($res > 0) { $res--; }
			$_ = "$no<>$re<>$lx<>$sub<>$eml<>$url<>$nam<>$dat<>$msg<>$tim<>$ho<>$pw<>$wr<>$oya<>$sml<>$res<>";
		}
		push(@new,"$_\n");
	}
	close(IN);

	if ($flag == 0) { &error("�Y���L���͌�����܂���"); }
	elsif ($flag == 2) { &error("�p�X���[�h���ݒ肳��Ă��܂���"); }
	elsif ($flag == 3) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# ���O���X�V
	unshift(@new,$top);
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# ���b�N����
	&unlock if ($lockkey);

	# ���X�g�\�����ɂ��ǂ�
	&list_view;
}

#------------------#
#  �N�b�L�[���擾  #
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
#  �p�X���[�h�ƍ�����  #
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
#  �����t�H�[��  #
#----------------#
sub find {
	&header;
	print <<"EOM";
[<a href="$script?page=$page&list=$in{'list'}">���X�g�ɖ߂�</a>]
<table width="100%"><tr><th bgcolor="#004080">
  <font color="#FFFFFF">�L�[���[�h����</font></th></tr></table>
<P><a name="SEARCH"></a>
<UL>
<LI>����������<b>�L�[���[�h</b>����͂��A����������I�����āu�����v�������Ă��������B
<LI>�����̃L�[���[�h����͂���Ƃ��́A<b>���p�X�y�[�X</b>�ŋ�؂��ĉ������B
<form action="$script" method="POST">
<input type=hidden name=mode value="find">
<input type=hidden name=list value="$in{'list'}">
�L�[���[�h�F<input type=text name=word size=35 value="$in{'word'}">
�����F<select name="cond">
EOM
	foreach ('AND', 'OR') {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select> �\\���F<select name=view>\n";
	foreach (10,15,20,25,30) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_��\n";
		} else {
			print "<option value=\"$_\">$_��\n";
		}
	}
	print "</select> <input type=submit value=' ���� '></form></UL>\n";

	# ���[�h�����̎��s�ƌ��ʕ\��
	if ($in{'word'} ne "") { &search; }

	print "</body>\n</html>\n";
	exit;
}

#----------------#
#  �����������s  #
#----------------#
sub search {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml,$date,$back,$next);

	# ���͓��e�𐮗�
	$in{'word'} =~ s/�@/ /g;
	@wd = split(/\s+/, $in{'word'});

	# ���b�N�����F�T�[�o���ׂ��l�������d�N������̂���
	&lock if ($lockkey);

	# �t�@�C����ǂݍ���
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

	# �����I��
	$count = @new;
	print "�������ʁF<b>$count</b>��\n";
	if ($in{'page'} eq '') { $in{'page'} = 0; }
	$end_data = @new - 1;
	$page_end = $in{'page'} + $in{'view'} - 1;
	if ($page_end >= $end_data) { $page_end = $end_data; }

	# �L�[���[�h��URL�G���R�[�h
	$enwd = &url_enc($in{'word'});

	$next = $page_end + 1;
	$back = $in{'page'} - $in{'view'};

	if ($back_line >= 0) {
		print "[<a href=\"$script?mode=$mode&page=$back&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">�O��$in{'view'}��</a>]\n";
	}
	if ($page_end ne "$end_data") {
		print "[<a href=\"$script?mode=$mode&page=$next&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">����$in{'view'}��</a>]\n";
	}

	# �q�b�g�����L����\��
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
		"<tr><td>�^�C�g��</td><td>�F ",
		"<font color=\"$sub_color\"><b>$sub</b></font></td></tr>\n",
		"<tr><td>�L��No</td><td>�F <b>$no</b> &nbsp;&nbsp;";
		if ($in{'pastlog'}) {
			print "[<a href=\"$script?mode=allread&no=$oya&pastlog=$in{'pastlog'}&act=past\">�֘A�L��</a>]</td></tr>\n";
		} else {
			print "[<a href=\"$script?mode=allread&no=$oya\">�֘A�L��</a>]</td></tr>\n";
		}
		print "<tr><td>���e��</td><td>�F $date</td></tr>\n",
		"<tr><td>���e��</td><td>�F <b>$nam</b> ";
		if ($eml && $sml eq '0') {
			print "&nbsp; &lt;<a href=\"maito:$eml\" class=num>$eml</a>&gt;";
		}
		print "</td></tr>\n";
		if ($ur) {
			print "<tr><td>�Q�Ɛ�</td><td>�F ",
			"<a href=\"http://$url\" target=\"_blank\">",
			"http://$url</a></td></tr>\n";
		}
		print "</table><blockquote>$msg</blockquote><hr>\n";
	}
	if ($count) {
		print "<a href=\"#SEARCH\">��TOP</a>\n";
	}
	if ($back_line >= 0) {
		print "[<a href=\"$script?mode=$mode&page=$back&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">�O��$in{'view'}��</a>]\n";
	}
	if ($page_end ne $end_data) {
		print "[<a href=\"$script?mode=$mode&page=$next&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">����$in{'view'}��</a>]\n";
	}

	# �t�@�C�����b�N����
	&unlock if ($lockkey);
}

#--------------#
#  ���������N  #
#--------------#
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(http\:\/\/[\w\.\~\-\/\?\&\=\;\#\:\%\+\@]+)/$1<a href=\"$2\" target=\"_blank\">$2<\/a>/g;
}

#----------------#
#  �ߋ����O�\��  #
#----------------#
sub past_view {
	open(IN,"$nofile") || &error("Open Error : $nofile");
	$pastno = <IN>;
	close(IN);
	$pastno = sprintf("%04d", $pastno);
	if (!$in{'pastlog'}) { $in{'pastlog'} = $pastno; }

	&header;
	print <<"EOM";
[<a href="$script?">�f���ɖ߂�</a>]
<table width="100%"><tr><th bgcolor="#004080">
  <font color="#FFFFFF">�ߋ����O [ $in{'pastlog'} ]</font></th></tr></table>
<P><a name="SEARCH"></a>
<form action="$script" method="POST">
<input type=hidden name=mode value=past>
<table cellpadding=0 cellspacing=0>
<tr><td>�ߋ����O�F<select name=pastlog>
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
	print "</select>\n<input type=submit value='�ړ�'></td></form>\n";
	print "<td width=40></td><td>\n";
	print "<form action=\"$script\" method=GET>\n";
	print "<input type=hidden name=mode value=past>\n";
	print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
	print "���[�h�����F<input type=text name=word size=30 value=\"$in{'word'}\">\n";
	print "�����F<select name=cond>\n";

	foreach ('AND', 'OR') {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select> �\\���F<select name=view>\n";
	if ($in{'view'} eq "") { $in{'view'} = $p_tree; }
	foreach (10,15,20,25,30) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_��\n";
		} else {
			print "<option value=\"$_\">$_��\n";
		}
	}
	print "</select> <input type=submit value='����'>",
	"</td></form></tr></table><hr>\n";

	# �t�@�C�����`
	$logfile = "$pastdir$in{'pastlog'}\.cgi";

	# ���[�h��������
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
#  �L���^�C�g��������  #
#----------------------#
sub cut_subject {
	# �������ɖ����Ȃ����͖̂߂�
	if (length($_[0]) <= $sub_length) { return $_[0]; }

	# �J�b�g����
	($_[0], $folded) = &fold($_[0], $sub_length);
	$_[0] .= '..';

	return $_[0];
}

#----------------------#
#  �y�[�W�ړ��t�H�[��  #
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
		print "<input type=submit value=\"�O�y�[�W\"></td></form>\n";
	}
	if ($next < $i) {
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n" if ($in{'pastlog'} ne "");
		print "<input type=hidden name=page value=\"$next\">\n";
		print "<input type=hidden name=mode value=\"$mode\">\n" if ($mode eq 'past');
		print "<input type=hidden name=list value=\"$in{'list'}\">\n";
		print "<input type=submit value=\"���y�[�W\"></td></form>\n";
	}
	print "<td width=10></td><td class=num>";

	# �y�[�W�ړ��{�^���\��
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
#  URL�G���R�[�h  #
#-----------------#
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#------------------#
#  �`�F�b�N���[�h  #
#------------------#
sub check {
	&header;
	print "<h2>Check Mode</h2>\n<UL>\n";

	# ���O
	print "<LI>���O�p�X�F";
	if (-e $logfile) {
		print "OK\n";
		# �p�[�~�b�V����
		print "<LI>���O�p�[�~�b�V�����F";
		if (-r $logfile && -w $logfile) { print "OK\n"; }
		else { print "NG �� $logfile\n"; }
	} else {
		print "NG �� $logfile\n";
	}

	# ���b�N�f�B���N�g��
	print "<LI>���b�N�`���F";
	if ($lockkey == 0) { print "�ݒ�Ȃ�\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }

		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<LI>���b�N�f�B���N�g���F$lockdir\n";

		if (-d $lockdir) { print "<LI>���b�N�f�B���N�g���̃p�X�FOK\n"; }
		else { print "<LI>���b�N�f�B���N�g���̃p�X�FNG �� $lockdir\n"; }

		if (-r $lockdir && -w $lockdir && -x $lockdir) {
			print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�����FOK\n";
		} else {
			print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�����FNG �� $lockdir\n";
		}
	}

	# �ߋ����O
	print "<LI>�ߋ����O�F";
	if ($pastkey == 0) { print "�ݒ�Ȃ�\n"; }
	else {
		print "�ݒ肠��\n";

		# NO�t�@�C��
		if (-e $nofile) {
			print "<LI>NO�t�@�C���p�X�FOK\n";
			if (-r $nofile && -w $nofile) { print "<LI>NO�t�@�C���p�[�~�b�V�����FOK\n"; }
			else { print "<LI>NO�t�@�C���p�[�~�b�V�����FNG �� $nofile\n"; }
		} else { print "<LI>NO�t�@�C���̃p�X�FNG �� $nofile\n"; }

		# �f�B���N�g��
		if (-d $pastdir) {
			print "<LI>�ߋ����O�f�B���N�g���p�X�FOK\n";
			if (-r $pastdir && -w $pastdir && -x $pastdir) {
				print "<LI>�ߋ����O�f�B���N�g���p�[�~�b�V�����FOK\n";
			} else {
				print "<LI>�ߋ����O�f�B���N�g���p�[�~�b�V�����FNG �� $pastdir\n";
			}
		} else { print "<LI>�ߋ����O�f�B���N�g���̃p�X�FNG �� $pastdir\n"; }
	}

	print "</body></html>\n";
	exit;
}

__END__

