#!/usr/bin/perl

#��������������������������������������������������������������������
#�� Web Forum v4.07 <wf_admin.cgi> (2002/09/27)
#�� Copyright(C) KENT WEB 2002
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#============#
#  �ݒ荀��  #
#============#

# �O���t�@�C����荞��
require './jcode.pl';
require './wf_init.cgi';

# �p�X���[�h (���p�p������)
$pass = '0915';

#============#
#  �ݒ芮��  #
#============#

&decode;
if ($in{'pass'} eq "") { &enter; }
elsif ($mode eq "edit" && $in{'no'}) { &edit; }
elsif ($mode eq "edit2" && $in{'no'}) { &edit2; }
elsif ($mode eq "del" && $in{'no'}) { &del; }
&loglist;

#----------------#
#  ���O�{�����  #
#----------------#
sub loglist {
	local($no,$re,$lx,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya);

	if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	&header;
	print <<"EOM";
[<a href="$script">�߂�</a>]
<UL>
<LI>�c���[�̐擪�L�����폜����ƁA�c���[���ƈꊇ�폜����܂��B
<form action="$admin" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<select name=mode>
<option value="edit">�C��
<option value="del">�폜</select>
<input type=submit value="���M����">
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
#  �L���ҏW���  #
#----------------#
sub edit {
	local($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml);

	if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# ���O���J��
	open(IN,"$logfile") || &error("Can't open $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml) = split(/<>/);
		last if ($in{'no'} == $no);
	}
	close(IN);

	$msg =~ s/<br>/\r/g;

	# �ҏW�t�H�[�����o��
	&header;
	print <<"EOM";
[<a href="javascript:history.back()">�߂�</a>]
<UL>
<LI>�ύX�����������̂ݏC�����A�u���M����v�������Ă��������B
<form action="$admin" method=POST>
<input type=hidden name=mode value="edit2">
<input type=hidden name=no value="$in{'no'}">
<input type=hidden name=pass value="$in{'pass'}">
<table border=0>
<tr>
  <td><B>���e��</B></td>
  <td><input type=text name=name value="$nam" size=28></td>
</tr>
<tr>
  <td><B>�d���[��</B></td>
  <td><input type=text name=email value="$eml" size=28>
	<select name=smail>
EOM
	@sm = ('�\��', '��\��');
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
  <td><B>�^�C�g��</B></td>
  <td><input type=text name=sub value="$sub" size=38></td>
</tr>
<tr>
  <td colspan=2><B>���b�Z�[�W</B>
EOM
	@w1 = ('�蓮���s', '�������s', '�}�\���[�h');
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
  <td><B>�t�q�k</B></td>
  <td><input type=text name=url value="http://$url" size=55></td>
</tr>
</table>
<input type=submit value=" ���M���� "><input type=reset value="���Z�b�g">
</form>
</UL>
</body>
</html>
EOM
	exit;
}

#----------------#
#  �L���ҏW����  #
#----------------#
sub edit2 {
	local($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya,$sml,$res);

	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	$in{'url'} =~ s/^http\:\/\///;

	# ���b�N�J�n
	&lock if ($lockkey);

	# ���O���J��
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

	# ���O���X�V
	unshift(@new,$top);
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# ���b�N����
	&unlock if ($lockkey);

	# ������ʂɖ߂�
	&loglist;
}

#----------------#
#  �L���폜����  #
#----------------#
sub del {
	local($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya);

	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# ���b�N�J�n
	&lock if ($lockkey);

	# ���O���J��
	$flag=0;
	@new=();
	open(IN,"$logfile") || &error("Open Error : $logfile","LK");
	$top = <IN>;
	while (<IN>) {
		($no,$re,$x,$sub,$eml,$url,$nam,$dat,$msg,$t,$ho,$pw,$wr,$oya) = split(/<>/);

		if ($in{'no'} == $no) {
			# �e�L��
			if ($no == $oya) {
				$flag=1;
				next;
			# ���X�L��
			} else {
				next;
			}
		}
		if ($flag && $in{'no'} == $oya) { next; }
		push(@new,$_);
	}
	close(IN);

	# ���O���X�V
	unshift(@new,$top);
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# ���b�N����
	&unlock if ($lockkey);

	# ������ʂɖ߂�
	&loglist;
}

#------------#
#  �������  #
#------------#
sub enter {
	&header;
	print <<"EOM";
<div align="center">
<h4>�p�X���[�h����͂��Ă�������</h4>
<form action="$admin" method="POST">
<input type=password name=pass size=8>
<input type=submit value=" �F�� "></form>
</div><!-- $ver -->
</body>
</html>
EOM
	exit;
}

__END__

