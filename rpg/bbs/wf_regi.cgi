#!/usr/bin/perl

#��������������������������������������������������������������������
#�� Web Forum v4.07 <wf_regi.cgi> (2002/09/27)
#�� Copyright(C) KENT WEB 2002
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#------------#
#  ��{�ݒ�  #
#------------#

# �O���t�@�C����荞��
require './jcode.pl';
require './fold.pl';
require './wf_init.cgi';

#------------#
#  �ݒ芮��  #
#------------#

&decode;
&axs_check;
if ($mode eq "regist") { &regist; }
elsif ($mode eq "form" && $in{'pview'} ne "on") { &regist; }
elsif ($mode eq "form" && $in{'pview'} eq "on") { &preview; }
&error('�s���ȏ����ł�');

#----------------#
#  �������ݏ���  #
#----------------#
sub regist {
	local($count,$ango,$date);

	# ���̓`�F�b�N
	&chk_form;

	# ���b�N����
	&lock if ($lockkey);

	# ���O�t�@�C���ǂݍ���
	open(IN,"$logfile") || &error("Open Error : $logfile");
	@lines = <IN>;
	close(IN);

	# �J�E���g�t�@�C�����A�b�v
	$count = shift(@lines);
	$count =~ s/\n//;
	if ($count % 9999) { $count++; } else { $count=1; }

	# ��d���e�̋֎~
	$flag=0;
	foreach (@lines) {
		local(@f) = split(/<>/);
		if ($in{'name'} eq $f[6] && $in{'message'} eq $f[8]) { $flag=1; last; }
	}
	if ($flag) { &error("��d���e�͋֎~�ł�"); }

	# �N�b�L�[�𔭍s
	&set_cookie;

	# �p�X���[�h�Í���
	if ($in{'pwd'} ne "") { $ango = &encrypt($in{'pwd'}); }

	# ���Ԃ��擾
	$times = time;
	$date = &get_time($times, "log");

	## --- �e�L���̏ꍇ
	if ($in{'no'} eq 'new') {
		unshift (@lines,"$count<>no<>0<>$in{'sub'}<>$in{'email'}<>$in{'url'}<>$in{'name'}<>$date<>$in{'message'}<>$times<>$host<>$ango<>$in{'wrap'}<>$count<>$in{'smail'}<>0<>\n");
		@new = @lines;
	}
	## --- ���X�L���̏ꍇ
	else {
		## �c���[�\�[�g�u����v
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
				# ����c���[�̋L���� @new �ɔz�񕪊��i�����X�j
				if ($no == $in{'no'}) {
					$res++;
					push(@new,"$no<>$reno<>$lx<>$t<>$e<>$u<>$n<>$d<>$m<>$tm<>$h<>$a<>$w<>$OYA<>$smail<>$res<>\n");
				}
				# ����c���[�̋L���� @new �ɔz�񕪊�
				elsif ($in{'oya'} == $OYA) { push(@new,"$_\n"); }
				# �ʃc���[�̋L���� @tmp �ɔz�񕪊�
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
			# �z��ŏI����
			push(@new,@tmp);
		}
		## �c���[�\�[�g�u�Ȃ��v
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

				# ���e�L��
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
	# �ő�L��������
	@PAST=();
	if (@new > $max) {
		foreach (0 .. $#new) {
			# �ŏI���t�@�C����z�񂩂甲���o���ߋ����O�z���
			local($p_file) = pop(@new);
			push(@PAST,$p_file) if ($pastkey);

			local($no,$reno,$lx) = split(/<>/, $p_file);
			if ($#new+1 <= $max && $reno eq 'no') {
				last;
			}
		}
	}
	# ���O���X�V
	unshift(@new,"$count\n");
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# �ߋ����O����
	if (@PAST) { &pastlog; }

	# �t�@�C�����b�N����
	&unlock if ($lockkey);

	# ���[���ʒm
	if ($mailing == 2) { &mail_to; }
	elsif ($mailing == 1 && $in{'email'} ne $mailto) { &mail_to; }

	# ���e����
	&after;
}

#------------------#
#  �v���r���[���  #
#------------------#
sub preview {
	# ���̓`�F�b�N
	&chk_form;

	if ($in{'smail'} == 1) { $email = '��\��'; }
	else { $email = $in{'email'}; }

	&header;
	print <<"EOM";
<font color="$t_color"><big><b>- �ȉ��̓��e�Ń��b�Z�[�W�𓊍e���܂� -</b></big></font>
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
  <td><b>�^�C�g��</b></td>
  <td>�F <font color="$sub_color"><B>$in{'sub'}</B></font></td>
</tr>
<tr>
  <td><b>���e��</b></td>
  <td>�F <B>$in{'name'}</B></td>
</tr>
<tr>
  <td><b>�d���[��</b></td>
  <td>�F $email</td>
</tr>
<tr>
  <td><b>URL</b></td>
  <td>�F $in{'url'}</td>
</tr>
</table>
EOM
	@w1 = ('�蓮���s', '�������s', '�}�\���[�h');
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
<P><input type=submit value="���b�Z�[�W�𓊍e����"></form>
<P>[<A HREF="javascript:history.back()">���e�t�H�[���ɖ߂�</A>]
</body>
</html>
EOM
	exit;
}

#------------------------#
#  �������݌チ�b�Z�[�W  #
#------------------------#
sub after {
	if ($in{'url'}) { $in{'url'} = "http://$in{'url'}"; }

	# �c���[�g�b�v�ړ������̏ꍇ�͏������݌�̓g�b�v�y�[�W
	if ($top_sort) { $page = 0; }

	# ���p�F
	if ($refcolor) {
		$in{'message'} =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcolor\">$2<\/font>/g;
	}

	# �}�\���[�h
	if ($in{'wrap'} eq "pre") {
		$in{'message'} =~ s/<br>/\n/g;
		$in{'message'} = "<pre>$in{'message'}</pre>";
	}
	if ($in{'smail'} == 1) { $in{'email'} = '��\��'; }

	&header;
	print <<"EOM";
<center>
<b style="font-size:12pt;color:$sub_color">����ɏ������݂��������܂���</b>
<P><table border=1 cellpadding=10 width="90%">
<tr><td bgcolor="$tbl_color">
<table>
<tr>
  <td>�^�C�g��</td><td>�F <b style="color:$sub_color">$in{'sub'}</b></td>
</tr>
<tr>
  <td>���e��</td><td>�F <b>$in{'name'}</b></td>
</tr>
<tr>
  <td>e-mail</td><td>�F $in{'email'}</td>
</tr>
<tr>
  <td>�Q�Ɛ�</td><td>�F $in{'url'}</td>
</tr>
</table>
<br><br>
<blockquote>
$in{'message'}
</blockquote>
</td></tr></table>
<P><form action="$script" method="POST">
<input type=hidden name=page value="$page">
<input type=submit value="���X�g�ɂ��ǂ�">
</form>
</center>
</body>
</html>
EOM
	exit;
}

#--------------#
#  ���[�����M  #
#--------------#
sub mail_to {
	local($msg, $date2, $mail_sub, $mail_body);

	# ���[���^�C�g��
	$mail_sub = "[$count] $in{'sub'}";

	# ���[���{���̃^�O�E���s�𕜌�
	$msg = $in{'message'};
	$msg =~ s/<br>/\n/g;
	$msg =~ s/&lt;/</g;
	$msg =~ s/&gt;/>/g;
	$msg =~ s/&quot;/"/g;
	$msg =~ s/&amp;/&/g;

	if ($in{'url'}) { $in{'url'} = "http://$in{'url'}"; }
	$date2 = &get_time($times);

	# ���[���{��
	$mail_body = <<"EOM";
------------------------------------------------------------
���e���ԁF$date2
�z�X�g���F$host
�u���E�U�F$ENV{'HTTP_USER_AGENT'}

���e�Җ��F$in{'name'}
�d���[���F$in{'email'}
�^�C�g���F$in{'sub'}
�t�q�k  �F$in{'url'}
�R�����g�F

$msg
------------------------------------------------------------
EOM
	# JIS�R�[�h�ϊ�
	&jcode'convert(*mail_sub, 'jis', 'sjis');
	&jcode'convert(*mail_body, 'jis', 'sjis');

	# sendmail�N��
	if ($in{'email'} eq "") { $in{'email'} = $mailto; }
	open(MAIL,"| $sendmail -t") || &error("���[�����M�Ɏ��s���܂���");
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
#  �N�b�L�[�̔��s  #
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
#  �p�X���[�h�Í�����  #
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
#  �ߋ����O����  #
#----------------#
sub pastlog {
	local($past_flag)=0;

	# �ߋ����O�t�@�C�����`
	open(NO,"$nofile") || &error("Open Error : $nofile");
	$num = <NO>;
	close(NO);
#	$num = sprintf("%04d", $num);
#	$pastfile = "$pastdir$num\.cgi";
	$pastfile = sprintf("%s%04d\.cgi", $pastdir,$num);

	# �ߋ����O���J��
	open(IN,"$pastfile") || &error("Open Error : $pastfile");
	@data = <IN>;
	close(IN);

	# �K��̍s�����I�[�o�[����Ǝ��t�@�C������������
	if ($#data > $max_line) {
		$past_flag=1;

		# �J�E���g�t�@�C���X�V
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

	# �ߋ����O���X�V
	open(OUT,">$pastfile") || &error("Write Error : $pastfile");
	print OUT @data;
	close(OUT);

	if ($past_flag) { chmod(0666, $pastfile); }
}

__END__

