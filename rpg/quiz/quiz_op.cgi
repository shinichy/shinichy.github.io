#!/usr/bin/perl
$version='2.03';
chdir('qqqsystems2');
require 'function.cgi';
&main;
#----------------------------�͂��߂ɂ��ǂ݂�������------------------------------
#���̃X�N���v�g�́A�N�C�Y�^�c�Ǘ��p��CGI�v���O�����ł��B
#�N�C�Y�̍쐬�A�^�c�́A�T�[�o�[�ɐݒu��Aquiz_op.cgi�ɃA�N�Z�X���A
#Web��ł����Ȃ��Ă��������B
#--------------------------------------------------------------------------------
#************************************************
# �w�b�_�\������
#_HTML_��_HTML_�Ƃ̂�������
#�N�C�Y�̃y�[�W�̃w�b�_�[������HTML���L�����Ă��������B
#���ʂ�HTML�\�L�ł��܂��܂���B
#************************************************
sub header_html {
if($_[0] ne ''){
$subtitle1="- $_[0] -";
$subtitle2="<br>- $_[0] -";
}else{
$subtitle1='';
$subtitle2='';
}
$header_html = <<"_HTML_";
<html><head>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=x-sjis">
<title>�N�C�Y�Ǘ��l��$subtitle1</title></head><BODY bgcolor=white>
<table border=0 cellspacing=0 cellpadding=0 width="100%" >
<tr><td Valign=TOP>
$formop_hd
<input type=hidden name=type value=$FORM{type}>
<input type=hidden name=totop value=1>
<input type=submit value="�N�C�Y�Ǘ��l����">
</form>
</font></td><td Valign=TOP>
$formop_hb
$form_d
<input type=hidden name=totop value=1>
<input type=submit value="�V�K�E�C���h�E">
</form></td>
<td nowrap width=80%><div align=right><p><B><big>�N�C�Y�Ǘ��l��$subtitle2</big></B></p></div></td></tr></table>
<br><br>
_HTML_
}
#************************************************
# ���C���v���O����
#************************************************
sub main{
&header_html();
if(!(-f 'function.cgi')){
&error(811,'function.cgi');
$footer_html='<hr></body></html>';
&outputop;
}
require 'function.cgi';
&header_html();
&footer_html;
if(!(-f 'jcode.pl')){
&error(812,'jcode.pl');
&outputop;
}
require 'jcode.pl';
&setup;
&file_lock("$data_dir/$file_lock");
&buf_read;
&header_html();
if(!&ch_pwd_html){
&all_design_read;
&all_genre_read;
&ch_files;
&sys_read;
&header_html();
if($FORM{totop} ne ''){&menu_html;}
elsif($FORM{menu} eq ''){&sys_command;}
else{&genre_command;}
}
&outputop;
}
#************************************************
# �V�X�e���R�}���h
#************************************************
sub sys_command{
if($FORM{help} eq 'sys'){
&help_sys_html();
}elsif($FORM{help} eq 'newg'){
&help_newgenre_html();
}elsif($FORM{help} eq 'sysd'){
&help_sysdesign_html();
}elsif($FORM{help} eq 'gend'){
&help_genredesign_html();
}elsif($FORM{help} eq 'playlog'){
&help_playlog_html();
}elsif($FORM{help} eq 'log'){
&help_log_html();
}elsif($FORM{help} eq 'genre'){
&help_genre_html();
}elsif($FORM{help} eq 'delg'){
&help_delgenre_html();
}elsif($FORM{help} eq 'delq'){
&help_delquiz_html();
}elsif($FORM{help} eq 'madd'){
&help_multiadd_html();
}elsif($FORM{help} eq 'emes'){
&help_endmes_html();
}elsif($FORM{help} eq 'back'){
&help_backup_html();
}elsif($FORM{log} ne ''){
if(&log){
&header_html("�e�탍�O�{���E�ۑ�");
&log_html;
}
}elsif($FORM{type} eq 'sys'){
&header_html("�V�X�e���ݒ�ҏW");
&sys_to_form;
&edit_sys_html;
}elsif($FORM{type} eq 'sys2'){
if(&edit_sys){
&header_html("�V�X�e���ݒ�ҏW");
&edit_sys_html;
}else{
&menu_html;
}
}elsif($FORM{type} eq 'newj'){
&header_html("�V�W�������o�^");
&make_genre_html;
}elsif($FORM{type} eq 'newj2'){
if(&make_mes_cgi){
&header_html("�V�W�������o�^");
&make_genre_html;
}elsif(&make_genre){
&header_html("�V�W�������o�^");
&make_genre_html;
}else{
&header_html("�W�������̕ҏW");
&genre_array_to_form;
&edit_genre_html;
}
}elsif($FORM{type} eq 'sdesed'){
&header_html("�V�X�e���f�U�C���̕ҏW");
if($FORM{delid} ne ''){&del_sysdesign($FORM{delid});}
if($sysdesign_title{$FORM{id}} ne ''){
&sysdesign_to_form($FORM{id});
$FORM{sdt}=$FORM{id};
&edit_sysdesign_html($FORM{id},'edit');
}elsif($sysdesign_title{$FORM{copyid}} ne ''){
if($FORM{sdt} eq ''){
$FORM{sdt}="$FORM{copyid}(�R�s�[)";
if($sysdesign_title{$FORM{sdt}} ne ''){
for($id=2;$sysdesign_title{"$FORM{copyid}(�R�s�[$id)"} ne '';$id++){;}
$FORM{sdt}="$FORM{copyid}(�R�s�[$id)";
}
}
&sysdesign_to_form($FORM{copyid});
$FORM{id}=$FORM{copyid};
&edit_sysdesign_html($FORM{copyid},'copy');
}else{
if($FORM{sdt} eq ''){
for($id=$#sysdesign_list+2;$sysdesign_title{"�V�X�e���f�U�C��$id"} ne '';$id++){;}
$FORM{sdt}="�V�X�e���f�U�C��$id";
}
&def_sysdesign($FORM{sdt});
&sysdesign_to_sysdesign_array();
&sysdesign_to_form($FORM{sdt});
pop(@sysdesign_list);
&edit_sysdesign_html($FORM{sdt},'new');
}
}elsif($FORM{type} eq 'sdesed2'){
if(!&edit_sysdesign){
$FORM{edittype}='edit';
}
&header_html("�V�X�e���f�U�C���̕ҏW");
$FORM{id}=$FORM{sdt};
&edit_sysdesign_html($FORM{id},$FORM{edittype});
}elsif($FORM{type} eq 'gdesed'){
&header_html("�W�������f�U�C���̕ҏW");
if($FORM{delid} ne ''){&del_design($FORM{delid});}
if($design_title{$FORM{id}} ne ''){
&design_to_form($FORM{id});
$FORM{gdt}=$FORM{id};
&edit_design_html($FORM{id},'edit');
}elsif($design_title{$FORM{copyid}} ne ''){
&design_to_form($FORM{copyid});
if($FORM{gdt} eq ''){
$FORM{gdt}="$FORM{copyid}(�R�s�[)";
if($design_title{$FORM{gdt}} ne ''){
for($id=2;$design_title{"$FORM{copyid}(�R�s�[$id)"} ne '';$id++){;}
$FORM{gdt}="$FORM{copyid}(�R�s�[$id)";
}
}
$FORM{id}=$FORM{copyid};
&edit_design_html($FORM{copyid},'copy');
}else{
if($FORM{gdt} eq ''){
for($id=$#design_list+2;$design_title{"�W�������f�U�C��$id"} ne '';$id++){;}
$FORM{gdt}="�W�������f�U�C��$id";
}
&def_design($FORM{gdt});
&design_to_design_array();
&design_to_form($FORM{gdt});
pop(@design_list);
&edit_design_html($FORM{gdt},'new');
}
}elsif($FORM{type} eq 'gdesed2'){
if(!&edit_design){
$FORM{edittype}='edit';
}
&header_html("�W�������f�U�C���̕ҏW");
$FORM{id}=$FORM{gdt};
&edit_design_html($FORM{id},$FORM{edittype});
}elsif($FORM{type} eq 'sort'){
&header_html("�W�������̏����ύX");
&sort_genre_html;
}elsif($FORM{type} eq 'sort1'){
if(&sort_genre){
&sort_genre_html;
}else{
&menu_html;
}
}elsif($FORM{type} eq 'log'){
&header_html("�e�탍�O�{���E�ۑ�");
&log_html;
}elsif($FORM{type} eq 'play'){
&header_html("�v���C���O�g�p��");
&play_html;
}elsif($FORM{type} eq 'size'){
&header_html("�e�탍�O�e��");
&file_size_html;
}elsif($FORM{type} eq 'guard'){
&header_html("�A�N�Z�X����");
&edit_guard_html;
}elsif($FORM{type} eq 'guard1'){
if($FORM{guard} eq 1){$guard="guard";}
else{$guard="permit";}
if(!&write_file($guard_cgi,"$guard\n$FORM{iplist}")){
&mes(200,"�A�N�Z�X����IP���X�g");
}
&header_html("�A�N�Z�X����");
&edit_guard_html;
}elsif($FORM{type} eq 'help'){
&header_html("�w���v");
&help_html;
}else{
&menu_html;
}
}
#************************************************
# �W�������ʃR�}���h
#************************************************
sub genre_command{
&other_genre_html;
if($FORM{d} eq ''){
&error(404,'�W������');
&menu_html;
}elsif(&ch_dir_exist('�f�B���N�g����',$FORM{d})){
&menu_html;
}elsif(&ch_genre_exist($FORM{d}) eq 0){
&error(801,'�W���������');
&menu_html;
}elsif($FORM{type} eq ''){
&header_html();
&error(405,'�ҏW���j���[');
&menu_html;
}elsif($FORM{type} eq 'editg'){
&header_html("�W�������̕ҏW");
&list_genre_html($FORM{d});
&genre_array_to_form;
&edit_genre_html;
}elsif($FORM{type} eq 'editg2'){
if(&edit_genre){
&list_genre_html($FORM{d});
&edit_genre_html;
}else{
&menu_html;
}
}elsif($FORM{type} eq 'copy'){
&header_html("�W����������");
&list_genre_html($FORM{d});
&copy_genre_html;
}elsif($FORM{type} eq 'copy1'){
&list_genre_html($FORM{d});
if(&copy_genre){
&header_html("�W����������");
&copy_genre_html;
}else{
&header_html("�W�������̕ҏW");
&edit_genre_html;
}
}elsif($FORM{type} eq 'del'){
&header_html("�W�������̊e��폜");
&list_genre_html($FORM{d});
&del_genre_html;
}elsif($FORM{type} eq 'del1'){
if(&del_genre){
&list_genre_html($FORM{d});
&del_genre_html;
}else{
&menu_html;
}
}elsif($FORM{type} eq 'score'){
&header_html("�o��󋵕\\��");
&list_genre_html($FORM{d});
&rec_html('op');
}elsif($FORM{type} eq 'qmulti'){
if(&ch_mondai_exist){return;}
&header_html("���̈ꊇ�ǉ�");
&list_genre_html($FORM{d});
&multi_add_quiz_form;
}elsif($FORM{type} eq 'qmulti1'){
if(&ch_mondai_exist){return;}
&header_html("���̈ꊇ�ǉ��m�F");
&list_genre_html($FORM{d});
if(&multi_add_quiz_html){
&multi_add_quiz_form;
}
}elsif($FORM{type} eq 'qmulti2'){
if(&ch_mondai_exist){return;}
if(&multi_add_quiz){
&list_genre_html($FORM{d});
&multi_add_quiz_form;
}else{
&menu_html;
}
}elsif($FORM{type} eq 'qedit'){
if(&ch_mondai_exist){return;}
&header_html("���̕ҏW");
&list_genre_html($FORM{d});
$FORM{ed}='new';$FORM{lst_q}=1;$FORM{lst_a}=1;
&edit_quiz_form;
&edit_quiz_html;
}elsif($FORM{type} eq 'qedit1'){
if(&ch_mondai_exist){return;}
&header_html("���̕ҏW");
&list_genre_html($FORM{d});
if(($FORM{ed} eq 'edit')&&($FORM{qn} ne '')){
if($FORM{qn} =~/\D/){&error(301,'���ԍ�');$FORM{qn} = '';}
elsif(($FORM{qn} > $#mondai+1)||($FORM{qn}<=0)){&error(531,'���ԍ�');$FORM{qn} = '';}
else{&quiz_array_to_form;}
}
&edit_quiz_form;
&edit_quiz_html;
}elsif($FORM{type} eq 'qedit2'){
if(&ch_mondai_exist){return;}
&header_html("���̕ҏW");
&list_genre_html($FORM{d});
if($FORM{ed} eq 'edit'){
&refresh_quiz;
&quiz_read($FORM{d});
if(!&edit_quiz("$mondai_$FORM{d}\.cgi")){
&mes(201,"�w$title{$FORM{d}}�x�̖��");
&refresh_quiz;
&quiz_read($FORM{d});
}
}else{
if(!&add_quiz){
$FORM{qn}=$#mondai+1;
&mes(150,"�w$title{$FORM{d}}�x�̖��");
&list_genre_html($FORM{d});
}else{
&refresh_quiz;
&quiz_read($FORM{d});
}
}
&edit_quiz_form;
&edit_quiz_html;
}elsif($FORM{type} eq 'qcont'){
if(&ch_mondai_exist){return;}
&header_html("���e���̕ҏW");
&list_genre_html($FORM{d});
if($FORM{ed} eq ''){
($FORM{lst_q},$FORM{lst_a},$FORM{lst_m},$FORM{lst_am},$FORM{lst_mm},$FORM{lst_cf},$FORM{lst_dg},$FORM{lst_mm1},$FORM{lst_mm2},$FORM{lst_mm3},$FORM{lst_mm4},$FORM{lst_ath},$FORM{lst_at})=(1,1,1,1,1,1,1,1,1,1,1,1,1);
}
&del_cont;
&list_genre_html($FORM{d});
&refresh_quiz;
&quiz_read($FORM{d},'','',$contribute_cgi);
if($FORM{qn} ne ''){
&quiz_array_to_form;
&edit_cont_form;
}
&edit_cont_html;
}elsif($FORM{type} eq 'qcont1'){
if(&ch_mondai_exist){return;}
&header_html("���e���̕ҏW");
if($FORM{add} > 0){&add_cont;}
else{
&refresh_quiz;
&quiz_read($FORM{d},'','',$contribute_cgi);
if(&edit_quiz("$contribute_cgi")){
&edit_cont_form;
}else{
&mes(202,"���e���");
}
}
&list_genre_html($FORM{d});
&refresh_quiz;
&quiz_read($FORM{d},'','',$contribute_cgi);
&edit_cont_html;
}elsif($FORM{type} eq 'qdel'){
if(&ch_mondai_exist){return;}
&refresh_quiz;
&quiz_read($FORM{d});
if($#mondai<0){
&error(691);
&menu_html;
}else{
&list_genre_html($FORM{d});
&del_quiz_html;
}
}elsif($FORM{type} eq 'qdel1'){
if(&ch_mondai_exist){return;}
if(!&del_quiz){
&mes(250,"�w$title{$FORM{d}}�x�̖��");
}
&list_genre_html($FORM{d});
&del_quiz_html;
}elsif($FORM{type} eq 'mes'){
&header_html("�I�������b�Z�[�W�ҏW");
&list_genre_html($FORM{d});
&mes_dat_to_form;
&edit_final_mes_html;
}elsif($FORM{type} eq 'mes1'){
&header_html("�I�������b�Z�[�W�ҏW");
&list_genre_html($FORM{d});
if(!&ch_edit_mes_param){
&edit_mes;
}
&mes_dat_to_form;
&edit_final_mes_html;
}elsif($FORM{type} eq 'back'){
&header_html("�e�탍�O�̃o�b�N�A�b�v");
&list_genre_html($FORM{d});
&backup_html;
}elsif($FORM{type} eq 'back1'){
&list_genre_html($FORM{d});
&backup;
&backup_html;
}elsif($FORM{type} eq 'back2'){
&make_backup;
&list_genre_html($FORM{d});
&backup_html;
}elsif($FORM{type} eq 'high'){
&header_html("�����ю҃��O�ҏW");
&list_genre_html($FORM{d});
&edit_high_html;
}elsif($FORM{type} eq 'high1'){
if(&edit_high){
&header_html("�����ю҃��O�ҏW");
&list_genre_html($FORM{d});
&edit_high_html;
}else{
&menu_html;
}
}else{
&error(406,'�ҏW���j���[');
&menu_html;
}
}
#************************************************
# ���ǉ�����
#************************************************
sub add_quiz{
&refresh_quiz;
&quiz_read($FORM{d});
if(&ch_add_quiz_param){return 1;}
if(&ch_duplic_quiz){return 1;}
&push_quiz_palam($FORM4{qqu},$FORM4{qas},$FORM4{qmas1},$FORM4{qmas2},$FORM4{qmas3},$FORM4{qmas4},$FORM4{qac},$FORM4{qmac},$FORM{qcf},$FORM4{qdg},$FORM4{qmac1},$FORM4{qmac2},$FORM4{qmac3},$FORM4{qmac4},$FORM{atype},$FORM{auth});
if(&write_mondai("$mondai_$FORM{d}\.cgi")){return 1;}
&clear_form('qqu','qas','qmas1','qmas2','qmas3','qmas4','qac','qmac','qcf','qdg','qmac1','qmac2','qmac3','qmac4','atype','auth');
return 0;
}
#************************************************
# ���e���ǉ�����
#************************************************
sub add_cont{
if(&add_quiz){
&refresh_quiz;
&quiz_read($FORM{d},'','',$contribute_cgi);
&edit_cont_form;
}else{
&refresh_quiz;
&quiz_read($FORM{d},'','',$contribute_cgi);
$i=$FORM{qn};
($mondai[$i-1],$ans[$i-1],$misans1[$i-1],$misans2[$i-1],$misans3[$i-1],$misans4[$i-1],$anscom[$i-1],$misanscom[$i-1],$cf[$i-1],$digest[$i-1],$misanscom1[$i-1],$misanscom2[$i-1],$misanscom3[$i-1],$misanscom4[$i-1],$anstype[$i-1],$author[$i-1])=();
if(!&write_mondai("$contribute_cgi")){
$FORM{qn}='';
&mes(500,"���e���");
}
}
}
#************************************************
# ���ꊇ�ǉ�����
#************************************************
sub multi_add_quiz{
local($index);
&refresh_quiz;
&quiz_read($FORM{d});
$index=0;
while($FORM{"p_q$index"} ne ''){
if(($FORM{"p_a$index"} eq '') || ($FORM{"p_m1$index"} eq '')){&error(101,'�o�^������');return 1;}
&push_quiz_palam($FORM{"p_q$index"},$FORM{"p_a$index"},$FORM{"p_m1$index"},$FORM{"p_m2$index"},$FORM{"p_m3$index"},$FORM{"p_m4$index"},$FORM{"p_am$index"},$FORM{"p_mm$index"},$FORM{"p_cf$index"},$FORM{"p_dg$index"},$FORM{"p_1mm$index"},$FORM{"p_2mm$index"},$FORM{"p_3mm$index"},$FORM{"p_4mm$index"},$FORM{"p_at$index"},$FORM{"p_ath$index"});
$index++;
}
if(!&write_mondai("$mondai_$FORM{d}\.cgi")){
&mes(350,"�w$title{$FORM{d}}�x�̖��");return 0;
}else{return 1;}
}
#************************************************
# �W�����������ύX
#************************************************
sub sort_genre{
for($i=1;$i<=$#genre_dir_all+1;$i++){
if(&ch_genre_exist($FORM{"d$i"}) eq 0){&error(806,'�f�B���N�g��');return 1;}
push(@sort,$FORM{"s$i"}."\t".$FORM{"d$i"});
}
local($value);
$value="ver2\n";
foreach(sort {$a <=> $b} @sort){
($s,$dir)=split(/\t/,$_);
$value.=&genre_array_to_line($dir);
}
if(&write_file($genre_cgi,$value)){return 1;}
&all_genre_read;
&mes(400,'�W�������̏����ύX');
return 0;
}
#************************************************
# �W��������������
#************************************************
sub copy_genre{
if(&ch_dir_exist('��������f�B���N�g����',$FORM{d2})){return 1;}
if(&ch_genre_exist($FORM{d2}) eq 1){
&error(851,'��������f�B���N�g����');
return 1;
}
open(DB,"$FORM{d}/mes_$FORM{d}\.cgi");local(@list)=<DB>;close(DB);
if(&write_file("$FORM{d2}/mes_$FORM{d2}\.cgi",@list)){return 0;}
&genre_array_to_form;
$old_dir=$FORM{d};
$FORM{d}=$FORM{d2};
$FORM{me}=0;
push(@genre_dir_all,$FORM{d});
&form_to_genre_array;
if(!&write_genre_dat){
&mes(900,"�w$old_dir�f�B���N�g���x�̃W�������o�^����<br>�w$FORM{d2}�f�B���N�g���x�֕��������Ƃ�����ɏI�����܂����B<br>���у��O�t�@�C���A���t�@�C�����͕�������Ă��܂���B<br>���������W�������ʐݒ���s���Ă��������B");
return 0;
}else{return 1;}
}
#************************************************
# �t�@�C���̌����B�d���f�[�^���̂��������̂��������ށB
#************************************************
sub h_conv_file{
local($log,$day_limit,$num_limit,@files)=@_;
local(%data,%day);
if($#files<0){return;}
foreach $file(@files){
open(DB,"$FORM{d}/$file");@list=<DB>;close(DB);
foreach $line(@list){
if($line =~ /^date/){next;}
local($day,$high,$name,$host) = split(/\t/,$line);
if($day_limit > 0){
if(time > $day+$day_limit*(60*60*24)){next;}
}
$data{$line}=$high;
$day{$line}=$day;
}
}
local($line_num,$value);
$value ='date'.time."\n";
$line_num=0;
foreach(sort{$data{$b}*10000000000+$day{$b} <=> $data{$a}*10000000000+$day{$a}}keys %data){
if(($num_limit > 0)&&($line_num >= $num_limit)){last;}
$value .= $_;
}
return &write_file("$FORM{d}/$log\.cgi",$value);
}
#************************************************
# ���������̐���������ĕԂ��B
#************************************************
sub cut_num{
local($word)=@_;
if($word=~/(.*)[\d]+$/){$word=$1;}
return $word;
}
#************************************************
# �p�X���[�h�V�K�o�^HTML�\������
#************************************************
sub pass_new_html {
$main_html = <<"_HTML_";
<hr><ul>
<table bgcolor='$sys_color' $sys_tbl_opt><tr><td nowrap>
�Ǘ��җp�p�X���[�h���o�^����Ă��܂���B<br>
�V�K�p�X���[�h��o�^���Ă��������B<br><br>
<form action="$quiz_op_cgi" method="$method" name=frm>
<input type=hidden name=passnew value=1>
<input type=password name=passnew1><br>
<input type=password name=passnew2>(�m�F�p)<br><br>
<input type=submit value="�@�@ �o�^ �@�@"></form>
${&focus_move('passnew1')}$ret
</td></tr></table></ul>
_HTML_
}
#************************************************
# �p�X���[�h���͗pHTML�\������
#************************************************
sub pass_enter_html {
$main_html = <<"_HTML_";
<hr>
<table border='$border' bgcolor='$sys_color' width=400><tr><td nowrap><span>
�Ǘ��җp�p�X���[�h����͂��Ă��������B<br>
�p�X���[�h���������������ꍇ�́A$pass_cgi�t�@�C�����������Ă��������B<br>
<form action='$quiz_op_cgi' method='$method' name=frm>
<input type=password name=passch>
<input type=hidden name=passch1 value=1>
<input type=submit value="���M"></form></span>
${&focus_move('passch')}$ret
</td></tr></table>
<br>
<br>
<a href="$index_cgi">�N�C�Y�ւ��ǂ�</a>
_HTML_
}
#************************************************
# ���j���[�\������
#************************************************
sub menu_html{
local($type);$type=&cut_num($FORM{type});
$menu_ch{$type}=' checked';
$other_genre='';
$dir_ch{$FORM{d}}=' selected';
if($#genre_dir_all<0){
$center_menu1='<center>';
$center_menu2='</center>';
}
$menu_html = <<"_HTML_";
<b><span>���ҏW���j���[��</span></b>
<table $sys_tbl_opt bgcolor='$sys_color'><tr><td valign=top>
$center_menu1
<table border=$border cellpadding=2 bgcolor='$sys_color2'>
$formop_h
<input type=hidden name=type value=sys>
<tr><td colspan=2 nowrap>
<center><span>���V�X�e���R�}���h��</span></center>
</td></tr>
<tr><td>
<span>�V�X�e���ݒ�ҏW</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=newj>
<span>�V�W�������o�^</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=sdesed>
<span>�V�X�e���f�U�C���̕ҏW</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=gdesed>
<span>�W�������f�U�C���̕ҏW</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=play>
<span>�v���C���O�g�p��</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=log>
<span>�e�탍�O�{���E�ۑ�</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=size>
<span>�e�탍�O�e��</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
_HTML_
if($#genre_dir_all>=1){
$menu_html .= <<"_HTML_";
$formop_h
<tr><td>
<input type=hidden name=type value=sort>
<span>�W�������̏����ύX</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
_HTML_
}else{
$menu_html .= <<"_HTML_";
<tr><td>
�W�������̏����ύX</td><td>�s��
</td></tr>
_HTML_
}
$menu_html .= <<"_HTML_";
$formop_h
<tr><td>
<input type=hidden name=type value=guard>
<span>�A�N�Z�X����</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=help>
<span>�w���v</span></td><td><span><input type=submit value="���s"></span></td></tr></form>
</table>$center_menu2</td>
_HTML_
if($#genre_dir_all>=0){
$menu_html .= <<"_HTML_";
<td>
$formop_h
<input type=hidden name=menu value=1>
<table border=$border cellpadding=2 bgcolor='$sys_color2'>
<tr><td colspan=3 nowrap><center><span>���W�������ʃR�}���h��</span></center></td></tr>
<tr><td rowspan=12><span><select name=d size=20 width=200>
_HTML_
foreach $dir(@genre_dir_all){
if($dir ne ''){$menu_html .= "<option value='$dir'$dir_ch{$dir}>$title{$dir}�@�@ \n";}
}
$menu_html .= <<"_HTML_";
</select></span>
</td>
<tr><td nowrap><span>�W�������̕ҏW</span></td><td><span><input type=submit name=type_editg value='���s'></span></td></tr>
<tr><td nowrap><span>�W�������̕���</span></td><td><span><input type=submit name=type_copy value='���s'></span></td></tr>
<tr><td nowrap><span>�W�������̊e��폜</span></td><td><span><input type=submit name=type_del value='���s'></span></td></tr>
<tr><td nowrap><span>���̍쐬�ҏW</span></td><td><span><input type=submit name=type_qedit value='���s'></span></td></tr>
<tr><td nowrap><span>���̍폜�A�����ύX</span></td><td><span><input type=submit name=type_qdel value='���s'></span></td></tr>
<tr><td nowrap><span>���̈ꊇ�ǉ�</span></td><td><span><input type=submit name=type_qmulti value='���s'></span></td></tr>
<tr><td nowrap><span>���e���̕ҏW</span></td><td><span><input type=submit name=type_qcont value='���s'></span></td></tr>
<tr><td nowrap><span>�I�������b�Z�[�W�ҏW</span></td><td><span><input type=submit name=type_mes value='���s'></span></td></tr>
<tr><td nowrap><span>�o��󋵕\\��</span></td><td><span><input type=submit name=type_score value='���s'></span></td></tr>
<tr><td nowrap><span>�e�탍�O�̃o�b�N�A�b�v</span></td><td><span><input type=submit name=type_back value='���s'></span></td></tr>
<tr><td nowrap><span>�����ю҃��X�g�ҏW</span></td><td><span><input type=submit name=type_high value='���s'></span></td></tr>
</table>
</td></tr>
_HTML_
}
$menu_html .= '</table>';
&list_sys_html;
&list_genre_html(@genre_dir_all);
}
#************************************************
# �V�X�e�����̈ꗗ
#************************************************
sub list_sys_html{
if($SYS{quiz_form} eq 0){$quiz_f='�����N';}
elsif($SYS{quiz_form} eq 1){$quiz_f='���W�I�{�^��';}
else{$quiz_f='�{�^��';}
$system_list ="<br><b><span>���V�X�e�����</span></b><table border=$border>";
$system_list .="<tr><td colspan=6><center><small>�����ݒ�</small></center></td>";
$system_list .="<td colspan=11><center><small>�f�U�C��<small></center></td></tr><tr>";
$system_list .= &my_print2(<<"_MY_",'<td><small><center>','</center></small></td>');
�v<br>��<br>�C<br>��<br>�O<br>��<br>��<br>��<br>��<br>(��)
��<br>��<br>�v<br>��<br>�C<br>�l<br>��<br>(�l)
�I<br>��<br>��<br>�`<br>��
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>�^<br>�C<br>�g<br>��
�g<br>�b<br>�v<br>�y<br>�b<br>�W<br>��<br>��<br>��<br>��<br>�N
�\\<br>��<br>�`<br>��
�f<br>�U<br>�C<br>��<br>��
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>�w<br>�i<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>�W<br>��<br>��<br>��<br>��<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>��<br>��<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>��<br>��<br>��<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>��<br>��<br>��<br>��<br>�F
��<br>�{<br>��<br>��<br>�F
��<br>��<br>�N<br>��<br>��<br>�F
��<br>�K<br>��<br>��<br>��<br>�N<br>��<br>��<br>�F
�\\<br>��<br>�\\<br>��<br>��<br>��
�\\<br>��<br>��<br>��<br>�\\<br>��<br>��<br>��
_MY_
$system_list .='</tr><tr>';
$system_list .=&my_print2(<<"_MY_",'<td><small>','</small></td>');
$SYS{limit}
$SYS{max_player}
$quiz_f
<a href=$index_cgi>$SYS{main_title}</a>
_MY_
$align{l}='����';$align{c}='����';$align{r}='�E��';
$walign{l}='����';$walign{c}='����';$walign{r}='�E��';
$easy{0}='�ڍ�';$easy{1}='����';$easy{2}='�Ȉ�';$easy{3}='�ꗗ';
if($SYS{top_url} ne ''){$system_list .="<td><small><a href=$SYS{top_url}>��</a></small></td>";}
else{$system_list .='<td><small>�~</small></td>';}
$system_list .=<<"_HTML_";
<td><small>$easy{$SYS{easy}}</small></td>
<td><small>$SYS{design}</small></td>
<td bgcolor='$SYS{top_back_color}'><small><font color='$SYS{top_back_color}'>��</font></small></td>
<td bgcolor='$SYS{top_genre_color}'><small><font color='$SYS{top_genre_color}'>��</font></small></td>
<td bgcolor='$SYS{top_info_color}'><small><font color='$SYS{top_info_color}'>��</font></small></td>
<td bgcolor='$SYS{top_com_color}'><small><font color='$SYS{top_com_color}'>��</font></small></td>
<td bgcolor='$SYS{top_high_color}'><small><font color='$SYS{top_high_color}'>��</font></small></td>
<td bgcolor='$SYS{text_color}'><small><font color='$SYS{text_color}'>��</font></small></td>
<td bgcolor='$SYS{link_color}'><small><font color='$SYS{link_color}'>��</font></small></td>
<td bgcolor='$SYS{vlink_color}'><small><font color='$SYS{vlink_color}'>��</font></small></td>
<td><small>$align{$SYS{align}}</small></td>
<td><small>$walign{$SYS{walign}}</small></td>
</tr></table>
_HTML_
}
#************************************************
# �W���������̈ꗗ
#************************************************
sub list_genre_html{
local(@all_dirs)=@_;
local(@dirs);
foreach $dir(@all_dirs){if($dir ne ''){push(@dirs,$dir);}}
if($#dirs < 0){$genre_list='';return;}
$genre_list ="<br><b><span>���W�������ʏ��</span></b><table border=$border>";
$genre_list .="<tr><td colspan=9><center><small>�����ݒ�</small></center></td>";
$genre_list .="<td colspan=12><center><small>�f�U�C��<small></center></td>";
$genre_list .="<td colspan=21><center><small>���[�h��<small></center></td></tr>";
$genre_list .=&my_print2(<<'_MY_','<td><small><center>','</center></small></td>');
�\<br>��
dir
�o<br>�^<br>��<br>��<br>��<br>��<br>(��)
��<br>�e<br>��<br>��<br>��<br>(��)
��<br>�J<br>��
��<br>�e<br>��<br>��<br>��<br>��<br>�t
�e<br>�L<br>�X<br>�g<br>��<br>��<br>�`<br>��<br>��<br>��<br>�e<br>��<br>��
��<br>�e<br>��<br>��<br>��<br>��<br>��<br>��<br>�p
�o<br>��<br>��<br>��<br>��<br>��<br>��<br>��<br>��<br>�\<br>��
��<br>��<br>��<br>�\<br>��
�f<br>�U<br>�C<br>��<br>��
��<br>�{<br>��<br>��<br>�F
��<br>��<br>�N<br>��<br>��<br>�F
��<br>�K<br>��<br>��<br>��<br>�N<br>��<br>��<br>�F
�a<br>��<br>��<br>��<br>��<br>��<br>�F
��<br>�{<br>�w<br>�i<br>�F
��<br>��<br>�w<br>�i<br>�F
�s<br>��<br>��<br>�w<br>�i<br>�F
��<br>��<br>�E<br>�C<br>��<br>�h<br>�E<br>�F
�\<br>��<br>�w<br>�b<br>�_<br>�b<br>�F
�\<br>��<br>�F
�\<br>��<br>�g<br>��<br>�F
��<br>�O
��<br>��<br>�\<br>��
�o<br>��<br>��
�g<br>�p<br>��<br>��<br>��<br>(��)
�o<br>��<br>��<br>(��)
��<br>��<br>�o<br>��
�I<br>��<br>��<br>��<br>(��)
��<br>��<br>��<br>��<br>(�b)
��<br>�i<br>�_<br>(��)
��<br>��<br>��<br>��<br>�o<br>�b<br>�N<br>�A<br>�b<br>�v<br>(��)
��<br>��<br>��<br>��<br>�o<br>�b<br>�N<br>�A<br>�b<br>�v<br>��<br>��
��<br>��<br>��<br>�z<br>�o<br>�b<br>�N<br>�A<br>�b<br>�v<br>(��)
��<br>��<br>��<br>�z<br>�o<br>�b<br>�N<br>�A<br>�b<br>�v<br>��<br>��
��<br>��<br>��<br>�z<br>��<br>��<br>�\<br>��<br>(��)
��<br>��<br>��<br>�z<br>�W<br>�v<br>�P<br>��<br>(��)
��<br>��<br>��<br>��<br>��<br>��<br>��<br>��<br>(��)
��<br>��<br>��<br>��<br>�l<br>��<br>��<br>��<br>(�l)
�a<br>��<br>��<br>��<br>�l<br>��<br>(�l)
��<br>��<br>��<br>��<br>�R<br>��<br>��<br>�g<br>�L<br>�^
��<br>�z<br>�X<br>�g<br>��<br>�X<br>�R<br>�A<br>�o<br>�^
_MY_
foreach $dir(@dirs){
if($mode_name2{$dir} ne ''){
$rowspan=' rowspan=2';
}else{$rowspan='';}
$genre_list .="<tr><td$rowspan nowrap><small>$title{$dir}</small></td>\n";
$genre_list .="<td$rowspan nowrap><small>$dir</small></td>\n";
&refresh_quiz;
$quiz_num=0;
if($mondai_cgi{$dir} eq '.'){
foreach(@genre_dir_all){if($mondai_cgi{$_} ne '.'){&quiz_read($_);}}
$quiz_num='('.($#mondai+1).')';
}elsif($mondai_cgi{$dir} =~ /\//){
@mondai_dat=split(/\t/,$mondai_cgi{$dir});
foreach(@mondai_dat){
local($d,$val)=split(/\//,$_);
if($val eq 'all'){$val ='';}
&quiz_read($d,$val);
}
$quiz_num='('.($#mondai+1).')';
}else{&quiz_read($dir);$quiz_num=$#mondai+1;}
if($FORM{'qm1-2'} eq ''){$FORM{'qm1-2'}=$#mondai+1;}
if($FORM{'pm1-2'} eq ''){$FORM{'pm1-2'}=$FORM{'qm1-2'};}
if($FORM{'lm1-2'} eq ''){$FORM{'lm1-2'}=$FORM{'pm1-2'};}
if($FORM{'qm2-2'} eq ''){$FORM{'qm2-2'}=$#mondai+1;}
if($FORM{'pm2-2'} eq ''){$FORM{'pm2-2'}=$FORM{'qm2-2'};}
if($FORM{'lm2-2'} eq ''){$FORM{'lm2-2'}=$FORM{'pm2-2'};}
open(DB,"$dir/$contribute_cgi");local(@cont)=<DB>;close(DB);
$cont_num=0;
foreach(@cont){unless($_=~ /^#/)
{$cont_num++;}}
$genre_list .="<td$rowspan><small>$quiz_num</small></td>\n";
$genre_list .="<td$rowspan><small>$cont_num</small></td>\n";
if($mente{$dir}){$genre_list.="<td$rowspan><small>��</small></td>";}
else{$genre_list.="<td$rowspan><small>�~</small></td>";}
if($cont{$dir}){$genre_list.="<td$rowspan><small>��</small></td>";}
else{$genre_list.="<td$rowspan><small>�~</small></td>";}
if($notext{$dir}){$genre_list.="<td$rowspan><small>�~</small></td>";}
else{$genre_list.="<td$rowspan><small>��</small></td>";}
if($direct_cont{$dir}){$genre_list.="<td$rowspan><small>��</small></td>";}
else{$genre_list.="<td$rowspan><small>�~</small></td>";}
if($show_digest{$dir}){$genre_list.="<td$rowspan><small>�~</small></td>";}
else{$genre_list.="<td$rowspan><small>��</small></td>";}
if($show_auth{$dir} eq 1){$genre_list.="<td$rowspan><small>��</small></td>";}
else{$genre_list.="<td$rowspan><small>�~</small></td>";}
$id=$design{$dir};
if(!mygrep($id,@design_list)){
&def_design($id);
&design_to_design_array;
}
$genre_list .=<<"_HTML_";
<td$rowspan nowrap><small>$id</small></td>
<td$rowspan bgcolor='$text_color{$id}'><small><font color='$text_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$link_color{$id}'><small><font color='$link_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$vlink_color{$id}'><small><font color='$vlink_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$champ_color{$id}'><small><font color='$champ_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$main_color{$id}'><small><font color='$main_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$win_color{$id}'><small><font color='$win_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$lose_color{$id}'><small><font color='$lose_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$com_color{$id}'><small><font color='$com_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$th_color{$id}'><small><font color='$th_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$td_color{$id}'><small><font color='$td_color{$id}'>��</font></small></td>
<td$rowspan bgcolor='$border_color{$id}'><small><font color='$border_color{$id}'>��</font></small></td>
<td nowrap><small><a href=$quiz_cgi?d=$dir\&m=1&passch=$FORM{passch}>$mode_name1{$dir}</a></small></td>
_HTML_
if($show_ans1{$dir}){$genre_list.='<td><small>��</small></td>';}
else{$genre_list.='<td><small>�~</small></td>';}
if($random1{$dir}){$genre_list.='<td nowrap><small>�����_��</small></td>';}
else{$genre_list.='<td nowrap><small>�Œ�</small></td>';}
if($quiz_max1{$dir}ne ''){$genre_list.="<td><small>$quiz_max1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�S</small></td>\n";}
if($play_max1{$dir}ne ''){$genre_list.="<td><small>$play_max1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�S</small></td>\n";}
if($bundle1{$dir} eq 1){$genre_list.="<td><small>�L</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
if($lose_max1{$dir}ne ''){$genre_list.="<td><small>$lose_max1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�S</small></td>\n";}
if($time_limit1{$dir} > '0'){$genre_list.="<td><small>$time_limit1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
$genre_list.="<td><small>$high_border1{$dir}</small></td>\n";
if($high_back_day1{$dir}>0){$genre_list.="<td><small>$high_back_day1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�~</small></td>\n";}
if($high_back_w1{$dir}){$genre_list.="<td><small>��</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
if($scorehst_back_day1{$dir}>0){$genre_list.="<td><small>$scorehst_back_day1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�~</small></td>\n";}
if($scorehst_back_w1{$dir}){$genre_list.="<td><small>��</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
$genre_list.="<td><small>$graph_border1{$dir}</small></td>\n";
$genre_list.="<td><small>$histry_div1{$dir}</small></td>\n";
if($day_limit1{$dir} ne ''){$genre_list.="<td><small>$day_limit1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
if($num_limit1{$dir} ne ''){$genre_list.="<td><small>$num_limit1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
$genre_list.="<td><small>$no_limit1{$dir}</small></td>\n";
if($rec_com1{$dir} eq '1'){$genre_list.="<td><small>��</small></td>\n";}
else{$genre_list.="<td><small>�~</small></td>\n";}
if($double_high1{$dir} eq '0'){$genre_list.="<td><small>�~</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
$genre_list.='</tr>';
if($mode_name2{$dir} ne ''){
$genre_list.="<tr><td nowrap><small><a href=$quiz_cgi?d=$dir\&m=2&passch=$FORM{passch}>$mode_name2{$dir}</a></small></td>";
if($show_ans2{$dir}){$genre_list.='<td><small>��</small></td>';}else{$genre_list.='<td><small>�~</small></td>';}
if($random2{$dir}){$genre_list.='<td nowrap><small>�����_��</small></td>';}else{$genre_list.='<td nowrap><small>�Œ�</small></td>';}
if($quiz_max2{$dir}ne ''){$genre_list.="<td><small>$quiz_max2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�S</small></td>\n";}
if($play_max2{$dir}ne ''){$genre_list.="<td><small>$play_max2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�S</small></td>\n";}
if($bundle2{$dir} eq 1){$genre_list.="<td><small>�L</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
if($lose_max2{$dir}ne ''){$genre_list.="<td><small>$lose_max2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�S</small></td>\n";}
if($time_limit2{$dir} > '0'){$genre_list.="<td><small>$time_limit2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
$genre_list.="<td><small>$high_border2{$dir}</small></td>\n";
if($high_back_day2{$dir}>0){$genre_list.="<td><small>$high_back_day2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�~</small></td>\n";}
if($high_back_w2{$dir}){$genre_list.="<td><small>��</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
if($scorehst_back_day2{$dir}>0){$genre_list.="<td><small>$scorehst_back_day2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>�~</small></td>\n";}
if($scorehst_back_w2{$dir}){$genre_list.="<td><small>��</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
$genre_list.="<td><small>$graph_border2{$dir}</small></td>\n";
$genre_list.="<td><small>$histry_div2{$dir}</small></td>\n";
if($day_limit2{$dir} ne ''){$genre_list.="<td><small>$day_limit2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
if($num_limit2{$dir} ne ''){$genre_list.="<td><small>$num_limit2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
$genre_list.="<td><small>$no_limit2{$dir}</small></td>\n";
if($rec_com2{$dir} eq '1'){$genre_list.="<td><small>��</small></td>\n";}
else{$genre_list.="<td><small>�~</small></td>\n";}
if($double_high2{$dir} eq '0'){$genre_list.="<td><small>�~</small></td>\n";}
else{$genre_list.="<td><small>��</small></td>\n";}
$genre_list.='</tr>';
}
}
$genre_list.='</table><br>';
}
#************************************************
# �V�X�e���f�U�C�����̈ꗗ
#************************************************
sub list_sysdesign_html{
&color_html;
if($#sysdesign_list < 0){$sysdesign_list='';return;}
local($formtag)=<<"_HTML_";
$formop_h
<input type=hidden name=type value=sdesed>
_HTML_
$sysdesign_list ="<b>�������f�U�C���̕ҏW�E����������ꍇ�͊Y���f�U�C����I��ł�������<br><br>";
$sysdesign_list .="<span>���V�X�e���f�U�C���ʏ��</span></b>";
$sysdesign_list .="<br><table border=$border><tr>";
$sysdesign_list .=&my_print2(<<'_MY_','<td><small><center>','</center></small></td>');
�f<br>�U<br>�C<br>��<br>��
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>��
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>�w<br>�i<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>�\<br>��<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>�W<br>��<br>��<br>��<br>��<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>��<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>�R<br>��<br>��<br>�g<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>��<br>��<br>��<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>�\<br>��<br>�g<br>��<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>��<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>��<br>�N<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>�K<br>��<br>��<br>��<br>�N<br>�F
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>�\<br>��<br>�g<br>��<br>��<br>��
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>�\<br>��<br>�g<br>��<br>��
��<br>�j<br>��<br>�b<br>�y<br>�b<br>�W<br>��<br>�\<br>��<br>�g<br>��<br>��<br>��
��<br>��<br>�O<br>��<br>�t<br>��<br>��<br>�P
��<br>��<br>�O<br>��<br>�t<br>��<br>��<br>�Q
�\<br>��<br>��<br>�C<br>�A<br>�E<br>�g
�\<br>��<br>��<br>��<br>��<br>�C<br>�A<br>�E<br>�g
��<br>�W
��<br>��
��<br>��
_MY_
$alignj{l}='����';$alignj{c}='����';$alignj{r}='�E��';
foreach $id(@sysdesign_list){
if($SYS{design} eq $id){
$del_form='<td nowrap><small>�g�p��</small></td>';
}else{
$del_form="$formtag<td><input type=submit value='�폜'><input type=hidden name=delid value='$id'></td></form>";
}
if($FORM{id} eq $id && $FORM{copyid} ne $id){
$edit_form="<td>�ҏW��</td>";
}else{
$edit_form="$formtag<td><input type=submit value='�ҏW'><input type=hidden name=id value='$id'></td></form>";
}
$sysdesign_list .=<<"_HTML_";
</tr><tr>
<td nowrap><small>$sysdesign_title{$id}</small></td>
<td nowrap><small><a href="$top_wall{$id}">$top_wall{$id}</a></small></td>
<td bgcolor='$top_back_color{$id}'><small><font color='$top_back_color{$id}'>��</font></small></td>
<td bgcolor='$top_table_color{$id}'><small><font color='$top_table_color{$id}'>��</font></small></td>
<td bgcolor='$top_genre_color{$id}'><small><font color='$top_genre_color{$id}'>��</font></small></td>
<td bgcolor='$top_info_color{$id}'><small><font color='$top_info_color{$id}'>��</font></small></td>
<td bgcolor='$top_com_color{$id}'><small><font color='$top_com_color{$id}'>��</font></small></td>
<td bgcolor='$top_high_color{$id}'><small><font color='$top_high_color{$id}'>��</font></small></td>
<td bgcolor='$top_border_color{$id}'><small><font color='$top_border_color{$id}'>��</font></small></td>
<td bgcolor='$top_text_color{$id}'><small><font color='$top_text_color{$id}'>��</font></small></td>
<td bgcolor='$top_link_color{$id}'><small><font color='$top_link_color{$id}'>��</font></small></td>
<td bgcolor='$top_vlink_color{$id}'><small><font color='$top_vlink_color{$id}'>��</font></small></td>
<td><small>$top_border_high{$id}</td>
<td><small>$top_border{$id}</td>
<td><small>$top_border_in{$id}</td>
<td><small><img width=10 height=10 src="$a_gif{$id}"></small></td>
<td><small><img width=10 height=10 src="$b_gif{$id}"></small></td>
<td><small>$alignj{$align{$id}}</small></td>
<td><small>$alignj{$walign{$id}}</small></td>
$edit_form
$formtag<td><input type=submit value="����"><input type=hidden name=copyid value="$id"></td></form>
$del_form
_HTML_
}
$sysdesign_list.='</tr></table><br>';
}
#************************************************
# �W�������f�U�C�����̈ꗗ
#************************************************
sub list_design_html{
if($#design_list < 0){$design_list='';return;}
local($formtag)=<<"_HTML_";
$formop_h
<input type=hidden name=type value=gdesed>
_HTML_
$design_list ="<br><b><span>���W�������f�U�C���ʏ��</span></b><table border=$border><tr>";
$design_list .=&my_print2(<<'_MY_','<td><small><center>','</center></small></td>');
�f<br>�U<br>�C<br>��<br>��
��<br>��<br>�F
��<br>��<br>�N<br>��<br>��<br>�F
��<br>�K<br>��<br>��<br>��<br>�N<br>��<br>��<br>�F
�a<br>��<br>��<br>��<br>��<br>�F
��<br>�{<br>�w<br>�i<br>�F
��<br>��<br>��<br>�w<br>�i<br>�F
�s<br>��<br>��<br>��<br>�w<br>�i<br>�F
��<br>��<br>�E<br>�C<br>��<br>�h<br>�E<br>�F
�\<br>��<br>�w<br>�b<br>�_<br>�b<br>�F
�\<br>��<br>�F
�\<br>��<br>�g<br>��<br>�F
�\<br>��<br>�g<br>��<br>��<br>��
�\<br>��<br>�g<br>��<br>��
�\<br>��<br>�g<br>��<br>��<br>��
��<br>�{<br>��<br>��
��<br>��<br>��<br>��<br>��
�s<br>��<br>��<br>��<br>��<br>��
��<br>��<br>�p<br>MIDI
�s<br>��<br>��<br>�p<br>MIDI
��<br>��<br>��<br>��<br>�p<br>MIDI
��<br>��<br>��<br>��<br>�p<br>MIDI
�g<br>�p<br>��
��<br>�W
��<br>��
��<br>��
_MY_
$alignj{l}='����';$alignj{c}='����';$alignj{r}='�E��';
foreach $id(@design_list){
if($FORM{id} eq $id && $FORM{copyid} ne $id){
$edit_form="<td>�ҏW��</td>";
}else{
$edit_form="$formtag<td><input type=submit value='�ҏW'><input type=hidden name=id value='$id'></td></form>";
}
if($design_use{$id} ne ''){
$use_form='<td nowrap><small><form><select>';
foreach $dir(split(/\t/,$design_use{$id})){
if($dir ne ''){
$use_form.="<option>$title{$dir}";
}
}
$use_form.='</select></small></td></form>';
$del_form='<td>�g�p��</td>';
}else{
$use_form='<td>�@</td>';
$del_form="$formtag<td><input type=submit value='�폜'><input type=hidden name=delid value='$id'></td></form>";
}
if($wall{$id} ne ''){$wall_a="<a href='$wall{$id}'>��</a>"}
else{$wall_a='�@';}
if($win_wall{$id} ne ''){$win_wall_a="<a href='$win_wall{$id}'>��</a>";}
else{$win_wall_a='�@';}
if($lose_wall{$id} ne ''){$lose_wall_a="<a href='$lose_wall{$id}'>��</a>";}
else{$lose_wall_a='�@';}
if($win_midi{$id} ne ''){$win_midi_a="<a href='$win_midi{$id}'>��</a>";}
else{$win_midi_a='�@';}
if($lose_midi{$id} ne ''){$lose_midi_a="<a href='$lose_midi{$id}'>��</a>";}
else{$lose_midi_a='�@';}
if($end_midi{$id} ne ''){$end_midi_a="<a href='$end_midi{$id}'>��</a>";}
else{$end_midi_a='�@';}
if($high_midi{$id} ne ''){$high_midi_a="<a href='$high_midi{$id}'>��</a>";}
else{$high_midi_a='�@';}
$design_list .=<<"_HTML_";
</tr><tr>
<td nowrap><small>$design_title{$id}</small></td>
<td bgcolor='$text_color{$id}'><small><font color='$text_color{$id}'>��</font></small></td>
<td bgcolor='$link_color{$id}'><small><font color='$link_color{$id}'>��</font></small></td>
<td bgcolor='$vlink_color{$id}'><small><font color='$vlink_color{$id}'>��</font></small></td>
<td bgcolor='$champ_color{$id}'><small><font color='$champ_color{$id}'>��</font></small></td>
<td bgcolor='$main_color{$id}'><small><font color='$main_color{$id}'>��</font></small></td>
<td bgcolor='$win_color{$id}'><small><font color='$win_color{$id}'>��</font></small></td>
<td bgcolor='$lose_color{$id}'><small><font color='$lose_color{$id}'>��</font></small></td>
<td bgcolor='$com_color{$id}'><small><font color='$com_color{$id}'>��</font></small></td>
<td bgcolor='$th_color{$id}'><small><font color='$th_color{$id}'>��</font></small></td>
<td bgcolor='$td_color{$id}'><small><font color='$td_color{$id}'>��</font></small></td>
<td bgcolor='$border_color{$id}'><small><font color='$border_color{$id}'>��</font></small></td>
<td><small>$border_high{$id}</small></td>
<td><small>$border{$id}</small></td>
<td><small>$border_in{$id}</small></td>
<td><small>$wall_a</small></td>
<td><small>$win_wall_a</small></td>
<td><small>$lose_wall_a</small></td>
<td><small>$win_midi_a</small></td>
<td><small>$lose_midi_a</small></td>
<td><small>$end_midi_a</small></td>
<td><small>$high_midi_a</small></td>
$use_form
$edit_form
$formtag<td><input type=submit value="����"><input type=hidden name=copyid value="$id"></td></form>
$del_form
_HTML_
}
$design_list.='</tr></table><br>';
}
#************************************************
# �V�X�e���ݒ�ҏWHTML�\������
#************************************************
sub edit_sys_html{
&list_sys_html;
&color_html;
&form_to_form;
$main_html.=<<"_HTML_";
$formop_nh
<input type=hidden name=type value=sys2>
<span><br><br><b>���e���ڂ���͂��ҏW�{�^���������Ă��������B</b>( * ��͕K�{����)<br><br>
<b>���V�X�e���ݒ�t�H�[����</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=sys target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3 bgcolor=#eeaaee><span><center>�����������V�X�e���ݒ聡��������</center></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(1)�v���C���O�ی���� *
<input type=text name='li' value="$FORM2{li}" size=10>���@(���p����)
(2)�����v���C�l�� *
<input type=text name='mp' value="$FORM2{mp}" size=10>�l�@(�C�ӂ̐���)
(3)�N�b�L�[ID *
<input type=text name='cok' value="$FORM2{cok}" size=10>�@(���p�p��)
(4)�I�����`�� *
<input type=radio name='qf' value=2$FORM{'qf-2'}>�t�H�[���{�^���@<input type=radio name='qf' value=1$FORM{'qf-1'}>���W�I�{�^���@<input type=radio name='qf' value=0$FORM{'qf-0'}>�����N
(5)�g�b�v�y�[�W�ւ�URL
<input type=text name='tu' value="$FORM2{tu}" size=40>
(6)���j���[�y�[�W�̃^�C�g�� *
<input type=text name='mt' value="$FORM2{mt}" size=40>
_MY_
$main_html.=<<"_HTML_";
<tr><td nowrap><small>(7)���j���[�y�[�W�̃w�b�_�[</small></td><td colspan=2><span>
\$title�����j���[�y�[�W�̃^�C�g��<br>\$top���g�b�v�y�[�W�ւ̃����N<br>\$imode���g�ѐ�p�ւ̃����N�@�@�Ɏ����ϊ�<br><textarea cols=70 rows=5 name=hd>\n$FORM3{hd}</textarea></span></td></tr>
<tr><td nowrap><small>(8)�T�u�y�[�W�̃w�b�_�[</small></td><td colspan=2><span>
\$title�����j���[�y�[�W�̃^�C�g��<br>\$sub_title���T�u�y�[�W�̃^�C�g��<br>\$genre���W��������<br>\$mode�����[�h��<br>\$top���g�b�v�y�[�W�ւ̃����N<br>\$index�����j���[�y�[�W�̃����N<br>\$challenge������y�[�W�ւ̃����N<br>\$high�������ю҃y�[�W�ւ̃����N<br>\$graph�����ѕ��z�ւ̃����N<br>\$score���o��󋵂ւ̃����N<br>\$add����蓊�e�ւ̃����N�@�@�Ɏ����ϊ�<br><textarea cols=70 rows=5 name=shd>\n$FORM3{shd}</textarea></span></td></tr>
<tr><td nowrap><small>(9)���j���[�y�[�W�̃R�����g</small></td><td colspan=2><span>
���s��&lt;BR&gt;�@�@�Ɏ����ϊ�<br><textarea cols=70 rows=5 name=tmes>\n$FORM3{tmes}</textarea><br><input type=checkbox name=tt value=1$FORM{'tt-1'}>table�ŕ\\��</span></td></tr>
<tr><td nowrap><small>(10)�X�^�C���V�[�g *</small></td><td colspan=2><span>
<input type=radio name=stl value=0$FORM{'stl-0'}>�g��Ȃ�<br>
<input type=radio name=stl value=1$FORM{'stl-1'}>�g��<br>
<textarea cols=70 rows=5 name=stl-2>\n$FORM3{'stl-2'}</textarea></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(11)�V�X�e���f�U�C��
${&select_sysdesign($FORM{sdes})}$ret
(12)���j���[�y�[�W�\\������ *
<input type=radio name='ey' value="0"$FORM{'ey-0'}>�ڍׁ@<input type=radio name='ey' value="1"$FORM{'ey-1'}>���ʁ@<input type=radio name='ey' value="2"$FORM{'ey-2'}>�ȈՁ@<input type=radio name='ey' value="3"$FORM{'ey-3'}>�ꗗ
(13)�񓚎��Ԃɂ�鏇�ʕt�� *
<input type=radio name='rt' value="0"$FORM{'rt-0'}>�s��Ȃ��@<input type=radio name='rt' value="1"$FORM{'rt-1'}>�s��
(14)���������܂�Ԃ� *
<input type=radio name='wr' value="0"$FORM{'wr-0'}>�s��Ȃ��@<input type=radio name='wr' value="1"$FORM{'wr-1'}>�s��
_MY_
$main_html.=<<"_HTML_";
<tr><td colspan=3><center><br><span><input type=submit value="�@�@�ۑ��@�@"></span></center></td></tr></table></form>
${&focus_move('li')}$ret
_HTML_
}
#************************************************
# �W�������ҏW���HTML�\������
#************************************************
sub edit_genre_html{
&list_genre_html($FORM{d});
&color_html;
&form_to_form;
$main_html.=<<"_HTML_";
$formop_nh
<input type=hidden name=type value=editg2>
<input type=hidden name=menu value=1>
<span><br><br><b>���e���ڂ���͂��ҏW�{�^���������Ă��������B</b>( * ��͕K�{����)<br><br>
<b>���W�������ݒ�t�H�[����</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=genre target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
_HTML_
$main_html.=&my_print(<<"_MY_");
<center>�����������V�W�������쐬���̐ݒ聡��������</center></span>\t#bbbbbb\n
(1)�f�B���N�g�� *
<input type=hidden name=d value="$FORM{d}">$FORM{d}
<center>�����������W�������̓���ݒ聡��������</center>\t#eeaaaa\n
(2)�^�C�g�� *
<input type=text name='t' value="$FORM2{t}" size=45>
_MY_
$main_html.="<tr><td nowrap><small>(3)�Љ</small></td><td colspan=2><span>���s��&lt;BR&gt;�@�@�Ɏ����ϊ�<br><textarea name='tc' cols=45 rows=5>\n$FORM3{tc}</textarea></span></td></tr>";
$main_html.="<tr><td nowrap><small>(4)�N�C�Y�J�n���b�Z�[�W</small></td><td colspan=2><span>
<table border=0><tr><td nowrap><span>���s<br>\$title<br>\$quiz_max<br>\$play_max<br>\$lose_max<br>\$challenge<br>\$high<br>\$time<br>\$champion</span></td><td nowrap><span>��&lt;BR&gt;<br>���W�������^�C�g��<br>������萔<br>���o�萔<br>�����e�듚��<br>������Ґ�<br>�����i���C��(��)<br>����������(�b)<br>���ō�����</span></td></tr></table>�Ɏ����ϊ�<br><textarea name='stc' cols=45 rows=5>\n$FORM3{stc}</textarea></span></td></tr>";
$main_html.=<<"_HTML_";
<tr><td nowrap><small>(5)���t�@�C�� *</small></td><td colspan=2>
_HTML_
if($#genre_dir_orign > 0){
$main_html.=<<"_HTML_";
<span><input type=radio name='md' value='0'$FORM{'md-0'}>�I���W�i�����t�@�C�����g�p����<br>
<table border=0 cellspacing=0 cellpadding=0>
<tr><td colspan=2 nowrap><span>
<input type=radio name='md' value='1'$FORM{'md-1'}>���̃W�������̖��t�@�C�����g�p����@</span></td></tr>
<tr><td><span>�@�@�@�@</span></td><td>
<table border=1><tr><td>�W��������</td><td>�g�p��萔</td>
_HTML_
foreach(@genre_dir_orign){
if($FORM{d} eq $_){next;}
$main_html.=<<"_HTML_";
<tr><td nowrap><span>$title{$_}</span></td>
<td nowrap><span><input type=text size=4 name='smd-$_' value="$FORM2{"smd-$_"}" size=15>�� (���p���� ���� all)</span></td></tr>
_HTML_
}
$main_html.='</table></td></tr></table></td></tr>';
}else{
$main_html.="<span><input type=hidden name='md' value='0'>�I���W�i�����t�@�C�����g�p����</td></tr>";
}
$main_html.=&my_print(<<"_MY_");
(6)�W�������̓����� *
<input type=radio name='me' value='1'$FORM{'me-1'}>���J��\t<input type=radio name='me' value='0'$FORM{'me-0'}>$_underconst
(7)���e���̎�t *
<input type=radio name='ct' value="1"$FORM{'ct-1'}>�󂯕t����@<input type=radio name='ct' value="0"$FORM{'ct-0'}>�󂯕t���Ȃ�
(8)�e�L�X�g�`���̓��e��� *
<input type=radio name='nt' value="0"$FORM{'nt-0'}>�󂯕t����@<input type=radio name='nt' value="1"$FORM{'nt-1'}>�󂯕t���Ȃ�
(9)���e���̎����̗p *
<input type=radio name='dc' value="0"$FORM{'dc-0'}>�s��Ȃ��@<input type=radio name='dc' value="1"$FORM{'dc-1'}>�s��
(10)�o��󋵕\\���ł̖�蕶�\\�� *
<input type=radio name='sd' value="1"$FORM{'sd-1'}>�s��Ȃ��@<input type=radio name='sd' value="0"$FORM{'sd-0'}>�s��
(11)��蕶�ւ̍쐬�ҕ\\�� *
<input type=radio name='ath' value="1"$FORM{'ath-1'}>�s���@<input type=radio name='ath' value="0"$FORM{'ath-0'}>�s��Ȃ�
(12)�f�U�C��
${&select_design($FORM{gdes})}$ret
<center>�������������[�h�P�̓���ݒ聡��������</center>\t#eeeeaa\n
(13)���[�h�� *
<input type=text name='mn1' value="$FORM2{mn1}" size=20>
(14)����\\�� *
<input type=radio name='sa1' value='0'$FORM{'sa1-0'}>�s��Ȃ�\t<input type=radio name='sa1' value='1'$FORM{'sa1-1'}>�s��
(15)�o�菇�� *
<input type=radio name='r1' value='1'$FORM{'r1-1'}>�����_��\t<input type=radio name='r1' value='0'$FORM{'r1-0'}>�Œ�
(16)�g�p��萔 *
<input type=radio name=qm1 value="1"$FORM{'qm1-1'}>�S�o�^��萔\t<input type=radio name=qm1 value="0"$FORM{'qm1-0'}><input type=text name='qm1-2' value="$FORM2{'qm1-2'}" size=5>��܂�
(17)�o���萔 *
<input type=radio name=pm1 value="1"$FORM{'pm1-1'}>�S�g�p��萔\t<input type=radio name=pm1 value="0"$FORM{'pm1-0'}><input type=text name='pm1-2' value="$FORM2{'pm1-2'}" size=5>��
(18)�ꊇ�o�� *
<input type=radio name=bd1 value="0"$FORM{'bd1-0'}>�s��Ȃ�\t<input type=radio name=bd1 value="1"$FORM{'bd1-1'}>�s��
(19)�I�������듚�� *
<input type=radio name=lm1 value="1"$FORM{'lm1-1'}>�S�o���萔\t<input type=radio name=lm1 value="0"$FORM{'lm1-0'}><input type=text name='lm1-2' value="$FORM2{'lm1-2'}" size=5>��
(20)�������� *
<input type=radio name=tl1 value="1"$FORM{'tl1-1'}>����\t<input type=radio name=tl1 value="0"$FORM{'tl1-0'}><input type=text name='tl1-2' value="$FORM2{'tl1-2'}" size=5>�b
(21)���i�_ *
<input type=text name='hb1' value="$FORM2{hb1}" size=5>���ȏ�
(22)�����ю҂�BACK UP *
<input type=radio name=hbu1 value="0"$FORM{'hbu1-0'}>�s��Ȃ�\t<input type=radio name=hbu1 value="1"$FORM{'hbu1-1'}>�s��<input type=text name='hbu1-2' value="$FORM2{'hbu1-2'}" size=5>������
(23)�����ю҂�BACK UP���� *
<input type=radio name=hbw1 value="1"$FORM{'hbw1-1'}>�㏑��\t<input type=radio name=hbw1 value="0"$FORM{'hbw1-0'}>�ʃt�@�C��
(24)���ѕ��z��BACK UP *
<input type=radio name=sbu1 value="0"$FORM{'sbu1-0'}>�s��Ȃ�\t<input type=radio name=sbu1 value="1"$FORM{'sbu1-1'}>�s��<input type=text name='sbu1-2' value="$FORM2{'sbu1-2'}" size=5>������
(25)���ѕ��z��BACK UP���� *
<input type=radio name=sbw1 value="1"$FORM{'sbw1-1'}>�㏑��\t<input type=radio name=sbw1 value="0"$FORM{'sbw1-0'}>�ʃt�@�C��
(26)���ѕ��z�ȗ��\\�� *
<input type=text name='gb1' value="$FORM2{gb1}" size=5>���ȏ�̃O���t�͏ȗ��\\��
(27)���ѕ��z�W�v�P�� *
<input type=text name='hd1' value="$FORM2{hd1}" size=5>�█�ɏW�v
(28)�����юғ������� *
<input type=radio name=dl1 value="1"$FORM{'dl1-1'}>������\t<input type=radio name=dl1 value="0"$FORM{'dl1-0'}>�ߋ�<input type=text name='dl1-2' value="$FORM2{'dl1-2'}" size=5>��
(29)�����юҐl������ *
<input type=radio name=nl1 value="1"$FORM{'nl1-1'}>������\t<input type=radio name=nl1 value="0"$FORM{'nl1-0'}>���<input type=text name='nl1-2' value="$FORM2{'nl1-2'}" size=5>�l
(30)�a������l�� *
���<input type=text name=no1 value="$FORM2{no1}" size=5>�l
(31)�����ю҃R�����g�L�^ *
<input type=radio name=rc1 value="0"$FORM{'rc1-0'}>�s��Ȃ�\t<input type=radio name=rc1 value="1"$FORM{'rc1-1'}>�s��
(32)���z�X�g���X�R�A *
<input type=radio name=dh1 value="1"$FORM{'dh1-1'}>�F�߂�\t<input type=radio name=dh1 value="0"$FORM{'dh1-0'}>�F�߂Ȃ�
<center>�������������[�h�Q�̓���ݒ聡��������</center></span>\t#eeaaee\n
(33)���[�h��<font color=red>(��)</cont>
<input type=text name='mn2' value="$FORM2{mn2}" size=20>
(34)����\\��
<input type=radio name='sa2' value='0'$FORM{'sa2-0'}>�s��Ȃ�\t<input type=radio name='sa2' value='1'$FORM{'sa2-1'}>�s��
(35)�o�菇��
<input type=radio name='r2' value='1'$FORM{'r2-1'}>�����_��\t<input type=radio name='r2' value='0'$FORM{'r2-0'}>�Œ�
(36)�g�p��萔
<input type=radio name=qm2 value="1"$FORM{'qm2-1'}>�S�o�^��萔\t<input type=radio name=qm2 value="0"$FORM{'qm2-0'}><input type=text name='qm2-2' value="$FORM2{'qm2-2'}" size=5>��܂�
(37)�o���萔
<input type=radio name=pm2 value="1"$FORM{'pm2-1'}>�S�g�p��萔\t<input type=radio name=pm2 value="0"$FORM{'pm2-0'}><input type=text name='pm2-2' value="$FORM2{'pm2-2'}" size=5>��
(38)�ꊇ�o�� *
<input type=radio name=bd2 value="0"$FORM{'bd2-0'}>�s��Ȃ�\t<input type=radio name=bd2 value="1"$FORM{'bd2-1'}>�s��
(39)�I�������듚��
<input type=radio name=lm2 value="1"$FORM{'lm2-1'}>�S�o���萔\t<input type=radio name=lm2 value="0"$FORM{'lm2-0'}><input type=text name='lm2-2' value="$FORM2{'lm2-2'}" size=5>��
(40)�������� *
<input type=radio name=tl2 value="1"$FORM{'tl2-1'}>����\t<input type=radio name=tl2 value="0"$FORM{'tl2-0'}><input type=text name='tl2-2' value="$FORM2{'tl2-2'}" size=5>�b
(41)���i�_
<input type=text name='hb2' value="$FORM2{hb2}" size=5>���ȏ�
(42)�����ю҂�BACK UP *
<input type=radio name=hbu2 value="0"$FORM{'hbu2-0'}>�s��Ȃ�\t<input type=radio name=hbu2 value="1"$FORM{'hbu2-1'}>�s��<input type=text name='hbu2-2' value="$FORM2{'hbu2-2'}" size=5>������
(43)�����ю҂�BACK UP���� *
<input type=radio name=hbw2 value="1"$FORM{'hbw2-1'}>�㏑��\t<input type=radio name=hbw2 value="0"$FORM{'hbw2-0'}>�ʃt�@�C��
(44)���ѕ��z��BACK UP *
<input type=radio name=sbu2 value="0"$FORM{'sbu2-0'}>�s��Ȃ�\t<input type=radio name=sbu2 value="1"$FORM{'sbu2-1'}>�s��<input type=text name='sbu2-2' value="$FORM2{'sbu2-2'}" size=5>������
(45)���ѕ��z��BACK UP���� *
<input type=radio name=sbw2 value="1"$FORM{'sbw2-1'}>�㏑��\t<input type=radio name=sbw2 value="0"$FORM{'sbw2-0'}>�ʃt�@�C��
(46)���ѕ��z�ȗ��\\��
<input type=text name='gb2' value="$FORM2{gb2}" size=5>���ȏ�̃O���t�͏ȗ��\\��
(47)���ѕ��z�W�v�P��
<input type=text name='hd2' value="$FORM2{hd2}" size=5>�█�ɏW�v
(48)�����юғ�������
<input type=radio name=dl2 value="1"$FORM{'dl2-1'}>������\t<input type=radio name=dl2 value="0"$FORM{'dl2-0'}>�ߋ�<input type=text name='dl2-2' value="$FORM2{'dl2-2'}" size=5>��
(49)�����юҐl������
<input type=radio name=nl2 value="1"$FORM{'nl2-1'}>������\t<input type=radio name=nl2 value="0"$FORM{'nl2-0'}>���<input type=text name='nl2-2' value="$FORM2{'nl2-2'}" size=5>�l
(50)�a������l�� *
���<input type=text name=no2 value="$FORM2{no2}" size=5>�l
(51)�����ю҃R�����g�L�^ *
<input type=radio name=rc2 value="0"$FORM{'rc2-0'}>�s��Ȃ�\t<input type=radio name=rc2 value="1"$FORM{'rc2-1'}>�s��
(52)���z�X�g���X�R�A
<input type=radio name=dh2 value="1"$FORM{'dh2-1'}>�F�߂�\t<input type=radio name=dh2 value="0"$FORM{'dh2-0'}>�F�߂Ȃ�
<center><br><input type=submit value="�@�@�ۑ��@�@"></center>
_MY_
$main_html.='</table><small><font color=red>(��)</font>���[�h�Q�̃��[�h�������͂���Ă���Ƃ��̂݃��[�h�Q�����삷��B</small></form>';
$main_html.="${&focus_move('t')}$ret";
}
#************************************************
# �V�X�e���f�U�C���ҏWHTML
#************************************************
sub edit_sysdesign_html{
local($button);
local($edit,$type)=@_;
if($#sysdesign_list>=0){
&list_sysdesign_html();
}
&form_to_form;
if($type eq 'edit'){
$button='�ۑ�';
$edit=$sysdesign_title{$edit};
}elsif($type eq 'copy'){
$button='�����ۑ�';
$edit="$sysdesign_title{$edit}";
}else{
$button='�V�K�쐬�ۑ�';
$edit="�V�K�쐬";
}
$main_html.=<<"_HTML_";
$formop_nh
<input type=hidden name=type value=sdesed2>
<input type=hidden name=id value="$FORM{id}">
<input type=hidden name=edittype value="$type">
<span><br><br><b>���e���ڂ���͂�$button�{�^���������Ă��������B</b>( * ��͕K�{����)<br><br>
<b>���V�X�e���f�U�C���ݒ�t�H�[����</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=sysd target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3 bgcolor=#eeaaee><span><center>�����������V�X�e���f�U�C���ݒ聡��������</center></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(1)�ҏW��
$edit
(2)�V�X�e���f�U�C���� *
<input type=text name='sdt' value="$FORM{sdt}" size=30>
(3)���j���[�y�[�W�̕ǎ�
<input type=text name='tw' value="$FORM2{tw}" size=30>
(4)���j���[�y�[�W�̔w�i�F *
<input type=text name='tbc' value="$FORM2{tbc}" size=10>
(5)���j���[�y�[�W�̕\\�̐F *
<input type=text name='ttc' value="$FORM2{ttc}" size=10>
(6)���j���[�y�[�W�̃W�������F *
<input type=text name='tjc' value="$FORM2{tjc}" size=10>
(7)���j���[�y�[�W�̏��F *
<input type=text name='tic' value="$FORM2{tic}" size=10>
(8)���j���[�y�[�W�̃R�����g�F *
<input type=text name='tcc' value="$FORM2{tcc}" size=10>
(9)���j���[�y�[�W�̍����юҐF *
<input type=text name='thc' value="$FORM2{thc}" size=10>
(10)���j���[�y�[�W�̕\\�̘g�̐F *
<input type=text name='tbdc' value="$FORM2{tbdc}" size=10>
(11)���j���[�y�[�W�̕����F *
<input type=text name='txc' value="$FORM2{txc}" size=10>
(12)���j���[�y�[�W�̃����N�F *
<input type=text name='lc' value="$FORM2{lc}" size=10>
(13)���j���[�y�[�W�̊��K�⃊���N�F *
<input type=text name='vc' value="$FORM2{vc}" size=10>
(14)���j���[�y�[�W�̕\\�̘g�̍��� *
<input type=text name='tbdh' value="$FORM2{tbdh}" size=10>
(15)���j���[�y�[�W�̕\\�̘g�̕� *
<input type=text name='tbd' value="$FORM2{tbd}" size=10>
(16)���j���[�y�[�W�̕\\�̘g�̓��� *
<input type=text name='tbdi' value="$FORM2{tbdi}" size=10>
(17)���ї����O���t�摜�P *
<input type=text name='ag' value="$FORM2{ag}" size=30>
(18)���ї����O���t�摜�Q *
<input type=text name='bg' value="$FORM2{bg}" size=30>
(19)�\\�̃��C�A�E�g *
<input type=radio name='al' value="l"$FORM{'al-l'}>�����@<input type=radio name='al' value="c"$FORM{'al-c'}>�����@<input type=radio name='al' value="r"$FORM{'al-r'}>�E��
(20)�\\���������C�A�E�g *
<input type=radio name='wal' value="l"$FORM{'wal-l'}>�����@<input type=radio name='wal' value="c"$FORM{'wal-c'}>�����@<input type=radio name='wal' value="r"$FORM{'wal-r'}>�E��
_MY_
$main_html.=<<"_HTML_";
<tr><td colspan=3><center><br><span><input type=submit value="�@�@ $button �@�@"></span></center></td></tr></table></form>
${&focus_move('sdt')}$ret
_HTML_
}
#************************************************
# �W�������f�U�C���ҏWHTML
#************************************************
sub edit_design_html{
local($button);
local($edit,$type)=@_;
if($#design_list>=0){
&list_design_html();
}
&form_to_form;
if($type eq 'edit'){
$button='�ۑ�';
$edit=$design_title{$edit};
}elsif($type eq 'copy'){
$button='�����ۑ�';
$edit="$design_title{$edit}";
}else{
$button='�V�K�쐬�ۑ�';
$edit="�V�K�쐬";
}
$main_html.=<<"_HTML_";
$formop_nh
<input type=hidden name=type value=gdesed2>
<input type=hidden name=id value="$FORM{id}">
<input type=hidden name=edittype value="$type">
<span><br><br><b>���e���ڂ���͂�$button�{�^���������Ă��������B</b>( * ��͕K�{����)<br><br>
<b>���W�������f�U�C���ݒ�t�H�[����</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=gend target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3 bgcolor=#eeaaee><span><center>�����������W�������f�U�C���ݒ聡��������</center></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(1)�ҏW��
$edit
(2)�W�������f�U�C���� *
<input type=text name='gdt' value="$FORM{gdt}" size=30>
(3)�����F *
<input type=text name='gtc' value="$FORM2{gtc}" size=10>
(4)�����N�����F *
<input type=text name='glc' value="$FORM2{glc}" size=10>
(5)���K�⃊���N�����F *
<input type=text name='gvc' value="$FORM2{gvc}" size=10>
(6)�a������ҕ����F *
<input type=text name='gcc' value="$FORM2{gcc}" size=10>
(7)��{�w�i�F *
<input type=text name='gmc' value="$FORM2{gmc}" size=10>
(8)�������w�i�F *
<input type=text name='gwi' value="$FORM2{gwi}" size=10>
(9)�s�������w�i�F *
<input type=text name='glo' value="$FORM2{glo}" size=10>
(10)���E�C���h�E�̐F *
<input type=text name='gcm' value="$FORM2{gcm}" size=10>
(11)�\\�̃w�b�_�[�F *
<input type=text name='thc' value="$FORM2{thc}" size=10>
(12)�\\�̐F *
<input type=text name='tdc' value="$FORM2{tdc}" size=10>
(13)�\\�̘g�̐F *
<input type=text name='bdc' value="$FORM2{bdc}" size=10>
(14)�\\�̘g�̍��� *
<input type=text name='bdh' value="$FORM2{bdh}" size=10>
(15)�\\�̘g�̕� *
<input type=text name='bd' value="$FORM2{bd}" size=10>
(16)�\\�̘g�̓��� *
<input type=text name='bdi' value="$FORM2{bdi}" size=10>
(17)��{�ǎ�
<input type=text name='gw' value="$FORM2{gw}" size=30>
(18)�������ǎ�
<input type=text name='gww' value="$FORM2{gww}" size=30>
(19)�s�������ǎ�
<input type=text name='glw' value="$FORM2{glw}" size=30>
(20)����\\�� *
<input type=text name='wsg' value="$FORM2{wsg}" size=100>
(21)�s����\\�� *
<input type=text name='lsg' value="$FORM2{lsg}" size=100>
(22)�^�C���I�[�o�[�\\�� *
<input type=text name='osg' value="$FORM2{osg}" size=100>
(23)������MIDI
<input type=text name='wmd' value="$FORM2{wmd}" size=30>
(24)�s������MIDI
<input type=text name='lmd' value="$FORM2{lmd}" size=30>
(25)�N�C�Y�I����MIDI
<input type=text name='emd' value="$FORM2{emd}" size=30>
(26)�����юҗpMIDI
<input type=text name='hmd' value="$FORM2{hmd}" size=30>
_MY_
$main_html.=<<"_HTML_";
<tr><td colspan=3><center><br><span><input type=submit value="�@�@ $button �@�@"></span></center></td></tr></table></form>
${&focus_move('gdt')}$ret
_HTML_
}
#************************************************
# ���o�^����HTML
#************************************************
sub edit_quiz_html{
if($#mondai < 0){$main_html.='<span><br><br><b>���ҏW���I�����X�g��</b><br><br>�����݂��̃W�������œo�^�ς݂̖��͂���܂���B</span>';return;}
$main_html.=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qedit1>
<input type=hidden name=menu value=1>
<input type=hidden name=ed value=edit>
<span><br><br><b>���ȉ��̃��X�g����ҏW���������̃��W�I�{�^���Ƀ`�F�b�N�����A���s�{�^���������Ă��������B</b><br><br>
_HTML_
local($colspan);$colspan=2;
$FORM{"qn-$FORM{qn}"}=' checked';
$main_html.='<b>���ҏW���I�����X�g��</b></span>';
$main_html.="<table $sys_tbl_opt bgcolor='$sys_color'><tr><td nowrap><small>�ԍ�</small></td>";
$main_html.="<td><small>�I��</small></td>";
if($FORM{lst_q} ne ''){$main_html.='<td><small>���</small></td>';$colspan++;}
if($FORM{lst_a} ne ''){$main_html.='<td><small>��</small></td>';$colspan++;}
if($FORM{lst_m} ne ''){$main_html.='<td colspan=4><small>�듚</small></td>';$colspan=$colspan+4;}
if($FORM{lst_am} ne ''){$main_html.='<td><small>�𓚃��b�Z�[�W</small></td>';$colspan++;}
if($FORM{lst_mm} ne ''){$main_html.='<td><small>�듚���b�Z�[�W</small></td>';$colspan++;}
if($FORM{lst_cf} ne ''){$main_html.='<td><small>�Q�l����</small></td>';$colspan++;}
if($FORM{lst_dg} ne ''){$main_html.='<td><small>�����e</small></td>';$colspan++;}
if($FORM{lst_mm1} ne ''){$main_html.='<td colspan=4><small>�듚�ʃ��b�Z�[�W</small></td>';$colspan=$colspan+4;}
if($FORM{lst_ath} ne ''){$main_html.='<td colspan=1><small>�쐬��</small></td>';$colspan++;}
if($FORM{lst_at} ne ''){$main_html.='<td colspan=1><small>�񓚕���</small></td>';$colspan++;}
$main_html.='</tr>';
$i=0;@opt=('�I��','����');
foreach (@mondai){
$i++;
$main_html.="<tr><td nowrap>$i</td>\n";
$main_html.="<td><input type=radio name=qn value='$i'".$FORM{"qn-$i"}."></td>";
if($FORM{lst_q} ne ''){$main_html.="<td nowrap>$mondai[$i-1]</td>";}
if($FORM{lst_a} ne ''){$main_html.="<td nowrap>$ans[$i-1]</td>";}
if($FORM{lst_m} ne ''){$main_html.="<td nowrap>$misans1[$i-1]</td><td nowrap>$misans2[$i-1]</td><td nowrap>$misans3[$i-1]</td><td nowrap>$misans4[$i-1]</td>";}
if($FORM{lst_am} ne ''){$main_html.="<td nowrap>$anscom[$i-1]</td>";}
if($FORM{lst_mm} ne ''){$main_html.="<td nowrap>$misanscom[$i-1]</td>";}
if($FORM{lst_cf} ne ''){$main_html.="<td nowrap>$cf[$i-1]</td>";}
if($FORM{lst_dg} ne ''){$main_html.="<td nowrap>$digest[$i-1]</td>";}
if($FORM{lst_mm1} ne ''){$main_html.="<td nowrap>$misanscom1[$i-1]</td><td nowrap>$misanscom2[$i-1]</td><td nowrap>$misanscom3[$i-1]</td><td nowrap>$misanscom4[$i-1]</td>";}
if($FORM{lst_ath} ne ''){$main_html.="<td nowrap>$author[$i-1]</td>";}
if($FORM{lst_at} ne ''){$main_html.="<td nowrap>$opt[$anstype[$i-1]]</td>";}
$main_html.='</tr>';
}
$FORM{"lst_q_$FORM{lst_q}"}=' checked';
$FORM{"lst_a_$FORM{lst_a}"}=' checked';
$FORM{"lst_m_$FORM{lst_m}"}=' checked';
$FORM{"lst_am_$FORM{lst_am}"}=' checked';
$FORM{"lst_mm_$FORM{lst_mm}"}=' checked';
$FORM{"lst_cf_$FORM{lst_cf}"}=' checked';
$FORM{"lst_dg_$FORM{lst_dg}"}=' checked';
$FORM{"lst_mm1_$FORM{lst_mm1}"}=' checked';
$FORM{"lst_ath_$FORM{lst_ath}"}=' checked';
$FORM{"lst_at_$FORM{lst_at}"}=' checked';
$main_html.=<<"_HTML_";
<tr><td colspan=$colspan nowrap><span><center><input type=submit value="  ���s  ">
<input type=checkbox name=lst_q$FORM{lst_q_1} value=1>���
<input type=checkbox name=lst_a$FORM{lst_a_1} value=1>��
<input type=checkbox name=lst_m$FORM{lst_m_1} value=1>�듚
<input type=checkbox name=lst_am$FORM{lst_am_1} value=1>�𓚃��b�Z�[�W
<input type=checkbox name=lst_mm$FORM{lst_mm_1} value=1>�듚���b�Z�[�W
<input type=checkbox name=lst_cf$FORM{lst_cf_1} value=1>�Q�l����
<input type=checkbox name=lst_dg$FORM{lst_dg_1} value=1>�����e
<input type=checkbox name=lst_mm1$FORM{lst_mm1_1} value=1>�듚�ʃ��b�Z�[�W
<input type=checkbox name=lst_ath$FORM{lst_ath_1} value=1>�쐬��
<input type=checkbox name=lst_at$FORM{lst_at_1} value=1>�񓚕���
</center></span></td></tr></table></form>
_HTML_
}
#************************************************
# ������formHTML
#************************************************
sub edit_quiz_form{
&form_to_form;
$file_age=time-(-M "$FORM{d}/$mondai_$FORM{d}\.cgi")*(60*60*24);
if($FORM{ed} eq 'edit'){$FORM{ed_edit}=' checked';}
else{$FORM{ed_new}=' checked';}
if($FORM{qn} ne ''){
if($FORM{ed} eq 'edit'){
$FORM{ed_edit}=' checked';
$num_text="<input type=radio name=ed value='edit'$FORM{ed_edit}>�ҏW���� $FORM{qn} ���";
}else{$FORM{ed_new}=' checked';}
}else{$FORM{ed_new}=' checked';$FORM{"qn-$FORM{qn}"}=' checked';$FORM{qn}='';}
$FORM{"atype_$FORM{atype}"}=' checked';
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qedit2>
<input type=hidden name=fa value="$file_age">
<input type=hidden name=qn value="$FORM2{qn}">
<input type=hidden name=lst_q value="$FORM2{lst_q}">
<input type=hidden name=lst_a value="$FORM2{lst_a}">
<input type=hidden name=lst_m value="$FORM2{lst_m}">
<input type=hidden name=lst_am value="$FORM2{lst_am}">
<input type=hidden name=lst_mm value="$FORM2{lst_mm}">
<input type=hidden name=lst_cf value="$FORM2{lst_cf}">
<input type=hidden name=lst_dg value="$FORM2{lst_dg}">
<input type=hidden name=lst_mm1 value="$FORM2{lst_mm1}">
<input type=hidden name=lst_ath value="$FORM2{lst_ath}">
<input type=hidden name=lst_at value="$FORM2{lst_at}">
<input type=hidden name=menu value=1>
<span><br><br><b>���e���ڂɓ��͂��A���M�{�^���������Ă��������B<br>
���o�^�̖��̕ҏW�́A�܂����̕ҏW���I�����X�g����I��ł���s���ĉ������B</b>�@( * ��͕K�{���ڂł��B)<br><br>
<b>�����ҏW�t�H�[����</b></span><small>���s��&lt;BR&gt;�@�@�Ɏ����ϊ�</small>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3><center><span>
<input type=radio name=ed value='new'$FORM{ed_new}>�V�K�ǉ��@
$num_text
</center></span></td></tr>
<tr><td><small>�񓚕���</small></td><td colspan=2><input type=checkbox name=atype value=1 $FORM{atype_1}>�e�L�X�g���͕���</td></tr>
<tr><td><small>��蕶 *</small></td><td colspan=2><textarea name=qqu cols=65 rows=3>\n$FORM3{qqu}</textarea></td></tr>
<tr><td><small>���� * ��</small></td><td colspan=2><textarea name=qas cols=65 rows=3>\n$FORM3{qas}</textarea></td></tr>
<tr><td><small>�듚�P * ��</small></td><td colspan=2><textarea name=qmas1 cols=65 rows=3>\n$FORM3{qmas1}</textarea></td></tr>
<tr><td><small>�듚�Q ��</small></td><td colspan=2><textarea name=qmas2 cols=65 rows=3>\n$FORM3{qmas2}</textarea></td></tr>
<tr><td><small>�듚�R ��</small></td><td colspan=2><textarea name=qmas3 cols=65 rows=3>\n$FORM3{qmas3}</textarea></td></tr>
<tr><td><small>�듚�S ��</small></td><td colspan=2><textarea name=qmas4 cols=65 rows=3>\n$FORM3{qmas4}</textarea></td></tr>
<tr><td><small>�������R�����g</small></td><td colspan=2><textarea name=qac cols=65 rows=2>\n$FORM3{qac}</textarea></span></td></tr>
<tr><td nowrap><small>�s�������R�����g</small></td><td colspan=2><textarea name=qmac cols=65 rows=2>\n$FORM3{qmac}</textarea></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
�Q�l����
<small><input type=text size=65 name=qcf value="$FORM2{qcf}"></small>
�����e
<small><input type=text size=65 name=qdg value="$FORM2{qdg}"></small>
_MY_
$main_html.=<<"_HTML_";
<tr><td nowrap><small>�듚�P���R�����g</small></td><td colspan=2><textarea name=qmac1 cols=65 rows=2>\n$FORM3{qmac1}</textarea></span></td></tr>
<tr><td nowrap><small>�듚�Q���R�����g</small></td><td colspan=2><textarea name=qmac2 cols=65 rows=2>\n$FORM3{qmac2}</textarea></span></td></tr>
<tr><td nowrap><small>�듚�R���R�����g</small></td><td colspan=2><textarea name=qmac3 cols=65 rows=2>\n$FORM3{qmac3}</textarea></span></td></tr>
<tr><td nowrap><small>�듚�S���R�����g</small></td><td colspan=2><textarea name=qmac4 cols=65 rows=2>\n$FORM3{qmac4}</textarea></span></td></tr>
<tr><td nowrap><small>�쐬��</small></td><td colspan=2><small><input type=text size=65 name=auth value="$FORM2{auth}"></small></td></tr>
<tr><td colspan=3><center><table border=0><tr><td><span><input type=submit value="�@�@ ���M �@�@"></span></td></form>
$formop_hd
<input type=hidden name=type value=qedit1>
<input type=hidden name=ed value=new>
<input type=hidden name=fa value="$file_age">
<input type=hidden name=lst_q value="$FORM2{lst_q}">
<input type=hidden name=lst_a value="$FORM2{lst_a}">
<input type=hidden name=lst_m value="$FORM2{lst_m}">
<input type=hidden name=lst_am value="$FORM2{lst_am}">
<input type=hidden name=lst_mm value="$FORM2{lst_mm}">
<input type=hidden name=lst_cf value="$FORM2{lst_cf}">
<input type=hidden name=lst_dg value="$FORM2{lst_dg}">
<input type=hidden name=lst_mm1 value="$FORM2{lst_mm1}">
<input type=hidden name=lst_ath value="$FORM2{lst_ath}">
<input type=hidden name=lst_at value="$FORM2{lst_at}">
<input type=hidden name=menu value=1>
<td><span><input type=submit value="�@�@�N���A�@�@"></span></td></tr></table>
</center></td></tr></table></form>
���񓚕������e�L�X�g���͌`���̏ꍇ�A�e�s�������i�듚�j�ƂȂ�܂��B<br>
�����ꂩ�̍s�ƁA�񓚗��ɓ��͂��ꂽ�����񂪈�v�����ꍇ�����i�듚�j�ƂȂ�܂��B<br>
_HTML_
}
#************************************************
# ���o�^����HTML
#************************************************
sub edit_cont_html{
if($#mondai < 0){$main_html.='<span><br><br><b>���ҏW���I�����X�g��</b><br><br>���݂��̃W�������œo�^�ς݂̓��e���͂���܂���B</span>';return;}
$main_html.=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qcont>
<input type=hidden name=menu value=1>
<input type=hidden name=ed value=1>
<span><br><br><b>���ȉ��̃��X�g����ҏW���������̃��W�I�{�^���Ƀ`�F�b�N�����A���s�{�^���������Ă��������B<br>
�܂��A�ǉ��폜�A�폜���s���������Ƀ`�F�b�N�����ĉ������B(�����I����)</b><br><br>
_HTML_
local($colspan);$colspan=4;
$FORM{"qn-$FORM{qn}"}=' checked';
$main_html.='<b>���ҏW���I�����X�g��</b></span>';
$main_html.="<table border=3 cellspacing=1 cellpadding=2 bgcolor='$sys_color'><tr><td nowrap><small>��<br>��</small></td>";
$main_html.="<td><small>��<br>�W</small></td><td nowrap><small>�ǉ�<br>�폜</small></td><td><small>��<br>��</small></td>";
if($FORM{lst_q} ne ''){$main_html.='<td width=300 nowrap><small>���</small></td>';$colspan++;}
if($FORM{lst_a} ne ''){$main_html.='<td width=100 nowrap><small>��</small></td>';$colspan++;}
if($FORM{lst_m} ne ''){$main_html.='<td width=100 nowrap><small>�듚</small></td>';$colspan=$colspan+4;}
if($FORM{lst_am} ne ''){$main_html.='<td width=100 nowrap><small>�������b�Z�[�W</small></td>';$colspan++;}
if($FORM{lst_mm} ne ''){$main_html.='<td width=100 nowrap><small>�듚���b�Z�[�W</small></td>';$colspan++;}
if($FORM{lst_mm1} ne ''){$main_html.='<td width=100 nowrap><small>�듚�ʃ��b�Z�[�W</small></td>';$colspan=$colspan+4;}
if($FORM{lst_cf} ne ''){$main_html.='<td width=100 nowrap><small>�Q�l����</small></td>';$colspan++;}
if($FORM{lst_dg} ne ''){$main_html.='<td width=100 nowrap><small>�����e</small></td>';$colspan++;}
if($FORM{lst_ath} ne ''){$main_html.='<td width=100 nowrap><small>�쐬��</small></td>';$colspan++;}
if($FORM{lst_at} ne ''){$main_html.='<td><small>�񓚕���</small></td>';$colspan++;}
$main_html.='</tr>';
$i=0;
my(%atype);
$atype{""}="�I��";
$atype{1}="����";
foreach (@mondai){
$i++;
if($FORM{lst_m} ne '' || $FORM{lst_mm1} ne ''){
$rownum=' rowspan=4';
}else{
$rownum='';
}
$main_html.="<tr><td nowrap$rownum>$i</td>\n";
$main_html.="<td$rownum><span><input type=radio name=qn value='$i'".$FORM{"qn-$i"}."></span></td>";
$main_html.="<td$rownum><span><input type=checkbox name='qc-$i' value='1'></span></td>";
$main_html.="<td$rownum><span><input type=checkbox name='qcd-$i' value='1'></span></td>";
if($FORM{lst_q} ne ''){$main_html.="<td$rownum>$mondai[$i-1]</td>";}
if($FORM{lst_a} ne ''){$main_html.="<td$rownum>$ans[$i-1]</td>";}
if($FORM{lst_m} ne ''){$main_html.="<td>$misans1[$i-1]</td>";}
if($FORM{lst_am} ne ''){$main_html.="<td$rownum>$anscom[$i-1]�@</td>";}
if($FORM{lst_mm} ne ''){$main_html.="<td$rownum>$misanscom[$i-1]�@</td>";}
if($FORM{lst_mm1} ne ''){$main_html.="<td>$misanscom1[$i-1]�@</td>";}
if($FORM{lst_cf} ne ''){$main_html.="<td$rownum>$cf[$i-1]�@</td>";}
if($FORM{lst_dg} ne ''){$main_html.="<td$rownum>$digest[$i-1]�@</td>";}
if($FORM{lst_ath} ne ''){$main_html.="<td$rownum>$author[$i-1]</td>";}
if($FORM{lst_at} ne ''){$main_html.="<td$rownum>$atype{$anstype[$i-1]}</td>";}
$main_html.='</tr>';
if($FORM{lst_m} ne '' && $FORM{lst_mm1} ne ''){
$main_html.=<<"_HTML_";
<tr>
<td>$misans2[$i-1]�@</td><td>$misanscom2[$i-1]�@</td>
</tr><tr>
<td>$misans3[$i-1]�@</td><td>$misanscom3[$i-1]�@</td>
</tr><tr>
<td>$misans4[$i-1]�@</td><td>$misanscom4[$i-1]�@</td>
</tr>
_HTML_
}elsif($FORM{lst_m} ne ''){
$main_html.=<<"_HTML_";
<tr>
<td>$misans2[$i-1]�@</td>
</tr><tr>
<td>$misans3[$i-1]�@</td>
</tr><tr>
<td>$misans4[$i-1]�@</td>
</tr>
_HTML_
}elsif($FORM{lst_mm1} ne ''){
$main_html.=<<"_HTML_";
<tr>
<td>$misans2[$i-1]�@</td>
</tr><tr>
<td>$misans3[$i-1]�@</td>
</tr><tr>
<td>$misans4[$i-1]�@</td>
</tr>
_HTML_
}
}
$FORM{"lst_q_$FORM{lst_q}"}=' checked';
$FORM{"lst_a_$FORM{lst_a}"}=' checked';
$FORM{"lst_m_$FORM{lst_m}"}=' checked';
$FORM{"lst_am_$FORM{lst_am}"}=' checked';
$FORM{"lst_mm_$FORM{lst_mm}"}=' checked';
$FORM{"lst_cf_$FORM{lst_cf}"}=' checked';
$FORM{"lst_dg_$FORM{lst_dg}"}=' checked';
$FORM{"lst_mm1_$FORM{lst_mm1}"}=' checked';
$FORM{"lst_ath_$FORM{lst_ath}"}=' checked';
$FORM{"lst_at_$FORM{lst_at}"}=' checked';
$main_html.=<<"_HTML_";
<tr><td colspan=$colspan nowrap><span><center><input type=submit value="  ���s  ">
<input type=checkbox name=lst_q$FORM{lst_q_1} value=1>��� 
<input type=checkbox name=lst_a$FORM{lst_a_1} value=1>��
<input type=checkbox name=lst_m$FORM{lst_m_1} value=1>�듚
<input type=checkbox name=lst_am$FORM{lst_am_1} value=1>�������b�Z�[�W
<input type=checkbox name=lst_mm$FORM{lst_mm_1} value=1>�듚���b�Z�[�W
<input type=checkbox name=lst_cf$FORM{lst_cf_1} value=1>�Q�l����
<input type=checkbox name=lst_dg$FORM{lst_dg_1} value=1>�����e
<input type=checkbox name=lst_mm1$FORM{lst_mm1_1} value=1>�듚�ʃ��b�Z�[�W
<input type=checkbox name=lst_ath$FORM{lst_ath_1} value=1>�쐬��
<input type=checkbox name=lst_at$FORM{lst_at_1} value=1>�񓚕���
</center></span></td></tr></table></form>
_HTML_
}
#************************************************
# ������formHTML
#************************************************
sub edit_cont_form{
&form_to_form;
$file_age=time-(-M "$FORM{d}/$contribute_cgi")*60*60*24;
$FORM{"atype_$FORM{atype}"}=' checked';
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qcont1>
<input type=hidden name=fa value="$file_age">
<input type=hidden name=qn value="$FORM2{qn}">
<input type=hidden name=lst_q value="$FORM2{lst_q}">
<input type=hidden name=lst_a value="$FORM2{lst_a}">
<input type=hidden name=lst_m value="$FORM2{lst_m}">
<input type=hidden name=lst_am value="$FORM2{lst_am}">
<input type=hidden name=lst_mm value="$FORM2{lst_mm}">
<input type=hidden name=lst_cf value="$FORM2{lst_cf}">
<input type=hidden name=lst_dg value="$FORM2{lst_dg}">
<input type=hidden name=lst_mm1 value="$FORM2{lst_mm1}">
<input type=hidden name=lst_ath value="$FORM2{lst_ath}">
<input type=hidden name=lst_at value="$FORM2{lst_at}">
<input type=hidden name=menu value=1>
<span><br><br><b>���e���ڂɓ��͂��A���s�{�^���������Ă��������B</b>( * ��͕K�{���ڂł��B)<br>
�w�ҏW�x�͓��e����ҏW���܂��B<br>
�w�ǉ��폜�x�͓��e�����̗p���A���e��胊�X�g����폜���܂��B<br><br>
<b>�������̓t�H�[����</b></span><small>���s��&lt;BR&gt;�@�@�Ɏ����ϊ�</small>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=2><center>
<input type=radio name=add value=0 checked>�ҏW
<input type=radio name=add value=1>�ǉ��폜
</center></td></tr>
<tr><td><small>�񓚕���</small></td><td><input type=checkbox name=atype value=1 $FORM{atype_1}>�e�L�X�g���͕���</td></tr>
<tr><td><small>��蕶 *</small></td><td><textarea name=qqu cols=65 rows=3>\n$FORM3{qqu}</textarea></td></tr>
<tr><td><small>���� * ��</small></td><td><textarea name=qas cols=65 rows=3>\n$FORM3{qas}</textarea></td></tr>
<tr><td><small>�듚�P * ��</small></td><td><textarea name=qmas1 cols=65 rows=3>\n$FORM3{qmas1}</textarea></td></tr>
<tr><td><small>�듚�Q ��</small></td><td><textarea name=qmas2 cols=65 rows=3>\n$FORM3{qmas2}</textarea></td></tr>
<tr><td><small>�듚�R ��</small></td><td><textarea name=qmas3 cols=65 rows=3>\n$FORM3{qmas3}</textarea></td></tr>
<tr><td><small>�듚�S ��</small></td><td><textarea name=qmas4 cols=65 rows=3>\n$FORM3{qmas4}</textarea></td></tr>
<tr><td><small>�������R�����g</small></td><td><textarea name=qac cols=65 rows=2>\n$FORM3{qac}</textarea></td></tr>
<tr><td nowrap><small>�s�������R�����g</td><td><textarea name=qmac cols=65 rows=2>\n$FORM3{qmac}</textarea></td></tr>
<tr><td nowrap><small>�Q�l����</td><td><input type=text size=65 name=qcf value="$FORM2{qcf}"></td></tr>
<tr><td nowrap><small>�����e</td><td><input type=text size=65 name=qdg value="$FORM2{qdg}"></td></tr>
<tr><td nowrap><small>�듚�P���R�����g</td><td><textarea name=qmac1 cols=65 rows=2>\n$FORM3{qmac1}</textarea></td></tr>
<tr><td nowrap><small>�듚�Q���R�����g</td><td><textarea name=qmac2 cols=65 rows=2>\n$FORM3{qmac2}</textarea></td></tr>
<tr><td nowrap><small>�듚�R���R�����g</td><td><textarea name=qmac3 cols=65 rows=2>\n$FORM3{qmac3}</textarea></td></tr>
<tr><td nowrap><small>�듚�S���R�����g</td><td><textarea name=qmac4 cols=65 rows=2>\n$FORM3{qmac4}</textarea></td></tr>
<tr><td nowrap><small>�쐬��</td><td><input type=text name=auth value="$FORM2{auth}" size=65></td></tr>
<tr><td colspan=2><center>
<table border=0><tr><td><input type=submit value="�@ ���s �@"></td></form>
$formop_hd
<input type=hidden name=type value=qcont1>
<input type=hidden name=ed value=new>
<input type=hidden name=fa value="$file_age">
<input type=hidden name=lst_q value="$FORM2{lst_q}">
<input type=hidden name=lst_a value="$FORM2{lst_a}">
<input type=hidden name=lst_m value="$FORM2{lst_m}">
<input type=hidden name=lst_am value="$FORM2{lst_am}">
<input type=hidden name=lst_mm value="$FORM2{lst_mm}">
<input type=hidden name=lst_cf value="$FORM2{lst_cf}">
<input type=hidden name=lst_dg value="$FORM2{lst_dg}">
<input type=hidden name=lst_mm1 value="$FORM2{lst_mm1}">
<input type=hidden name=lst_at value="$FORM2{lst_ath}">
<input type=hidden name=lst_at value="$FORM2{lst_at}">
<input type=hidden name=menu value=1>
<td><input type=submit value="�@�@�N���A�@�@"></td></tr></table>
</center></td></tr></table></form>
���񓚕������e�L�X�g���͌`���̏ꍇ�A�e�s�������i�듚�j�ƂȂ�܂��B<br>
�����ꂩ�̍s�ƁA�񓚗��ɓ��͂��ꂽ�����񂪈�v�����ꍇ�����i�듚�j�ƂȂ�܂��B<br>
_HTML_
}
#************************************************
# �����ю҃��X�g�̕ҏW
#************************************************
sub edit_high_html{
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=high>
<input type=hidden name=menu value=1>
<small>
_HTML_
if($FORM{mod} ne 2){
$main_html.=<<"_HTML_";
<input type=hidden name=mod value=2>
<input type=submit value='$mode_name2{$FORM{d}}�����ю҃��X�g�\\��'>
_HTML_
}else{$main_html.=<<"_HTML_";
<input type=hidden name=mod value=1>
<input type=submit value='$mode_name1{$FORM{d}}�����ю҃��X�g�\\��'>
_HTML_
}
$main_html.=<<"_HTML_";
</form>
</small><br>
_HTML_
if($FORM{mod} ne '2'){&del_high_html("$high_cgi1{$FORM{d}}\.cgi",'1he',$mode_name1{$FORM{d}});}
else{&del_high_html("$high_cgi2{$FORM{d}}\.cgi",'2he',$mode_name2{$FORM{d}});}
}
#************************************************
# �I�������b�Z�[�WHTML
#************************************************
sub edit_final_mes_html{
$i=0;
&form_to_form;
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=mes1>
<input type=hidden name=menu value=1>
<input type=hidden name=mn value="$FORM2{mn}">
<span><br><br><b>���e���ڂ���͂��ҏW�{�^���������Ă��������B</b><br><br>
<b>���I�������b�Z�[�W�ҏW�t�H�[����</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=emes target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
_HTML_
$main_html.=&my_print(<<"_MY_");
<center>�����������o�^�ς݃��b�Z�[�W����������</center>\t#aaeeaa\n
���𗦁i0�`100�j
���b�Z�[�W
_MY_
if($FORM{mn}>0){
for($i=0;$i<=$FORM{mn};$i++){
$main_html.=&my_print(<<"_MY_");
<span><input type=text name="per-$i" size=5 value="$FORM2{"per-$i"}">������</span>
<input type=text name="mes-$i" size=30 value="$FORM2{"mes-$i"}">�@<input type=checkbox name="mod1-$i" value=1$FORMCH{"ch1-$i"}>���[�h�P�@<input type=checkbox name="mod2-$i" value=1$FORMCH{"ch2-$i"}>���[�h�Q
_MY_
}
}else{$FORM{mn}=0;}
$main_html.=&my_print(<<"_MY_");
<span>�P�O�O��(���[�h�P)</span>
<input type=text name="mes-top1" size=30 value="$FORM2{'mes-top1'}">
<span>�P�O�O��(���[�h�Q)</span>
<input type=text name="mes-top2" size=30 value="$FORM2{'mes-top2'}">
<center>�����������ǉ��p�t�H�[������������</center>\t#eeaaee\n
<span>���𗦁i0�`100�j</span>
���b�Z�[�W
<span><input type=text name="per-$i" size=5 value="$FORM2{per-$FORM{mn}}">������</span>
<input type=text name="mes-$i" size=30 value="$FORM2{'mes-'.$FORM{mn}}">�@<input type=checkbox name="mod1-$i" checked>���[�h�P�@<input type=checkbox name="mod2-$i" checked>���[�h�Q
<br><center><input type=submit value="�@�@ �ۑ� �@�@"></center>\n
_MY_
$main_html.='</table>';
}
#************************************************
# �W�������폜�����m�FHTML
#************************************************
sub del_genre_html{
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value="del1">
<input type=hidden name=menu value=1>
<span><br><br><b>�����̃W�������ŁA�쐬���鍀�ڂɃ`�F�b�N�����A�폜�{�^���������ĉ�����<br><br>
���W�������̊e��폜��</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=delg target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td><input type=checkbox value=1 name=delj><span>�W�����������폜����
<br><input type=checkbox value=1 name=delh>�����ю҃��O�t�@�C���̍폜
<br><input type=checkbox value=1 name=delf>���ѕ��z�t�@�C���̍폜
<br><input type=checkbox value=1 name=delq>���t�@�C���̍폜
<br><input type=checkbox value=1 name=delc>���e���t�@�C���̍폜
<br><input type=checkbox value=1 name=delm>�ݖ�ʐ��уt�@�C���̍폜
<br><input type=checkbox value=1 name=dele>�I�����b�Z�[�W�t�@�C���̍폜
<br><input type=checkbox value=1 name=deld>�W�������֘A�t�@�C���A�f�B���N�g���̑S�폜</span></td></tr>
<tr><td><center><input type=submit value="�@�@ �폜 �@�@"></center></td>
</tr></table></form>
_HTML_
}
#************************************************
# ���폜���ԕύX����HTML
#************************************************
sub del_quiz_html{
&header_html("���̍폜�A�����ύX");
if($#mondai<0){$main_html="<span>�����̃W�������ɓo�^����Ă�����͂���܂���B</span>";return;}
$file_age=time-(-M "$FORM{d}/$mondai_$FORM{d}\.cgi")*(60*60*24);
$main_html=<<"_HTML_";
<span><b><br><br>�����ԍ���ҏW��(�����_��)�A�`�F�b�N�{�b�N�X���`�F�b�N��A<br>�@�ŉ����̎��s�{�^���������Ă��������B</b><br><br>
$formop_hd
<input type=hidden name=type value=qdel1>
<input type=hidden name=fa value="$file_age">
<b>����胊�X�g��</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=delq target=help>Help</a>]<span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td><small>���ԍ�</small></td><td><small>��蕶</small></td><td><small>��</small></td><td><small>�폜</small></td></tr>
_HTML_
$i=0;
foreach(@mondai){
$i++;
$main_html.=<<"_HTML_";
<tr><td nowrap><span><input type=text size=5 name="qn$i" value="$i"></span></td>
<td nowrap width=400>$mondai[$i-1]</td>
<td nowrap>$ans[$i-1]</td>
<td nowrap><span><input type=checkbox name="qd$i" value=1></span></td></tr>
_HTML_
}
$main_html.=<<"_HTML_";
<tr><td colspan=4><br><center><input type=hidden name=menu value=1>
<span><input type=submit value="�@�@ ���s �@�@"><br><span></center></td></tr></table></form>
_HTML_
return 0;
}
#************************************************
# �����ю҃��X�g�̍폜�pHTML
#************************************************
sub del_high_html{
local($file,$syg,$mode_name)=@_;
open(DB,"$FORM{d}/$file");@lines = <DB>;close(DB);
if(($num_limit eq '0')||($day_limit eq '0')){$main_html.='<span><b><br><br>�����̃N�C�Y�́A�����ю҃��X�g�͎g�p���Ă��܂���B</b><br><br></span>';return;}
elsif($#lines < 1){
&error(762);
return;
}
$main_html.=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=high1>
<input type=hidden name=menu value=1>
<input type=hidden name=mod value=$FORM{mod}>
<span><br><br><b>���ȉ��̃��X�g����폜�������X�R�A�̃`�F�b�N�{�b�N�X�Ƀ`�F�b�N�����A<br>�ŉ����̍폜�{�^���������Ă��������B</b><br><br>
<b>�������ю҃��X�g��</b></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=6 nowrap><center><b>$mode_name�����ю҃��X�g</b></center></td></tr>
<tr><td nowrap><center>�폜</center></td>
<td nowrap><center>����</center></td>
<td nowrap><center>����</center></td>
<td nowrap><center>����</center></td>
<td nowrap><center>���O</center></td>
<td nowrap><center>IP</center></td>
</tr>
_HTML_
foreach $line (@lines) {
if($line =~ /^date/){next;}
if($line eq "\n"){next;}
($day,$high,$name,$host) = split(/\t/,$line);
$val="$day\_$high";
$day=&time_set($day);
if($last eq $high){$tai++;}
else{$grade=$grade+$tai+1;$tai=0;}
$space1= ' ' x (4-length($grade));
$space2= ' ' x (4-length($high));
$main_html.=<<"_HTML_";
<tr><td nowrap><input type=checkbox name="$syg$val" value="1"></td>
<td nowrap>$space1$grade</td>
<td nowrap>$day</td>
<td nowrap>$space2$high</td>
<td nowrap>$name</td>
<td nowrap>$host</td>
</tr>
_HTML_
push(@log,"$space1$grade�@ $day�@ $space2$high�@�@ $name�@\n");
$last=$high;
$mass=$mass+$high;
}
$main_html.= "<tr><td colspan=6><center><input type=submit value='    �폜    '><center></td></tr></table></form>";
}
#************************************************
# �V�X�e���ݒ�w���vHTML�\������
#************************************************
sub help_sys_html{
&header_html("�V�X�e���ݒ�p�w���v");
$main_html.=&help_print(<<"_HELP_");
<center>�����������V�X�e���ݒ聡��������</center>\t#eeaaee\n
(1)�v���C���O�ی����
�ی���ԓ��ɃA�N�Z�X�̂���v���C���̓v���C���Ƃ݂Ȃ����B���̎��Ԉȏ�A�N�Z�X�̂Ȃ��v���C���̃v���C���O�́A���̐V�K�v���C���ɂ̃v���C���O�ŏ㏑�������\\��������B
(2)�����v���C�l��
�����Ƀv���C�ł���l���̏���B�v���C���������v���C�l���ɒB�����ꍇ�A�V�K�v���C���͎󂯕t���Ȃ��Ȃ�B�v���C�l���~1KB�̗e�ʂ�K�v�Ƃ���B
(3)�N�b�L�[ID
�l���т��L�^���Ă������߂�ID�B����T�[�o�[���ŁA������qqqsystems�𗧂��グ��ꍇ�A�l���т�ʁX�Ɏ������邽�߂ɂ́A���̃N�b�L�[ID���قȂ�l�ɐݒ肷��
(4)�I���`��
<form>�I���`�����A<a href=javascript:void(0)>�����N</a><input type=radio>���W�I�{�^��<input type=button value=�t�H�[���{�^��>�ƂőI�ԁB</form>
(5)�g�b�v�y�[�W�ւ�URL
�N�C�Y�̃��j���[�y�[�W��肳��ɏ�ʂ̃y�[�W�ւ�URL�B
(6)���j���[�y�[�W�̃^�C�g��
�N�C�Y�̃��j���[�y�[�W�̃��C���^�C�g���B
(7)���j���[�y�[�W�̃w�b�_�[
�N�C�Y�̃��j���[�y�[�W�̃w�b�_�[�����ɕ\\������镶����ł��B<br>\$title�Ƃ���������̓��j���[�y�[�W�̃^�C�g���ɕϊ�����܂��B<br>\$top�Ƃ���������̓g�b�v�y�[�W�ւ�URL�ɕϊ�����܂��B<br>\$add�Ƃ���������͖�蓊�e�y�[�W�ւ�URL�ɕϊ�����܂��B<br>\$imode�Ƃ���������͌g�ѐ�p�y�[�W�ւ�URL�ɕϊ�����܂��B
(8)�T�u�y�[�W�̃w�b�_�[
����y�[�W�A�����ю҃y�[�W�A���ѕ��z�y�[�W�A�o��󋵃y�[�W�̃w�b�_�[�����ɕ\\������镶����ł��B
(9)���j���[�y�[�W�̃R�����g
���j���[�y�[�W�̃��j���[�ɁA�R�����g��\\���ł��܂��B�w�����e�i���X���x�w�P���Ԍチ���e�i���X�\\��x���̍��m�ɂ����p�ł��܂��B
(10)�X�^�C���V�[�g
�S�Ẵy�[�W�ɍ�p����X�^�C���V�[�g���`���邱�Ƃ��ł��܂��B
(11)�V�X�e���f�U�C��
�V�X�e���ݒ�̐F�ݒ蓙�̃f�U�C����I������B�V�X�e���f�U�C���̐ݒ�́A�V�X�e���f�U�C���ݒ��ʂɂčs���B
(12)���j���[�y�[�W�\\������
���j���[�y�[�W�̕\\�����኱�y���Ȃ�܂��B���j���[�y�[�W�̕\\�����x���Ɗ������Ƃ��ɂ����p�������B
(13)�񓚎��Ԃɂ�鏇�ʕt��
�������𐔂ł���΁A�񓚎��Ԃɂ��A�����ю҂̏��ʕt�����s���܂��B�s��Ȃ��ꍇ�͓����ʂƂȂ�܂��B
(14)���������܂�Ԃ�
�����܂�Ԃ����������ꍇ�A�\�̕��ɉ����āA����������s����B�Ӑ}���Ȃ��ꏊ�ŉ��s�����ꍇ���C�A�E�g�������ꍇ������B���C�A�E�g���d������ꍇ�́A�����܂�Ԃ����֎~(nowrap)���A���s���������ŉ��s�������K�v������B
_HELP_
}
#************************************************
# �W�������쐬�w���vHTML�\������
#************************************************
sub help_newgenre_html{
&header_html("�V�W�������쐬�p�w���v");
$main_html.=&help_print(<<"_HELP_");
<center>�����������V�W�������쐬���̐ݒ聡��������</center>\t#bbbbbb\n
(1)�f�B���N�g��
�N�C�Y�̖��A���тȂǂ�ۑ�����f�B���N�g����
_HELP_
}
#************************************************
# �V�X�e���f�U�C���ݒ�w���vHTML�\������
#************************************************
sub help_sysdesign_html{
&header_html("�V�X�e���f�U�C���ݒ�p�w���v");
$main_html.=&help_print(<<"_HELP_");
<center>�����������V�X�e���f�U�C���ݒ聡��������</center>\t#eeaaee\n
(1)�ҏW��
�ҏW���A�R�s�[���̃V�X�e���f�U�C����
(2)�V�X�e���f�U�C����
�V�X�e���f�U�C���̖��O�B�V�X�e���ݒ��ʂ���f�U�C����I������Ƃ��́A���̖��O��I�����܂��B
(3)���j���[�y�[�W�̕ǎ�
���j���[�y�[�W�̕ǎ��摜�̃t�@�C�����ł��Bhttp://����͂��܂�URL���ݒ�\�ł��B
(4)���j���[�y�[�W�̔w�i�F
�w�i�F������킵�܂��B#����͂��܂�RGB�̐ݒ�ƁAred�̂悤�ɐF��\\��������̗������ݒ�\�ł��B
(5)���j���[�y�[�W�̕\\�̐F
�\\�̐F��\\���܂��B
(6)���j���[�y�[�W�̃W�������F
�W�����������\\�������Z���̐F�B
(7)���j���[�y�[�W�̏��F
���j���[�y�[�W�̍ŏ�ʂɕ\\�������R�����g�̕\\�̐F
(8)���j���[�y�[�W�̃R�����g�F
�e�W�������̃R�����g���\\�������Z���̐F
(9)���j���[�y�[�W�̍����юҐF
�����юҖ����\\�������Z���̐F
(10)���j���[�y�[�W�̕\\�̘g�̐F
�\\�̘g���̐F
(11)���j���[�y�[�W�̕����F
�����̐F
(12)���j���[�y�[�W�̃����N�F
�����N������̐F
(13)���j���[�y�[�W�̊��K�⃊���N�F
���ɖK��ς݂̃����N������̐F
(14)���j���[�y�[�W�̕\\�̘g�̍���
�\\�̘g�̍���(border)
(15)���j���[�y�[�W�̕\\�̘g�̕�
�\\�̘g�̕�(cellpadding)
(16)���j���[�y�[�W�̕\\�̘g�̓���
�\\�̘g�̓����̕�(cellspacing)
(17)���ї����O���t�摜�P
���ї����̖_�O���t�̉摜�B�N�C�Y�I�����Ɏg�p���A���̎��̐��тɊY������O���t�Ɏg�p����
(18)���ї����O���t�摜�Q
���ї����̖_�O���t�̉摜�B
(19)�\\�̃��C�A�E�g
�\\�ʒu���������A�������A�E�����ɂ���ݒ�
(20)�\\���������C�A�E�g_HELP_
�\\�̒��̕����ʒu���������A�������A�E�����ɂ���ݒ�
_HELP_
}
#************************************************
# �W�������f�U�C���ݒ�w���vHTML�\������
#************************************************
sub help_genredesign_html{
&header_html("�W�������f�U�C���ݒ�p�w���v");
$main_html.=&help_print(<<"_HELP_");
<center>�����������W�������f�U�C���̐ݒ聡��������</center>\t#eeaaaa\n
(1)�ҏW��
�ҏW���A�R�s�[���̃V�X�e���f�U�C����
(2)�W�������f�U�C����
�W�������f�U�C���̖��O�B�W�������ݒ��ʂ���f�U�C����I������Ƃ��́A���̖��O��I�����܂��B
(3)�����F
�����̐F
(4)�����N�����F
�����N������̐F
(5)���K�⃊���N�����F
���ɖK��ς݂̃����N������̐F
(6)�a������ҕ����F
�����ю҈ꗗ�ŁA�a������̃v���C���̖��O�̐F
(7)��{�w�i�F
�N�C�Y�J�n���A���ї����A�o��󋵁A�����ю҈ꗗ�̔w�i�F
(8)�������w�i�F
�N�C�Y�ɐ����������̔w�i�F
(9)�s�������w�i�F
�N�C�Y�ɕs�������������̔w�i�F
(10)���E�C���h�E�̐F
�N�C�Y�J�n���̃R�����g�̕\\�̐F
(11)�\\�̃w�b�_�[�F
�\\�̃w�b�_�[�����̃Z���̐F
(12)�\\�̐F
�\\�̐F
(13)�\\�̘g�̐F
�\\�̘g���̐F
(14)�\\�̘g�̍���
�\\�̘g�̍���(border)
(15)�\\�̘g�̕�
�\\�̘g�̕�(cellpadding)
(16)�\\�̘g�̓���
�\\�̘g�̓����̕�(cellspacing)
(17)��{�ǎ�
�N�C�Y�J�n���A���ї����A�o��󋵁A�����ю҈ꗗ�̕ǎ�
(18)�������ǎ�
�N�C�Y�ɐ����������̕ǎ�
(19)�s�������ǎ�
�N�C�Y�ɕs�������������̕ǎ�
(20)����\\��
�N�C�Y�ɐ��������Ƃ��́A�������b�Z�[�W
(21)�s����\\��
�N�C�Y�ɕs�����������Ƃ��́A�s�������b�Z�[�W
(22)�^�C���I�[�o�[�\\��
�N�C�Y�Ƀ^�C���I�[�o�[�������Ƃ��́A�^�C���I�[�o�[���b�Z�[�W
(23)������MIDI
�N�C�Y�ɐ��������Ƃ��̌��ʉ�
(24)�s������MIDI
�N�C�Y�ɕs�����������Ƃ��̌��ʉ�
(25)�N�C�Y�I����MIDI
�N�C�Y�I�����̌��ʉ�
(26)�����юҗpMIDI
�N�C�Y�I�����A�����т������ꍇ�̌��ʉ�
_HELP_
}
#************************************************
# �v���C���O�ꗗ�w���vHTML�\������
#************************************************
sub help_playlog_html{
&header_html("�v���C���O�p�w���v");
$main_html.=&help_print(<<"_HELP_");
��<b>�ŐV�v���C���O���p����</b>�Ƃ͍ł��ŋ߂Ɏg�p���ꂽ�v���C���O�̍X�V�����ł��B\n
��<b>�ŌÃv���C���O���p����</b>�Ƃ͍ł��ߋ��Ɏg�p���ꂽ�v���C���O�̍X�V�����ł��B\n
��<b>�v���C���O���p�Ԋu</b>�Ƃ͍ŐV���O���p�����ƁA�ŌÃ��O���p�����Ƃ̍��ł��B\n
��<b>�����v���C����</b>�Ƃ̓V�X�e���ݒ�Őݒ肵���l�ŁA�v���C���O�̑�����\\���܂��B\n
��<b>�v���C���O�ی����</b>�Ƃ̓V�X�e���ݒ�Őݒ肵���l�ŁA���̊��ԓ��ɍX�V���ꂽ���O�͕ی삳��܂��B\n
��<b>�v���C���O</b>�Ƃ́A�v���C���̃v���C���[�̏�Ԃ�ۑ����郍�O�ł��B\n
���v���C���O�́A�P�t�@�C���Pkb�̗e�ʂ�K�v�Ƃ��܂��B\n
���v���C���O�̑����̏���͓����v���C�����Ŏw�肳��܂��B\n
���V�K�v���C���́A�󂢂Ă���v���C���O��T���A�󂢂Ă��郍�O������΂���𗘗p���A�󂢂Ă��郍�O���Ȃ���΂��̎����v���C���ɍ����܂��B\n
���v���C���O�ی���Ԉȏ�X�V�̖����������O�́w�󂢂Ă���x�ƌ��Ȃ���܂��B\n
���v���C���O���p�Ԋu�����X����ׁA�K�؂ȃ��O�ی���Ԃ�ݒ肵�Ă��������B���O���p�Ԋu���啝�ɒ����Ɩ��ʂȃ��O���������莑���̖��ʌ������Ƃ������ƂɂȂ�܂��B\n
_HELP_
}
#************************************************
# �e�탍�O�{���E�ۑ��w���vHTML�\������
#************************************************
sub help_log_html{
&header_html("�e�탍�O�{���E�ۑ��p�w���v");
$main_html.=&help_print(<<"_HELP_");
���{���Ƃ́A�{�����ڃt�@�C���ɃA�N�Z�X���Ă��Acgi�t�@�C���ł��邽�߂ɕ\\���ł��Ȃ��t�@�C����\\�����܂��B\n
���e�탍�O�̃o�b�N�A�b�v�́A�{����A���j���[���ۑ����邱�Ƃōs�Ȃ��܂��B\n
���ǉ��`���Ƃ́A�����ꊇ�ǉ�����`���Ń��O��\\�����܂��B\n
_HELP_
}
#************************************************
# �W�������ݒ�w���vHTML�\������
#************************************************
sub help_genre_html{
&header_html("�W�������ݒ�p�w���v");
$main_html.=&help_print(<<"_HELP_");
<center>�����������V�W�������쐬���̐ݒ聡��������</center>\t#bbbbbb\n
(1)�f�B���N�g��
�N�C�Y�̖��A���тȂǂ�ۑ�����f�B���N�g����
<center>�����������W�������̓���ݒ聡��������</center>\t#eeaaaa\n
(2)�^�C�g��
�N�C�Y�ꗗ�ŕ\\������邱�̃W�������̃^�C�g��
(3)�Љ
���j���[�y�[�W�Ŋe�W�������̐����Ɏg�p���܂��B
(4)�N�C�Y�J�n���b�Z�[�W
�N�C�Y�̊J�n���ɕ\\������郁�b�Z�[�W�ł��B
(5)���t�@�C��
����o�^����t�@�C���̐ݒ�B���̃W����������ǂݍ��ނ��Ƃ��ł��܂��B
(6)�W�������̓�����
�W��������$_underconst�ɐݒ肵�Ă����ƁA���j���[�y�[�W�ł��̃W�������͕\\������Ȃ�
(7)���e���̎�t
���̃W�������ւ̖��̓��e���󂯕t���邱�Ƃ��ł��܂�
(8)�e�L�X�g�`���̓��e���
���e���󂯕t����ꍇ�A�e�L�X�g�`���̖��̓��e���󂯕t���邩�ǂ�����ݒ�ł��܂��B
(9)���e���̎����̗p
���e���󂯕t����ꍇ�A�Ǘ��҂̏��F���o���Ɏ����I�ɖ��Ƃ��č̗p���邩��ݒ�ł��܂��B
(10)�o��󋵕\���ł̖�蕶�\��
�o��󋵕\���ŁA��蕶��\�����邩�A���̓��e������\�����邩��ݒ�ł��܂��B
(11)�W�������f�U�C��
�F�̐ݒ��\�̃W�������f�U�C����I���ł��܂��B�W�������f�U�C���́A�W�������f�U�C���ݒ�Őݒ�ł��܂��B
<center>�������������[�h�ʂ̓���ݒ聡��������</center>\t#eeeeaa\n
(12)(32)���[�h��
�e���[�h�̖��O�B���[�h�Q�́A���[�h�Q�̖��O�����͂���Ă���Ƃ��̂ݓ��삷��B
(13)(33)����\\��
�񓚌�ɐ�����\\�����邩�ǂ����̐ݒ�
(14)(34)�o�菇��
�o�菇���������_���ɍs�����A�o�^���ɍs�����̐ݒ�
(15)(35)�g�p��萔
�o�^���Ă���S�Ă̖�萔���g������A�g�p�����萔�ɐ����������鎖���ł���B
(16)(36)�o���萔
�ő�o�萔
(17)(37)�ꊇ�o��
�o����A�S��ꊇ�\\�����邱�Ƃ��ł��܂��B
(18)(38)�I�������듚��
����ԈႦ���GAME OVER�ɂȂ邩�̐ݒ�
(19)(39)��������
��█�̐������Ԃ��w�肷�邱�Ƃ��ł��܂��B
(20)(40)���i���C��
�񓚗������i���C���𒴂���ƃn�C�X�R�A�o�^���\\�ƂȂ�B
(21)(41)�����ю҂�back up
�w�肵���Ԋu(��)�ȏ�A�o�b�N�A�b�v������Ă��Ȃ������ю҃t�@�C���̃o�b�N�A�b�v���s�����ǂ����̐ݒ�B
(22)(42)�����ю҂�back up����
�����ю҃t�@�C���̃o�b�N�A�b�v���A�P�̃t�@�C��(.bak)�Ƀo�b�N�A�b�v����邩�A�����̃t�@�C��(.bak1)�Ɏ��̂���ݒ肷��B
(23)(43)���ѕ��z��back up
�w�肵���Ԋu(��)�ȏ�A�o�b�N�A�b�v������Ă��Ȃ����ѕ��z�t�@�C���̃o�b�N�A�b�v���s�����ǂ����̐ݒ�B
(24)(44)���ѕ��z��back up����
���ѕ��z�t�@�C���̃o�b�N�A�b�v���A�P�̃t�@�C��(.bak)�Ƀo�b�N�A�b�v����邩�A�����̃t�@�C��(.bak1)�Ɏ��̂���ݒ肷��B
(25)(45)���ѕ��z�ȗ��\\��
��聓�ȏ�̖_�O���t���ȗ������\\���ɂ���
(26)(46)���ѕ��z�W�v�P��
�ŏI���т̏W�v�O���t���W�v����P�ʂ�ݒ肷��
(27)(47)�����юғ�������
�����ю҃��X�g�ŁA�L�^��������ɐ����������邱�Ƃ��ł���B��������ȏ�O�̋L�^�́A�V�K�L�^�o�^�̍ۂɍ폜�����B
(28)(48)�����юҐl������
�����ю҃��X�g�ŁA�L�^����l���ɐ����������邱�Ƃ��ł���B�o�^�͏�ʋL�^���c��B
(29)(49)�a������l��
�a������Ƃ́A�����ю҂̂����A���������l���������󂯂ċL�^���폜�����l�̂��Ƃł��B�a�����蒆�́A�����ɂ��L�^���폜����邱�Ƃ͂���܂��񂪁A���т�h��ւ����a�����肩��O�ꂽ�ꍇ�́A���������A�l���������󂯂邱�ƂɂȂ�܂��B
(30)(50)�����ю҃R�����g�L�^
�����ю҃��X�g�ɃR�����g�̓��͂��������ǂ����̐ݒ�ł��B�f�B�X�N�e�ʂƑ��k���ݒ���s���ĉ������B
(31)(51)���z�X�g���X�R�A
����IP�A�h���X�ŁA�����X�R�A�̏ꍇ�͍����юғo�^�ł��Ȃ����邱�Ƃ��ł���B�����юҐ����ɗ͌��炵�����ꍇ�ɗL���B
_HELP_
}
#************************************************
# �W�������ݒ�̊e��폜�p�w���vHTML�\������
#************************************************
sub help_delgenre_html{
&header_html("�W�������ݒ�̊e��폜�p�w���v");
$main_html.=&help_print(<<"_HELP_");
�W���������̍폜
�W�����������ꊇ���ĕۑ����Ă���t�@�C������A���̃W�������̏����폜���܂��B�o�^���Ă����f�B���N�g����A�e�탍�O�t�@�C���폜���܂���B
�����ю҃��O�t�@�C���̍폜
�����ю҂�ۑ��������O���폜���܂��B
���ѕ��z�t�@�C���̍폜
�ŏI���т��W�v�����t�@�C�����폜���܂��B
���t�@�C���̍폜
���o�^�����t�@�C�����폜���܂��B
���e���t�@�C���̍폜
���e��肪�o�^����Ă���t�@�C�����폜���܂��B�V���ɖ�肪���e�����Ύ����쐬����܂��B
�ݖ�ʐ��уt�@�C���̍폜
�ݖ�ʂɐ��𗦂��W�v�����t�@�C�����폜���܂��B
�ݒ�f�B���N�g���̍폜
�o�^���Ă���f�B���N�g�����폜���܂��B�����ю҃��O�A���ѕ��z�t�@�C���A���t�@�C���A�ݖ�ʐ��уt�@�C���́A���̃f�B���N�g���ɕۑ�����Ă��邽�߂ɍ폜����܂��B�W���������͍폜���܂���B
_HELP_
}
#************************************************
# ���̍폜�E�����ύX�p�w���vHTML�\������
#************************************************
sub help_delquiz_html{
&header_html("���̍폜�E�����ύX�p�w���v");
$main_html.=&help_print(<<"_HELP_");
�����ԍ����ɖ�����ёւ��܂��B\n
�����ԍ��ɂ͏����_���܂܂�Ă��\\�ł��B\n
���y�폜�z���`�F�b�N����Ă�����͍폜����܂��B\n
_HELP_
}
#************************************************
# �N�C�Y�ꊇ�o�^�̏����p�w���vHTML�\������
#************************************************
sub help_multiadd_html{
&header_html("�N�C�Y�ꊇ�o�^�̏����p�w���v");
$main_html.=&help_print(<<"_HELP_");
<center>�������ꊇ�o�^�̏���������<center>\t#eeaaaa\n
���ォ��P�s���ǂ݂Ƃ��čs���܂��B\n
�����ʎqq:�ł͂��܂�s����A���ɍĂю��ʎqq:�������܂ŁA�P�̖��ł���ƔF�����܂��B\n
�����ʎqq:�ɑ���������͖�蕶�Ƃ��ĔF�����܂��B\n
�����ʎqans:�ɑ���������͐����Ƃ��ĔF�����܂��B\n
�����ʎqmis1:�ɑ���������͌듚�P�Ƃ��ĔF�����܂��B\n
�����ʎqmis2:�ɑ���������͌듚�Q�Ƃ��ĔF�����܂��B\n
�����ʎqmis3:�ɑ���������͌듚�R�Ƃ��ĔF�����܂��B\n
�����ʎqmis4:�ɑ���������͌듚�S�Ƃ��ĔF�����܂��B\n
�����ʎqansmes:�ɑ���������͐����R�����g�Ƃ��ĔF�����܂��B\n
�����ʎqmismes:�ɑ���������͌듚�R�����g�Ƃ��ĔF�����܂��B\n
�����ʎqcf:�ɑ���������͎Q�l�����Ƃ��ĔF�����܂��B\n
�����ʎqdigest:�ɑ���������͖����e�Ƃ��ĔF�����܂��B\n
�����ʎqanstype:�ɑ���������͉񓚕����Ƃ��ĔF�����܂��B1���w�肵���Ƃ��e�L�X�g���͕����B0���w�肵���Ƃ��I������ƂȂ�܂��B\n
�����ʎqmismes����:�ɑ���������́A�듚�w��̌듚�R�����g�Ƃ��ĔF�����܂��B\n
�����ʎqauthor:�ɑ���������́A��Җ��Ƃ��ĔF�����܂��B\n
�����ʎq#�ɑ���������͒��߂Ƃ��āA���������F�����܂���B\n
���󔒍s�͔F�����܂���B\n
����L�̗�ӊO�̍s�����͂����΁A�ǂݍ��݃G���[�ƂȂ�܂��B\n
��q:�Ǝ���q:�܂ł̊Ԃ̎��ʎq�̏����́A���s���ł��B\n
�����ʎqq:,ans:�̂Q�̎��ʎq�͕K�{�ł��B�񓚕������I������̏ꍇ�Amis1:���ʎq���K�{�ƂȂ�܂��B\n
���e�L�X�g���͌`���ŁA�����̉𓚃p�^�[��������ꍇ�́A&lt;br&gt;�ŋ�؂�܂��B(�Q�F��2)\n
����1<br>#-------���P-------<br>q:�P�{�P��<br>ans:2<br>mis1:3<br>mis2:4<br>mis3:5<br>mis4:6<br>ansmes:�吳���I<br>mismes:���߂���<br>cf:�Z���̋��ȏ�<br>mismes1:3���Ă��Ƃ͂Ȃ��ł���B<br>mismes2:4���Ă��Ƃ͂Ȃ��ł���B<br>digest:�ȒP�ȑ����Z<br>anstype:0<br>author:jun\n
����2<br>#-------���P-------<br>q:�P�{�Q��<br>ans:3&lt;br&gt;�R<br>mis1:2&lt;br&gt;�Q<br>mis2:4&lt;br&gt;�S<br>mis3:5&lt;br&gt;�T<br>mis4:6&lt;br&gt;�U<br>ansmes:�吳���I<br>mismes:���߂���<br>cf:�Z���̋��ȏ�<br>mismes1:2���Ă��Ƃ͂Ȃ��ł���B<br>mismes2:4���Ă��Ƃ͂Ȃ��ł���B<br>digest:�ȒP�ȑ����Z<br>anstype:1<br>author:jun\n
�����ɓo�^����Ă�������A�ꊇ�o�^�`���̃��O�Ƃ��ĕۑ����邱�Ƃ��ł��܂��B�V�X�e���R�}���h�́w�e�탍�O�{���E�ۑ��x�������p���������B\n
_HELP_
}
#************************************************
# �e�탍�O�̃o�b�N�A�b�v�p�w���vHTML�\������
#************************************************
sub help_backup_html{
&header_html("�e�탍�O�̃o�b�N�A�b�v�p�w���v");
$main_html.=&help_print(<<"_HELP_");
���y�ǉ��z�Ƃ́A���݂̃��O�ɏd���f�[�^�ȊO�̃f�[�^�������܂��B<br>�@�y�ǉ��z�́y�㏑�z�����D�悳��܂��B\n
���y�㏑�z�Ƃ́A�S�f�[�^�����݂̃��O�ƒu�������܂��B<br>�@�����t�@�C�����w�肳��Ă���ꍇ�́A���̏d���f�[�^���̂������f�[�^�ƒu�������܂��B<br>�@�y�ǉ��z�́y�㏑�z�����D�悳��܂��B\n
���y�폜�z�Ƃ́A�o�b�N�A�b�v�t�@�C�����폜���܂��B<br>�@�y�ǉ��z��y�㏑�z�ƕ��p�����ꍇ�A�Ō�Ɂy�폜�z�����s����܂��B\n
���y�o�b�N�A�b�v�t�@�C���̍쐬�z�Ƃ́A�������o�b�N�A�b�v�t�@�C�����쐬����R�}���h�ł��B\n
���y�쐬���[�h�z�Ƃ́A�o�b�N�A�b�v�t�@�C�����쐬������@�ł��B<br>[�㏑��]��I�ԂƁA���****.bak���́A***_bak.cgi�ɕۑ�����܂��B<br>[�ʃt�@�C��]��I�ԂƁA***.bak1,***.bak2�Ƃ����������ɕʃt�@�C���Ƃ��ĕۑ�����܂��B<br>[�����ю҃t�@�C��][���ѕ��z�t�@�C��]�̃f�t�H���g�ݒ�́y�W�������̕ҏW�z�Őݒ肵�܂��B<br>�����̃f�t�H���g�ݒ�́A�����o�b�N�A�b�v�̐ݒ�Ɠ����ł��B\n
_HELP_
}
#************************************************
# �I�������b�Z�[�W�ҏW�p�w���vHTML�\������
#************************************************
sub help_endmes_html{
&header_html("�I�������b�Z�[�W�ҏW�p�w���v");
$main_html.=&help_print(<<"_HELP_");
���I�����̐��𗦂ɂ���āA�o�����b�Z�[�W��ς��邱�Ƃ��ł��܂��B\n
���w�肷�鐳�𗦂͎����I�Ƀ\\�[�g�����̂ŁA���Ԃɕ���ł��Ȃ��Ă��n�j�ł��B\n
���w�肷�鐳�𗦂͂O�`�P�O�O�͈̔͂ŁA�����_�ł��ł��B\n
�����b�Z�[�W��ǉ��������ꍇ�͒ǉ��t�H�[�����s���Ă��������B\n
�����𗦂��󗓂̏ꍇ�A���̃��b�Z�[�W�͍폜����܂��B\n
_HELP_
}
#************************************************
# �V�X�e���f�U�C���I��pHTML�\������
#************************************************
sub select_sysdesign{
local($sysid)=@_;
local(%selected);
$selected{$sysid}=" selected";
$ret="<select name=sdes>";
foreach $id(@sysdesign_list){
if($id eq ''){next;}
$ret.="<option value='$sysdesign_title{$id}'$selected{$id}>$sysdesign_title{$id}";
}
if(!mygrep($sysid,@sysdesign_list)){
$ret.="<option value='$sysid' selected>$sysid";
}
$ret.='</select>';
}
#************************************************
# �f�U�C���I��pHTML�\������
#************************************************
sub select_design{
local($designid)=@_;
local(%selected);
$selected{$designid}=" selected";
$ret="<select name=gdes>";
foreach $id(@design_list){
if($id eq ''){next;}
$ret.="<option value=$id$selected{$id}>$design_title{$id}";
}
}
#************************************************
# ���ꊇ�ǉ�HTML
#************************************************
sub multi_add_quiz_form{
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qmulti1>
<input type=hidden name=menu value=1>
<span><b><br><br>�����t�@�C���`���̃e�L�X�g����f�[�^�ɒǉ����܂��B</b><br>
�@���t�@�C���`���̃e�L�X�g���e�L�X�g�G���A�ɃR�s�[���A�ꊇ�ǉ��{�^���������Ă��������B<br><br>
<b>�������̓t�H�[����</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=madd target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td><span>
<textarea rows=40 cols=60 name='newq'>\n$FORM{newq}</textarea>
</span></td></tr><tr><td>
<span><center>
<input type=submit value="�@�ꊇ�ǉ��@">
<br></center></span></td></tr></table></form>
_HTML_
}
#************************************************
# ���ꊇ�ǉ��m�FHTML
#************************************************
sub multi_add_quiz_html{
local(@log,$index,$line,@q,@ans,@mis1,@mis2,@mis3,@mis4,@ansmes,@mismes,@mismes1,@mismes2,@mismes3,@mismes4,@cf,@digest,@atype,@auth);
@log=split(/\n/,$FORM{newq});
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qmulti2>
<input type=hidden name=menu value=1>
<span><br><br><b>���o�^������肪��������΁A�ꊇ�ǉ��{�^���������Ă��������B</b><br><br></span>
_HTML_
$index=-1;$linenum=0;
foreach $line(@log){
$linenum++;
$line=~ s/\n//g;
if($line eq ''){next;}
if($line=~ /^q:(.*)/){
$index++;
$q[$index]=$1;
next;
}
if($index<0){next;}
if($line=~ /^ans:(.*)/){$ans[$index]=$1;}
elsif($line=~ /^mis1:(.*)/){$mis1[$index]=$1;}
elsif($line=~ /^mis2:(.*)/){$mis2[$index]=$1;}
elsif($line=~ /^mis3:(.*)/){$mis3[$index]=$1;}
elsif($line=~ /^mis4:(.*)/){$mis4[$index]=$1;}
elsif($line=~ /^ansmes:(.*)/){$ansmes[$index]=$1;}
elsif($line=~ /^mismes:(.*)/){$mismes[$index]=$1;}
elsif($line=~ /^cf:(.*)/){$cf[$index]=$1;}
elsif($line=~ /^digest:(.*)/){$digest[$index]=$1;}
elsif($line=~ /^mismes1:(.*)/){$mismes1[$index]=$1;}
elsif($line=~ /^mismes2:(.*)/){$mismes2[$index]=$1;}
elsif($line=~ /^mismes3:(.*)/){$mismes3[$index]=$1;}
elsif($line=~ /^mismes4:(.*)/){$mismes4[$index]=$1;}
elsif($line=~ /^author:(.*)/){$auth[$index]=$1;}
elsif($line=~ /^anstype:(.*)/){$atype[$index]=$1;}
elsif($line=~ /^#/){;}
else{&error(911,$linenum);return 1;}
}
if($index<0){&error(901);return 1;}
$main_html.="<table $sys_tbl_opt bgcolor='$sys_color'>";
for($i=0;$i<=$index;$i++){
local($num);$num=$i+1;
if($q[$i]eq ''){&error(921,$num);return 1;}
if($ans[$i]eq ''){&error(931,$num);return 1;}
if(($mis1[$i]eq '')&&($FORM{atype} eq '')){&error(941,$num);return 1;}
if($i>0){$main_html.='<tr><td></td></tr>';}
local($q,$ans,$mis1,$mis2,$mis3,$mis4,$ansmes,$mismes,$cf,$digest,$mismes1,$mismes2,$mismes3,$mismes4,$atype,$auth);
&conv_for_html($q,$q[$i]);
&conv_for_html($ans,$ans[$i]);
&conv_for_html($mis1,$mis1[$i]);
&conv_for_html($mis2,$mis2[$i]);
&conv_for_html($mis3,$mis3[$i]);
&conv_for_html($mis4,$mis4[$i]);
&conv_for_html($ansmes,$ansmes[$i]);
&conv_for_html($mismes,$mismes[$i]);
&conv_for_html($cf,$cf[$i]);
&conv_for_html($digest,$digest[$i]);
&conv_for_html($mismes1,$mismes1[$i]);
&conv_for_html($mismes2,$mismes2[$i]);
&conv_for_html($mismes3,$mismes3[$i]);
&conv_for_html($mismes4,$mismes4[$i]);
&conv_for_html($atype,$atype[$i]);
&conv_for_html($auth,$auth[$i]);
@opt=('�I��','�e�L�X�g����');
$main_html.=<<"_HTML_";
<input type=hidden name="p_q$i" value="$q">
<input type=hidden name="p_a$i" value="$ans">
<input type=hidden name="p_m1$i" value="$mis1">
<input type=hidden name="p_m2$i" value="$mis2">
<input type=hidden name="p_m3$i" value="$mis3">
<input type=hidden name="p_m4$i" value="$mis4">
<input type=hidden name="p_am$i" value="$ansmes">
<input type=hidden name="p_mm$i" value="$mismes">
<input type=hidden name="p_1mm$i" value="$mismes1">
<input type=hidden name="p_2mm$i" value="$mismes2">
<input type=hidden name="p_3mm$i" value="$mismes3">
<input type=hidden name="p_4mm$i" value="$mismes4">
<input type=hidden name="p_cf$i" value="$cf">
<input type=hidden name="p_dg$i" value="$digest">
<input type=hidden name="p_at$i" value="$atype">
<input type=hidden name="p_ath$i" value="$auth">
<tr><td colspan=2><span><center>������ �ǉ� $num ��� ������</center></span></td></tr>
<tr><td>��@��F</td><td><b>$q[$i]</b></td></tr>
<tr><td>���@���F</td><td><b>$ans[$i]</b></td></tr>
<tr><td>�듚�P�F</td><td><b>$mis1[$i]</b></td></tr>
<tr><td>�듚�Q�F</td><td><b>$mis2[$i]</b></td></tr>
<tr><td>�듚�R�F</td><td><b>$mis3[$i]</b></td></tr>
<tr><td>�듚�S�F</td><td><b>$mis4[$i]</b></td></tr>
<tr><td>�����R�����g�F</td><td><b>$ansmes[$i]</b></td></tr>
<tr><td>�듚�R�����g�F</td><td><b>$mismes[$i]</b></td></tr>
<tr><td>�Q�l�����F</td><td><b>$cf[$i]</b></td></tr>
<tr><td>�����e�F</td><td><b>$digest[$i]</b></td></tr>
<tr><td>�듚�R�����g�P�F</td><td><b>$mismes1[$i]</b></td></tr>
<tr><td>�듚�R�����g�Q�F</td><td><b>$mismes2[$i]</b></td></tr>
<tr><td>�듚�R�����g�R�F</td><td><b>$mismes3[$i]</b></td></tr>
<tr><td>�듚�R�����g�S�F</td><td><b>$mismes4[$i]</b></td></tr>
<tr><td>�쐬�ҁF</td><td><b>$auth[$i]</b></td></tr>
<tr><td>�񓚕����F</td><td><b>$opt[$atype[$i]]</b></td></tr>
_HTML_
}
$main_html.=<<"_HTML_";
<tr><td colspan=2><span><center><input type=submit value="�@�ꊇ�ǉ��@">
<br></center></span></td></tr></form></table>
_HTML_
return 0;
}
#************************************************
# �W�������V�K�쐬���HTML�\������
#************************************************
sub make_genre_html{
&list_genre_html(@genre_dir_all);
$main_html =<<"_HTML_";
$formop_nh
<input type=hidden name=type value=newj2>
<span><br><br><b>���e���ڂ���͂��V�K�쐬�{�^���������Ă��������B</b><br><br>
<b>���V�W�������ݒ聡</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=newg target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3 bgcolor=#eeaaee><center><span>�����������V�W�������쐬���̐ݒ聡��������</span></center></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(1)�f�B���N�g��
<input type=text name='d' value="$FORM2{d}" size=10>(���p�p��)
_MY_
$main_html .=<<"_HTML_";
<tr><td colspan=3><center><br><input type=submit value=�V�K�쐬></center></td></tr>
</table></form>
${&focus_move('d')}$ret
_HTML_
}
#************************************************
# �w���v���HTML�\������
#************************************************
sub help_html{
$formop_hb=~s/\n//g;
$main_html =<<"_HTML_";
<input type=hidden name=type value=newj2>
<span><br><br>
<b>���w���v���j���[��</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=newg target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td nowrap>�V�X�e���ݒ�</td>
$formop_hb<td><input type=hidden name='help' value="sys"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�V�W�������쐬</td>
$formop_hb<td><input type=hidden name='help' value="newg"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�V�X�e���f�U�C���ݒ�</td>
$formop_hb<td><input type=hidden name='help' value="sysd"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�W�������f�U�C���ݒ�</td>
$formop_hb<td><input type=hidden name='help' value="gend"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�v���C���O</td>
$formop_hb<td><input type=hidden name='help' value="playlog"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�e�탍�O�{���E�ۑ�</td>
$formop_hb<td><input type=hidden name='help' value="log"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�W�������ݒ�</td>
$formop_hb<td><input type=hidden name='help' value="genre"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�W�������ݒ�̊e��폜�p�w���v</td>
$formop_hb<td><input type=hidden name='help' value="delg"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>���̍폜�E�����ύX</td>
$formop_hb<td><input type=hidden name='help' value="delq"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�N�C�Y�ꊇ�o�^�̏����p</td>
$formop_hb<td><input type=hidden name='help' value="madd"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�I�����b�Z�[�W�ҏW</td>
$formop_hb<td><input type=hidden name='help' value="emes"><input type=submit value='�w���v'></td></tr></form>
<tr><td nowrap>�e�탍�O�̃o�b�N�A�b�v</td>
$formop_hb<td><input type=hidden name='help' value="back"><input type=submit value='�w���v'></td></tr></form>
</table></form>
_HTML_
}
#************************************************
# �F�쐬�E�C���h�E�\��HTML
#************************************************
sub color_html{
$main_html.=<<'_HTML_';
<script language=javascript>
//<!--
function wopen(){
var win=window.open("color","right", "toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=0,resizable=1,width=200,height=50");
if (win !=null){
main="<html><head><title>�F�e�X�g</title>\n"
main+="<script language=javascript>\n"
main+="function change(){\n"
main+="document.bgColor=document.frm.col.value;\n"
main+="document.frm.col.value=document.bgColor;\n"
main+="document.frm.red.value=document.frm.col.value.substring(1,3);\n"
main+="document.frm.green.value=document.frm.col.value.substring(3,5);\n"
main+="document.frm.blue.value=document.frm.col.value.substring(5,7);\n"
main+="}\n"
main+="function rgb(){\n"
main+="document.bgColor='#'+document.frm.red.value+document.frm.green.value+document.frm.blue.value;\n"
main+="document.frm.col.value=document.bgColor;\n"
main+="}\n"
main+="</script>\n"
main+="</head><body bgcolor=white><form name=frm>\n"
main+="<table border=$border><tr><td nowrap>\n"
main+="�F�R�[�h<input type=text name=col size=7 value='#ffffff'>\n"
main+="<input type=button value=OK onclick=\"change()\">\n"
main+="<tr><td nowrap>\n"
main+="��<input type=text name=red size=2 value='ff'>\n"
main+="��<input type=text name=green size=2 value='ff'>\n"
main+="��<input type=text name=blue size=2 value='ff'>\n"
main+="<input type=button value=OK onclick=\"rgb()\">\n"
main+="</td></tr></table>\n"
main+="</form></bo"
main+="dy></html>\n"
win.document.write(main)
win.document.close()
}
}
document.write("<form><input type=button value=\"�F�\\���e�X�g�E�C���h�E\" onclick=\"wopen()\"></form>");
//-->
</script>
_HTML_
}
#************************************************
# �W�����������ύXHTML
#************************************************
sub sort_genre_html{
&list_genre_html(@genre_dir_all);
$main_html=<<"_HTML_";
$formop_h
<b><span>���W�������̏����ύX��</span></b>
<table $sys_tbl_opt bgcolor='$sys_color'>
<input type=hidden name=type value=sort1>
<tr><td width=400><small>�^�C�g��</small></td><td><small>�f�B���N�g��</small></td><td><small>����</small></td></tr>
_HTML_
$i=0;
foreach $dir(@genre_dir_all){
if($dir eq ''){next;}
$i++;
$main_html.=<<"_HTML_";
<input type=hidden name=d$i value="$dir">
<tr><td><small>$title{$dir}</small></td>
<td><small>$dir</small></td>
<td><span><input type=text name=s$i size=5 value="$i"><span></td></tr>
_HTML_
}
$main_html.='<tr><td colspan=3><span><center><input type=submit value="�@�@�ύX�@�@"><br><center></span></td></tr></table>';
$main_html.="<small>(�W�������̏����́A�l�̏��������ɕ��ёւ����܂��B�����ł��ł��B)</small></form>";
}
#************************************************
# �v���C���O�\��
#************************************************
sub play_html{
local(@play_log);
for($i=1;$i<=$SYS{max_player};$i++){
$file="$data_dir/$header$i\.cgi";
$file_t=-M $file;
if($file_t eq ''){next;}
if($file_t > $max_t){$max_t = $file_t;$max_f=$file;}
if(($file_t < $min_t)||($min_t eq '')){$min_t = $file_t;$min_f=$file;}
open(DB,"$data_dir/$header$i\.cgi");@list=<DB>;close(DB);
$list[0]=~ s/\n//g;
($LOG{num},$LOG{win},$LOG{lose},$LOG{seed},$LOG{old},$LOG{write},$LOG{name},$LOG{'time'},$LOG{lap},$LOG{last_lap},$LOG{genre},$LOG{mode},$LOG{ck_s},$LOG{ck_n}) = split(/\t/,$list[0]);
if($LOG{mode} eq 1){$LOG{mode}=$mode_name1{$LOG{genre}};}
elsif($LOG{mode} eq 2){$LOG{mode}=$mode_name2{$LOG{genre}};}
else{$LOG{mode}='-----';}
push(@play_log,join("\t",(time-$file_t*60*60*24,$LOG{'time'},$LOG{num},$LOG{win},$LOG{lose},$LOG{seed},$LOG{old},$LOG{write},$LOG{name},$LOG{lap},$LOG{last_lap},$title{$LOG{genre}},$LOG{mode},$LOG{ck_s},$LOG{ck_n})));
}
foreach(sort {$b cmp $a} @play_log){
($file_t,$LOG{'time'},$LOG{num},$LOG{win},$LOG{lose},$LOG{seed},$LOG{old},$LOG{write},$LOG{name},$LOG{lap},$LOG{last_lap},$LOG{genre},$LOG{mode},$LOG{ck_s},$LOG{ck_n})= split(/\t/,$_);
if($LOG{'time'} eq ''){$LOG{'time'} = '-----';}
if($LOG{genre} eq ''){$LOG{genre} = '-----';}
if($LOG{ck_s} eq ''){$LOG{ck_s} = '-----';}
if($LOG{ck_n} eq ''){$LOG{ck_n} = '-----';}
($sec,$min)=&score_time($LOG{lap}-$LOG{'time'});
$file_t=&time_set($file_t);
split(/\t/,$list[0]);
$play_log_list.=<<"_HTML_";
<tr>
<td nowrap>$file_t</td>
<td nowrap>$LOG{genre}</td>
<td nowrap>$LOG{mode}</td>
<td nowrap>$LOG{num}</td>
<td nowrap>$LOG{win}</td>
<td nowrap>$min��$sec�b</td>
<td nowrap>$LOG{ck_s}</td>
<td nowrap>$LOG{ck_n}</td>
</tr>
_HTML_
}
if($min_t ne ''){
$t=($max_t-$min_t)*(60*60*24);
$day=$t-$t%(86400);
$hour=$t-$day-$t%(60*60);
$min=$t-$day-$hour-$t%(60);
$sec=$t-$day-$hour-$min;
$day=int(($day-1)/(86400)+0.5);
$hour=$hour/(60*60);
$min=$min/60;
$term="$day��$hour����$min��$sec�b";
}
if($min_t ne ''){$min_t = &time_set(time-$min_t*(60*60*24));}
else{$min_t = '-----';$term='-----';}
if($max_t ne ''){$max_t = &time_set(time-$max_t*(60*60*24));}
else{$max_t = '-----';$term='-----';}
$a=$t%(86400);
$main_html=<<"_HTML_";
<b><span>���v���C���O�̎g�p�󋵁��@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=playlog target=help>Help</a>]<span></b>
<table $sys_tbl_opt bgcolor='$sys_color'>
_HTML_
$main_html.=&my_print(<<"_MY_");
�ŐV�v���C���O���p����
$min_t
�ŌÃv���C���O���p����
$max_t
�v���C���O���p�Ԋu
$term
�����v���C����
$SYS{max_player}�l
�v���C���O�ی����
$SYS{limit}��
_MY_
$main_html.='</td></tr></table><br><br>';
if($play_log_list ne ''){
$main_html.=<<"_HTML_";
<b><span>���v���C���O�ꗗ��<span></b>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr>
<td>�v���C���O���p����</td>
<td>�W������</td>
<td>���[�h</td>
<td>�o<br>��<br>��</td>
<td>��<br>��<br>��</td>
<td>�񓚎���</td>
<td>��<br>��<br>��</td>
<td>���O</td>
</tr>
$play_log_list
</table>
_HTML_
}
}
#************************************************
# �e��t�@�C���̃T�C�Y��\��
#************************************************
sub file_size_html{
local($return);
$main_html=<<"_HTML_";
<span><br><br><b>���e��V�X�e���p�t�@�C���̗e�ʁ�</b></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr>
<td nowrap><small><b>�N�C�Y�X�N���v�g</b></small></td>
<td nowrap><small><b>�ݒ胍�O</b></small></td>
<td nowrap><small><b>�v���C���O</b></small></td>
<td nowrap><small><b>���v</b></small></td>
</tr>
_HTML_
$cgi_file_size=0;
local(@cgi_files)=($quiz_op_cgi,$quiz_cgi,$function_cgi,$index_cgi);
foreach $cgi_file(@cgi_files){
$cgi_file_size=$cgi_file_size+&file_size_kb("$cgi_file");
}
$log_file_size=0;
local(@cgi_files)=($genre_cgi,$design_cgi,$sysdesign_cgi,$pass_cgi,$system_cgi,$contribute_cgi);
foreach $cgi_file(@cgi_files){
$log_file_size=$log_file_size+&file_size_kb("$cgi_file");
}
$playlog_file_size=0;
opendir(DIR,$data_dir);
local(@cgi_files)=readdir(DIR);close(DIR);
foreach $cgi_file(@cgi_files){
$playlog_file_size=$playlog_file_size+&file_size_kb("$data_dir/$cgi_file");
}
$main_html.=<<"_HTML_";
<tr>
<td>${cgi_file_size}kb</td>
<td>${log_file_size}kb</td>
<td>${playlog_file_size}kb</td>
<td>${$ret=$cgi_file_size+$log_file_size+$playlog_file_size}${ret}kb</td>
</tr>
</table>
_HTML_
if($#genre_dir_all <0){return;}
$main_html.=<<"_HTML_";
<span><br><br><b>���e��W�������p�t�@�C���̗e�ʁ�</b></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td nowrap><small><b>�W��������</b></small></td>
<td nowrap><small><b>���<br>�t�@�C��</b></small></td>
<td nowrap><small><b>�e����<br>�t�@�C��</b></small></td>
<td nowrap><small><b>�I�����b�Z�[�W�t�@�C��</b></small></td>
<td nowrap><small><b>�e�o�b�N�A�b�v</b></small></td>
<td nowrap><small><b>�ݖ��<br>���уt�@�C��</b></small></td>
<td></td><td nowrap><small><b>���v</b></small></td></tr>
_HTML_
foreach $dir(@genre_dir_all){
$genre_size=0;
$mon_size=0;
$mes_size=0;
$back_size=0;
$seiseki_size=0;
$q_size=0;
if(($mondai_cgi{$dir} ne '.')&&!($mondai_cgi{$dir} =~ /\//)){
$mon_size=&file_size_kb("$dir/$mondai_$dir\.cgi");
$mon_size=$mon_size+&file_size_kb("$dir/$contribute_cgi");
}
$seiseki_size=&file_size_kb("$dir/$high_cgi1{$dir}\.cgi")
+&file_size_kb("$dir/$scorehst_cgi1{$dir}\.cgi")
+&file_size_kb("$dir/$high_cgi2{$dir}\.cgi")
+&file_size_kb("$dir/$scorehst_cgi2{$dir}\.cgi");
$mes_size=&file_size_kb("$dir/mes_${dir}.cgi");
(@h_back1,@s_back1,@h_back2,@s_back2)=();
&backup_list($dir);
foreach $file(@h_back1,@s_back1,@h_back2,@s_back2,@q_back,@m_back){
$back_size=$back_size+&file_size_kb("$dir/$file");
}
&refresh_quiz;
&quiz_read($dir);
if(($mondai_cgi{$dir} ne '.')&&!($mondai_cgi{$dir} =~ /\//)){
for($i=0;$i<=$#mondai;$i++){
$q_size=$q_size+&file_size_kb("$dir/$quiz_header$i\.cgi");
}
}
$genre_size=$mon_size+$seiseki_size+$back_size+$q_size+$mes_size;
$all_size=$all_size+$genre_size;
$mon_all=$mon_all+$mon_size;
$mes_all=$mes_all+$mes_size;
$seiseki_all=$seiseki_all+$seiseki_size;
$back_all=$back_all+$back_size;
$q_all=$q_all+$q_size;
$main_html.=<<"_HTML_";
<tr><td nowrap><small>$title{$dir}</small></td>
<td nowrap><small>${mon_size}kb</small></td>
<td nowrap><small>${seiseki_size}kb</small></td>
<td nowrap><small>${mes_size}kb</small></td>
<td nowrap><small>${back_size}kb</small></td>
<td nowrap><small>${q_size}kb</small></td>
<td></td>
<td nowrap><small>$genre_size\kb</small></td>
</tr>
_HTML_
}
$main_html.= <<"_HTML_";
<tr></tr>
<tr>
<td><small>�S�W�������v</small></td>
<td><small>${mon_all}kb</small></td>
<td><small>${seiseki_all}kb</small></td>
<td><small>${mes_all}kb</small></td>
<td><small>${back_all}kb</small></td>
<td><small>${q_all}kb</small></td>
<td></td>
<td><small>${all_size}kb</small></td>
</tr>
</table><br>
_HTML_
}
#************************************************
# �e�탍�O�{��
#************************************************
sub log_html{
&list_genre_html(@genre_dir_all);
$main_html=<<"_HTML_";
<span><br><br><b>���e�탍�O���{���ł��܂��B</b><br>�@�ۑ�����ꍇ�́A�{����u���E�U�́w���O��t���ĕۑ��x�ŕۑ����Ă��������B<br><br></span>
<span>���V�X�e�����O���@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=log target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td nowrap><small>�V�X�e���ݒ�t�@�C��($system_cgi)</small></td>
$formop_hb
<input type=hidden name=log value=sys>
<td colspan=2><span><input type=submit value=�{��></td></tr></form>
<tr><td nowrap><small>�W�������ݒ�t�@�C��($genre_cgi)</small></td>
$formop_hb
<input type=hidden name=log value=genre>
<td colspan=2><span><input type=submit value=�{��></span></td></tr></form>
<tr><td nowrap><small>�V�X�e���f�U�C���ݒ�t�@�C��($sysdesign_cgi)</small></td>
$formop_hb
<input type=hidden name=log value=sysdesign>
<td colspan=2><span><input type=submit value=�{��></span></td></tr></form>
<tr><td nowrap><small>�W�������f�U�C���ݒ�t�@�C��($design_cgi)</small></td>
$formop_hb
<input type=hidden name=log value=design>
<td colspan=2><span><input type=submit value=�{��></span></td></tr></form>
</table><br><br>
_HTML_
if($#genre_dir_all>=0){
$main_html.=<<"_HTML_";
<span>���W�������ʃ��O���@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=log target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr>
<td nowrap rowspan=2><small>�W��������</td>
<td nowrap rowspan=2 colspan=2><small><center>��胍�O</small></center></td>
<td nowrap rowspan=2 colspan=2><small><center>���e��胍�O</small></center></td>
<td nowrap colspan=2><center><small>���[�h�P</small></center></td>
<td nowrap colspan=2><center><small>���[�h�Q</small></center></td></tr>
<tr><td nowrap><small>�����ю҃��O</small></td>
<td nowrap><small>���ѕ��z���O</small></td>
<td nowrap><small>�����ю҃��O</small></td>
<td nowrap><small>���ѕ��z���O</small></td>
</tr>
_HTML_
foreach $dir(@genre_dir_all){
if($dir eq ''){next;}
$main_html.=<<"_HTML_";
<tr><td nowrap><small>$title{$dir}</small></td>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=m>
<td><span><input type=submit value=�{��></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=m2>
<td><span><input type=submit value=�ǉ��`��></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=c>
<td><span><input type=submit value=�{��></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=c2>
<td><span><input type=submit value=�ǉ��`��></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=h1>
<td><span><input type=submit value=�{��></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=s1>
<td><span><input type=submit value=�{��></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=h2>
<td><span><input type=submit value=�{��></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=s2>
<td><span><input type=submit value=�{��></span></td></form></tr>
_HTML_
}
$main_html.='</table>';
}
}
#************************************************
# �W���������������m�FHTML
#************************************************
sub copy_genre_html{
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value="copy1">
<input type=hidden name=menu value=1>
<span><br><br><b>�����̃W�������́A������f�B���N�g������͂��Ă��������B</b><br><br>
<b>���R�s�[��W��������</b></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
_HTML_
$main_html.=&my_print(<<"_MY_");
<center>�����������R�s�[��W�������̐ݒ聡��������</center>\t#eeaaee\n
(1)�f�B���N�g��
<input type=text name=d2 value="$FORM2{d2}">
<center><br><input type=submit value="�@�����@"></center>\n
_MY_
$main_html.='</table></form>';
}
#************************************************
# �e�탍�O�̃o�b�N�A�b�vHTML
#�e���[�h�e�t�@�C���̃o�b�N�A�b�v���O�����X�g�A�b�v
#�폜�A�g�ݍ��݂�checkbox
#************************************************
sub backup_html{
&backup_list($FORM{d});
$max=max($#m_back,$#q_back,$#h_back1,$#s_back1,$#h_back2,$#s_back2);
$hmod1=$#h_back1+1;$smod1=$#s_back1+1;
$mod1=$#h_back1+$#s_back1+2;
$hmod2=$#h_back2+1;$smod2=$#s_back2+1;
$mod2=$#h_back2+$#s_back2+2;
$m_span=$#m_back+1;
$q_span=$#q_back+1;
$main_html=<<"_HTML_";
<span><b><br><br>���`�F�b�N�{�b�N�X��ON�ɂ��A���s�{�^���������Ă��������B<br><br>���o�b�N�A�b�v�t�@�C���̓ǂݍ��݁�</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=back target=help>Help</a>]</span>
_HTML_
if($max >= 0){
$main_html.=<<"_HTML_";
<table $sys_tbl_opt bgcolor='$sys_color'>
$formop_hd
<input type=hidden name=type value=back1>
<input type=hidden name=menu value=1>
<tr><td colspan=2><small><b>���</b></small></td>
<td nowrap><small><b>backup���O��</b></small></td>
<td><small><b>�쐬����</b></small></td>
<td><small><b>���l</b></small></td>
<td><small><b>��<br>��</b></small></td>
<td><small><b>��<br>��</b></small></td>
<td><small><b>��<br>��</b></small></td></tr>
<tr>
_HTML_
$bu=0;
if($#m_back >= 0){
$main_html.= "<td nowrap rowspan=$m_span colspan=2><small>���t�@�C��</small></td>";
$bu=&m_box_html($bu,'mbu',@m_back);
}
if($#q_back >= 0){
$main_html.= "<td nowrap rowspan=$m_span colspan=2><small>�ݖ�ʐ��уt�@�C��</small></td>";
$bu=&q_box_html($bu,'qbu',@q_back);
}
if($mod1 > 0){$main_html.= "<td nowrap rowspan=$mod1><small>���[�h�P</small></td>";}
if($hmod1 > 0){
$main_html.="<td nowrap rowspan=$hmod1><small>�����ю҃t�@�C��</small></td>";
$bu=&h_box_html($bu,'buh1',@h_back1);
}
if($smod1 > 0){
$main_html.="<td nowrap rowspan=$smod1><small>���ѕ��z�t�@�C��</small></td>";
$bu=&s_box_html($bu,'bus1',@s_back1);
}
if($mod2 > 0){
$main_html.="<td nowrap rowspan=$mod2><small>���[�h�Q</small></td>";
}
if($hmod2 > 0){
$main_html.="<td nowrap rowspan=$hmod2><small>�����ю҃t�@�C��</small></td>";
$bu=&h_box_html($bu,'buh2',@h_back2);
}
if($smod2 > 0){
$main_html.="<td nowrap rowspan=$smod2><small>���ѕ��z�t�@�C��</small></td>";
$bu=&s_box_html($bu,'bus2',@s_back2);
}
$main_html.=<<"_HTML_";
<td nowrap colspan=8><span><center>
<input type=submit value='    ���s    '>
</center></span></td></tr></table></form>
_HTML_
}else{
$main_html.="<span><br>�����̃W�������̃o�b�N�A�b�v�t�@�C���͂���܂���B<br><br></span>";
}
if($high_back_w1{$FORM{d}}){$hw1{w}=' selected';}else{$hw1{o}=' selected';}
if($scorehst_back_w1{$FORM{d}}){$sw1{w}=' selected';}else{$sw1{o}=' selected';}
if($high_back_w2{$FORM{d}}){$hw2{w}=' selected';}else{$hw2{o}=' selected';}
if($scorehst_back_w2{$FORM{d}}){$sw2{w}=' selected';}else{$sw2{o}=' selected';}
$mw{$FORM{mbuw}}=' selected';
$qw{$FORM{qbuw}}=' selected';
local($h1_count,$s1_count,$h2_count,$s2_count);
$h1_count=&high_count($high_cgi1{$FORM{d}});
$s1_count=&hst_count($scorehst_cgi1{$FORM{d}});
$h2_count=&high_count($high_cgi2{$FORM{d}});
$s2_count=&hst_count($scorehst_cgi2{$FORM{d}});
&refresh_quiz;
&quiz_read($FORM{d});
$mon=$#mondai+1;
$main_html.=<<"_HTML_";
<span><br><b>���o�b�N�A�b�v�t�@�C���̍쐬��</b>�@[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=back target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
$formop_hd
<input type=hidden name=type value=back2>
<input type=hidden name=menu value=1>
<tr><td colspan=2><small><b>���</b></small></td><td><b><small>�쐬���[�h</small></b></td><td><small><b>���l</b></small></td><td><small><b>�쐬</b></small></td></tr>
<tr><td nowrap colspan=2><small>���t�@�C��</small></td><td><span><select name=mbuw><option value=1$mw{1}>�㏑��<option value=0$mw{0}>�ʃt�@�C��</select></span></td><td><small>��萔�F$mon��</small></td><td><span><input type=checkbox name=mbu value=1></span></td></tr>
<tr><td nowrap colspan=2><small>�ݖ�ʐ��уt�@�C��</small></td><td><span><select name=qbuw><option value=1$qw{1}>�㏑��<option value=0$qw{0}>�ʃt�@�C��</select></span></td><td><small>��萔�F$mon��</small></td><td><span><input type=checkbox name=qbu value=1></span></td></tr>
<tr><td nowrap rowspan=2><small>���[�h�P</small></td>
<td nowrap><small>�����ю҃t�@�C��</small></td><td><span><select name=hbu1w><option value=1$hw1{w}>�㏑��<option value=0$hw1{o}>�ʃt�@�C��</select></span></td><td><small>�o�^�Ґ��F$h1_count�l<small></td><td><span><input type=checkbox name=hbu1 value=1></span></td></tr>
<tr><td nowrap><small>���ѕ��z�t�@�C��</small></td><td><span><select name=sbu1w><option value=1$sw1{w}>�㏑��<option value=0$sw1{o}>�ʃt�@�C��</select></span></td><td><small>����Ґ��F$s1_count�l</small></td><td><span><input type=checkbox name=sbu1 value=1></span></td></tr>
<tr><td nowrap rowspan=2><small>���[�h�Q</small></td>
<td nowrap><small>�����ю҃t�@�C��</small></td><td><span><select name=hbu2w><option value=1$hw2{w}>�㏑��<option value=0$hw2{o}>�ʃt�@�C��</select></span></td><td><small>�o�^�Ґ��F$h2_count�l<small></td><td><span><input type=checkbox name=hbu2 value=1></span></td></tr>
<tr><td nowrap><small>���ѕ��z�t�@�C��</small></td><td><span><select name=sbu2w><option value=1$sw2{w}>�㏑��<option value=0$sw2{o}>�ʃt�@�C��</select></span></td><td><small>����Ґ��F$s2_count�l</small></td><td><span><input type=checkbox name=sbu2 value=1></span></td></tr>
<tr><td nowrap colspan=5><span><center><input type=submit value='    ���s    '></center></span></td></tr>
</table></form>
_HTML_
}
#************************************************
# backup_html���t�@�C���p�̃`�F�b�N�{�b�N�X
#************************************************
sub m_box_html{
local($num,$syg,@file)=@_;
local($count);
foreach $file(@file){
$count=0;
local($time)=&time_set(time - (-M "$FORM{d}/$file")*60*60*24);
&refresh_quiz;
&quiz_read($FORM{d},'','',$file);
$count=$#mondai+1;
$num++;
&box_html($file,$time,"��萔�F$count��",0,$syg,$num);
}
return $num;
}
#************************************************
# backup_html���t�@�C���p�̃`�F�b�N�{�b�N�X
#************************************************
sub q_box_html{
local($num,$syg,@file)=@_;
local($count);
foreach $file(@file){
open(DB,"$FORM{d}/$file");local(@list)=<DB>;close(DB);
local($time)=&time_set(time - (-M "$FORM{d}/$file")*60*60*24);
$count=@list;
if($list[0]=~ /^ver2/){$count=int(($count-1)/2);}
$num++;
&box_html($file,$time,"��萔�F$count��",0,$syg,$num);
}
return $num;
}
#************************************************
# backup_html�����ю҃t�@�C���p�̃`�F�b�N�{�b�N�X
#************************************************
sub h_box_html{
local($num,$syg,@file)=@_;
local($count);
foreach $file(@file){
$count=0;
open(DB,"$FORM{d}/$file");local(@list)=<DB>;close(DB);
local($time);
if($list[0]=~ /^date([\d]+)/){$time=&time_set($1);$count=@list-1;}
else{$count=@list;}
$num++;
&box_html($file,$time,"�o�^�Ґ��F$count�l",1,$syg,$num);
}
return $num;
}
#************************************************
# backup_html���ѕ��z�t�@�C���p�`�F�b�N�{�b�N�X
#************************************************
sub s_box_html{
local($num,$syg,@file)=@_;
local($count);
foreach $file(@file){
$count=0;
open(DB,"$FORM{d}/$file");local(@list)=<DB>;close(DB);
local($time);
if($list[0]=~ /^date([\d]+)/){$time=&time_set($1);$list[0]='';}
else{$time=' ';}
foreach(@list){$count=$count+$_;}
$num++;
&box_html($file,$time,"����Ґ��F$count�l",0,$syg,$num);
}
return $num;
}
#************************************************
# backup_html���ѕ��z�t�@�C���p�`�F�b�N�{�b�N�X
#************************************************
sub box_html{
local($file,$time,$cf,$i_box,$syg,$num)=@_;
if($i_box eq 1){$i_box="<input type=checkbox name='$syg\i$num' value='$file'>";}
else{$i_box='�@';}
$main_html.=<<"_HTML_";
<td nowrap><small>$file</small></td>
<td nowrap><small>$time</small></td>
<td nowrap><small>$cf</small></td>
<td><span>$i_box</span></td>
<td><span><input type=checkbox name="$syg\w$num" value="$file"></span></td>
<td><span><input type=checkbox name="$syg\d$num" value="$file"></span></td></tr><tr>
_HTML_
}
#************************************************
# �A�N�Z�X�����ݒ���
#************************************************
sub edit_guard_html{
open(DB,$guard_cgi);
@list=<DB>;
close(DB);
if($list[0] eq "guard\n"){
$guard{1}=' checked';
$list[0]='';
}elsif($list[0] eq "permit\n"){
$guard{0}=' checked';
$list[0]='';
}else{
$guard{1}=' checked';
}
$iplist=join('',@list);
$main_html.=<<"_HTML_";
$formop_h
<input type=hidden name=type value=guard1>
<span><br><br><b>���A�N�Z�X�������s��IP����͂��Ă��������B(�O����v)</b><br><br></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td><span>
<input type=radio name='guard' value=1$guard{1}>�ȉ���IP���A�N�Z�X�֎~�ɂ���<br>
<input type=radio name='guard' value=0$guard{0}>�ȉ���IP���A�N�Z�X���ɂ���<br>
<textarea rows=20 cols=60 name='iplist'>$iplist</textarea>
</span></td></tr><tr><td>
<span><center>
<input type=submit value="�@�ҏW�@">
<br></center></span></td></tr></table></form>
_HTML_
}
#************************************************
# �ʃW�������ւ̈ړ�
#************************************************
sub other_genre_html{
$type=&cut_num($FORM{type});
$other_genre=<<"_HTML_";
<script language=javascript>
//<!--
with (document){
write("<form action=\\"$quiz_op_cgi\\" name=\\"gogenre\\" method=\\"$method\\">")
write("<input type=hidden name=passch value=\\"$FORM2{passch}\\">")
write("<input type=hidden name=menu value=1>")
write("<table border=0><tr><td><span><select name=d onChange=\\"document.forms.gogenre.submit();\\">")
write("<option value='$FORM{d}'>�ʃW�������ֈړ�")
_HTML_
foreach $dir(@genre_dir_all){
$other_genre.="write(\"<option value=$dir>$title{$dir}\")\n";
}
$other_genre.=<<"_HTML_";
write("</select></span></td><td><span><select name=type onChange=\\"document.forms.gogenre.submit();\\">")
write("<option value='$type'>���̃R�}���h")
write(\"<option value=editg>�W�������̕ҏW\")
write(\"<option value=copy>�W�������̕���\")
write(\"<option value=del>�W�������̊e��폜\")
write(\"<option value=qedit>���̍쐬�ҏW\")
write(\"<option value=qdel>���̍폜�A�����ύX\")
write(\"<option value=qmulti>���̈ꊇ�ǉ�\")
write(\"<option value=qcont>���e���̕ҏW\")
write(\"<option value=mes>�I�������b�Z�[�W�ǉ�\")
write(\"<option value=score>�o��󋵕\\\\��\")
write(\"<option value=back>�e�탍�O�̃o�b�N�A�b�v\")
write(\"<option value=high>�����ю҃��X�g�ҏW\")
write("</select></span></td></tr></table></form>")
}
//--></script>
_HTML_
}
#************************************************
# �o�b�N�A�b�v�t�@�C�������X�g�A�b�v����B
#************************************************
sub backup_list{
$dir=$_[0];
opendir(DIR,$dir);
local(@dir_files)=readdir(DIR);close(DIR);
foreach $file(@dir_files){
if($file=~ /^$mondai_$dir\_bak/){push(@m_back,$file);}
if($file=~ /^$quiz_header\_bak/){push(@q_back,$file);}
if($file=~ /^$high_cgi1{$dir}_bak/){push(@h_back1,$file);}
if($file=~ /^$scorehst_cgi1{$dir}_bak/){push(@s_back1,$file);}
if($file=~ /^$high_cgi2{$dir}_bak/){push(@h_back2,$file);}
if($file=~ /^$scorehst_cgi2{$dir}_bak/){push(@s_back2,$file);}
}
}
#************************************************
# �����ю҃��X�g�̓o�^�l���v�Z
#************************************************
sub high_count{
local($file)=@_;
local($count);
open(DB,"$FORM{d}/$file\.cgi");local(@list)=<DB>;close(DB);
if($list[0]=~ /^date([\d]+)/){$count=@list-1;}
else{$count=@list;}
return $count;
}
#************************************************
# ���ѕ��z�t�@�C���̓o�^�l���v�Z
#************************************************
sub hst_count{
local($file)=@_;
local($count);
open(DB,"$FORM{d}/$file\.cgi");local(@list)=<DB>;close(DB);
if($list[0]=~ /^date([\d]+)/){$list[0]='';}
foreach(@list){$count=$count+$_;}
return $count+0;
}
#************************************************
# �e�탍�O�{��
#************************************************
sub log{
if(($FORM{log} eq 'm2')||($FORM{log} eq 'c2')){
if($FORM{log} eq 'm2'){$file="$FORM{d}/$mondai_$FORM{d}\.cgi";}
else{$file="$FORM{d}/$contribute_cgi";}
if(!(-f $file)){&error(814,$file);return 1;}
open(DB,$file);local(@line)=<DB>;close(DB);
$index=0;
$main_html=<<"_HTML_";
#-----����-----# 
#q:��蕶
#ans:����
#mis1:�듚�P
#mis2:�듚�Q
#mis3:�듚�R
#mis4:�듚�S
#ansmes:�������b�Z�[�W
#mismes:�s�������b�Z�[�W
#cf:�Q�l����
#digest:�����e
#mismes1:�듚�P���b�Z�[�W
#mismes2:�듚�Q���b�Z�[�W
#mismes3:�듚�R���b�Z�[�W
#mismes4:�듚�S���b�Z�[�W
#author:�쐬��
#anstype:�񓚕���
_HTML_
foreach(@line){
$_=~ s/\n//g;
if($_ eq ''){next;}
if($_=~ /^#/){next;}
$index++;
local($mondai,$ans,$misans1,$misans2,$misans3,$misans4,$anscom,$misanscom,$cf,$digest,$misanscom1,$misanscom2,$misanscom3,$misanscom4,$anstype,$author)=split(/\t/,$_);
$main_html.=<<"_HTML_";
#-----��$index��-----# 
q:$mondai
ans:$ans
mis1:$misans1
mis2:$misans2
mis3:$misans3
mis4:$misans4
ansmes:$anscom
mismes:$misanscom
cf:$cf
digest:$digest
mismes1:$misanscom1
mismes2:$misanscom2
mismes3:$misanscom3
mismes4:$misanscom4
author:$author
anstype:$anstype
_HTML_
}
if($#line < 0){&error(821,$file);return 1;}
}else{
if($FORM{log} eq 'sys'){$file=$system_cgi;}
elsif($FORM{log} eq 'genre'){$file=$genre_cgi;}
elsif($FORM{log} eq 'sysdesign'){$file=$sysdesign_cgi;}
elsif($FORM{log} eq 'design'){$file=$design_cgi;}
elsif($FORM{log} eq 'm'){$file="$FORM{d}/$mondai_$FORM{d}\.cgi";}
elsif($FORM{log} eq 'c'){$file="$FORM{d}/$contribute_cgi";}
elsif($FORM{log} eq 'h1'){$file="$FORM{d}/$high_cgi1{$FORM{d}}\.cgi";}
elsif($FORM{log} eq 's1'){$file="$FORM{d}/$scorehst_cgi1{$FORM{d}}\.cgi";}
elsif($FORM{log} eq 'h2'){$file="$FORM{d}/$high_cgi2{$FORM{d}}\.cgi";}
elsif($FORM{log} eq 's2'){$file="$FORM{d}/$scorehst_cgi2{$FORM{d}}\.cgi";}
if(!(-f $file)){&error(815,$file);return 1;}
open(DB,$file);
@line=<DB>;close(DB);
foreach(@line){
$_=~ s/\n//g;
$main_html.= "$_\r";
}
if($#line < 0){&error(822,$file);return 1;}
}
$Content_type='text/plain';
$header_html='';
$footer_html='';
return 0;
}
#************************************************
# �p�[�~�b�V���������ɂ��ݒ胁�b�Z�[�W�\������
#************************************************
sub permit_mes {
local($dirs)=join('<br>',@_);
&mes(<<"_HTML_");
�v���o�C�_�̊֌W��p�[�~�b�V�����ɐ���������<br>
�t�@�C���A�f�B���N�g���̎����쐬���ł��Ȃ��ꍇ<br>
�W�������̐V�K�쐬�ɂ́A���炩���߈ȉ��̃t�@�C���A�f�B���N�g����<br>
�蓮�ō쐬����K�v������܂��B
<br><br>
<table border=0><tr><td nowrap>
$dirs
</td></tr></table>
<br><br>
�Ȃ��AWindows�����g���̕��͓Y�t�v���O�����ɂ��<br>
�p�\\�R����ŕK�v�t�@�C�����쐬���邱�Ƃ��ł��܂��B
_HTML_
}
#************************************************
# �\�쐬�pprint
#************************************************
sub my_print{
local(@word1,@word2,$i,$word3,$return);
$i=0;$word3=$_[0];
while($word3 ne ''){($word1[$i],$word2[$i],$word3)=split(/\n/,$word3,3);$i++;}
$i=0;
foreach(@word1){
local(@dummy)=split(/\t/,$word2[$i]);
if($#dummy>0){$return.="<tr><td nowrap><small>$word1[$i]</small></td><td nowrap><span>$dummy[0]</span></td><td nowrap><span>$dummy[1]</span></td></tr>\n";}
elsif($#dummy == 0){$return.="<tr><td nowrap><small>$word1[$i]</small></td><td colspan=2 width=100%><span>$dummy[0]</span></td></tr>\n";}
else{
($word1[$i],$col)=split(/\t/,$word1[$i]);
if($col ne ''){$col=" bgcolor='$col'";}
$return.="<tr><td colspan=3$col><span>$word1[$i]</span></td></tr>\n";
}
$i++;
}
return $return;
}
#************************************************
# �\�쐬�pprint2
#************************************************
sub my_print2{
local($return);
local(@word)=split(/\n/,$_[0]);
foreach(@word){$return .="$_[1]$_$_[2]\n";}
return $return;
}
#************************************************
# �w���v�쐬�pprint
#************************************************
sub help_print{
local($return);
$return="<br><br><hr><br><b><span>���w���v��</span></b><table $sys_tbl_opt bgcolor='$sys_color'>";
$return.=&my_print(@_);
$return.='</table>';
return $return;
}
#************************************************
# �G���[�\������
#************************************************
sub error_html_op{
if($error_mes ne ''){
return <<"_HTML_";
<table $sys_tbl_opt bgcolor=#eeaaaa><tr><td>
<big><center><b>�������G���[���b�Z�[�W������<br><br></b></big>
<table border=0><tr><td><span><b>$error_mes</b></span></td></tr></table>
</center></td></tr></table><br>
_HTML_
}
}
#************************************************
# HTML�o��
#************************************************
sub outputop{
if($Content_type ne ''){print "Content-type: $Content_type\n\n";}
else{print "Content-type: text/html\n\n";}
print "$header_html";
if($Content_type eq ''){print "$align1";}
print "$other_genre";
print &error_html_op;
print &mes_html;
print "$menu_html";
print "$system_list";
print "$genre_list";
print "$sysdesign_list";
print "$design_list";
print $test;
if($main_html ne ''){print "$main_html";}
if($Content_type eq ''){print "$align2";}
print "$footer_html";
&file_unlock("$data_dir/$file_lock");
exit;
}
#************************************************
# �t�@�C���̍폜
#************************************************
sub del_file{
local($name,@files)=@_;
local($flg)=0;
foreach(@files){
if(-f "$_"){
unlink "$_";
$flg=1;
}
}
if(($flg)&&($name ne '')){&mes(300,$name);}
return $flg;
}
#************************************************
# �W�������ʊe��폜����
#************************************************
sub del_genre{
local(@all_list,@qu_list);
if($FORM{delj} ne ''){
$flag=0;
for($i=0;$i<=$#genre_dir_all;$i++){
if($FORM{d} eq $genre_dir_all[$i]){
$genre_dir_all[$i]='';
$flag=1;
}
}
if($flag eq 0){&error(802,'�W���������');return 1;}
if(&write_genre_dat){return 1;}
}
opendir(DIR,"$FORM{d}");
local(@dir_files)=readdir(DIR);close(DIR);
foreach $dir_file(@dir_files){
if(-f "$FORM{d}/$dir_file"){
if($FORM{deld} eq '1'){
unlink "$FORM{d}/$dir_file";
}else{
if($FORM{delm}){
if($dir_file=~ /^qu/){
push(@qu_list,"$FORM{d}/$dir_file");
}
}
}
}
}
&del_file("�w$title{$FORM{d}}�x�̐ݖ�ʐ��уt�@�C��",@qu_list);
if($FORM{delh} eq 1){
&del_file("�w$title{$FORM{d}}�x�̍����ю҃��O�t�@�C��",("$FORM{d}/$high_cgi1{$FORM{d}}\.cgi","$FORM{d}/$high_cgi2{$FORM{d}}\.cgi"));
}
if($FORM{delf} eq 1){
&del_file("�w$title{$FORM{d}}�x�̐��ѕ��z�t�@�C��",("$FORM{d}/$scorehst_cgi1{$FORM{d}}\.cgi","$FORM{d}/$scorehst_cgi2{$FORM{d}}\.cgi"));
}
if($FORM{delq} eq 1){
&del_file("�w$title{$FORM{d}}�x�̖��t�@�C��","$FORM{d}/$mondai_$FORM{d}\.cgi");
}
if($FORM{delc} eq 1){
&del_file("�w$title{$FORM{d}}�x�̓��e���t�@�C��","$FORM{d}/$contribute_cgi");
}
if($FORM{dele} eq 1){
&del_file("�w$title{$FORM{d}}�x�̏I�����b�Z�[�W�t�@�C��","$FORM{d}/$mes_$FORM{d}\.cgi");
}
if($FORM{deld} eq 1){rmdir $FORM{d};&mes(301,"$FORM{d}�f�B���N�g���ƁA����Ɋ܂܂��t�@�C��")}#�f�B���N�g���̍폜
&mes(302,"�w$title{$FORM{d}}�x�̃W�������o�^���");
return 0;
}
#************************************************
# ���폜���ԕύX����
#************************************************
sub del_quiz{
if(&ch_file_stump("$FORM{d}/$mondai_$FORM{d}\.cgi",'���t�@�C��',$FORM{fa})){return 1;}
&refresh_quiz;
&quiz_read($FORM{d});
$i=0;
local(@list)=();
foreach(@mondai){
$i++;
if($FORM{"qd$i"} eq "1"){next;}
push(@list,join("\t",$FORM{"qn$i"},$mondai[$i-1],$ans[$i-1],$misans1[$i-1],$misans2[$i-1],$misans3[$i-1],$misans4[$i-1],$anscom[$i-1],$misanscom[$i-1],$cf[$i-1],$digest[$i-1],$misanscom1[$i-1],$misanscom2[$i-1],$misanscom3[$i-1],$misanscom4[$i-1],$anstype[$i-1],$author[$i-1],"\n"));
}
&refresh_quiz;
foreach $line(sort{$a <=> $b}@list){
local($dumy1,@dumy2)=split(/\t/,$line);
&push_quiz_palam(@dumy2);
}
return &write_mondai("$mondai_$FORM{d}\.cgi");
}
#************************************************
# ���e���폜����
#************************************************
sub del_cont{
local(@del_conts,@add_conts);
foreach $key(keys %FORM){
if($key =~ /^qc-([\d]+$)/){
push(@add_conts,$1);
push(@del_conts,$1);
}elsif($key =~ /^qcd-([\d]+$)/){
push(@del_conts,$1);
}
}
&refresh_quiz;
&quiz_read($FORM{d},'','',$contribute_cgi);
foreach $i(@add_conts){
push(@cmondai,$mondai[$i-1]);
push(@cans,$ans[$i-1]);
push(@cmisans1,$misans1[$i-1]);
push(@cmisans2,$misans2[$i-1]);
push(@cmisans3,$misans3[$i-1]);
push(@cmisans4,$misans4[$i-1]);
push(@canscom,$anscom[$i-1]);
push(@cmisanscom,$misanscom[$i-1]);
push(@ccf,$cf[$i-1]);
push(@cdigest,$digest[$i-1]);
push(@cmisanscom1,$misanscom1[$i-1]);
push(@cmisanscom2,$misanscom2[$i-1]);
push(@cmisanscom3,$misanscom3[$i-1]);
push(@cmisanscom4,$misanscom4[$i-1]);
push(@canstype,$anstype[$i-1]);
push(@cauthor,$author[$i-1]);
}
if($#add_conts >= 0){
&refresh_quiz;
&quiz_read($FORM{d});
$i=0;
foreach(@cmondai){
&push_quiz_palam($cmondai[$i],$cans[$i],$cmisans1[$i],$cmisans2[$i],$cmisans3[$i],$cmisans4[$i],$canscom[$i],$cmisanscom[$i],$ccf[$i],$cdigest[$i],$cmisanscom1[$i],$cmisanscom2[$i],$cmisanscom3[$i],$cmisanscom4[$i],$canstype[$i],$cauthor[$i]);
$i++;
}
if(&write_mondai("$mondai_$FORM{d}\.cgi")){return 1;}
&mes(501,"�w�肳�ꂽ���e���");
}
if($#del_conts >=0){
&refresh_quiz;
&quiz_read($FORM{d},'','',$contribute_cgi);
$flag=0;
foreach $i(@del_conts){
($mondai[$i-1],$ans[$i-1],$misans1[$i-1],$misans2[$i-1],$misans3[$i-1],$misans4[$i-1],$anscom[$i-1],$misanscom[$i-1],$cf[$i-1],$digest[$i-1],$misanscom1[$i-1],$misanscom2[$i-1],$misanscom3[$i-1],$misanscom4[$i-1],$anstype[$i-1],$author[$i-1])=();
}
if(!&write_mondai("$contribute_cgi")){
&mes(303,"�w�肳�ꂽ���e���");
}
}
}
#************************************************
# �V�X�e���f�U�C���̍폜
#************************************************
sub del_sysdesign{
local($id)=@_;
if($SYS{design} eq $id){&error(831,'���̃V�X�e���f�U�C��');return 1;}
if($sysdesign_title{$id} eq ''){&error(803,'�V�X�e���f�U�C��');return 1;}
$sysdesign_title{$id} = '';
if(!&write_sysdesign_dat()){
&mes(304,"�w�肳�ꂽ�V�X�e���f�U�C��");
}
&all_sysdesign_read;
}
#************************************************
# �W�������f�U�C���̍폜
#************************************************
sub del_design{
local($id)=@_;
if($design_use{$id} ne ''){&error(832,'���̃W�������f�U�C��');return 1;}
if($design_title{$id} eq ''){&error(804,'�W�������f�U�C��');return 1;}
$design_title{$id} = '';
if(!&write_design_dat()){
&mes(305,"�w�肳�ꂽ�W�������f�U�C��");
}
&all_design_read;
}
#************************************************
# ���ҏW����
#************************************************
sub edit_quiz{
if(&ch_edit_quiz_param("$FORM{d}/$_[0]",)){return 1;}
if(&ch_file_stump("$FORM{d}/$_[0]",'���t�@�C��',$FORM{fa})){return 1;}
$mondai[$FORM{qn}-1]      =$FORM4{qqu};
$ans[$FORM{qn}-1]         =$FORM4{qas};
$misans1[$FORM{qn}-1]     =$FORM4{qmas1};
$misans2[$FORM{qn}-1]     =$FORM4{qmas2};
$misans3[$FORM{qn}-1]     =$FORM4{qmas3};
$misans4[$FORM{qn}-1]     =$FORM4{qmas4};
$anscom[$FORM{qn}-1]      =$FORM4{qac};
$misanscom[$FORM{qn}-1]   =$FORM4{qmac};
$cf[$FORM{qn}-1]          =$FORM{qcf};
$digest[$FORM{qn}-1]      =$FORM{qdg};
$misanscom1[$FORM{qn}-1]  =$FORM4{qmac1};
$misanscom2[$FORM{qn}-1]  =$FORM4{qmac2};
$misanscom3[$FORM{qn}-1]  =$FORM4{qmac3};
$misanscom4[$FORM{qn}-1]  =$FORM4{qmac4};
$anstype[$FORM{qn}-1]     =$FORM4{atype};
$author[$FORM{qn}-1]      =$FORM{auth};
if(&write_mondai("$_[0]")){return 1;}
return 0;
}
#************************************************
# �W�������̕ҏW
#************************************************
sub edit_genre{
if(&ch_edit_genre_palam){return 1;}
&form_to_genre_array;
if(&write_genre_dat){return 1;}
&mes(203,'�W�������ݒ�');
&genre_array_to_form;
return 0;
}
#************************************************
# �V�X�e���ݒ�̕ҏW
#************************************************
sub edit_sys{
if(&ch_sys_palam){return 1;}
&form_to_sys;
if(&write_system_dat){return 1;}
&mes(204,'�V�X�e���ݒ�');
&sys_read;
return 0;
}
#************************************************
# �V�X�e���f�U�C���ݒ�̕ҏW
#************************************************
sub edit_sysdesign{
if(&ch_sysdesign_palam){return 1;}
&form_to_sysdesign_array;
if(&write_sysdesign_dat){return 1;}
if($SYS{design} eq $FORM{id}
&& $FORM{id} ne $FORM{sdt}
&& $FORM{edittype} ne 'copy'){
$SYS{design} = $FORM{sdt};
if(&write_system_dat){return 1;}
}
if($FORM{edittype} eq 'new'){
&mes(100,'�V�X�e���f�U�C���ݒ�');
}elsif($FORM{edittype} eq 'copy'){
&mes(750,'�V�X�e���f�U�C���ݒ�');
}else{
&mes(205,'�V�X�e���f�U�C���ݒ�');
}
&all_sysdesign_read;
&sys_read;
return 0;
}
#************************************************
# �W�������f�U�C���ݒ�̕ҏW
#************************************************
sub edit_design{
if(&ch_design_palam){return 1;}
&form_to_design_array;
if(&write_design_dat){return 1;}
if($FORM{edittype} eq 'edit' && $FORM{id} ne $FORM{gdt} && $design_use{$FORM{id}} ne ''){
foreach $dir(@genre_dir_all){
if($design{$dir} eq $FORM{id}){
$design{$dir} = $FORM{gdt};
}
}
if(&write_genre_dat){return 1;}
}
if($FORM{edittype} eq 'new'){
&mes(101,'�W�������f�U�C���ݒ�');
}elsif($FORM{edittype} eq 'copy'){
&mes(751,'�W�������f�U�C���ݒ�');
}else{
&mes(206,'�W�������f�U�C���ݒ�');
}
&all_design_read;
&all_genre_read;
return 0;
}
#************************************************
# �I�������b�Z�[�W�̕ҏW
#************************************************
sub edit_mes{
local(@new);
for($i=0;$i<=$FORM{mn}+1;$i++){
if($FORM{"per-$i"} ne ''){
if($FORM{"mod1-$i"} ne ''){$mod1='1';}else{$mod1='0';}
if($FORM{"mod2-$i"} ne ''){$mod2='1';}else{$mod2='0';}
push(@new,join("\t",$FORM{"per-$i"},$FORM{"mes-$i"},$mod1,$mod2,"\n"));
}
}
@new=sort{$a <=> $b}@new;
push(@new,"top1\t$FORM{'mes-top1'}\t\n");
push(@new,"top2\t$FORM{'mes-top2'}\t\n");
if(!&write_file("$FORM{d}/mes_$FORM{d}\.cgi",@new)){
&mes(207,"�w$title{$FORM{d}}�x�I�������b�Z�[�W");
}
}
#************************************************
# �����ю҃��X�g�̕ҏW
#************************************************
sub edit_high{
local(%del_list1,%del_list2,$key,@new1,@new2,$error);
$error=$error_mes;
foreach $key(keys %FORM){
if($key=~ /^1he(.*)/){$del_list1{$1}=1;}
elsif($key=~ /^2he(.*)/){$del_list2{$1}=1;}
}
if(%del_list1){
open(DB,"$FORM{d}/$high_cgi1{$FORM{d}}\.cgi");@list=<DB>;close(DB);
foreach $line(@list){
if($line =~ /^date/){push(@new1,$line);next;}
if($line eq "\n"){next;}
($day,$high,$name,$host) = split(/\t/,$line);
if($del_list1{"$day\_$high"} eq ''){push(@new1,$line);}
}
&write_file("$FORM{d}/$high_cgi1{$FORM{d}}\.cgi",@new1);
}
if(%del_list2){
open(DB,"$FORM{d}/$high_cgi2{$FORM{d}}\.cgi");@list=<DB>;close(DB);
foreach $line(@list){
if($line =~ /^date/){next;}
if($line eq "\n"){next;}
($day,$high,$name,$host) = split(/\t/,$line);
if($del_list2{"$day\_$high"} eq ''){push(@new2,$line);}
}
&write_file("$FORM{d}/$high_cgi2{$FORM{d}}\.cgi",@new2);
}
if($error eq $error_mes){
&mes(208,"�w$title{$FORM{d}}�x�����ю҃��X�g");
return 0;
}else{return 1;}
}
#************************************************
# �I�������b�Z�[�W�t�@�C���̐V�K�쐬
#************************************************
sub make_mes_cgi{
local($value);
$value=<<"_HTML_";
30\t�S�R�ʖڂ��ˁB\t1\t1\t
50\t�܂��܂����ˁB\t1\t1\t
60\t�܂��܂����ˁB\t1\t1\t
70\t����΂�݂͂Ƃ߂��B\t1\t1\t
80\t���\���ˁ`�B\t1\t1\t
90\t���ƈꑧ�Ȃ񂾂��ǂˁB\t1\t1\t
100\t��������������΂�B\t1\t1\t
top1\t���΂炵���B�p�[�t�F�N�g�I�I\t
top2\t���΂炵���B�p�[�t�F�N�g�I�I\t
_HTML_
if(&ch_dir_exist("$FORM{d}�f�B���N�g��",$FORM{d})){return 1;}
return &write_file("$FORM{d}/mes_$FORM{d}\.cgi",$value);
}
#************************************************
# �W�������̐V�K�쐬
#************************************************
sub make_genre{
if($FORM{d} eq 'data'){
&error(841,'(1)�f�B���N�g����');
return 1;
}
if(&ch_genre_exist($FORM{d}) eq 1){
&error(852,'(1)�f�B���N�g����');
return 1;
}
local($err)=&ch_dir_exist('(1)�f�B���N�g����',$FORM{d});
if($err > 0){
if($err eq 2){&permit_mes(
"$FORM{d}/"
,"$FORM{d}/mes_$FORM{d}.cgi"
,"$FORM{d}/contribute.cgi"
,"$FORM{d}/high1_$FORM{d}.cgi"
,"$FORM{d}/hst1_$FORM{d}.cgi"
,"$FORM{d}/high2_$FORM{d}.cgi"
,"$FORM{d}/hst2_$FORM{d}.cgi"
,"$FORM{d}/mondai_$FORM{d}.cgi"
,"$FORM{d}/qu0.cgi"
,"."
,"."
,"$FORM{d}/qu100.cgi(��萔�Ɠ����ȏ�K�v)");
}
return 1;
}
&def_genre;
$GENRE{dir}=$FORM{d};
&genre_to_genre_array;
if(&write_genre_dat){return 1;}
&mes(903,'�W�������̐V�K�쐬������ɏI�����܂����B<br>���������W�������ʐݒ���s���Ă��������B');
return 0;
}
#************************************************
# ���O�̃o�b�N�A�b�v
#************************************************
sub backup{
local(%m_back,%h_back1,%s_back1,%h_back2,%s_back2,$back_mes);
foreach(keys %FORM){
if($_=~ /^mbu(.*)[\d]+/){$m_back{$FORM{$_}}.=$1;}
if($_=~ /^qbu(.*)[\d]+/){$q_back{$FORM{$_}}.=$1;}
if($_=~ /^buh1(.*)[\d]+/){$h_back1{$FORM{$_}}.=$1;}
elsif($_=~ /^bus1(.*)[\d]+/){$s_back1{$FORM{$_}}.=$1;}
if($_=~ /^buh2(.*)[\d]+/){$h_back2{$FORM{$_}}.=$1;}
elsif($_=~ /^bus2(.*)[\d]+/){$s_back2{$FORM{$_}}.=$1;}
}
$back_mes=$system_mes;
&mondai_file_backup(%m_back);
&quiz_file_backup(%q_back);
&high_file_backup($high_cgi1{$FORM{d}},$day_limit1{$FORM{d}},$num_limit1{$FORM{d}},%h_back1);
&hst_file_backup($scorehst_cgi1{$FORM{d}},%s_back1);
&high_file_backup($high_cgi2{$FORM{d}},$day_limit2{$FORM{d}},$num_limit2{$FORM{d}},%h_back2);
&hst_file_backup($scorehst_cgi2{$FORM{d}},%s_back2);
if($back_mes eq $system_mes){&error(407,'�ǂݍ��ރo�b�N�A�b�v�t�@�C��');}
}
#************************************************
# �o�b�N�A�b�v�t�@�C���̍쐬
#************************************************
sub make_backup{
local($back_mes,@list,@list2);
if(($FORM{hbu1} eq '')&&($FORM{sbu1} eq '')&&($FORM{hbu2} eq '')&&($FORM{sbu2} eq '')&&($FORM{mbu} eq '')&&($FORM{qbu} eq '')){
&error(407,'�o�b�N�A�b�v���쐬����t�@�C��');return;
}
if($FORM{mbu} ne ''){
$back_mes.=&copy_file("$mondai_$FORM{d}",$FORM{mbuw},0).'<br>';
}
if($FORM{qbu} ne ''){
for($i=0;$i<=$#mondai;$i++){
open(DB,"$FORM{d}/$quiz_header$i\.cgi");@list2=<DB>;close(DB);
$list2[0]=~ s/\n//g;
$list2[1]=~ s/\n//g;
push(@list,"$list2[0]\n$list2[1]\n");
}
$tofile=&buckup_filename($quiz_header,$FORM{qbuw},1);
if(!&write_file("$FORM{d}/$tofile",("ver2\n",@list))){$back_mes.="$FORM{d}/$tofile<br>";}
}
if($FORM{hbu1} ne ''){
$back_mes.=&copy_file($high_cgi1{$FORM{d}},$FORM{hbu1w},1).'<br>';
&renew_date("$FORM{d}/$high_cgi1{$FORM{d}}\.cgi");
}
if($FORM{sbu1} ne ''){
$back_mes.=&copy_file($scorehst_cgi1{$FORM{d}},$FORM{sbu1w},1).'<br>';
&renew_date("$FORM{d}/$scorehst_cgi1{$FORM{d}}\.cgi");
}
if($FORM{hbu2} ne ''){
$back_mes.=&copy_file($high_cgi2{$FORM{d}},$FORM{hbu2w},1).'<br>';
&renew_date("$FORM{d}/$high_cgi2{$FORM{d}}\.cgi");
}
if($FORM{sbu2} ne ''){
$back_mes.=&copy_file($scorehst_cgi2{$FORM{d}},$FORM{sbu2w},1).'<br>';
&renew_date("$FORM{d}/$scorehst_cgi2{$FORM{d}}\.cgi");
}
&mes(904,"$back_mes��L�̃o�b�N�A�b�v�t�@�C�����쐬���܂����B");
}
#************************************************
# �o�b�N�A�b�v�t�@�C���̑�����s��
#************************************************
sub high_file_backup{
local($log,$day_limit,$num_limit,%list)=@_;
$sounyu=0;
local(%include_i,%include_w);
@del_list=();
@un_del_list=();
$include_i{"$log\.cgi"}=1;
foreach(keys %list){
if($list{$_}=~/i/){$include_i{$_}=1;$sounyu=1;}
if($list{$_}=~/w/){$include_w{$_}=1;}
if($list{$_}=~/d/){
if(-f "$FORM{d}/$_"){push(@del_list,"$FORM{d}/$_");}
else{push(@un_del_list,"$FORM{d}/$_");}
}
}
local($mes);
if($sounyu){
if(!&h_conv_file($log,$day_limit,$num_limit,keys %include_i)){
foreach(keys %include_i){if($_ ne "$log\.cgi"){$mes.="$FORM{d}/$_<br>";}}
if($mes ne ''){&mes(905,$mes."��L�̃t�@�C����$FORM{d}/$log\.cgi�ɒǉ����܂����B");}
}
}else{
if(!&h_conv_file($log,$day_limit,$num_limit,keys %include_w)){
foreach(keys %include_w){$mes.="$FORM{d}/$_<br>";}
if($mes ne ''){&mes(906,$mes."��L�̃t�@�C����$FORM{d}/$log\.cgi�ɏ㏑���܂����B");}
}
}
&del_file(join('<br>',@del_list),@del_list);
}
#************************************************
# �o�b�N�A�b�v�t�@�C���̑�����s��
#************************************************
sub hst_file_backup{
local($log,%list)=@_;
local(%include_w,$mes);
@del_list=();
$file_time=0;
foreach(keys %list){
if($list{$_}=~/w/){
if(-M "$FORM{d}/$_" > $file_time){$file_time = "$FORM{d}/$_";$include_w{$_}=1;}
}
if($list{$_}=~/d/){push(@del_list,"$FORM{d}/$_");}
}
if(!&s_conv_file($log,keys %include_w)){
foreach(keys %include_w){$mes.="$FORM{d}/$_<br>";}
if($mes ne ''){&mes(907,$mes."��L�̃t�@�C����$FORM{d}/$log\.cgi�ɏ㏑���܂����B");}
}
&del_file(join('<br>',@del_list),@del_list);
}
#************************************************
# �o�b�N�A�b�v�t�@�C���̑�����s��
#************************************************
sub mondai_file_backup{
local(%list)=@_;
local(%include_w,$mes,$include_w);
@del_list=();
$file_time=0;
foreach(keys %list){
if($list{$_}=~/w/){
if(-M "$FORM{d}/$_" > $file_time){$file_time = "$FORM{d}/$_";$include_w=$_;}
}
if($list{$_}=~/d/){push(@del_list,"$FORM{d}/$_");}
}
if($include_w ne ''){
open(DB,"$FORM{d}/$include_w");@list=<DB>;close(DB);
if(! &write_file("$FORM{d}/$mondai_$FORM{d}.cgi",@list)){
&mes(908,"$FORM{d}/$include_w<br>��L�̃t�@�C����$FORM{d}/$mondai_$FORM{d}.cgi�ɏ㏑���܂����B");
}
&list_genre_html($FORM{d});
}
&del_file(join('<br>',@del_list),@del_list);
}
#************************************************
# �o�b�N�A�b�v�t�@�C���̑�����s��
#************************************************
sub quiz_file_backup{
local(%list)=@_;
local(%include_w,$mes,$include_w);
@del_list=();
$file_time=0;
foreach(keys %list){
if($list{$_}=~/w/){
if(-M "$FORM{d}/$_" > $file_time){$file_time = "$FORM{d}/$_";$include_w=$_;}
}
if($list{$_}=~/d/){push(@del_list,"$FORM{d}/$_");}
}
if($include_w ne ''){
open(DB,"$FORM{d}/$include_w");@list=<DB>;close(DB);
$i=0;$j=0;
if($list[0]=~ /^ver2/){
for($i=1;$i<=$#list;){
$list[$i]=~ s/\n//g;
$list[$i+1]=~ s/\n//g;
if(&write_file("$FORM{d}/$quiz_header$j\.cgi","$list[$i]\n$list[$i+1]")){return;}
$i=$i+2;$j++;
}
}else{
foreach(@list){
$_=~ s/\n//g;
if(&write_file("$FORM{d}/$quiz_header$i\.cgi",$_)){return;}
$i++;
}
}
&mes(909,"$FORM{d}/$include_w<br>��L�̃t�@�C����$FORM{d}/$quiz_header??\.cgi�ɏ㏑���܂����B");
}
&del_file(join('<br>',@del_list),@del_list);
}
#************************************************
# �t�@�C���̃o�b�N�A�b�v�̕���
#************************************************
sub s_conv_file{
local($log,@files)=@_;
local($max,$file);$max=0;
foreach(@files){
open(DB,"$FORM{d}/$_");@list=<DB>;close(DB);
if($list[0]=~ /^date([\d]+)/){
if($max < $1){$max = $1;$file=$_;}
}
}
if($file ne ''){
open(DB,"$FORM{d}/$file");@list=<DB>;close(DB);
return &write_file("$FORM{d}/$log\.cgi",@list);
}else{return 0;}
}
