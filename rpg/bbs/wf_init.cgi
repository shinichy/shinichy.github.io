#��������������������������������������������������������������������
#��  Web Forum v4.07 (2002/09/27)
#��  Copyright(C) KENT WEB 2002
#��  webmaster@kent-web.com
#��  http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'Web Forum v4.07';
#��������������������������������������������������������������������
#��[ ���ӎ��� ]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B
#��������������������������������������������������������������������
#
# [�ݒu��] ���������̓p�[�~�b�V����
#
#    public_html / index.html (�z�[���y�[�W)
#       |
#       +-- bbs / wforum.cgi   [755]
#            |    wf_regi.cgi  [755]
#            |    wf_admin.cgi [755]
#            |    wf_init.cgi  [644]
#            |    wf_log.cgi   [666]
#            |    jcode.pl     [644]
#            |    fold.pl      [644]
#            |    pastno.dat   [666] ... (�ߋ����O�p)
#            |    note.html
#            |    title.gif
#            |
#            +-- past [777] / 0001.cgi [666] ... (�ߋ����O�p)
#            |
#            +-- lock [777] /
#

#------------#
#  ��{�ݒ�  #
#------------#

# �f���^�C�g����
$title = "�Q�[���U���f����";

# �^�C�g���̐F
$t_color = "#004080";

# �^�C�g���̃T�C�Y
$t_point = '18pt';

# �^�C�g���^�{���̕����^�C�v
$t_face = 'MS UI Gothic';

# �^�C�g���摜���g�p����Ƃ�
$t_img = "";
$t_w = 151; 	# ���T�C�Y�i�s�N�Z���j
$t_h = 28;	# �c�T�C�Y�i�s�N�Z���j

# �{���̕����傫���i�|�C���g��:�X�^�C���V�[�g�j
$pt = '10pt';

# �ő�L����
$max = 200;

# �߂��̂t�q�k(index.html�Ȃ�)
$home = "../index.html";

# �ǎ��E�w�i�F�E�����F�Ȃ�
$bg = "";		# �ǎ��̎w�� (http://����L�q)
$bc = "#EEEEEE";	# �w�i�F
$te = "#004080";	# �����F
$li = "#0000FF";	# �����N�F�i���K��j
$vl = "#008080";	# �����N�F�i���K��j
$al = "#DD0000";	# �����N�F�i�K�⒆�j

# �X�N���v�gURL
$script = './wforum.cgi';

# ���O�t�@�C����
$logfile = './wf_log.cgi';

# �Ǘ��t�@�C��URL
$admin = './wf_admin.cgi';

# �������݃t�@�C��
$regist = './wf_regi.cgi';

# ���ӎ����y�[�WURL
$note = './note.html';

# ���b�N�t�@�C���@�\
#   0 : �s�Ȃ�Ȃ�
#   1 : �s�Ȃ��isymlink�֐����j
#   2 : �s�Ȃ��imkdir�֐����j
$lockkey = 2;

# ���b�N�t�@�C��
$lockfile = './lock/wforum.lock';

# URL���������N (0=no 1=yes)
$autolink = 1;

# �L���� [�薼] �̐F
$sub_color = "#BC0000";

# �L�����n�̐F�i�ꊇ�\�������j
$tbl_color = "#FFFFFF";

# �L����NEW�}�[�N��t���鎞��
$new_time = 48;

# NEW�}�[�N�̕\���`��
#  �� �摜���g�p����ꍇ�ɂ� $newmark = '<img src="./new.gif">';
#     �Ƃ����悤�� IMG�^�O���L�q���Ă��悢
$newmark = '<font color="#FF3300">new!</font>';

# �L��NO�̐F
$no_color = "#800000";

# �V���L���ꊇ�\���̋L����
$sortcnt = 10;

# �ł�����c���[�\����
$p_tree = 10;

# ���X�g�ɕ\������u�L���^�C�g���v�̍ő咷�i�������F���p�������Z�j
$sub_length = 30;

# ���[���A�h���X�̓��͂�K�{ (0=no 1=yes)
$in_email = 0;

# ���X��������c���[���g�b�v�ֈړ� (0=no 1=yes)
$top_sort = 1;

# ���X�͉����珇�ɕt���� (0=no 1=yes)
$bot_res = 1;

# ���p���F�ύX
#  �� �����ɐF�w����s���Ɓu���p���v��F�ύX���܂�
#  �� ���̋@�\���g�p���Ȃ��ꍇ�͉����L�q���Ȃ��ŉ����� ($refcolor="";)
$refcolor = "#804000";

# �L���̍X�V�́umethod=POST�v����i�Z�L�����e�B�΍�j
#  0 : no
#  1 : yes
$postonly = 1;

# ���e������ƃ��[���ʒm���� : sendmail�K�{
#  0 : �ʒm���Ȃ�
#  1 : �ʒm����i�����̋L���͑��M���Ȃ��j
#  2 : �ʒm����i�����̋L�������M����j
$mailing = 0;

# ���[���ʒm����ۂ̃��[���A�h���X
$mailto = 'xxx@xxx.xxx';

# sendmail�p�X�i���[���ʒm���鎞�j
$sendmail = '/usr/lib/sendmail';

# �c���[�̃w�b�_�[�L��
$treehead = "��";

# �ߋ����O�@�\ (0=no 1=yes)
$pastkey = 1;

# �ߋ����O�J�E���g�t�@�C��
$nofile = './pastno.dat';

# �ߋ����O�̃f�B���N�g���i�Ō�� / �ŕ���)
$pastdir = './past/';

# �ߋ����O�P�y�[�W����̍ő�s��
#  �� ����𒴂���Ǝ����I�Ɏ��t�@�C���𐶐����܂�
$max_line = 650;

# �A�N�Z�X�����i���p�X�y�[�X�ŋ�؂�j
#  �� ���ۂ���z�X�g������IP�A�h���X���L�q�i�A�X�^���X�N�j
#  �� �L�q�� $deny = '*.anonymizer.com *.denyhost.xx.jp 211.154.120.*';
$deny = '';

#------------#
#  �ݒ芮��  #
#------------#

$headflag=0;

#----------------#
#  �f�R�[�h����  #
#----------------#
sub decode {
	local($buf, $key, $val);

	$post_flag=0;
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag=1;
		if ($ENV{'CONTENT_LENGTH'} > 25000) { &error("���e�ʂ��傫�����܂�"); }
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else { $buf = $ENV{'QUERY_STRING'}; }
	foreach (split(/&/, $buf)) {
		($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# S-JIS�ϊ�
		&jcode'convert(*val, "sjis", "", "z");

		# �^�O����
		$val =~ s/&/&amp;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/"/&quot;/g;

		# �s�v�ȉ��s���폜
		if ($key ne "message") {
			$val =~ s/\r//g;
			$val =~ s/\n//g;
		}
		$in{$key} = $val;
	}
	$mode = $in{'mode'};
	$page = $in{'page'};
	if ($page eq "") { $page = 0; }
	$in{'url'} =~ s/^http\:\/\///;
	$in{'pastlog'} =~ s/\D//g;

	# �������s
	if (($mode eq "form" && $in{'pview'} ne "on" && $in{'wrap'} eq "hard") || ($mode eq "regist" && $in{'wrap'} eq "hard")) {
		local($tmp) = '';
		while (length $in{'message'}) {
			($folded, $in{'message'}) = &fold ($in{'message'}, 64);
			$tmp .= "$folded<br>";
		}
		$in{'message'} = $tmp;
	}
	# ���s�R�[�h����
	$in{'message'} =~ s/\r\n/<br>/g;
	$in{'message'} =~ s/\r/<br>/g;
	$in{'message'} =~ s/\n/<br>/g;
	while ($in{'message'} =~ /<br>$/) { $in{'message'} =~ s/<br>$//g; }

	# �^�C���]�[������{���Ԃɍ��킹��
	$ENV{'TZ'} = "JST-9";
}

#--------------#
#  ���b�N����  #
#--------------#
sub lock {
	local($retry) = 5;
	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 60) { &unlock; }
	}
	# symlink�֐������b�N
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	# mkdir�֐������b�N
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	}
	$lockflag=1;
}

#--------------#
#  ���b�N����  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }
	$lockflag=0;
}

#------------------#
#  HTML�̃w�b�_�[  #
#------------------#
sub header {
	if ($headflag) { return; }
	if ($bg) { $bg = "background=\"$bg\""; }
	print <<"EOM";
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
<STYLE type="text/css">
<!--
body,tr,td,th { font-size:$pt; font-family:"$t_face"; }
a:hover       { text-decoration:underline; color:$al; }
big           { font-size:12pt; }
.num           { font-size:9pt; font-family:Verdana; }
-->
</STYLE>
<title>$title</title></head>
<body bgcolor="$bc" text="$te" link="$li" vlink="$vl" alink="$al" $bg>
EOM
	$headflag = 1;
}

#--------------#
#  �G���[����  #
#--------------#
sub error {
	&unlock if ($lockflag);

	&header;
	print <<"EOM";
<div align="center"><h3>ERROR !</h3>
<font color="#dd0000">$_[0]</font>
<form>
<input type=button value="�O��ʂɂ��ǂ�" onClick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#----------------#
#  �A�N�Z�X����  #
#----------------#
sub axs_check {
	# �z�X�g�����擾
	&get_host;

	local($flag)=0;
	foreach (split(/\s+/, $deny)) {
		s/\*/\.\*/g;
		if ($host =~ /$_/i) { $flag=1; last; }
	}
	if ($flag) { &error("�A�N�Z�X��������Ă��܂���"); }
}

#--------------#
#  ���Ԃ̎擾  #
#--------------#
sub get_time {
	local($time, $log) = @_;

	if (!$time) { $time = time };
	($min,$hour,$day,$mon,$year,$wday) = (localtime($time))[1..6];

	if ($log eq "log") {
		$date = sprintf("%02d/%02d-%02d:%02d", $mon+1,$day,$hour,$min);
		return $date;
	} else {
		@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
		$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
				$year+1900,$mon+1,$day,$week[$wday],$hour,$min);
		return $date;
	}
}

#----------------#
#  �z�X�g���擾  #
#----------------#
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($host eq "" || $host eq $addr) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2) || $addr;
	}
}

#----------------#
#  ���̓`�F�b�N  #
#----------------#
sub chk_form {
	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	# �t�H�[���`�F�b�N
	if ($in{'name'} eq "" || $in{'message'} eq "")
		{ &error("���O���̓��b�Z�[�W�ɋL������������܂�"); }
	if ($in_email && $in{'email'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/)
		{ &error("E-Mail�̓��͂��s���ł�"); }
	# URL����
#	if ($in{'no'} eq 'new' && !$in{'url'})
#		{ &error("�ݒu�X�N���v�g��URL�L�q�͕K�{�ł�"); }
	# �薼����
	if ($in{'sub'} eq "") { &error("�u�薼�v�̓��̓����ł�"); }
}

1;

