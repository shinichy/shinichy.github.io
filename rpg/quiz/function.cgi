#!/usr/bin/perl
$version='2.03';
#************************************************
# �ϐ������ݒ�
#************************************************
sub setup{
$mod_cgi='0705';#CGI�X�N���v�g�t�@�C���̃p�[�~�b�V����
$mod_dat='0600';#�f�[�^�t�@�C���̃p�[�~�b�V����
$mod_dir='0701';#�f�B���N�g���̃p�[�~�b�V����
if($ENV{'HTTP_X_JPHONE_MSNAME'} ne ''){$imode=1;}
elsif($ENV{'HTTP_USER_AGENT'} =~ /J-PHONE/){$imode=1;}
elsif($ENV{'HTTP_USER_AGENT'} =~ /DoCoMo/){$imode=1;}
else{$imode=0;}
$header='log';
$quiz_header='qu';
$mondai_='mondai_';
$mes_='mes_';
$high1_='high1_';
$hst1_='hst1_';
$high2_='high2_';
$hst2_='hst2_';
$id= $ENV{'REMOTE_HOST'};
$ip= $ENV{'REMOTE_HOST'};
if($id = ''){
$id=$ENV{'REMOTE_ADDR'};
$ip=$ENV{'REMOTE_ADDR'};
}
$sys_color='#dfdfff';
$sys_color2='#ddffdd';
$border='3';
$sys_tbl_opt='border=3 width=80% cellspacing=1 cellpadding=2';
$method='get';
$time_lag=0;
$max_en=30;
$max_com=100;
$graph_w=300;
$graph_h=10;
$now= time();
$high_i=5;
$genre_cgi='genre.cgi';
$design_cgi='design.cgi';
$sysdesign_cgi='sysdesign.cgi';
$pass_cgi='pass.cgi';
$system_cgi='system.cgi';
$contribute_cgi='contribute.cgi';
$quiz_op_cgi='quiz_op.cgi';
$quiz_cgi='quiz.cgi';
$function_cgi='function.cgi';
$index_cgi='index.cgi';
$data_dir='data';
$file_lock='file.lock';
$count_file='count_file';
$guard_cgi='guard.cgi';
$_try='����';
$_underconst='�H����';
$_high='�����ю�';
$_graph='���ѕ��z';
$_score='�o���';
$_add='��蓊�e';
$_imode='�g�ѐ�p';
$_op='�Ǘ��l��';
$_top='TOP';
}
#************************************************
# �p�X���[�h�̃`�F�b�N
#************************************************
sub ch_pwd{
local($pass)=@_;
open(DB,$pass_cgi);@line=<DB>;close(DB);
$line[0]=~ s/\n//g;
if(crypt($pass,"ARRAY(0xb74f5c)") ne $line[0]){return 1;}
else{return 0;}
}
#************************************************
# �A�h���X�`�F�b�N�֐�
# ��������A�S�����̐�����Ԃ��܂��B
#************************************************
sub ch_address {
local($key)=@_;
local($sin,$r);
$sin=sin($key*$LOG{seed}*10);
if($sin<0){$sin=-$sin;}
$r=int(9999*$sin);
if($r<10){$r="000$r";}
elsif($r<100){$r="00$r";}
elsif($r<1000){$r="0$r";}
return $r;
}
#************************************************
# �N�C�Y�������֐�
#************************************************
sub refresh_quiz{
(@mondai,@ans,@misans1,@misans2,@misans3,@misans4,@anscom,@misanscom,@cf,@digest,@misanscom1,@misanscom2,@misanscom3,@misanscom4,@anstype,@author)=();
}
#************************************************
# �t�@�C���T�C�Y��Ԃ�(kb)
#************************************************
sub file_size_kb{
local($file_name)=@_;
local($mon_size)=-s $file_name;
local($mon_size2)=int($mon_size/1024);
if(0 < $mon_size % 1024){$mon_size2++;}
return $mon_size2;
}
#************************************************
# system.dat��V�K�쐬����
#************************************************
sub make_new_system_dat{
&def_sys;
return &write_system_dat;
}
#************************************************
# �N�C�Y�Ŏg�p����W���������X�g�𐶐�����
#************************************************
sub get_genre_dir_use{
if($mondai_cgi =~ /\//){
@mondai_dat=split(/\t/,$mondai_cgi);
foreach(@mondai_dat){
local($dir,$val)=split(/\//,$_);
push(@genre_dir_use,$dir);
if($val eq 'all'){$val ='-1';}
$genre_num{$dir}=$val;
}
}else{
push(@genre_dir_use,$FORM{d});
$genre_num{$FORM{d}}=$quiz_max;
}
}
#************************************************
# ���ԍ�����A�W�����������擾����
#************************************************
sub get_question_dir{
local($num)=@_;
local($count);
foreach $genre(@genre_dir_use){
$count = $count + $genre_num{$genre};
if($num < $count){
return $genre;
}
}
}
#************************************************
# MAX�œK���֐�
#************************************************
sub max_set{
if($quiz_max eq ''){$quiz_max = $#mondai+1;}
elsif($quiz_max > $#mondai+1){$quiz_max = $#mondai+1;}
if($play_max eq ''){$play_max = $quiz_max;}
elsif($play_max > $quiz_max){$play_max = $quiz_max;}
if($lose_max eq ''){$lose_max = $play_max;}
elsif($lose_max > $play_max){$lose_max = $play_max;}
}
#************************************************
# html�o�͗p�Ɉ����P��ϊ��������Q�Ɋi�[
#************************************************
sub conv_for_html{
$_[0]=$_[1];
$_[0]=~ s/</&lt;/g;
$_[0]=~ s/>/&gt;/g;
$_[0]=~ s/"/&quot;/g;
@_;
}
#************************************************
# html�o�͗p��%FORM��ϊ���%FORM2�Ɋi�[
#************************************************
sub form_to_form2{
foreach $pal(@_){&conv_for_html($FORM2{$pal},$FORM{$pal});}
}
#************************************************
# ���s�^�O�����s�ɕϊ���%FORM3�Ɋi�[
#************************************************
sub form_to_form3{
foreach $pal(@_){
$FORM3{$pal}=$FORM{$pal};
$FORM3{$pal}=~ s/<br>/\n/g;
&conv_for_html($FORM3{$pal},$FORM3{$pal});
}
}
#************************************************
# ���s�����s�^�O�ɕϊ���%FORM4�Ɋi�[
#************************************************
sub form_to_form4{
foreach $pal(@_){
$FORM4{$pal}=$FORM{$pal};
$FORM4{$pal}=~ s/\n/<br>/g;
}
}
#************************************************
# ���s���폜��%FORM5�Ɋi�[
#************************************************
sub form_to_form5{
foreach $pal(@_){
$FORM5{$pal}=$FORM{$pal};
$FORM5{$pal}=~ s/\n//g;
}
}
#************************************************
# FORM����̓��͒l�̃o���G�[�V�����t�H�[�}�b�g�̍쐬
#************************************************
sub form_to_form{
foreach(keys %FORM){
&form_to_form2($_);
&form_to_form3($_);
&form_to_form4($_);
}
}
#************************************************
# FORM�ϐ����N���A
#************************************************
sub clear_form{
foreach $pal(@_){
($FORM{$pal},$FORM2{$pal},$FORM3{$pal},$FORM4{$pal})=();
}
}
#************************************************
# �t�@�C���ւ̏�������
#************************************************
sub write_file{
local($file_name,@value)=@_;
local($opt);
if($file_name =~ /^(>)(.*)$/){$opt=$1;$file_name=$2;}
local($exist)=-f $file_name;
local($edit)=-M $file_name;
open(DB,">$opt$file_name");print DB @value;close(DB);
chmod(oct($mod_dat),$file_name);
if(!(-f $file_name)){
&error(731,$file_name);
return 1;
}elsif(!($exist)){
&mes(450,$file_name);
}elsif((-M $file_name eq $edit)&&($edit > 0)){
&error(741,$file_name);
return 1;
}
return 0;
}
#************************************************
# �����\�L�֐�
#************************************************
sub time_set{
local($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($_[0]+$time_lag);
$month = ($mon + 1);
$year=$year+1900;
if ($sec < 10)  { $sec = "0$sec";   }
if ($min < 10)  { $min = "0$min";   }
if ($hour < 10) { $hour = "0$hour"; }
if ($mday < 10) { $mday = "0$mday"; }
if ($month < 10) { $month = "0$month"; }
if($year<10){$year="0$year";}
return "[$year/$month/$mday $hour'$min\"$sec]";
}
#************************************************
# �X�R�A�p�����\�L�֐�
#************************************************
sub score_time{
local($hour,$min,$sec);
$hour=int($_[0]/60/60);
$min=int($_[0]/60);
$sec=($_[0])%60;
$min='0' x (2-length($min)) .$min;
$sec='0' x (2-length($sec)) .$sec;
return ($sec,$min,$hour);
}
#************************************************
# �p�[�~�b�V�����\������
#************************************************
sub permition {
local(@permit)=('---','--x','-w-','-wx','r--','r-x','rw-','rwx');
return "\($permit[substr($_,length($_[0])-3,1)]$permit[substr($_,length($_[0])-2,1)]$permit[substr($_,length($_[0])-1,1)]\)";
}
#************************************************
# �t�H�[�J�X�ړ��X�N���v�g����
#************************************************
sub focus_move {
local($field)=@_;
$ret=<<"_HTML_";
<script language=javascript>
//<!--
document.frm.${field}.focus();
//-->
</script>
_HTML_
}
#************************************************
# ���b�Z�[�W�\������
#************************************************
sub mes {
$mesno="�@ message($_[0])";
if (!($_[0] =~ /^\d+$/)){
$system_mes .= $_[0];
$mesno='';
}elsif ($_[0] <= 149) {
$system_mes .= "$_[1]�̐V�K�쐬������ɏI�����܂����B";
}elsif ($_[0] <= 199) {
$system_mes .= "$_[1]�̒ǉ�������ɏI�����܂����B";
}elsif ($_[0] <= 249) {
$system_mes .= "$_[1]�̕ҏW������ɏI�����܂����B";
}elsif ($_[0] <= 299) {
$system_mes .= "$_[1]�̍폜�A�����ύX������ɏI�����܂����B";
}elsif ($_[0] <= 349) {
$system_mes .= "$_[1]�̍폜������ɏI�����܂����B";
}elsif ($_[0] <= 399) {
$system_mes .= "$_[1]�̈ꊇ�ǉ�������ɏI�����܂����B";
}elsif ($_[0] <= 449) {
$system_mes .= "$_[1]�̏����ύX������ɏI�����܂����B";
}elsif ($_[0] <= 499) {
$system_mes .= "$_[1]�̎����쐬������ɏI�����܂����B";
}elsif ($_[0] <= 549) {
$system_mes .= "$_[1]����t�@�C���ɒǉ����܂����B";
}elsif ($_[0] <= 599) {
$system_mes .= "$_[1]����t�@�C���ɒǉ����܂����B";
}elsif ($_[0] <= 649) {
$system_mes .= "$_[1]�̈ꊇ�ǉ�������ɏI�����܂����B";
}elsif ($_[0] <= 699) {
$system_mes .= "$_[1]�̈ꊇ�ǉ�������ɏI�����܂����B";
}elsif ($_[0] <= 749) {
$system_mes .= "$_[1]�̈ꊇ�ǉ�������ɏI�����܂����B";
}elsif ($_[0] <= 999) {
$system_mes .= "$_[1]";
}
$system_mes .="$mesno<br><br>";
}
#************************************************
# ���b�Z�[�W�\������
#************************************************
sub mes_html {
if($system_mes ne ''){
return <<"_HTML_";
<table $sys_tbl_opt bgcolor="#eeeeaa"><tr><td>
<center><big><b>�������V�X�e�����b�Z�[�W������<br></b><big><br>
<table border=0><tr><td><span><b>$system_mes</b></span></td></tr></table>
</center>
</td></tr></table><br>
_HTML_
}
}
#************************************************
# �����_�ʓ���֐�
#************************************************
sub point {
local($num,$point)=@_;
local($over,$under)=split(/\./,$num);
$under=substr($under,0,$point);
$under=$under . '0' x ($point - length($under));
return "$over.$under";
}
#************************************************
# �t�b�^�\������
#_HTML_��_HTML_�Ƃ̂�������
#�N�C�Y�̃y�[�W�̃t�b�^�[������HTML���L�����Ă��������B
#���ʂ�HTML�\�L�ł��܂��܂���B
#���̍ہA���쌠�\�L�͏����Ȃ��ł��������B
#************************************************
sub footer_html {
$footer_html = <<"_HTML_";
<hr width="100%"><div align=right><span>
<a href="http://ha1.seikyou.ne.jp/home/jun/" target="_parent">qqq systems Ver$version</a></span>
</div></body></html>
_HTML_
}
#************************************************
# �o��󋵕\������
#************************************************
sub rec_html {
local(@line);
local($type)=@_;
if($type eq 'op'){$cgi_file=$quiz_op_cgi;}
else{$cgi_file=$quiz_cgi;}
($QU_ALL{play_win},$QU_ALL{play_num})=(0,0);
if($type eq 'op'){
&refresh_quiz();
&get_genre_dir_use();
&quiz_read_all();
&max_set();
}
if($quiz_max < 1){
&error(692);
return;
}
if($type eq 'op'){
$td=" bgcolor='$sys_color'";
$th=" bgcolor='$sys_color'";
$opt=$sys_tbl_opt;
$bdc=$td_color;
}else{
$td=" bgcolor='$td_color'";
$th=" bgcolor='$th_color'";
$opt=$tbl_opt;
$bdc=$border_color;
}
for($quiz_index=0;$quiz_index<$quiz_max;$quiz_index++){
&quiz_log_read();
my($mondai_str);
if($show_auth eq 0){
$mondai_str=$mondai[$quiz_index];
}elsif($author[$quiz_index] ne ''){
$mondai_str=$mondai[$quiz_index]."<div align=right>by $author[$quiz_index]</div>";
}
@mon_name=('����','�듚�P','�듚�Q','�듚�R','�듚�S');
if($FORM{item} eq 'list'){
$per[int($QU{win_ratio}/5)]++;
}elsif($type eq 'op'){
$dumy=$quiz_index+1;
$value=<<"_HTML_";
<table width="80%"border=0 cellpadding=0 cellspacing=0 bgcolor="$bdc"><tr><td>
<table $opt>
<tr><td$td colspan=4>
�p$dumy\�D$mondai_str
</td></tr>
<tr><td$td colspan=4>
$QU{play_num}�l��$QU{play_win}�l�����@�������� $QU{ave2}�b
_HTML_
local(@ans_list)=($ans[$quiz_index],$misans1[$quiz_index],$misans2[$quiz_index],$misans3[$quiz_index],$misans4[$quiz_index]);
for($i=0;$i<5;$i++){
$qu[$i]=$qu[$i]+0;
if($QU{play_num} > 0){
$per=&point($qu[$i]*100/$QU{play_num},1);
}else{
$per='0.0';
}
if($ans_list[$i] ne ''){
$value=$value."<tr><td$td nowrap>$mon_name[$i]</td><td$td nowrap>$qu[$i]�l</td><td$td nowrap>$per��</td><td$td width=100%>$ans_list[$i]</td></tr>\n"
}
}
if($anstype[$quiz_index] > 0){
local($qu_else)=$QU{play_num};
foreach(@qu){
$qu_else=$qu_else - $_;
if($QU{play_num} > 0){
$per=&point($qu_else*100/$QU{play_num},1);
}else{
$per='0.0';
}
}
$value=$value."<tr><td$td nowrap>�듚(���̑�)</td><td$td nowrap>$qu_else�l</td><td$td nowrap>$per��</td><td$td width=100%>�@</td></tr>\n"
}
$value=$value.'</table></td></tr></table><br>';
}else{
$dumy=$quiz_index+1;
if($show_digest eq 1){
$mon_digest=$digest[$quiz_index];
}else{
$mon_digest=$mondai_str
}
if($mon_digest eq ''){
$mon_digest='------';
}
if($#genre_dir_use > 1){
$genre_name="<td nowrap bgcolor='$td_color'>$title{&get_question_dir($quiz_index)}</td>";
}else{
$genre_name='';
}
$value=<<"_HTML_";
<tr>
<td bgcolor='$td_color' nowrap>�p$dumy�D</td>
<td bgcolor='$td_color' nowrap>$QU{play_num}�l��$QU{play_win}�l����</td>
<td bgcolor='$td_color' nowrap>$QU{win_ratio}��</td>
<td bgcolor='$td_color' nowrap>$QU{ave2}�b</td>
<td bgcolor='$td_color' nowrap>$author[$quiz_index]</td>
<td bgcolor='$td_color' nowrap>$mon_digest</td>
$genre_name
</tr>
_HTML_
}
$QU_ALL{play_num}=$QU_ALL{play_num}+$QU{play_num};
$QU_ALL{play_win}=$QU_ALL{play_win}+$QU{play_win};
$QU_ALL{ave_sum} =$QU_ALL{ave_sum}+$QU{ave}*$QU{play_win};
push(@line,$value);
if($FORM{item} eq 'num'){
push(@sort,"$QU{play_num}\t$quiz_index");
}elsif($FORM{item} eq 'aper'){
push(@sort,"$QU{win_ratio}\t$quiz_index");
}elsif($FORM{item} eq 'time'){
push(@sort,"$QU{ave2}\t$quiz_index");
}elsif($FORM{item} eq 'auth'){
push(@sort,"$author[$quiz_index] \t$quiz_index");
}else{
push(@sort,"$quiz_index\t$quiz_index");
}
}
if($QU_ALL{play_win} > 0){
$QU_ALL{ave2}=&point($QU_ALL{ave_sum}/$QU_ALL{play_win},2);
}else{$QU_ALL{ave2}='0.00';}
if($QU_ALL{play_num} > 0){
$QU_ALL{win_ratio}=&point($QU_ALL{play_win}*100/$QU_ALL{play_num},2);
}else{
$QU_ALL{win_ratio}='0.00';
}
$QU_ALL{play_lose}=$QU_ALL{play_num}-$QU_ALL{play_win};
$FORM{"item-$FORM{item}"}=' selected';
$FORM{"sort-$FORM{sort}"}=' selected';
$main_html=<<"_HTML_";
<br><span><b>��$_score���</b></span>
$align1
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$bdc"><tr><td>
<table $opt>
<tr><td$th><small>����萔</small></td>
<td$td width=100%><small>$walign1$quiz_max��$walign2</small></td></tr>
<tr><td$th><small>���o���</small></td>
<td$td><small>$walign1$QU_ALL{play_num}��$walign2</small></td></tr>
<tr><td$th><small>��������</small></td>
<td$td><small>$walign1$QU_ALL{play_win}��$walign2</small></td></tr>
<tr><td$th nowrap><small>���ϐ�������</small></td>
<td$td><small>$walign1$QU_ALL{ave2}�b$walign2</small></td></tr>
<tr><td$th><small>������</small></td>
<td$td><small>$walign1$QU_ALL{win_ratio}��$walign2</small></td></tr></table>
</td></tr></table>
<form action="$cgi_file" method="$method">
_HTML_
if($type eq 'op'){
$main_html.=<<"_HTML_";
<input type=hidden name=passch value="$FORM2{passch}">
<input type=hidden name=menu value=1>
<input type=hidden name=type value=score>
_HTML_
}else{
$main_html.='<input type=hidden name=s value=1>';
if($FORM{passch} ne ''){
$main_html.="<input type=hidden name=passch value='$FORM2{passch}'>";
}
}
$main_html.=<<"_HTML_";
<input type=hidden name=d value="$FORM{d}">
<table border=0 cellpadding=0 cellspacing=0 bgcolor="$bdc"><tr><td>
<table $opt>
<tr>
<td$td><select name=item>
<option value=mon$FORM{'item-mon'}>���ԍ���
<option value=num$FORM{'item-num'}>�o�萔��
<option value=aper$FORM{'item-aper'}>���𗦏�
<option value=time$FORM{'item-time'}>�������ԏ�
<option value=list$FORM{'item-list'}>���𗦕��z
<option value=auth$FORM{'item-auth'}>�쐬��
</select></td>
<td$td><select name=sort>
<option value=up$FORM{'sort-up'}>����
<option value=down$FORM{'sort-down'}>�~��
</select></td>
<td$td>
<input type=submit value=�\\��>
</td></tr></table></td></tr></table></form><hr>
_HTML_
if($FORM{sort} eq 'down'){
if($FORM{item} eq 'auth'){
@sort=sort {$b cmp $a} @sort;
}else{@sort=sort {$b <=> $a} @sort;}
}else{
if($FORM{item} eq 'auth'){
@sort=sort {$a cmp $b} @sort;
}else{@sort=sort {$a <=> $b} @sort;}
}
if($#genre_dir_use > 1){$genre_name="<td nowrap bgcolor='$th_color'>�W������</td>";}
else{$genre_name='';}
if($FORM{item} eq 'list'){
$main_html.='�����𗦕��z��';
$main_html.="<table width='80%'border=0 cellpadding=0 cellspacing=0 bgcolor='$bdc'><tr><td><table $opt>";
$max=0;$sum=0;
for($i=0;$i<=20;$i++){
$sum=$sum+$per[$i];
if($max < $per[$i]){$max=$per[$i];}
}
for($i=0;$i<=20;$i++){
$per[$i]=$per[$i]+0;
if($max > 0){
$rate=&point($per[$i]/$sum*100,1);
$width=int($per[$i]/$max*$graph_w);
}else{$rate=0.0;$width=1;}
if($width < 1){$width=1;}
$from=$i*5;$to=$i*5+5;
if($i<20){
$main_html.="<tr><td$th nowrap>$from\%-$to\%</td><td$td nowrap><img src='$SYS{b_gif}' width='$width' height='$graph_h'> $per[$i]��\($rate��\)</td></tr>";
}else{
$main_html.="<tr><td$th nowrap>$from\%</td><td$td nowrap><img src='$SYS{b_gif}' width='$width' height='$graph_h'> $per[$i]��\($rate��\)</td></tr>";
}
}
$main_html.='</table></td></tr></table>';
}elsif($type ne 'op'){
$main_html.=<<"_HTML_";
<table width="80%"border=0 cellpadding=0 cellspacing=0 bgcolor="$bdc"><tr><td>
<table $opt><tr>
<td nowrap bgcolor="$th_color">���ԍ�</td>
<td nowrap bgcolor="$th_color">����</td>
<td nowrap bgcolor="$th_color">����</td>
<td nowrap bgcolor="$th_color">��������</td>
<td nowrap bgcolor="$th_color">�쐬��</td>
<td nowrap bgcolor="$th_color">�����e</td>
$genre_name
</tr>
_HTML_
}
foreach(@sort){
($dum,$num)=split(/\t/,$_);
$main_html.= $line[$num];
}
if($type ne 'op'){$main_html.='</table></td></tr></table>';}
$main_html.= "$align2\n";
}
#************************************************
# �����̂����ő吔��Ԃ��B
#************************************************
sub max{
local(@list)=@_;
local($max);$max=$list[0];
foreach(@list[1..$#list]){if($max < $_){$max = $_;}}
return $max;
}
#************************************************
# �����̂����ő吔��Ԃ��B
#************************************************
sub mygrep{
local($item);
local($sorce,@list)=@_;
foreach $item(@list){
if($sorce eq $item){return 1;}
}
return 0;
}
#************************************************
# �G���[�\������
#************************************************
sub error {
local($errno);
$errno="�@ error($_[0])";
if (!($_[0] =~ /^\d+$/)){
$error_mes .= $_[0];
$errno='';
}elsif ($_[0] <= 199) {
$error_mes .= "$_[1]���s���ł��B";
}elsif ($_[0] <= 299) {
$error_mes .= "$_[1]�����͂���Ă��܂���";
}elsif ($_[0] <= 399) {
$error_mes .= "$_[1]���s���ł��B���p��������͂��Ă�������";
}elsif ($_[0] <= 499) {
$error_mes .= "$_[1]���������I������Ă��܂���";
}elsif ($_[0] <= 509) {
$error_mes .= "$_[1]�͔��p��$max_en�����܂łł��B<br>$_[1]���������܂��B<br>�o�^�ł��܂���ł����B";
}elsif ($_[0] <= 519) {
$error_mes .= "$_[1]�͔��p��$max_com�����܂łł��B<br>$_[1]���������܂��B<br>�o�^�ł��܂���ł����B";
}elsif ($_[0] <= 529) {
$error_mes .= "$_[1]���������܂��B<br>���p20�����ȓ��œ��͂��ĉ������B";
}elsif ($_[0] <= 539) {
$error_mes .= "$_[1]���͈͊O�ł��B";
}elsif ($_[0] <= 549) {
$error_mes .= "$_[1]����v���܂���B<br>�ē��͂��Ă��������B";
}elsif ($_[0] <= 609) {
$error_mes .= '����������\��������܂��B����ɏ�������܂���ł����B<br><br>�Ȃ��A�Ǘ��҂���Ƃ��s���Ă����\��������܂��B���΂炭���Ă��烊���[�h���Ă݂ĉ������B';
}elsif ($_[0] <= 619) {
$error_mes .= '���̃W�������ł́A��葽���̕��ɓo�^���Ă����������߂ɁA<br>����IP�A�h���X�ɂ�铯��X�R�A�̓o�^�͏o���܂���B';
}elsif ($_[0] <= 629) {
$error_mes .= "���̃n�C�X�R�A�́A���$num_limit�l���̃X�R�A���L�^���Ă��܂��B<br>�c�O�Ȃ��炱�̋L�^�͓o�^�ł��܂���ł����B";
}elsif ($_[0] <= 639) {
$error_mes .= '���łɂ��̋L�^�͓o�^����Ă��܂��B�o�^�o���܂���ł����B';
}elsif ($_[0] <= 649) {
$error_mes .= '���̃N�C�Y�́A�����ю҂�o�^�ł��܂���B';
}elsif ($_[0] <= 659) {
$error_mes .= "���̃N�C�Y�͌���$_underconst�ł��B\n�܂��̂����������҂����Ă��܂��B";
}elsif ($_[0] <= 669) {
$error_mes .= "���ݓ����v���C�l�����x$SYS{max_player}�l���v���C���ł��B<br>���΂炭���Ă��炨�z�����������B";
}elsif ($_[0] <= 679) {
$error_mes .= '�o�^���ꂽ��肪����܂���B<br><br>���΂炭���Ă���A�܂����z�����������B';
}elsif ($_[0] <= 689) {
$error_mes .= '�N�C�Y�̃W���������o�^����Ă��܂���B';
}elsif ($_[0] <= 699) {
$error_mes .= '���̃W�������́A��肪���o�^�ł��B';
}elsif ($_[0] <= 709) {
$error_mes .= '���̃W�������́A���t�@�C��������܂���B';
}elsif ($_[0] <= 719) {
$error_mes .= '�V�X�e���t�@�C���̓ǂݍ��݂Ɏ��s���܂����B<br>�Ǘ��҂ɂ��₢���킹�������B';
}elsif ($_[0] <= 729) {
$error_mes .= '�W�������t�@�C���̓ǂݍ��݂Ɏ��s���܂����B<br>�Ǘ��҂ɂ��₢���킹�������B';
}elsif ($_[0] <= 739) {
local($permition);
$permition=&permition($mod_dir);
$error_mes .="$_[1]�������쐬�ł��܂���ł����B<br>�{�v���O������ݒu���Ă���f�B���N�g���̃p�[�e�B�V������<br>$mod_dir$permition�ɂ��Ă��������B<br>�Ȃ��A�v���o�C�_�̊֌W��p�[�~�b�V�����ɐ���������A<br>���̃G���[����������ꍇ�́A<br>FTP���g���蓮��$_[0]���쐬���ĉ������B";
}elsif ($_[0] <= 749) {
local($permition);
$permition=&permition($mod_dat);
$error_mes .="$_[1]�ɏ������݂��ł��܂���ł����B<br>�t�@�C���̃p�[�e�B�V������<br>$mod_dat$permition�ɂ��Ă��������B";
}elsif ($_[0] <= 759) {
$error_mes .= '���̃W�������́A���̓��e���ł��܂���B';
}elsif ($_[0] <= 769) {
$error_mes .= '���݁A�����ю҂͓o�^����Ă��܂���B';
}elsif ($_[0] <= 779) {
$error_mes .= "$_[1]�͂��łɓo�^����Ă��܂��B";
}elsif ($_[0] <= 809) {
$error_mes .= "$_[1]�����݂��܂���B";
}elsif ($_[0] <= 819) {
$error_mes .= "$_[1]�����݂��܂���B�t�@�C���\\�����m�F���Ă��������B";
}elsif ($_[0] <= 829) {
$error_mes .= "$_[1]�͋�ł�";
}elsif ($_[0] <= 839) {
$error_mes .= "$_[1]�͌��ݎg�p���ł��B<br>�폜�ł��܂���ł����B";
}elsif ($_[0] <= 849) {
$error_mes .= "$_[1]�͎g�p�ł��܂���B<br>�ʂ̃f�B���N�g��������͂��Ă��������B";
}elsif ($_[0] <= 859) {
$error_mes .= "$_[1]�͂��łɓo�^����Ă��܂��B<br>�ʂ̖��O����͂��Ă��������B";
}elsif ($_[0] <= 869) {
$error_mes .= "$_[1]�̃^�C���X�^���v���Ⴂ�܂��B<br>��ƒ��ɕύX���ꂽ���A��x���M���s�����\\��������܂��B<br>�������ύX����Ă��邩�m�F���Ă��������B";
}elsif ($_[0] <= 909) {
$error_mes .= '��肪�����o�^����܂���ł����B';
}elsif ($_[0] <= 919) {
$error_mes .= "$_[1]�s�ڂɃG���[������܂��B";
}elsif ($_[0] <= 929) {
$error_mes .= "$_[1]��ڂ̖�蕶������܂���B";
}elsif ($_[0] <= 939) {
$error_mes .= "$_[1]��ڂ̐���������܂���B";
}elsif ($_[0] <= 949) {
$error_mes .= "$_[1]��ڂ̌듚�P������܂���B";
}else {
$error_mes .= '�����ɉ��炩�̃G���[����������Ƃ͒��~����܂����B';
$errno='';
}
#$error_mes .="$errno<br><br>";
#open(DB,">>error.dat");
#print DB &time_set(time)."$error_mes\n";
#close(DB);
}
#************************************************
# �G���[�\������
#************************************************
sub error_html{
local($return,$color);
if($error_mes ne ''){
if($com_color eq ''){$color='#eeeebb';}
else{$color=$com_color;}
$return = <<"_HTML_";
<hr><br>
<table width="80%" border=0 cellpadding=0 cellspacing=0><tr><td>
<table $top_tbl_opt bgcolor="$color"><tr><td$nowrap>
<center><big><font color=#ff0000>���@���m�点�@��</font><br><br> </big>
<table border=0><tr><td><span><b>$error_mes</b></span></td></tr></table>
</center>
</td></tr></table>
</td></tr></table><br>
_HTML_
}
return $return;
}
#************************************************
# HTML�o��
#************************************************
sub output{
local($er);
$er=&error_html;
print"Content-type: text/html\n\n";
print <<"_HTML_";
$header_html
$align1
$er
$start_html
$test
$main_html
$align2
$midi_html
$footer_html
_HTML_
exit;
}
#************************************************
# HTML�o��(�g�їp)
#************************************************
sub output_i{
print "Content-type: text/html\n\n";
print <<"_HTML_";
$header_i_html
$error_mes
$start_i_html
$main_i_html
$footer_i_html
_HTML_
exit;
}
#************************************************
# �r�W�[�\��
#************************************************
sub busy_html{
$header_html=<<"_HTML_";
<html><head><title>�r�W�[</title></head><BODY bgcolor='$sys_color'>
<br><br><b>
���t�@�C����ǂݍ��߂܂���ł�����<br></b>
<br>
�Ǘ��l����ƒ��̉\\��������܂��B<br>
������x���̏�Ń����[�h���Ă��������B<br><br><br>
_HTML_
}
#************************************************
# �A�N�Z�X�����\��
#************************************************
sub guard_html{
$header_html=<<"_HTML_";
<html><head><title>�A�N�Z�X����</title></head><BODY bgcolor='$sys_color'>
<br><br><b>
���A�N�Z�X�ł��܂���ł�����<br></b>
<br>
���݁A�Ǘ��l�ɂ��A�N�Z�X�������������Ă���܂��B<br><br>
_HTML_
}
#************************************************
# �t�@�C�����b�N
#************************************************
sub file_lock{
open(DB,">$_[0]");
close(DB);
}
#************************************************
# �t�@�C���A�����b�N
#************************************************
sub file_unlock{
unlink "$_[0]";
}
#************************************************
# ���b�N��Ԃ��`�F�b�N�B
#************************************************
sub ch_lock{
local($file,$count)=@_;
while($count--){
if(-f $file){
if((-M $file)*60*60*24 < 60){sleep(1);}
else{return 0;}
}else{return 0;}
}
return 1;
}
#************************************************
# �Ǘ��l����ƒ��łȂ����Ƃ��`�F�b�N
#************************************************
sub ch_sys_lock{
return &ch_lock("$data_dir/$file_lock",10);
}
#************************************************
# �Ǘ��l��ƊJ�n�ɂ�郍�b�N
#************************************************
sub sys_lock{
return &file_lock("$data_dir/$file_lock");
}
#************************************************
# �Ǘ��l��ƏI���ɂ��A�����b�N
#************************************************
sub sys_unlock{
return &file_unlock("$data_dir/$file_lock");
}
#************************************************
# �n�C�X�R�A�t�@�C�����X�V���łȂ����Ƃ��`�F�b�N
#************************************************
sub ch_hist_lock{
local($dir_name)=@_;
return &ch_lock("$dir_name/$scorehst_cgi\.lock",10);
}
#************************************************
# �n�C�X�R�A�t�@�C���̍X�V�J�n�ɂ�郍�b�N
#************************************************
sub hist_lock{
local($dir_name)=@_;
return &file_lock("$dir_name/$scorehst_cgi\.lock");
}
#************************************************
# �n�C�X�R�A�t�@�C���̍X�V�I���ɂ��A�����b�N
#************************************************
sub hist_unlock{
local($dir_name)=@_;
return &file_unlock("$dir_name/$scorehst_cgi\.lock");
}
#************************************************
# �N�b�L�[����ǂݍ���
#************************************************
sub get_cookie{
local(@pairs,$pair,$name,$value);
if($imode){return;}
@pairs = split(/;/,$ENV{'HTTP_COOKIE'});
foreach $pair (@pairs) {
($name,$value) = split(/=/,$pair,2);
$name =~ s/ //g;
$DUMMY{$name} = $value;
}
@pairs = split(/,/,$DUMMY{$SYS{cookie}});
foreach $pair (@pairs) {
($name,$value) = split(/:/,$pair,2);
$COOKIE{$name} = $value;
}
}
#************************************************
# �N�b�L�[�֏�������
#************************************************
sub set_cookie{
if($imode){return;}
($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time + 90*24*60*60);
$y0='Sunday'; $y1='Monday'; $y2='Tuesday'; $y3='Wednesday'; $y4='Thursday'; $y5='Friday'; $y6='Saturday';
@youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6);
$m0='Jan'; $m1='Feb'; $m2='Mar'; $m3='Apr'; $m4='May'; $m5='Jun';
$m6='Jul'; $m7='Aug'; $m8='Sep'; $m9='Oct'; $m10='Nov'; $m11='Dec';
@monthg = ($m0,$m1,$m2,$m3,$m4,$m5,$m6,$m7,$m8,$m9,$m10,$m11);
$date_gmt = sprintf("%s\, %02d\-%s\-%04d %02d:%02d:%02d GMT",$youbi[$wdayg],$mdayg,$monthg[$mong],$yearg +1900,$hourg,$ming,$secg);
@data=();
foreach(sort{$a cmp $b} keys %COOKIE){
push(@data,"$_\:$COOKIE{$_}");
}
$data=join(',',@data);
print "Set-Cookie: $SYS{cookie}=$data; expires=$date_gmt\n";
}#���̃N�b�L�[�͂�������3�����ԗL���ł��B
#************************************************
# �t�@�C���̃o�b�N�A�b�v����
#************************************************
sub backup_file{
local($file,$write,$span)=@_;
local($backuptime)=&get_recent_backuptime($file,$write);
if($now - $backuptime > $span*60*60*24){
&copy_file($file,$write);
}
}
#************************************************
# �t�@�C���w�b�_�̍X�V�������X�V
#************************************************
sub renew_date{
local($file_name)=@_;
open(DB,"$file_name");local(@list)=<DB>;close(DB);
if($list[0]=~ /^date/){$list[0]='';}
&write_file($file_name,('date'.time."\n",@list));
}
#************************************************
# �o�b�N�A�b�v�t�@�C�����쐬
#************************************************
sub copy_file{
local($fromfile,$LOG{write})=@_;
local(@list,$tofile,$max);
$tofile=&buckup_filename($fromfile,$LOG{write},$update);
open(DB,"$fromfile");
@list=<DB>;
close(DB);
if($list[0] =~ /^date/){$list[0]='';}
if(&write_file($tofile,("date$now\n",@list))){return;}
return $tofile;
}
#************************************************
# �o�b�N�A�b�v�t�@�C������Ԃ�
#************************************************
sub buckup_filename{
local($fromfile,$write,$update)=@_;
local($head,$dir);
$max=0;
if($fromfile =~ /(.*)\/(.*)\.cgi$/){
$dir="$1/";
$head=$2;
}elsif($fromfile =~ /(.*)\.cgi$/){
$head=$1;
}
if($write){
return "${dir}${head}_bak.cgi";
}else{
opendir(DIR,$FORM{d});
local(@dir_files)=readdir(DIR);
close(DIR);
foreach $file(@dir_files){
if($file=~ /^${dir}${head}_bak(\d+).cgi/){
if($max < $1){$max=$1;}
}
}
$max++;
return "${dir}${head}_bak${max}.cgi";
}
}
#************************************************
# �ŐV�̃o�b�N�A�b�v�������擾����
#************************************************
sub get_recent_backuptime{
local($fromfile,$write,$update)=@_;
$max=0;
local($head,$dir,$backup_file);
if($fromfile =~ /(.*)\/(.*)\.cgi$/){
$dir="$1/";
$head=$2;
}elsif($fromfile =~ /(.*)\.cgi$/){
$head=$1;
}
if($write){
$backup_file = "${dir}${head}_bak.cgi";
}else{
opendir(DIR,$FORM{d});
local(@dir_files)=readdir(DIR);
close(DIR);
foreach $file(@dir_files){
if($file=~ /^${dir}${head}_bak(\d+).cgi/){
if($max < $1){$max=$1;}
}
}
$backup_file = "${dir}${head}_bak${max}.cgi";
}
open (DB,$backup_file);
local(@list)=<DB>;
close(DB);
if($list[0] =~ /^date(\d+)/){
return $1;
}else{
return 0;
}
}
#************************************************
# %SYS�ϐ��̏����l
#************************************************
sub def_sys{
$SYS{design}='�f�t�H���g�V�X�e���f�U�C��';
$SYS{limit}=10;
$SYS{max_player}=50;
$SYS{cookie}='QQQ';
$SYS{quiz_form}=2;
$SYS{main_title}='����';
$SYS{header}='<table cellspacing=0 cellpadding=0 width="100%"><tr>'
.'<td Valign=TOP><small>$top$quiz_op$imode</small></td>'
.'<td><div align=right><p><B><BIG>$title</BIG></B></p></div></td></tr></table>';
$SYS{sub_header}='<table cellspacing=0 cellpadding=0 width="100%"><tr>'
.'<td nowarap Valign=TOP><small>$index$challenge$high$graph$score$add</small></td>'
.'<td><div align=right><p><big><B>$genre</B>$sub_title<br> </big><br>'
.'<span>$mode</span></p></div></td></tr></table>';
$SYS{style}='BIG{font-size:12pt;}<br>'
.'SPAN{font-size:9pt;}<br>'
.'SMALL{font-size:8pt;}<br>'
.'BODY,TD{font-size:8pt;}';
$SYS{top_message}='';
$SYS{top_table}=1;
$SYS{top_url}='';
$SYS{easy}=0;
$SYS{'time'}='1';
$SYS{wrap}='0';
}
#************************************************
# %SYSDESIGN�ϐ��̏����l
#************************************************
sub def_sysdesign{
$SYSDESIGN{sysdesign_title}=$_[0];
$SYSDESIGN{top_wall}='';
$SYSDESIGN{top_back_color}='#ddffdd';
$SYSDESIGN{top_table_color}='#ffffdd';
$SYSDESIGN{top_genre_color}='#ffffdd';
$SYSDESIGN{top_info_color}='#cceeee';
$SYSDESIGN{top_com_color}='#ddffff';
$SYSDESIGN{top_high_color}='#ffdddd';
$SYSDESIGN{top_border_color}='#99ff99';
$SYSDESIGN{top_text_color}='#000000';
$SYSDESIGN{top_link_color}='#0000EE';
$SYSDESIGN{top_vlink_color}='#551A8B';
$SYSDESIGN{top_border_high}='1';
$SYSDESIGN{top_border}='2';
$SYSDESIGN{top_border_in}='1';
$SYSDESIGN{a_gif}='a.gif';
$SYSDESIGN{b_gif}='b.gif';
$SYSDESIGN{align}='c';
$SYSDESIGN{walign}='l';
}
#************************************************
# %GENRE�̏����ݒ�
#************************************************
sub def_genre {
$GENRE{design}='�f�t�H���g�W�������f�U�C��';
$GENRE{title}='����';
$GENRE{top_comment}='';
$GENRE{start_comment}='<center>$title�ɂ悤�����B���݁A����Ґ���$challenge�l�ł��B<br>'
.'�N�C�Y�̑���萔��$quiz_max��ŁA�o�萔��$play_max��ł����A<br>'
.'$lose_max��ԈႦ��ƃQ�[���I�[�o�[�ł��B<br>'
.'�Ȃ��������Ԃ�$time�b�ŁA������$high���ȏ�ō��i�ł��B<br>'
.'$champion�ō����іڎw���Ă���΂��Ă��������B</center>';
$GENRE{mondai_cgi}='';
$GENRE{mente}=0;
$GENRE{cont}=1;
$GENRE{notext}=0;
$GENRE{direct_cont}=0;
$GENRE{show_digest}=1;
$GENRE{show_auth}=1;
$GENRE{mode_name1}="���������탂�[�h";
$GENRE{show_ans1}=0;
$GENRE{random1}=1;
$GENRE{quiz_max1}='';
$GENRE{play_max1}='';
$GENRE{lose_max1}='3';
$GENRE{time_limit1}='60';
$GENRE{high_border1}=80;
$GENRE{high_back_day1}='0';
$GENRE{high_back_w1}='1';
$GENRE{scorehst_back_day1}='0';
$GENRE{scorehst_back_w1}='1';
$GENRE{graph_border1}=20;
$GENRE{histry_div1}=5;
$GENRE{day_limit1}='';
$GENRE{num_limit1}='';
$GENRE{no_limit1}='3';
$GENRE{rec_com1}='1';
$GENRE{double_high1}='1';
$GENRE{bundle1}='0';
$GENRE{mode_name2}="�Q�O�⃂�[�h";
$GENRE{show_ans2}=0;
$GENRE{random2}=1;
$GENRE{quiz_max2}='';
$GENRE{play_max2}='20';
$GENRE{lose_max2}='20';
$GENRE{time_limit2}='60';
$GENRE{high_border2}=80;
$GENRE{high_back_day2}='0';
$GENRE{high_back_w2}='1';
$GENRE{scorehst_back_day2}='0';
$GENRE{scorehst_back_w2}='1';
$GENRE{graph_border2}=40;
$GENRE{histry_div2}=2;
$GENRE{day_limit2}='';
$GENRE{num_limit2}='';
$GENRE{no_limit2}='3';
$GENRE{rec_com2}='1';
$GENRE{double_high2}='1';
$GENRE{bundle2}='0';
}
#************************************************
# %DESIGN�̏����ݒ�
#************************************************
sub def_design {
$DESIGN{design_title}=$_[0];
$DESIGN{text_color}='#000000';
$DESIGN{link_color}='#0000ee';
$DESIGN{vlink_color}='#551A8B';
$DESIGN{champ_color}='#ff0000';
$DESIGN{main_color}='#cccccc';
$DESIGN{win_color}='#ccccff';
$DESIGN{lose_color}='#ffcccc';
$DESIGN{com_color}='#eeeebb';
$DESIGN{th_color}='#bbeebb';
$DESIGN{td_color}='#ddffdd';
$DESIGN{border_color}='#ffdddd';
$DESIGN{border_high}='3';
$DESIGN{border}='1';
$DESIGN{border_in}='2';
$DESIGN{wall}='';
$DESIGN{win_wall}='';
$DESIGN{lose_wall}='';
$DESIGN{win_sign}='<font color="blue"><big><b>�����I</b></big></font>';
$DESIGN{lose_sign}='<font color="red"><big><b>�s�����I</b></big></font>';
$DESIGN{over_sign}='<font color="red"><big><b>���ԃI�[�o�[�I</b></big></font>';
$DESIGN{win_midi}='';
$DESIGN{lose_midi}='';
$DESIGN{end_midi}='';
$DESIGN{high_midi}='';
}
#************************************************
# �v���C���O�̏�����
#************************************************
sub def_log{
srand();
if($FORM{m} eq ''){$FORM{m}=1;}
$LOG{num}=0;
$LOG{win}=0;
$LOG{lose}=0;
$LOG{seed}=int(rand(1000)*100+1);
$LOG{old}=0;
$LOG{write}='';
$LOG{name}=$COOKIE{N};
$LOG{'time'}=$now;
$LOG{lap}=$now;
$LOG{last_lap}=0;
$LOG{genre}=$FORM{d};
$LOG{mode}=$FORM{m};
$LOG{ck_s}=$COOKIE{"S$FORM{m}$FORM{d}"};
$LOG{ck_n}=$COOKIE{N};
$LOG{bundle}=$bundle;
}
#************************************************
# �ݖ�ʐ���
#************************************************
sub def_qu{
@qu=();
$QU{play_num}=0;
$QU{play_win}=0;
$QU{ave}=0;
$QU{ave2}='0.00';
$QU{win_ratio}='0.0';
}
#************************************************
# �o�b�t�@��ϐ��ɓǂݍ���
#************************************************
sub buf_read {
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }
if($buffer ne ''){
@pairs = split(/&/,$buffer);
foreach $pair (@pairs){
local($name, $value) = split(/=/, $pair);
$value =~ tr/+/ /;
$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
if(($name ne 'newq')
&&($name ne 'qqu')
&&($name ne 'qas')
&&($name ne 'qmas1')
&&($name ne 'qmas2')
&&($name ne 'qmas3')
&&($name ne 'qmas4')
&&($name ne 'qac')
&&($name ne 'qmac')
&&($name ne 'qmac1')
&&($name ne 'qmac2')
&&($name ne 'qmac3')
&&($name ne 'qmac4')
&&($name ne 'qcf')
&&($name ne 'auth')
&&($name ne 'tc')
&&($name ne 'stc')
&&($name ne 'tmes')
&&($name ne 'stl-2')
&&($name ne 'iplist'))
{$value =~ s/\n//g;}
if($name eq 'EntryName' || $name eq 'com' ){
$value =~ s/</&lt;/g;
$value =~ s/>/&gt;/g;
}
$value =~ s/\t//g;
$value =~ s/\r//g;
&jcode'convert(*value,'sjis');
$FORM{$name} = $value;
&form_to_form2($name);
&form_to_form3($name);
&form_to_form4($name);
if($FORM{j} ne ''){$imode=1;}
if($name =~ /^type_(.*)/){
$FORM{type}=$1;
}
}
}
if($FORM2{passch} ne ''){
$formop_p="<input type=hidden name=passch value='$FORM2{passch}'>\n";
}
$formop_h="<form action='$quiz_op_cgi' method='$method' >\n$formop_p";
$formop_hb="<form action='$quiz_op_cgi' method='$method' target='_blank'>\n$formop_p";
$formop_nh="<form action='$quiz_op_cgi' method='$method' name=frm>\n$formop_p";
$formop_nhb="<form action='$quiz_op_cgi' method='$method' name=frm target='_blank'>\n$formop_p";
$form_d="<input type=hidden name=d value=$FORM{d}>";
$formop_hd="$formop_h$form_d";
$formop_nhd="$formop_nh$form_d";
if($FORM{m} eq ''){
$cid="1$FORM{d}";
}else{
$cid="$FORM{m}$FORM{d}";
}
if($buffer ne ''){
return 0;
}else{
return 1;
}
}
#************************************************
# �W���������t�@�C����S�W�������Ǘ��z��ɓǂݍ���
#************************************************
sub all_genre_read {
open(DB,$genre_cgi);@genres=<DB>;close(DB);
undef %GENRE;
@genre_dir_all=();
&def_genre();
if(($genres[0]=~ /^ver/)||($genres[0] eq '')||($genres[0] eq "\n")){
foreach $genre(@genres[1..$#genres]){
$genre=~ s/\n//g;
local($key,$val)=split(/\t/,$genre,2);
if($key eq 'dir'){
if($GENRE{dir}ne ''){&genre_to_genre_array;}
&def_genre($val);
}
$GENRE{$key}=$val;
}
if($GENRE{dir} ne ''){&genre_to_genre_array;}
}
}
#************************************************
# �f�U�C�����t�@�C����S�f�U�C���Ǘ��z��ɓǂݍ���
#************************************************
sub all_design_read {
open(DB,$design_cgi);@designs=<DB>;close(DB);
undef %DESIGN;
@design_list=();
&def_design();
if(($designs[0]=~ /^ver/)||($designs[0] eq '')||($designs[0] eq "\n")){
foreach $line(@designs[1..$#designs]){
$line=~ s/\n//g;
local($key,$val)=split(/\t/,$line,2);
if($key eq 'design_title'){
if($DESIGN{design_title}ne ''){&design_to_design_array;}
&def_design($val);
}
$DESIGN{$key}=$val;
}
if($DESIGN{design_title} ne ''){&design_to_design_array;}
}
&def_design();
}
#************************************************
# �V�X�e���f�U�C�����t�@�C����S�f�U�C���Ǘ��z��ɓǂݍ���
#************************************************
sub all_sysdesign_read {
open(DB,$sysdesign_cgi);@designs=<DB>;close(DB);
undef %SYSDESIGN;
@sysdesign_list=();
&def_sysdesign();
if(($designs[0]=~ /^ver/)||($designs[0] eq '')||($designs[0] eq "\n")){
foreach $line(@designs[1..$#designs]){
$line=~ s/\n//g;
local($key,$val)=split(/\t/,$line,2);
if($key eq 'sysdesign_title'){
if($SYSDESIGN{sysdesign_title}ne ''){&sysdesign_to_sysdesign_array;}
&def_sysdesign($val);
}
$SYSDESIGN{$key}=$val;
}
if($SYSDESIGN{sysdesign_title} ne ''){&sysdesign_to_sysdesign_array;}
}
&def_sysdesign();
}
#************************************************
# %GENRE���A�e�z��ϐ��ɓǂݍ���
#************************************************
sub genre_to_genre_array{
local($dir)=$GENRE{dir};
push(@genre_dir_all,$dir);
$design_use{$GENRE{design}}.="\t$dir";
$design{$dir}=$GENRE{design};
$title{$dir}=$GENRE{title};
$top_comment{$dir}=$GENRE{top_comment};
$start_comment{$dir}=$GENRE{start_comment};
$mondai_cgi{$dir}=$GENRE{mondai_cgi};
$mes_cgi{$dir}="$mes_$dir";
$mente{$dir}=$GENRE{mente};
$cont{$dir}=$GENRE{cont};
$notext{$dir}=$GENRE{notext};
$direct_cont{$dir}=$GENRE{direct_cont};
$show_digest{$dir}=$GENRE{show_digest};
$show_auth{$dir}=$GENRE{show_auth};
$mode_name1{$dir}=$GENRE{mode_name1};
$show_ans1{$dir}=$GENRE{show_ans1};
$random1{$dir}=$GENRE{random1};
$quiz_max1{$dir}=$GENRE{quiz_max1};
$play_max1{$dir}=$GENRE{play_max1};
$lose_max1{$dir}=$GENRE{lose_max1};
$time_limit1{$dir}=$GENRE{time_limit1};
$high_border1{$dir}=$GENRE{high_border1};
$high_cgi1{$dir}="$high1_$dir";
$high_back_day1{$dir}=$GENRE{high_back_day1};
$high_back_w1{$dir}=$GENRE{high_back_w1};
$scorehst_cgi1{$dir}="$hst1_$dir";
$scorehst_back_day1{$dir}=$GENRE{scorehst_back_day1};
$scorehst_back_w1{$dir}=$GENRE{scorehst_back_w1};
$graph_border1{$dir}=$GENRE{graph_border1};
$histry_div1{$dir}=$GENRE{histry_div1};
$day_limit1{$dir}=$GENRE{day_limit1};
$num_limit1{$dir}=$GENRE{num_limit1};
$no_limit1{$dir}=$GENRE{no_limit1};
$rec_com1{$dir}=$GENRE{rec_com1};
$double_high1{$dir}=$GENRE{double_high1};
$bundle1{$dir}=$GENRE{bundle1};
$mode_name2{$dir}=$GENRE{mode_name2};
$show_ans2{$dir}=$GENRE{show_ans2};
$random2{$dir}=$GENRE{random2};
$quiz_max2{$dir}=$GENRE{quiz_max2};
$play_max2{$dir}=$GENRE{play_max2};
$lose_max2{$dir}=$GENRE{lose_max2};
$time_limit2{$dir}=$GENRE{time_limit2};
$high_border2{$dir}=$GENRE{high_border2};
$high_cgi2{$dir}="$high2_$dir";
$high_back_day2{$dir}=$GENRE{high_back_day2};
$high_back_w2{$dir}=$GENRE{high_back_w2};
$scorehst_cgi2{$dir}="$hst2_$dir";
$scorehst_back_day2{$dir}=$GENRE{scorehst_back_day2};
$scorehst_back_w2{$dir}=$GENRE{scorehst_back_w2};
$graph_border2{$dir}=$GENRE{graph_border2};
$histry_div2{$dir}=$GENRE{histry_div2};
$day_limit2{$dir}=$GENRE{day_limit2};
$num_limit2{$dir}=$GENRE{num_limit2};
$no_limit2{$dir}=$GENRE{no_limit2};
$rec_com2{$dir}=$GENRE{rec_com2};
$double_high2{$dir}=$GENRE{double_high2};
$bundle2{$dir}=$GENRE{bundle2};
if(($mente{$dir} eq 1)&&($mondai_cgi{$dir} ne '.')&& !($mondai_cgi{$dir} =~ /\//)){
push(@genre_dir_orign,$dir);
}
if($mente{$dir} eq 1){
push(@genre_dir_available,$dir);
}
}
#************************************************
# %DESIGN���A�e�z��ϐ��ɓǂݍ���
#************************************************
sub design_to_design_array{
local($id)=$DESIGN{design_title};
push(@design_list,$id);
$design_title{$id}=$DESIGN{design_title};
$text_color{$id}=$DESIGN{text_color};
$link_color{$id}=$DESIGN{link_color};
$vlink_color{$id}=$DESIGN{vlink_color};
$champ_color{$id}=$DESIGN{champ_color};
$main_color{$id}=$DESIGN{main_color};
$win_color{$id}=$DESIGN{win_color};
$lose_color{$id}=$DESIGN{lose_color};
$com_color{$id}=$DESIGN{com_color};
$th_color{$id}=$DESIGN{th_color};
$td_color{$id}=$DESIGN{td_color};
$border_color{$id}=$DESIGN{border_color};
$border_high{$id}=$DESIGN{border_high};
$border{$id}=$DESIGN{border};
$border_in{$id}=$DESIGN{border_in};
$wall{$id}=$DESIGN{wall};
$win_wall{$id}=$DESIGN{win_wall};
$lose_wall{$id}=$DESIGN{lose_wall};
$win_sign{$id}=$DESIGN{win_sign};
$lose_sign{$id}=$DESIGN{lose_sign};
$over_sign{$id}=$DESIGN{over_sign};
$win_midi{$id}=$DESIGN{win_midi};
$lose_midi{$id}=$DESIGN{lose_midi};
$end_midi{$id}=$DESIGN{end_midi};
$high_midi{$id}=$DESIGN{high_midi};
}
#************************************************
# %DESIGN���A�e�z��ϐ��ɓǂݍ���
#************************************************
sub sysdesign_to_sysdesign_array{
local($id)=$SYSDESIGN{sysdesign_title};
push(@sysdesign_list,$id);
$sysdesign_title{$id}=$SYSDESIGN{sysdesign_title};
$top_wall{$id}=$SYSDESIGN{top_wall};
$top_back_color{$id}=$SYSDESIGN{top_back_color};
$top_table_color{$id}=$SYSDESIGN{top_table_color};
$top_genre_color{$id}=$SYSDESIGN{top_genre_color};
$top_info_color{$id}=$SYSDESIGN{top_info_color};
$top_com_color{$id}=$SYSDESIGN{top_com_color};
$top_high_color{$id}=$SYSDESIGN{top_high_color};
$top_border_color{$id}=$SYSDESIGN{top_border_color};
$top_text_color{$id}=$SYSDESIGN{top_text_color};
$top_link_color{$id}=$SYSDESIGN{top_link_color};
$top_vlink_color{$id}=$SYSDESIGN{top_vlink_color};
$top_border_high{$id}=$SYSDESIGN{top_border_high};
$top_border{$id}=$SYSDESIGN{top_border};
$top_border_in{$id}=$SYSDESIGN{top_border_in};
$a_gif{$id}=$SYSDESIGN{a_gif};
$b_gif{$id}=$SYSDESIGN{b_gif};
$align{$id}=$SYSDESIGN{align};
$walign{$id}=$SYSDESIGN{walign};
}
#************************************************
# ����W����������ϐ��ɓǂݍ���
#************************************************
sub genre_read {
&all_genre_read;
if(!mygrep($FORM{d},@genre_dir_all)){
&error(805,'�w�肵���W������');
return 1;
}
$dir=$FORM{d};
$design=$design{$dir};
&design_read($design);
$title=$title{$dir};
$top_comment=$top_comment{$dir};
$start_comment=$start_comment{$dir};
$top_table=$top_table{$dir};
$mondai_cgi=$mondai_cgi{$dir};
$mes_cgi=$mes_cgi{$dir};
$mente=$mente{$dir};
$cont=$cont{$dir};
$notext=$notext{$dir};
$direct_cont=$direct_cont{$dir};
$show_digest=$show_digest{$dir};
$show_auth=$show_auth{$dir};
$mode_name1=$mode_name1{$dir};
$mode_name2=$mode_name2{$dir};
if($mode_name2{$dir} eq ''){$FORM{m}=1;}
if($FORM{m} ne 2){
$mode_name=$mode_name1{$dir};
$show_ans=$show_ans1{$dir};
$random=$random1{$dir};
$quiz_max=$quiz_max1{$dir};
$play_max=$play_max1{$dir};
$lose_max=$lose_max1{$dir};
$time_limit=$time_limit1{$dir};
$high_border=$high_border1{$dir};
$high_cgi=$high_cgi1{$dir};
$high_back_day=$high_back_day1{$dir};
$high_back_w=$high_back_w1{$dir};
$scorehst_cgi=$scorehst_cgi1{$dir};
$scorehst_back_day=$scorehst_back_day1{$dir};
$scorehst_back_w=$scorehst_back_w1{$dir};
$graph_border=$graph_border1{$dir};
$histry_div=$histry_div1{$dir};
$day_limit=$day_limit1{$dir};
$num_limit=$num_limit1{$dir};
$no_limit=$no_limit1{$dir};
$rec_com=$rec_com1{$dir};
$double_high=$double_high1{$dir};
$bundle=$bundle1{$dir};
}else{
$mode_name=$mode_name2{$dir};
$show_ans=$show_ans2{$dir};
$random=$random2{$dir};
$quiz_max=$quiz_max2{$dir};
$play_max=$play_max2{$dir};
$lose_max=$lose_max2{$dir};
$time_limit=$time_limit2{$dir};
$high_border=$high_border2{$dir};
$high_cgi=$high_cgi2{$dir};
$high_back_day=$high_back_day2{$dir};
$high_back_w=$high_back_w2{$dir};
$scorehst_cgi=$scorehst_cgi2{$dir};
$scorehst_back_day=$scorehst_back_day2{$dir};
$scorehst_back_w=$scorehst_back_w2{$dir};
$graph_border=$graph_border2{$dir};
$histry_div=$histry_div2{$dir};
$day_limit=$day_limit2{$dir};
$num_limit=$num_limit2{$dir};
$no_limit=$no_limit2{$dir};
$rec_com=$rec_com2{$dir};
$double_high=$double_high2{$dir};
$bundle=$bundle2{$dir};
}
return 0;
}
#************************************************
# ����f�U�C������ϐ��ɓǂݍ���
#************************************************
sub design_read {
local($design)=@_;
&all_design_read();
if(!mygrep($design,@design_list)){
&def_design($design);
&design_to_design_array;
}
$text_color=$text_color{$design};
$link_color=$link_color{$design};
$vlink_color=$vlink_color{$design};
$champ_color=$champ_color{$design};
$main_color=$main_color{$design};
$result_color[1]=$win_color{$design};
$result_color[0]=$lose_color{$design};
$com_color=$com_color{$design};
$th_color=$th_color{$design};
$td_color=$td_color{$design};
$border_color=$border_color{$design};
$border_high=$border_high{$design};
$border=$border{$design};
$border_in=$border_in{$design};
$wall=$wall{$design};
$result_wall[1]=$win_wall{$design};
$result_wall[0]=$lose_wall{$design};
$win_sign=$win_sign{$design};
$lose_sign=$lose_sign{$design};
$over_sign=$over_sign{$design};
$result_midi[1]=$win_midi{$design};
$result_midi[0]=$lose_midi{$design};
$end_midi=$end_midi{$design};
$high_midi=$high_midi{$design};
$tbl_opt="border='$border_high' width=100% cellspacing='$border' cellpadding='$border_in'";
}
#************************************************
# �ݒ�ҏW�p�����[�^�[�̓ǂݍ���
#************************************************
sub sys_read{
&def_sys;
if(!open(DB,"$system_cgi")){&make_new_system_dat;}
else{
@sys=<DB>;close(DB);
if(($sys[0] =~ /^ver/)||($sys[0] eq '')||($sys[0] eq "\n")){
foreach(@sys){
$_=~ s/\n//g;
local($key,$val)=split(/\t/,$_);
$SYS{$key}=$val;
}
if($SYS{top_junle_color} ne ''){$SYS{top_genre_color}=$SYS{top_junle_color};}
}
}
&def_sysdesign();
&sysdesign_read($SYS{design});
if($SYS{align} eq 'r'){$align1='<div align=right>';$align2='</div>';}
elsif($SYS{align} eq 'c'){$align1='<center>';$align2='</center>';}
else{$align1='';$align2='';}
if($SYS{walign} eq 'r'){$walign1='<div align=right>';$walign2='</div>';}
elsif($SYS{walign} eq 'c'){$walign1='<center>';$walign2='</center>';}
else{$walign1='';$walign2='';}
$style = $SYS{style};
$style=~ s/<br>/\n/g;
return 0;
}
#************************************************
# ���j���[�y�[�W�̃f�U�C���̓ǂݍ���
#************************************************
sub sysdesign_read{
local($id)=$SYS{design};
&all_sysdesign_read();
if(!mygrep($id,@sysdesign_list)){
&def_sysdesign($id);
&sysdesign_to_sysdesign_array;
pop(@sysdesign_list);
}
$SYS{top_wall}=$top_wall{$id};
$SYS{top_back_color}=$top_back_color{$id};
$SYS{top_table_color}=$top_table_color{$id};
$SYS{top_genre_color}=$top_genre_color{$id};
$SYS{top_info_color}=$top_info_color{$id};
$SYS{top_com_color}=$top_com_color{$id};
$SYS{top_high_color}=$top_high_color{$id};
$SYS{top_border_color}=$top_border_color{$id};
$SYS{text_color}=$top_text_color{$id};
$SYS{link_color}=$top_link_color{$id};
$SYS{vlink_color}=$top_vlink_color{$id};
$SYS{top_border_high}=$top_border_high{$id};
$SYS{top_border}=$top_border{$id};
$SYS{top_border_in}=$top_border_in{$id};
$SYS{a_gif}=$a_gif{$id};
$SYS{b_gif}=$b_gif{$id};
$SYS{align}=$align{$id};
$SYS{walign}=$walign{$id};
$top_tbl_opt="border='$SYS{top_border_high}' width=100% cellspacing='$SYS{top_border}' cellpadding='$SYS{top_border_in}'";#���j���[�y�[�W�̕\�̃I�v�V����
if($SYS{wrap} eq 0){
$nowrap=' nowrap';
}
}
#************************************************
# �v���C���O��ǂݍ���
#************************************************
sub play_log_read {
local(@list,@log);
local($quiz_id)=@_;
open(DB,"$data_dir/$header${quiz_id}.cgi");
@log = <DB>;
close(DB);
$log[0]=~ s/\n//g;
($LOG{num}
,$LOG{win}
,$LOG{lose}
,$LOG{seed}
,$LOG{old}
,$LOG{write}
,$LOG{name}
,$LOG{'time'}
,$LOG{lap}
,$LOG{last_lap}
,$LOG{genre}
,$LOG{mode}
,$LOG{ck_s}
,$LOG{ck_n}
,$LOG{bundle}
) = split(/\t/,$log[0]);
($LOG{sec}
,$LOG{min}
)=&score_time($LOG{lap}-$LOG{'time'});
$cid="$LOG{mode}$LOG{genre}";
@genre_dir_use=();
foreach(@log[1..$#log]){
local($genre,$num)=split(/\t/,$_);
push(@genre_dir_use,$genre);
$genre_num{$genre}=$num;
}
}
#************************************************
# �g�p�W�������S�ẴN�C�Y��ǂݍ���
#************************************************
sub quiz_read_all{
foreach(@genre_dir_use){
$quiz_num_dir{$_}=$#mondai+1;
&quiz_read($_,$genre_num{$_},$multiquiz);
$genre_num{$_}=$#mondai + 1 - $quiz_num_dir{$_};
}
}
#************************************************
# �w��W�������̃N�C�Y�ǉ��֐�
#************************************************
sub quiz_read{
local($dir_name,$maxnum,$multi,$file_name)=@_;
local(@lines,$line,$max,$i);
if($file_name eq ''){$file_name = "$mondai_$dir_name\.cgi";}
open(DB,"$dir_name/$file_name");@lines=<DB>;close(DB);
if($maxnum ne ''){
if($maxnum > $#lines+1){$maxnum=$#lines + 1;}
elsif($maxnum < 0){$maxnum=$#lines + 1;}
}else{$maxnum=$#lines + 1;}
$i=0;
foreach $line(@lines){
$line=~ s/\n//g;
if($line eq '') {next;}
if($line=~ /^#/){next;}
if($i >= $maxnum)  {last;}
$i++;
local($mondai,$ans,$misans1,$misans2,$misans3,$misans4,$anscom,$misanscom,$cf,$digest,$misanscom1,$misanscom2,$misanscom3,$misanscom4,$anstype,$author)=split(/\t/,$line);
if($multi > 0){
push(@mondai,"$mondai<br><div align=right>�y$title{$dir_name}�z���</div>");
}else{push(@mondai,$mondai);}
push(@ans,$ans);
push(@misans1,$misans1);
push(@misans2,$misans2);
push(@misans3,$misans3);
push(@misans4,$misans4);
push(@anscom,$anscom);
push(@misanscom,$misanscom);
push(@cf,$cf);
push(@digest,$digest);
push(@misanscom1,$misanscom1);
push(@misanscom2,$misanscom2);
push(@misanscom3,$misanscom3);
push(@misanscom4,$misanscom4);
push(@anstype,$anstype);
push(@author,$author);
}
}
#************************************************
# �ݖ�ʐ��уt�@�C���̓ǂݍ���
#************************************************
sub quiz_log_read{
$QU{dir}   = &get_question_dir($quiz_index);
$QU{index} = $quiz_index - $quiz_num_dir{$QU{dir}};
&def_qu();
if (open(DB,$QU{dir}."/$quiz_header$QU{index}\.cgi")){
local(@log)= <DB>;
close(DB);
$log[0] =~ s/\n//g;
@qu = split(/\t/, $log[0]);
local($qu_all_num);
for($i=0;$i<5;$i++){
$qu[$i]=$qu[$i]+0;
$qu_all_num+=$qu[$i];
}
($QU{ave},$QU{play_num}) = split(/\t/,$log[1]);
if($qu_all_num>$QU{play_num}){
$QU{play_num}=$qu_all_num;
}
&quiz_log_calc();
}
}
#************************************************
# �ݖ�ʐ��т̌v�Z
#************************************************
sub quiz_log_calc{
if($QU{ave} eq ''){$QU{ave}='0';}
$QU{play_win} = $qu[0]+0;
if($QU{play_num} ne 0){
$QU{win_ratio}=&point($QU{play_win}*100/$QU{play_num},1);
}
$QU{ave2}=&point($QU{ave},2);
}
#************************************************
# %SYS����%FORM��
#************************************************
sub sys_to_form{
$FORM{sdes}=$SYS{design};
$FORM{li}=$SYS{limit};
$FORM{mp}=$SYS{max_player};
$FORM{cok}=$SYS{cookie};
$FORM{qf}=$SYS{quiz_form};
$FORM{"qf-$SYS{quiz_form}"}=' checked';
$FORM{mt}=$SYS{main_title};
$FORM{hd}=$SYS{header};
$FORM{shd}=$SYS{sub_header};
if($SYS{style} eq ''){$FORM{'stl-2'}='BIG{font-size:12pt;}<br>SPAN{font-size:9pt;}<br>SMALL{font-size:8pt;}<br>BODY,TD{font-size:8pt;}';$FORM{'stl-0'}=' checked';}
else{$FORM{'stl-2'}=$SYS{style};$FORM{'stl-1'}=' checked';}
$FORM{tmes}=$SYS{top_message};
$FORM{tu}=$SYS{top_url};
$FORM{"tt-$SYS{top_table}"}=' checked';
$FORM{"ey-$SYS{easy}"}=' checked';
$FORM{"rt-$SYS{'time'}"}=' checked';
$FORM{wr}=$wrap{$id};
$FORM{"wr-$SYS{wrap}"}=' checked';
}
#************************************************
# ���������genre�z����A%FORM�ɃZ�b�g����
#************************************************
sub genre_array_to_form{
$dir=$FORM{d};
$FORM{gdes}=$design{$dir};
$FORM{t}=$title{$dir};
$FORM{tc}=$top_comment{$dir};
$FORM{stc}=$start_comment{$dir};
if($mondai_cgi{$dir} eq '.'){
$FORM{md}=1;$FORM{'md-1'}=' checked';
foreach(@genre_dir_all){
if(($dir eq $_)||($mondai_cgi{$_} eq '.')||($mondai_cgi{$_} =~ /\//)){next;}
$FORM2{"smd-$_"}='all';
}
}elsif($mondai_cgi{$dir} =~ /\//){
$FORM{'md-1'}=' checked';
@mondai_dat=split(/\t/,$mondai_cgi{$dir});
foreach(@mondai_dat){
local($d,$val)=split(/\//,$_);
$FORM2{"smd-$d"}=$val;
}
}else{
$FORM{'md-0'}=' checked';
foreach(@genre_dir_all){
if(($mondai_cgi{$_} eq '.')||($mondai_cgi{$_} =~ /\//)){next;}
&refresh_quiz;
&quiz_read($_);
$FORM2{"smd-$_"}=$#mondai+1;
}
}
$FORM{"me-$mente{$dir}"}=' checked';
$FORM{me}=$mente{$dir};
$FORM{ct}=$cont{$dir};
$FORM{"ct-$cont{$dir}"}=' checked';
$FORM{nt}=$notext{$dir};
$FORM{"nt-$notext{$dir}"}=' checked';
$FORM{dc}=$direct_cont{$dir};
$FORM{"dc-$direct_cont{$dir}"}=' checked';
$FORM{sd}=$show_digest{$dir};
$FORM{"sd-$show_digest{$dir}"}=' checked';
$FORM{ath}=$show_auth{$dir};
$FORM{"ath-$show_auth{$dir}"}=' checked';
$FORM{mn1}=$mode_name1{$dir};
$FORM{sa1}=$show_ans1{$dir};
$FORM{"sa1-$show_ans1{$dir}"}=' checked';
$FORM{r1}=$random1{$dir};
$FORM{"r1-$random1{$dir}"}=' checked';
if($quiz_max1{$dir} eq ''){$FORM{'qm1-1'}=' checked';}
else{$FORM{'qm1-0'}=' checked';$FORM{'qm1-2'}=$quiz_max1{$dir};}
if($play_max1{$dir} eq ''){$FORM{'pm1-1'}=' checked';}
else{$FORM{'pm1-0'}=' checked';$FORM{'pm1-2'}=$play_max1{$dir};}
if($lose_max1{$dir} eq ''){$FORM{'lm1-1'}=' checked';}
else{$FORM{'lm1-0'}=' checked';$FORM{'lm1-2'}=$lose_max1{$dir};}
if($time_limit1{$dir} eq ''){$FORM{'tl1-1'}=' checked';$FORM{'tl1-2'}=60;}
else{$FORM{'tl1-0'}=' checked';$FORM{'tl1-2'}=$time_limit1{$dir};}
$FORM{hb1}=$high_border1{$dir};
if($high_back_day1{$dir} > 0){$FORM{'hbu1-1'}=' checked';$FORM{'hbu1-2'}=$high_back_day1{$dir};}
else{$FORM{'hbu1-0'}=' checked';$FORM{'hbu1-2'}=30;}
$FORM{hbw1}=$high_back_w1{$dir};
$FORM{"hbw1-$high_back_w1{$dir}"}=' checked';
if($scorehst_back_day1{$dir} > 0){$FORM{'sbu1-1'}=' checked';$FORM{'sbu1-2'}=$scorehst_back_day1{$dir};}
else{$FORM{'sbu1-0'}=' checked';$FORM{'sbu1-2'}=30;}
$FORM{sbw1}=$scorehst_back_w1{$dir};
$FORM{"sbw1-$scorehst_back_w1{$dir}"}=' checked';
$FORM{gb1}=$graph_border1{$dir};
$FORM{hd1}=$histry_div1{$dir};
if($day_limit1{$dir} eq ''){$FORM{'dl1-1'}=' checked';$FORM{'dl1-2'}=30;}
else{$FORM{'dl1-0'}=' checked';$FORM{'dl1-2'}=$day_limit1{$dir};}
if($num_limit1{$dir} eq ''){$FORM{'nl1-1'}=' checked';$FORM{'nl1-2'}=100;}
else{$FORM{'nl1-0'}=' checked';$FORM{'nl1-2'}=$num_limit1{$dir};}
$FORM{no1}=$no_limit1{$dir};
$FORM{rc1}=$rec_com1{$dir};
$FORM{"rc1-$rec_com1{$dir}"}=' checked';
$FORM{dh1}=$double_high1{$dir};
$FORM{"dh1-$double_high1{$dir}"}=' checked';
$FORM{bd1}=$bundle1{$dir};
$FORM{"bd1-$bundle1{$dir}"}=' checked';
$FORM{mn2}=$mode_name2{$dir};
$FORM{sa2}=$show_ans2{$dir};
$FORM{"sa2-$show_ans2{$dir}"}=' checked';
$FORM{r2}=$random2{$dir};
$FORM{"r2-$random2{$dir}"}=' checked';
if($quiz_max2{$dir} eq ''){$FORM{'qm2-1'}=' checked';}
else{$FORM{'qm2-0'}=' checked';$FORM{'qm2-2'}=$quiz_max2{$dir};}
if($play_max2{$dir} eq ''){$FORM{'pm2-1'}=' checked';}
else{$FORM{'pm2-0'}=' checked';$FORM{'pm2-2'}=$play_max2{$dir};}
if($lose_max2{$dir} eq ''){$FORM{'lm2-1'}=' checked';}
else{$FORM{'lm2-0'}=' checked';$FORM{'lm2-2'}=$lose_max2{$dir};}
if($time_limit2{$dir} eq ''){$FORM{'tl2-1'}=' checked';$FORM{'tl2-2'}=60;}
else{$FORM{'tl2-0'}=' checked';$FORM{'tl2-2'}=$time_limit2{$dir};}
$FORM{hb2}=$high_border2{$dir};
if($high_back_day2{$dir} > 0){$FORM{'hbu2-1'}=' checked';$FORM{'hbu2-2'}=$high_back_day2{$dir};}
else{$FORM{'hbu2-0'}=' checked';$FORM{'hbu2-2'}=30;}
$FORM{hbw2}=$high_back_w2{$dir};
$FORM{"hbw2-$high_back_w2{$dir}"}=' checked';
if($scorehst_back_day2{$dir} > 0){$FORM{'sbu2-1'}=' checked';$FORM{'sbu2-2'}=$scorehst_back_day2{$dir};}
else{$FORM{'sbu2-0'}=' checked';$FORM{'sbu2-2'}=30;}
$FORM{sbw2}=$scorehst_back_w2{$dir};
$FORM{"sbw2-$scorehst_back_w2{$dir}"}=' checked';
$FORM{gb2}=$graph_border2{$dir};
$FORM{hd2}=$histry_div2{$dir};
if($day_limit2{$dir} eq ''){$FORM{'dl2-1'}=' checked';$FORM{'dl2-2'}=30;}
else{$FORM{'dl2-0'}=' checked';$FORM{'dl2-2'}=$day_limit2{$dir};}
if($num_limit2{$dir} eq ''){$FORM{'nl2-1'}=' checked';$FORM{'nl2-2'}=100;}
else{$FORM{'nl2-0'}=' checked';$FORM{'nl2-2'}=$num_limit2{$dir};}
$FORM{no2}=$no_limit2{$dir};
$FORM{rc2}=$rec_com2{$dir};
$FORM{"rc2-$rec_com2{$dir}"}=' checked';
$FORM{dh2}=$double_high2{$dir};
$FORM{"dh2-$double_high2{$dir}"}=' checked';
$FORM{bd2}=$bundle2{$dir};
$FORM{"bd2-$bundle2{$dir}"}=' checked';
&form_to_form;
}
#************************************************
# %SYSDESIGN����%FORM��
#************************************************
sub sysdesign_to_form{
local($id)=@_;
$FORM{tw}=$top_wall{$id};
$FORM{tbc}=$top_back_color{$id};
$FORM{ttc}=$top_table_color{$id};
$FORM{tjc}=$top_genre_color{$id};
$FORM{tic}=$top_info_color{$id};
$FORM{tcc}=$top_com_color{$id};
$FORM{thc}=$top_high_color{$id};
$FORM{tbdc}=$top_border_color{$id};
$FORM{txc}=$top_text_color{$id};
$FORM{lc}=$top_link_color{$id};
$FORM{vc}=$top_vlink_color{$id};
$FORM{tbdh}=$top_border_high{$id};
$FORM{tbd}=$top_border{$id};
$FORM{tbdi}=$top_border_in{$id};
$FORM{ag}=$a_gif{$id};
$FORM{bg}=$b_gif{$id};
$FORM{al}=$align{$id};
$FORM{"al-$align{$id}"}=' checked';
$FORM{wal}=$walign{$id};
$FORM{"wal-$walign{$id}"}=' checked';
}
#************************************************
# %DESIGN����%FORM��
#************************************************
sub design_to_form{
local($id)=@_;
$FORM{gtc}=$text_color{$id};
$FORM{glc}=$link_color{$id};
$FORM{gvc}=$vlink_color{$id};
$FORM{gcc}=$champ_color{$id};
$FORM{gmc}=$main_color{$id};
$FORM{gwi}=$win_color{$id};
$FORM{glo}=$lose_color{$id};
$FORM{gcm}=$com_color{$id};
$FORM{thc}=$th_color{$id};
$FORM{tdc}=$td_color{$id};
$FORM{bdc}=$border_color{$id};
$FORM{bdh}=$border_high{$id};
$FORM{bd}=$border{$id};
$FORM{bdi}=$border_in{$id};
$FORM{gw}=$wall{$id};
$FORM{gww}=$win_wall{$id};
$FORM{glw}=$lose_wall{$id};
$FORM{wsg}=$win_sign{$id};
$FORM{lsg}=$lose_sign{$id};
$FORM{osg}=$over_sign{$id};
$FORM{wmd}=$win_midi{$id};
$FORM{lmd}=$lose_midi{$id};
$FORM{emd}=$end_midi{$id};
$FORM{hmd}=$high_midi{$id};
}
#************************************************
# ��������̖������A������form�p�ϐ��ɃZ�b�g����
#************************************************
sub quiz_array_to_form{
local($quiz_num)=$FORM{qn}-1;
$FORM{qqu}   =$mondai[$quiz_num];
$FORM{qas}   =$ans[$quiz_num];
$FORM{qmas1} =$misans1[$quiz_num];
$FORM{qmas2} =$misans2[$quiz_num];
$FORM{qmas3} =$misans3[$quiz_num];
$FORM{qmas4} =$misans4[$quiz_num];
$FORM{qac}   =$anscom[$quiz_num];
$FORM{qmac}  =$misanscom[$quiz_num];
$FORM{qcf}   =$cf[$quiz_num];
$FORM{qdg}   =$digest[$quiz_num];
$FORM{qmac1} =$misanscom1[$quiz_num];
$FORM{qmac2} =$misanscom2[$quiz_num];
$FORM{qmac3} =$misanscom3[$quiz_num];
$FORM{qmac4} =$misanscom4[$quiz_num];
$FORM{atype} =$anstype[$quiz_num];
$FORM{auth} =$author[$quiz_num];
}
#************************************************
# %FORM����%SYS��
#************************************************
sub form_to_sys{
$SYS{design}=$FORM{sdes};
$SYS{limit}=$FORM{li};
$SYS{max_player}=$FORM{mp};
$SYS{cookie}=$FORM{cok};
$SYS{quiz_form}=$FORM{qf};
$SYS{main_title}=$FORM{mt};
$SYS{header}=$FORM{hd};
$SYS{sub_header}=$FORM{shd};
if($FORM{stl} eq '1'){$SYS{style}=$FORM4{'stl-2'};}
else{$SYS{style}='';}
$SYS{top_message}=$FORM4{tmes};
$SYS{top_table}=$FORM{tt};
$SYS{top_url}=$FORM{tu};
$SYS{easy}=$FORM{ey};
$SYS{'time'}=$FORM{rt};
$SYS{wrap}=$FORM{wr};
}
#************************************************
# %FORM�̓��e���A���������genre�z��ɃZ�b�g����
#************************************************
sub form_to_genre_array{
$dir=$FORM{d};
$design{$dir}=$FORM{gdes};
$title{$dir}=$FORM{t};
$top_comment{$dir}=$FORM4{tc};
$start_comment{$dir}=$FORM4{stc};
$mondai_cgi{$dir}='';
if($FORM{md}){
foreach(@genre_dir_all){
if(($mondai_cgi{$_} eq '.')||($mondai_cgi{$_} =~ /\//)){next;}
$mondai_cgi{$dir}.="$_\/".$FORM{"smd-$_"}."\t";
}
}
$mente{$dir}=$FORM{me};
$cont{$dir}=$FORM{ct};
$notext{$dir}=$FORM{nt};
$direct_cont{$dir}=$FORM{dc};
$show_digest{$dir}=$FORM{sd};
$show_auth{$dir}=$FORM{ath};
$mode_name1{$dir}=$FORM{mn1};
$show_ans1{$dir}=$FORM{sa1};
$random1{$dir}=$FORM{r1};
if($FORM{hbu1}){$high_back_day1{$dir}=$FORM{'hbu1-2'};}
else{$high_back_day1{$dir}='0';}
$high_back_w1{$dir}=$FORM{hbw1};
if($FORM{dl1}){$day_limit1{$dir}='';}
else{$day_limit1{$dir}=$FORM{'dl1-2'};}
if($FORM{nl1}){$num_limit1{$dir}='';}
else{$num_limit1{$dir}=$FORM{'nl1-2'};}
$no_limit1{$dir}=$FORM{no1};
$rec_com1{$dir}=$FORM{rc1};
$double_high1{$dir}=$FORM{dh1};
$bundle1{$dir}=$FORM{bd1};
if($FORM{sbu1}){$scorehst_back_day1{$dir}=$FORM{'sbu1-2'};}
else{$scorehst_back_day1{$dir}='0';}
$scorehst_back_w1{$dir}=$FORM{sbw1};
$graph_border1{$dir}=$FORM{gb1};
$histry_div1{$dir}=$FORM{hd1};
if($FORM{qm1}){$quiz_max1{$dir}='';}
else{$quiz_max1{$dir}=$FORM{'qm1-2'};}
if($FORM{pm1}){$play_max1{$dir}='';}
else{$play_max1{$dir}=$FORM{'pm1-2'};}
if($FORM{lm1}){$lose_max1{$dir}='';}
else{$lose_max1{$dir}=$FORM{'lm1-2'};}
if($FORM{tl1}){$time_limit1{$dir}='';}
else{$time_limit1{$dir}=$FORM{'tl1-2'};}
$high_border1{$dir}=$FORM{hb1};
$mode_name2{$dir}=$FORM{mn2};
$show_ans2{$dir}=$FORM{sa2};
$random2{$dir}=$FORM{r2};
if($FORM{hbu2}){$high_back_day2{$dir}=$FORM{'hbu2-2'};}
else{$high_back_day2{$dir}='0';}
$high_back_w2{$dir}=$FORM{hbw2};
if($FORM{dl2}){$day_limit2{$dir}='';}
else{$day_limit2{$dir}=$FORM{'dl2-2'};}
if($FORM{nl2}){$num_limit2{$dir}='';}
else{$num_limit2{$dir}=$FORM{'nl2-2'};}
$no_limit2{$dir}=$FORM{no2};
$rec_com2{$dir}=$FORM{rc2};
$double_high2{$dir}=$FORM{dh2};
$bundle2{$dir}=$FORM{bd2};
if($FORM{sbu2}){$scorehst_back_day2{$dir}=$FORM{'sbu2-2'};}
else{$scorehst_back_day2{$dir}='0';}
$scorehst_back_w2{$dir}=$FORM{sbw2};
$graph_border2{$dir}=$FORM{gb2};
$histry_div2{$dir}=$FORM{hd2};
if($FORM{qm2}){$quiz_max2{$dir}='';}
else{$quiz_max2{$dir}=$FORM{'qm2-2'};}
if($FORM{pm2}){$play_max2{$dir}='';}
else{$play_max2{$dir}=$FORM{'pm2-2'};}
if($FORM{lm2}){$lose_max2{$dir}='';}
else{$lose_max2{$dir}=$FORM{'lm2-2'};}
if($FORM{tl2}){$time_limit2{$dir}='';}
else{$time_limit2{$dir}=$FORM{'tl2-2'};}
$high_border2{$dir}=$FORM{hb2};
}
#************************************************
# %FORM���烁�������sysdesign�z��ɃZ�b�g����
#************************************************
sub form_to_sysdesign_array{
$id=$FORM{sdt};
$sysdesign_title{$id}=$FORM{sdt};
$top_wall{$id}=$FORM{tw};
$top_back_color{$id}=$FORM{tbc};
$top_table_color{$id}=$FORM{ttc};
$top_genre_color{$id}=$FORM{tjc};
$top_info_color{$id}=$FORM{tic};
$top_com_color{$id}=$FORM{tcc};
$top_high_color{$id}=$FORM{thc};
$top_border_color{$id}=$FORM{tbdc};
$top_text_color{$id}=$FORM{txc};
$top_link_color{$id}=$FORM{lc};
$top_vlink_color{$id}=$FORM{vc};
$top_border_high{$id}=$FORM{tbdh};
$top_border{$id}=$FORM{tbd};
$top_border_in{$id}=$FORM{tbdi};
$a_gif{$id}=$FORM{ag};
$b_gif{$id}=$FORM{bg};
$align{$id}=$FORM{al};
$walign{$id}=$FORM{wal};
}
#************************************************
# %FORM���烁�������design�z��ɃZ�b�g����
#************************************************
sub form_to_design_array{
$id=$FORM{gdt};
$design_title{$id}=$FORM{gdt};
$text_color{$id}=$FORM{gtc};
$link_color{$id}=$FORM{glc};
$vlink_color{$id}=$FORM{gvc};
$champ_color{$id}=$FORM{gcc};
$main_color{$id}=$FORM{gmc};
$win_color{$id}=$FORM{gwi};
$lose_color{$id}=$FORM{glo};
$com_color{$id}=$FORM{gcm};
$th_color{$id}=$FORM{thc};
$td_color{$id}=$FORM{tdc};
$border_color{$id}=$FORM{bdc};
$border_high{$id}=$FORM{bdh};
$border{$id}=$FORM{bd};
$border_in{$id}=$FORM{bdi};
$wall{$id}=$FORM{gw}; 
$win_wall{$id}=$FORM{gww};
$lose_wall{$id}=$FORM{glw};
$win_sign{$id}=$FORM{wsg};
$lose_sign{$id}=$FORM{lsg};
$over_sign{$id}=$FORM{osg};
$win_midi{$id}=$FORM{wmd};
$lose_midi{$id}=$FORM{lmd};
$end_midi{$id}=$FORM{emd};
$high_midi{$id}=$FORM{hmd};
}
#************************************************
# dir����Agenre.cgi�p�̃��O��Ԃ�
#************************************************
sub genre_array_to_line{
local($dir)=@_;
return join("\n"
,"dir\t$dir"
,"design\t$design{$dir}"
,"title\t$title{$dir}"
,"top_comment\t$top_comment{$dir}"
,"start_comment\t$start_comment{$dir}"
,"mente\t$mente{$dir}"
,"cont\t$cont{$dir}"
,"notext\t$notext{$dir}"
,"direct_cont\t$direct_cont{$dir}"
,"show_digest\t$show_digest{$dir}"
,"show_auth\t$show_auth{$dir}"
,"mondai_cgi\t$mondai_cgi{$dir}"
,"mode_name1\t$mode_name1{$dir}"
,"show_ans1\t$show_ans1{$dir}"
,"random1\t$random1{$dir}"
,"quiz_max1\t$quiz_max1{$dir}"
,"play_max1\t$play_max1{$dir}"
,"lose_max1\t$lose_max1{$dir}"
,"time_limit1\t$time_limit1{$dir}"
,"high_border1\t$high_border1{$dir}"
,"high_back_day1\t$high_back_day1{$dir}"
,"high_back_w1\t$high_back_w1{$dir}"
,"scorehst_back_day1\t$scorehst_back_day1{$dir}"
,"scorehst_back_w1\t$scorehst_back_w1{$dir}"
,"graph_border1\t$graph_border1{$dir}"
,"histry_div1\t$histry_div1{$dir}"
,"day_limit1\t$day_limit1{$dir}"
,"num_limit1\t$num_limit1{$dir}"
,"no_limit1\t$no_limit1{$dir}"
,"rec_com1\t$rec_com1{$dir}"
,"double_high1\t$double_high1{$dir}"
,"bundle1\t$bundle1{$dir}"
,"mode_name2\t$mode_name2{$dir}"
,"show_ans2\t$show_ans2{$dir}"
,"random2\t$random2{$dir}"
,"quiz_max2\t$quiz_max2{$dir}"
,"play_max2\t$play_max2{$dir}"
,"lose_max2\t$lose_max2{$dir}"
,"time_limit2\t$time_limit2{$dir}"
,"high_border2\t$high_border2{$dir}"
,"high_back_day2\t$high_back_day2{$dir}"
,"high_back_w2\t$high_back_w2{$dir}"
,"scorehst_back_day2\t$scorehst_back_day2{$dir}"
,"scorehst_back_w2\t$scorehst_back_w2{$dir}"
,"graph_border2\t$graph_border2{$dir}"
,"histry_div2\t$histry_div2{$dir}"
,"day_limit2\t$day_limit2{$dir}"
,"num_limit2\t$num_limit2{$dir}"
,"no_limit2\t$no_limit2{$dir}"
,"rec_com2\t$rec_com2{$dir}"
,"double_high2\t$double_high2{$dir}"
,"bundle2\t$bundle2{$dir}"
,"\n");
}
#************************************************
# id����Asysdesign.cgi�p�̃��O��Ԃ�
#************************************************
sub sysdesign_array_to_line{
local($id)=@_;
return join("\n"
,"sysdesign_title\t$sysdesign_title{$id}"
,"top_wall\t$top_wall{$id}"
,"top_back_color\t$top_back_color{$id}"
,"top_table_color\t$top_table_color{$id}"
,"top_genre_color\t$top_genre_color{$id}"
,"top_info_color\t$top_info_color{$id}"
,"top_com_color\t$top_com_color{$id}"
,"top_high_color\t$top_high_color{$id}"
,"top_border_color\t$top_border_color{$id}"
,"top_text_color\t$top_text_color{$id}"
,"top_link_color\t$top_link_color{$id}"
,"top_vlink_color\t$top_vlink_color{$id}"
,"top_border_high\t$top_border_high{$id}"
,"top_border\t$top_border{$id}"
,"top_border_in\t$top_border_in{$id}"
,"a_gif\t$a_gif{$id}"
,"b_gif\t$b_gif{$id}"
,"align\t$align{$id}"
,"walign\t$walign{$id}"
,"\n");
}
#************************************************
# id����Adesign.cgi�p�̃��O��Ԃ�
#************************************************
sub design_array_to_line{
local($id)=@_;
return join("\n"
,"design_title\t$design_title{$id}"
,"text_color\t$text_color{$id}"
,"link_color\t$link_color{$id}"
,"vlink_color\t$vlink_color{$id}"
,"champ_color\t$champ_color{$id}"
,"main_color\t$main_color{$id}"
,"win_color\t$win_color{$id}"
,"lose_color\t$lose_color{$id}"
,"com_color\t$com_color{$id}"
,"th_color\t$th_color{$id}"
,"td_color\t$td_color{$id}"
,"border_color\t$border_color{$id}"
,"border_high\t$border_high{$id}"
,"border\t$border{$id}"
,"border_in\t$border_in{$id}"
,"wall\t$wall{$id}"
,"win_wall\t$win_wall{$id}"
,"lose_wall\t$lose_wall{$id}"
,"win_sign\t$win_sign{$id}"
,"lose_sign\t$lose_sign{$id}"
,"over_sign\t$over_sign{$id}"
,"win_midi\t$win_midi{$id}"
,"lose_midi\t$lose_midi{$id}"
,"end_midi\t$end_midi{$id}"
,"high_midi\t$high_midi{$id}"
,"\n");
}
#************************************************
# %SYS����system.dat�`���̏o��
#************************************************
sub sys_to_system_dat{
local($return);$return="ver2\n";
foreach(
'design'
,'limit'
,'max_player'
,'cookie'
,'quiz_form'
,'main_title'
,'header'
,'sub_header'
,'style'
,'top_message'
,'top_table'
,'top_url'
,'easy'
,'time'
,'wrap'
){
$return.="$_\t$SYS{$_}\n";
}
return $return;
}
#************************************************
# �������A��������̖��z��ϐ��Ɋi�[
#************************************************
sub push_quiz_palam{
local($mondai,$ans,$misans1,$misans2,$misans3,$misans4,$anscom,$misanscom,$cf,$digest,$misanscom1,$misanscom2,$misanscom3,$misanscom4,$anstype,$author)=@_;
push(@mondai,$mondai);
push(@ans,$ans);
push(@misans1,$misans1);
push(@misans2,$misans2);
push(@misans3,$misans3);
push(@misans4,$misans4);
push(@anscom,$anscom);
push(@misanscom,$misanscom);
push(@cf,$cf);
push(@digest,$digest);
push(@misanscom1,$misanscom1);
push(@misanscom2,$misanscom2);
push(@misanscom3,$misanscom3);
push(@misanscom4,$misanscom4);
push(@anstype,$anstype);
push(@author,$author);
}
#************************************************
# ���z�񂩂�A���t�@�C���p���O��Ԃ�
#************************************************
sub quiz_to_line{
local($ret);
local($id,$num)=@_;
if($num ne ''){
$ret=('#' x 5) ."$num".('#' x 5)."\n";
}
$ret.=join("\t",$mondai[$id],$ans[$id],$misans1[$id],$misans2[$id],$misans3[$id],$misans4[$id],$anscom[$id],$misanscom[$id],$cf[$id],$digest[$id],$misanscom1[$id],$misanscom2[$id],$misanscom3[$id],$misanscom4[$id],$anstype[$id],$author[$id],"\n");
return $ret;
}
#************************************************
# �I�������b�Z�[�W�p�����[�^�ǂݍ���
#************************************************
sub mes_dat_to_form{
unless(-f "$FORM{d}/$mes_cgi{$FORM{d}}\.cgi"){&make_mes_cgi;}
open(DB,"$FORM{d}/$mes_cgi{$FORM{d}}\.cgi");@lines= <DB>;close(DB);
$FORM{mn}=-1;
$i=0;
foreach $line(@lines){
$line=~ s/\n//g;
if($line eq ''){next;}
local($per,$mes,$mod1,$mod2)=split(/\t/,$line);
if($mod1 ne '0'){$mod1 = ' checked';}else{$mod1='';}
if($mod2 ne '0'){$mod2 = ' checked';}else{$mod2='';}
if($per eq 'top'){$FORM{'mes-top1'}=$mes;$FORM{'mes-top2'}=$mes;}
elsif($per eq 'top1'){$FORM{'mes-top1'}=$mes;}
elsif($per eq 'top2'){$FORM{'mes-top2'}=$mes;}
else{
$FORM{mn}++;
$FORM{"per-$i"}=$per;
$FORM{"mes-$i"}=$mes;
$FORMCH{"ch1-$i"}=$mod1;
$FORMCH{"ch2-$i"}=$mod2;
$i++;
}
}
}
#************************************************
# �\���t�@�C���̃`�F�b�N
#************************************************
sub ch_files{
local($i,$mes,@cgis,@dirs,$err_files,$err_cgis,$err_dirs);
@cgis=($quiz_op_cgi,$quiz_cgi,$index_cgi,$function_cgi);
@dirs=($data_dir);
foreach $cgi(@cgis){
&ch_file_exist($cgi,$cgi);
}
&ch_file_ver(@cgis);
foreach $dir(@dirs){
&ch_dir_exist("$dir�f�B���N�g��",$dir);
}
}
#************************************************
# �t�@�C���̃o�[�W�����`�F�b�N
#************************************************
sub ch_file_ver{
local(@cgis)=@_;
local($mes,$ver_max,%cgis_ver);
$ver_max=0;
foreach $cgi(@cgis){
unless(-f $cgi){next;}
open(DB,$cgi);@list=<DB>;close(DB);
if($list[1]=~ /\$version=\'(.*)\'/){
$cgis_ver{$cgi}=$1;
if($ver_max < $1){$ver_max=$1;}
}
}
foreach(keys %cgis_ver){
if($ver_max > $cgis_ver{$_}){$mes.="�y$_�z<br>";}
}
if($mes ne ''){
&mes(901,$mes.'��L�̃X�N���v�g�́A�ŐV�o�[�W�����ł͂���܂���B<br>����Ɏx����������\��������܂��B');
}
}
#************************************************
# �f�B���N�g���̖��O�`�F�b�N�Ƒ��݊m�F�B������΍쐬
#************************************************
sub ch_dir_exist{
local($dir_nick,$dir_name)=@_;
if($dir_name eq ''){&error(202,$dir_nick);return 1;}
if($dir_name=~ /\W/){&error(106,$dir_nick);return 1;}
if(!(-d $dir_name)){
mkdir($dir_name,$mod_dir);
chmod(oct($mod_dir),$dir_name);
if(!(-d $dir_name)){
&error(732,"$dir_name�f�B���N�g��");
return 2;
}
else{&mes(451,"$dir_name�f�B���N�g��");}
}
return 0;
}
#************************************************
# �t�@�C���̖��O�`�F�b�N�Ƒ��݊m�F�B
#************************************************
sub ch_file_exist{
local($file_nick,$file_name)=@_;
if($file_name =~ /^http:\/\//){return 1;}
if(!(-f $file_name)){
&error(813,"�y$file_nick�z");
return 1;
}
return 0;
}
#************************************************
# �t�@�C���X�^���v�`�F�b�N
#************************************************
sub ch_file_stump{
local($file_age);
local($file_name,$file_nick,$file_stump)=@_;
$file_age = $now - (-M "$file_name")*60*60*24;
if(($file_stump > $file_age+10)||($file_stump < $file_age-10)){
&error(861,$file_nick);
return 1;
}
return 0;
}
#************************************************
# �p�X���[�h�`�F�b�N����
#************************************************
sub ch_pwd_html {
local(@line);
open(DB,$pass_cgi);@line=<DB>;close(DB);
$line[0]=~ s/\n//g;
if($line[0] eq ''){
if($FORM{passnew} ne ''){
if($FORM{passnew1} eq ''){
&header_html("�p�X���[�h�G���[");
&error(209,'�V�K�p�X���[�h');
&pass_new_html;
}elsif($FORM{passnew1} ne $FORM{passnew2}){
&header_html("�p�X���[�h�G���[");
&error(541,'�V�K�p�X���[�h�Ɗm�F�p�p�X���[�h');
&pass_new_html;
}else{
$pass=crypt($FORM2{passnew1},"ARRAY(0xb74f5c)");
if(&write_file($pass_cgi,$pass)){
&header_html("�p�X���[�h�V�K�o�^���s");
}else{
&header_html("�p�X���[�h�V�K�o�^����");
&mes(902,"�Ǘ��җp�p�X���[�h��o�^���܂���<br>�p�X���[�h���������������ꍇ�́A$pass_cgi�t�@�C�����������Ă��������B");
}
}
}else{
&header_html("�p�X���[�h�V�K�o�^");
&pass_new_html;
}
return 1;
}elsif($FORM{passch} ne ''){
if(&ch_pwd($FORM2{passch})){
&header_html("�p�X���[�h�G���[");
&error(542,'�p�X���[�h');
&pass_enter_html;
return 1;
}
}elsif($FORM{passch1} ne ''){
&header_html("�p�X���[�h�G���[");
&error(209,'�p�X���[�h');
&pass_enter_html;
return 1;
}else{
&header_html("�p�X���[�h����");
&pass_enter_html;
return 1;
}
return 0;
}
#************************************************
# �W���������̑��ݔ���
#************************************************
sub ch_genre_exist{
local($dir)=@_;
foreach(@genre_dir_all){
if(($_ ne '')&&($_ eq $dir)){return 1;}
}
return 0;
}
#************************************************
# �Ǝ��̖��t�@�C���������ǂ����`�F�b�N
#************************************************
sub ch_mondai_exist{
if(($mondai_cgi{$FORM{d}} eq '.')||($mondai_cgi{$FORM{d}} =~ /\//)){
&error(701);
&menu_html;
return 1;
}
return 0;
}
#************************************************
# �t�@�C�����̑Ó����`�F�b�N
#************************************************
sub ch_file_format{
unless($_[0]=~ /^[\w\$\#\~\.\/\-\?\=\&:]+$/){
return 1;
}
return 0;
}
#************************************************
# ���ǉ����̃p�����[�^�`�F�b�N
#************************************************
sub ch_add_quiz_param{
if($FORM{qqu} eq ''){&error(203,'��蕶');return 1;}
if($FORM{qas} eq ''){&error(203,'����');return 1;}
if(($FORM{qmas1} eq '')&&($FORM{atype} eq '')){&error(203,'�듚�P');return 1;}
return 0;
}
#************************************************
# ���ǉ����̏d���o�^�`�F�b�N
#************************************************
sub ch_duplic_quiz{
local($i);
foreach(@mondai){
if(join("\t",$mondai[$i],$ans[$i],$misans1[$i],$misans2[$i],$misans3[$i],$misans4[$i]) eq
join("\t",$FORM4{qqu},$FORM4{qas},$FORM4{qmas1},$FORM4{qmas2},$FORM4{qmas3},$FORM4{qmas4})){
&error('���̖��͂��łɓo�^����Ă��܂��B');return 1;
}
$i++;
}
return 0;
}
#************************************************
# ���ҏW���̃p�����[�^�`�F�b�N
#************************************************
sub ch_edit_quiz_param{
local($error)=$error_mes;
if($FORM{qn} eq ''){&error(204,'���ԍ�');}
elsif($FORM{qn} =~/\D/){&error(302,'���ԍ�');}
elsif(($FORM{qn}>$#mondai+1)&&($FORM{qn}<=0)){&error(531,'���ԍ�');}
if($FORM{qqu} eq ''){&error(204,'��蕶');}
if($FORM{qas} eq ''){&error(204,'����');}
if(($FORM{qmas1} eq '')&&($FORM{atype} eq '')){&error(204,'�듚�P');}
if($error eq $error_mes){return 0;}
else{return 1;}
}
#************************************************
# �V�X�e���ݒ�ҏW���̃p�����[�^�`�F�b�N
#************************************************
sub ch_sys_palam{
local(@return,$error);
$FORM{"qf-$FORM{qf}"}   =' checked';
$FORM{"stl-$FORM{stl}"} =' checked';
$FORM{"tt-$FORM{tt}"}   =' checked';
$FORM{"ey-$FORM{ey}"}     =' checked';
$FORM{"rt-$FORM{rt}"}     =' checked';
$FORM{"wr-$FORM{wr}"}     =' checked';
$error=$error_mes;
if($FORM{li} eq ''){&error(205,'(1)�v���C���O�ی����');}
elsif($FORM{li} =~ /\D/){&error(303,'(1)�v���C���O�ی����');}
if($FORM{mp} eq ''){&error(205,'(2)�����v���C�l��');}
elsif($FORM{mp} =~ /\D/){&error(303,'(2)�����v���C�l��');}
if($FORM{cok} eq ''){&error(205,'(3)�N�b�L�[ID');}
elsif($FORM{cok} =~ /\W/){&error(106,'(3)�N�b�L�[ID');}
if(!mygrep($FORM{qf},(0,1,2))){&error(401,'(4)�I�����`��');}
if($FORM{mt} eq ''){&error(205,'(6)���j���[�y�[�W�̃^�C�g��');}
if(!mygrep($FORM{stl},(0,1))){&error(401,'(10)�X�^�C���V�[�g');}
if(!mygrep($FORM{ey},(0,1,2,3))){&error(401,'(12)���j���[�y�[�W�\������');}
if(!mygrep($FORM{rt},(0,1))){&error(401,'(13)�񓚎��Ԃɂ�鏇�ʕt��');}
if(!mygrep($FORM{wr},(0,1))){&error(401,'(14)���������܂�Ԃ�');}
if($error eq $error_mes){return 0;}
else{return 1;}
}
#************************************************
# �V�X�e���f�U�C���ݒ�ҏW���̃p�����[�^�`�F�b�N
#************************************************
sub ch_sysdesign_palam{
local(@return,$error);
$FORM{"al-$FORM{al}"}   =' checked';
$FORM{"wal-$FORM{wal}"} =' checked';
$error=$error_mes;
if($FORM{sdt} eq ''){&error(206,'(2)�V�X�e���f�U�C����');}
foreach $id(@sysdesign_list){
if($id eq $FORM{sdt} && $FORM{edittype} ne 'edit'){
&error(853,'(2)�V�X�e���f�U�C����');
}elsif($id eq $FORM{sdt} && $FORM{sdt} ne $FORM{id} && $FORM{edittype} eq 'edit'){
&error(854,'(2)�V�X�e���f�U�C����');
}
}
if(($FORM{tw} ne '')&&(&ch_file_format($FORM{tw}))){&error(305,'(3)���j���[�y�[�W�̕ǎ�');}
if($FORM{tbc} eq ''){&error(206,'(4)���j���[�y�[�W�̔w�i�F');}
if($FORM{ttc} eq ''){&error(206,'(5)���j���[�y�[�W�̕\�̐F');}
if($FORM{tjc} eq ''){&error(206,'(6)���j���[�y�[�W�̃W�������F');}
if($FORM{tic} eq ''){&error(206,'(7)���j���[�y�[�W�̏��F');}
if($FORM{tcc} eq ''){&error(206,'(8)���j���[�y�[�W�̃R�����g�F');}
if($FORM{thc} eq ''){&error(206,'(9)���j���[�y�[�W�̍����юҐF');}
if($FORM{tbdc} eq ''){&error(206,'(10)���j���[�y�[�W�̕\�̘g�̐F');}
if($FORM{txc} eq ''){&error(206,'(11)�y�[�W�̕����F');}
if($FORM{lc} eq ''){&error(206,'(12)�y�[�W�̃����N�F');}
if($FORM{vc} eq ''){&error(206,'(13)�y�[�W�̊��K�⃊���N�F');}
if($FORM{tbdh} eq ''){&error(206,'(14)���j���[�y�[�W�̕\�̘g�̍���');}
elsif($FORM{tbdh} =~/\D/){&error(305,'(14)���j���[�y�[�W�̕\�̘g�̍���');}
if($FORM{tbd} eq ''){&error(206,'(15)���j���[�y�[�W�̕\�̘g�̕�');}
elsif($FORM{tbd} =~/\D/){&error(305,'(15)���j���[�y�[�W�̕\�̘g�̕�');}
if($FORM{tbdi} eq ''){&error(206,'(16)���j���[�y�[�W�̕\�̘g�̓���');}
elsif($FORM{tbdi} =~/\D/){&error(305,'(16)���j���[�y�[�W�̕\�̘g�̓���');}
if($FORM{ag} eq ''){&error(206,'(17)���ї����O���t�摜�P');}
elsif(&ch_file_format($FORM{ag})){&error(305,'(17)���ї����O���t�摜�P');}
else{&ch_file_exist('(17)���ї����O���t�摜�P',$FORM{ag});}
if($FORM{bg} eq ''){&error(206,'(18)���ї����O���t�摜�Q');}
elsif(&ch_file_format($FORM{bg})){&error(305,'(18)���ї����O���t�摜�Q');}
else{&ch_file_exist('(18)���ї����O���t�摜�Q',$FORM{bg});}
if(!mygrep($FORM{al},('l','c','r'))){&error(402,'(19)�\�̃��C�A�E�g');}
if(!mygrep($FORM{wal},('l','c','r'))){&error(402,'(20)�\���������C�A�E�g');}
if($error eq $error_mes){
if($FORM{edittype} ne 'edit'){
push(@sysdesign_list,$FORM{sdt});
}else{
$i=0;
foreach $id(@sysdesign_list){
if($id eq $FORM{id}){
$sysdesign_list[$i] = $FORM{sdt};
last;
}
$i++;
}
}
return 0;
}else{return 1;}
}
#************************************************
# �W�������f�U�C���ݒ�ҏW���̃p�����[�^�`�F�b�N
#************************************************
sub ch_design_palam{
local(@return,$error);
$error=$error_mes;
if($FORM{gdt} eq ''){&error(207,'(2)�W�������f�U�C����');}
foreach $id(@design_list){
if($id eq $FORM{gdt} && $FORM{edittype} ne 'edit'){
&error(855,'(2)�W�������f�U�C����');
}elsif($id eq $FORM{gdt} && $FORM{gdt} ne $FORM{id} && $FORM{edittype} eq 'edit'){
&error(856,'(2)�W�������f�U�C����');
}
}
if($FORM{gtc} eq ''){&error(207,'(3)�����F');}
if($FORM{glc} eq ''){&error(207,'(4)�����N�����F');}
if($FORM{gvc} eq ''){&error(207,'(5)���K�⃊���N�����F');}
if($FORM{gcc} eq ''){&error(207,'(6)�a������ҐF');}
if($FORM{gmc} eq ''){&error(207,'(7)��{�w�i�F');}
if($FORM{gwi} eq ''){&error(207,'(8)�������w�i�F');}
if($FORM{glo} eq ''){&error(207,'(9)�s�������w�i�F');}
if($FORM{gcm} eq ''){&error(207,'(10)���E�C���h�E�̐F');}
if($FORM{thc} eq ''){&error(207,'(11)�\�̃w�b�_�[�F');}
if($FORM{tdc} eq ''){&error(207,'(12)�\�̐F');}
if($FORM{bdc} eq ''){&error(207,'(13)�\�̘g�̐F');}
if($FORM{bdh} eq ''){&error(207,'(14)�\�̘g�̍���');}
elsif($FORM{bdh} =~/\D/){&error(306,'(14)�\�̘g�̍���');}
if($FORM{bd} eq ''){&error(207,'(15)�\�̘g�̕�');}
elsif($FORM{bd} =~/\D/){&error(306,'(15)�\�̘g�̕�');}
if($FORM{bdi} eq ''){&error(207,'(16)�\�̘g�̓���');}
elsif($FORM{bdi} =~/\D/){&error(306,'(16)�\�̘g�̓���');}
if(($FORM{gw} ne '')&& (&ch_file_format($FORM{gw}))){&error(104,'(17)��{�ǎ�');}
elsif($FORM{gw} ne ''){&ch_file_exist('(17)��{�ǎ�',$FORM{gw});}
if(($FORM{gww} ne '')&& (&ch_file_format($FORM{gww}))){&error(104,'(18)�������ǎ�');}
elsif($FORM{gww} ne ''){&ch_file_exist('(18)�������ǎ�',$FORM{gww});}
if(($FORM{glw} ne '')&& (&ch_file_format($FORM{glw}))){&error(104,'(19)�s�������ǎ�');}
elsif($FORM{glw} ne ''){&ch_file_exist('(19)�s�������ǎ�',$FORM{glw});}
if($FORM{wsg} eq ''){&error(207,'(20)����\��');}
if($FORM{lsg} eq ''){&error(207,'(21)�s����\��');}
if($FORM{osg} eq ''){&error(207,'(22)�^�C���I�[�o�[�\��');}
if(($FORM{wmd} ne '')&& (&ch_file_format($FORM{wmd}))){&error(104,'(23)������MIDI');}
elsif($FORM{wmd} ne ''){&ch_file_exist('(23)������MIDI',$FORM{wmd});}
if(($FORM{lmd} ne '')&& (&ch_file_format($FORM{lmd}))){&error(104,'(24)�s������MIDI');}
elsif($FORM{lmd} ne ''){&ch_file_exist('(24)�s������MIDI',$FORM{lmd});}
if(($FORM{emd} ne '')&& (&ch_file_format($FORM{emd}))){&error(104,'(25)�N�C�Y�I����MIDI');}
elsif($FORM{emd} ne ''){&ch_file_exist('(25)�N�C�Y�I����MIDI',$FORM{emd});}
if(($FORM{hmd} ne '')&& (&ch_file_format($FORM{hmd}))){&error(104,'(26)�����юҗpMIDI');}
elsif($FORM{hmd} ne ''){&ch_file_exist('(26)�����юҗpMIDI',$FORM{hmd});}
if($error eq $error_mes){
if($FORM{edittype} ne 'edit'){
push(@design_list,$FORM{gdt});
}else{
$i=0;
foreach $id(@design_list){
if($id eq $FORM{id}){
$design_list[$i] = $FORM{gdt};
last;
}
$i++;
}
}
return 0;
}else{return 1;}
}
#************************************************
# �I�������b�Z�[�W�ҏW�̃p�����[�^�`�F�b�N
#************************************************
sub ch_edit_mes_param{
for($i=0;$i<$FORM{mn};$i++){
if($FORM{"per-$i"} eq ''){next;}
if(($FORM{"per-$i"}<0.00000001)||($FORM{"per-$i"}>100)){
&error(531,'���𗦂̎w��');
return 1;
}
}
return 0;
}
#************************************************
# �W�������ҏW���̃p�����[�^�`�F�b�N
#************************************************
sub ch_edit_genre_palam{
$error=$error_mes;
$FORM{"md-$FORM{md}"}=' checked';
$FORM{"me-$FORM{me}"}=' checked';
$FORM{"nt-$FORM{nt}"}     =' checked';
$FORM{"dc-$FORM{dc}"}     =' checked';
$FORM{"ath-$FORM{ath}"} =' checked';
$FORM{"sa1-$FORM{sa1}"}=' checked';$FORM{"sa2-$FORM{sa2}"}=' checked';
$FORM{"r1-$FORM{r1}"}=' checked';$FORM{"r2-$FORM{r2}"}=' checked';
$FORM{"qm1-$FORM{qm1}"}=' checked';$FORM{"qm2-$FORM{qm2}"}=' checked';
$FORM{"pm1-$FORM{pm1}"}=' checked';$FORM{"pm2-$FORM{pm2}"}=' checked';
$FORM{"lm1-$FORM{lm1}"}=' checked';$FORM{"lm2-$FORM{lm2}"}=' checked';
$FORM{"tl1-$FORM{tl1}"}=' checked';$FORM{"tl2-$FORM{tl2}"}=' checked';
$FORM{"dl1-$FORM{dl1}"}=' checked';$FORM{"dl2-$FORM{dl2}"}=' checked';
$FORM{"nl1-$FORM{nl1}"}=' checked';$FORM{"nl2-$FORM{nl2}"}=' checked';
$FORM{"dh1-$FORM{dh1}"}=' checked';$FORM{"dh2-$FORM{dh2}"}=' checked';
$FORM{"bd1-$FORM{bd1}"}=' checked';$FORM{"bd2-$FORM{bd2}"}=' checked';
$FORM{"hbu1-$FORM{hbu1}"}=' checked';$FORM{"hbu2-$FORM{hbu2}"}=' checked';
$FORM{"hbw1-$FORM{hbw1}"}=' checked';$FORM{"hbw2-$FORM{hbw2}"}=' checked';
$FORM{"sbu1-$FORM{sbu1}"}=' checked';$FORM{"sbu2-$FORM{sbu2}"}=' checked';
$FORM{"sbw1-$FORM{sbw1}"}=' checked';$FORM{"sbw2-$FORM{sbw2}"}=' checked';
$FORM{"rc1-$FORM{rc1}"}=' checked';$FORM{"rc2-$FORM{rc2}"}=' checked';
if($FORM{qm} eq 1){$FORM{'qm-2'}='';}
if($FORM{pm} eq 1){$FORM{'pm-2'}='';}
if($FORM{lm} eq 1){$FORM{'lm-2'}='';}
if($FORM{dl} eq 1){$FORM{'dl-2'}='';}
if($FORM{nl} eq 1){$FORM{'nl-2'}='';}
if($FORM{t} eq ''){&error(208,'(2)�^�C�g��');}
if(!mygrep($FORM{md},(0,1))){&error(403,"(5)���t�@�C��");}
elsif($FORM{md} eq 1){
foreach(@genre_dir_orign){
if(($dir eq $_)||($mondai_cgi{$_} eq '.')||($mondai_cgi{$_} =~ /\//)){next;}
if(!($FORM{"smd-$_"} =~ /\d/)&&($FORM{"smd-$_"} ne 'all')){&error(304,'(5)���t�@�C��');last;}
}
}
if(!mygrep($FORM{me},(0,1))){&error(403,'(6)�W�������̓�����');}
if(!mygrep($FORM{ct},(0,1))){&error(403,'(7)���e���̎�t');}
if(!mygrep($FORM{nt},(0,1))){&error(403,'(8)�e�L�X�g�`���̓��e���');}
if(!mygrep($FORM{dc},(0,1))){&error(403,'(9)���e���̎����̗p');}
if(!mygrep($FORM{ath},(0,1))){&error(403,'(11��蕶�ւ̍쐬�ҕ\��');}
if($FORM{mn1} eq ''){&error(208,'(13)���[�h�P�̖��O');}
if(!mygrep($FORM{sa1},(0,1))){&error(403,'(14)���[�h�P����\��');}
if(!mygrep($FORM{r1},(0,1))){&error(403,'(15)���[�h�P�o�菇��');}
if(!mygrep($FORM{qm1},(0,1))){&error(403,'(16)���[�h�P�g�p��萔');}
elsif(($FORM{qm1} eq '0')&&($FORM{'qm1-2'} eq '')){&error(208,'(16)���[�h�P�g�p��萔');}
elsif(($FORM{qm1} eq '0')&&($FORM{'qm1-2'}=~ /\D/)){&error(304,'(16)���[�h�P�g�p��萔');}
if(!mygrep($FORM{pm1},(0,1))){&error(403,'(17)���[�h�P�o���萔');}
elsif(($FORM{pm1} eq '0')&&($FORM{'pm1-2'} eq '')){&error(208,'(17)���[�h�P�o���萔');}
elsif(($FORM{pm1} eq '0')&&($FORM{'pm1-2'}=~ /\D/)){&error(304,'(17)���[�h�P�o���萔');}
if(!mygrep($FORM{bd1},(0,1))){&error(403,'(18)���[�h�P�ꊇ�o��');}
if(!mygrep($FORM{lm1},(0,1))){&error(403,'(19)���[�h�P�I�������듚��');}
elsif(($FORM{lm1} eq '0')&&($FORM{'lm1-2'} eq '')){&error(208,'(19)���[�h�P�I�������듚��');}
elsif(($FORM{lm1} eq '0')&&($FORM{'lm1-2'}=~ /\D/)){&error(304,'(19)���[�h�P�I�������듚��');}
if(!mygrep($FORM{tl1},(0,1))){&error(403,'(20)���[�h�P��������');}
elsif(($FORM{tl1} eq '0')&&($FORM{'tl1-2'} eq '')){&error(208,'(20)���[�h�P��������');}
elsif(($FORM{tl1} eq '0')&&($FORM{'tl1-2'}=~ /\D/)){&error(304,'(20)���[�h�P��������');}
if($FORM{hb1} eq ''){&error(208,'(21)���[�h�P���i�_');}
elsif($FORM{hb1} =~ /\D/){&error(304,'(21)���[�h�P���i�_');}
if(!mygrep($FORM{hbu1},(0,1))){&error(403,'(22)�����ю҂�BACK UP');}
elsif(($FORM{hbu1} eq '1')&&($FORM{'hbu1-2'} eq '')){&error(208,'(22)�����ю҂�BACK UP�Ԋu(��)');}
elsif(($FORM{hbu1} eq '1')&&($FORM{'hbu1-2'}=~ /\D/)){&error(304,'(22)�����ю҂�BACK UP�Ԋu(��)');}
if(!mygrep($FORM{hbw1},(0,1))){&error(403,'(23)�����ю҂�BACK UP����');}
if(!mygrep($FORM{sbu1},(0,1))){&error(403,'(24)���ѕ��z��BACK UP');}
elsif(($FORM{sbu1} eq '1')&&($FORM{'sbu1-2'} eq '')){&error(208,'(24)���ѕ��z��BACK UP�Ԋu(��)');}
elsif(($FORM{sbu1} eq '1')&&($FORM{'sbu1-2'}=~ /\D/)){&error(304,'(24)���ѕ��z��BACK UP�Ԋu(��)');}
if(!mygrep($FORM{sbw1},(0,1))){&error(403,'(25)���ѕ��z��BACK UP����');}
if($FORM{gb1} eq ''){&error(208,'(26)���[�h�P���ѕ��z�ȗ��\\��');}
elsif($FORM{gb1} =~ /\D/){&error(304,'(26)���[�h�P���ѕ��z�ȗ��\\��');}
if($FORM{hd1} eq ''){&error(208,'(27)���[�h�P���ѕ��z�W�v�P��');}
elsif($FORM{hd1} =~ /\D/){&error(304,'(27)���[�h�P���ѕ��z�W�v�P��');}
if(!mygrep($FORM{dl1},(0,1))){&error(403,'(28)���[�h�P�����юғ�������');}
elsif(($FORM{dl1} eq '0')&&($FORM{'dl1-2'} eq '')){&error(208,'(28)���[�h�P�����юғ�������');}
elsif(($FORM{dl1} eq '0')&&($FORM{'dl1-2'}=~ /\D/)){&error(304,'(28)���[�h�P�����юғ�������');}
if(!mygrep($FORM{nl1},(0,1))){&error(403,'(29)���[�h�P�����юҐl������');}
elsif(($FORM{nl1} eq '0')&&($FORM{'nl1-2'} eq '')){&error(208,'(29)���[�h�P�����юҐl������');}
elsif(($FORM{nl1} eq '0')&&($FORM{'nl1-2'}=~ /\D/)){&error(304,'(29)���[�h�P�����юҐl������');}
if($FORM{no1} eq ''){&error(208,'(30)���[�h�P�a������l��');}
elsif($FORM{no1} =~ /\D/){&error(304,'(30)���[�h�P�a������l��');}
if(!mygrep($FORM{rc1},(0,1))){&error(403,'(31)���[�h�P�����ю҃R�����g�L�^');}
if(!mygrep($FORM{dh1},(0,1))){&error(403,'(32)���[�h�P���z�X�g���X�R�A');}
if($FORM{mn2} ne ''){
if(!mygrep($FORM{sa2},(0,1))){&error(403,'(34)���[�h�P����\��');}
if(!mygrep($FORM{r2},(0,1))){&error(403,'(35)���[�h�P�o�菇��');}
if(!mygrep($FORM{qm2},(0,1))){&error(403,'(36)���[�h�P�g�p��萔');}
elsif(($FORM{qm2} eq '0')&&($FORM{'qm2-2'} eq '')){&error(208,'(36)���[�h�P�g�p��萔');}
elsif(($FORM{qm2} eq '0')&&($FORM{'qm2-2'}=~ /\D/)){&error(304,'(36)���[�h�P�g�p��萔');}
if(!mygrep($FORM{pm2},(0,1))){&error(403,'(37)���[�h�P�o���萔');}
elsif(($FORM{pm2} eq '0')&&($FORM{'pm2-2'} eq '')){&error(208,'(37)���[�h�P�o���萔');}
elsif(($FORM{pm2} eq '0')&&($FORM{'pm2-2'}=~ /\D/)){&error(304,'(37)���[�h�P�o���萔');}
if(!mygrep($FORM{bd2},(0,1))){&error(403,'(38)���[�h�P�ꊇ�o��');}
if(!mygrep($FORM{lm2},(0,1))){&error(403,'(39)���[�h�P�I�������듚��');}
elsif(($FORM{lm2} eq '0')&&($FORM{'lm2-2'} eq '')){&error(208,'(39)���[�h�P�I�������듚��');}
elsif(($FORM{lm2} eq '0')&&($FORM{'lm2-2'}=~ /\D/)){&error(304,'(39)���[�h�P�I�������듚��');}
if(!mygrep($FORM{tl2},(0,1))){&error(403,'(40)���[�h�P��������');}
elsif(($FORM{tl2} eq '0')&&($FORM{'tl2-2'} eq '')){&error(208,'(40)���[�h�P��������');}
elsif(($FORM{tl2} eq '0')&&($FORM{'tl2-2'}=~ /\D/)){&error(304,'(40)���[�h�P��������');}
if($FORM{hb2} eq ''){&error(208,'(41)���[�h�P���i�_');}
elsif($FORM{hb2} =~ /\D/){&error(304,'(41)���[�h�P���i�_');}
if(!mygrep($FORM{hbu2},(0,1))){&error(403,'(42)�����ю҂�BACK UP');}
elsif(($FORM{hbu2} eq '1')&&($FORM{'hbu2-2'} eq '')){&error(208,'(42)�����ю҂�BACK UP�Ԋu(��)');}
elsif(($FORM{hbu2} eq '1')&&($FORM{'hbu2-2'}=~ /\D/)){&error(304,'(42)�����ю҂�BACK UP�Ԋu(��)');}
if(!mygrep($FORM{hbw2},(0,1))){&error(403,'(43)�����ю҂�BACK UP����');}
if(!mygrep($FORM{sbu2},(0,1))){&error(403,'(44)���ѕ��z��BACK UP');}
elsif(($FORM{sbu2} eq '1')&&($FORM{'sbu2-2'} eq '')){&error(208,'(44)���ѕ��z��BACK UP�Ԋu(��)');}
elsif(($FORM{sbu2} eq '1')&&($FORM{'sbu2-2'}=~ /\D/)){&error(304,'(44)���ѕ��z��BACK UP�Ԋu(��)');}
if(!mygrep($FORM{sbw2},(0,1))){&error(403,'(45)���ѕ��z��BACK UP����');}
if($FORM{gb2} eq ''){&error(208,'(46)���[�h�P���ѕ��z�ȗ��\\��');}
elsif($FORM{gb2} =~ /\D/){&error(304,'(46)���[�h�P���ѕ��z�ȗ��\\��');}
if($FORM{hd2} eq ''){&error(208,'(47)���[�h�P���ѕ��z�W�v�P��');}
elsif($FORM{hd2} =~ /\D/){&error(304,'(47)���[�h�P���ѕ��z�W�v�P��');}
if(!mygrep($FORM{dl2},(0,1))){&error(403,'(48)���[�h�P�����юғ�������');}
elsif(($FORM{dl2} eq '0')&&($FORM{'dl2-2'} eq '')){&error(208,'(48)���[�h�P�����юғ�������');}
elsif(($FORM{dl2} eq '0')&&($FORM{'dl2-2'}=~ /\D/)){&error(304,'(48)���[�h�P�����юғ�������');}
if(!mygrep($FORM{nl2},(0,1))){&error(403,'(49)���[�h�P�����юҐl������');}
elsif(($FORM{nl2} eq '0')&&($FORM{'nl2-2'} eq '')){&error(208,'(49)���[�h�P�����юҐl������');}
elsif(($FORM{nl2} eq '0')&&($FORM{'nl2-2'}=~ /\D/)){&error(304,'(49)���[�h�P�����юҐl������');}
if($FORM{no2} eq ''){&error(208,'(50)���[�h�P�a������l��');}
elsif($FORM{no2} =~ /\D/){&error(304,'(50)���[�h�P�a������l��');}
if(!mygrep($FORM{rc2},(0,1))){&error(403,'(51)���[�h�P�����ю҃R�����g�L�^');}
if(!mygrep($FORM{dh2},(0,1))){&error(403,'(52)���[�h�P���z�X�g���X�R�A');}
}
if($error eq $error_mes){return 0;}
else{return 1;}
}
#************************************************
# �A�N�Z�X����IP�`�F�b�N
#************************************************
sub ch_guard_ip{
open(DB,$guard_cgi);
@list=<DB>;
close(DB);
if($list[0] eq "guard\n"){
$guard=1;
$permit=0;
$list[0]='';
}elsif($list[0] eq "permit\n"){
$guard=0;
$permit=1;
$list[0]='';
}else{
$guard=1;
$permit=0;
}
foreach $line(@list){
$line=~ s/\n//g;
$line=~ s/ //g;
if($line eq ''){next;}
if($ip =~ /^$line/){
return $guard;
}
}
return $permit;
}
#************************************************
# �V�X�e���t�@�C���̏�������
#************************************************
sub write_system_dat{
return &write_file($system_cgi,&sys_to_system_dat);
}
#************************************************
# �W�������t�@�C���̏�������
#************************************************
sub write_genre_dat{
local($value);
$value = "ver2\n";
foreach $dir(@genre_dir_all){
if($dir ne ''){$value .= &genre_array_to_line($dir);}
}
return &write_file($genre_cgi,$value);
}
#************************************************
# �f�U�C���t�@�C���̏�������
#************************************************
sub write_design_dat{
local($value);
$value = "ver2\n";
foreach $id(@design_list){
if($id ne ''){$value .= &design_array_to_line($id);}
}
return &write_file($design_cgi,$value);
}
#************************************************
# �V�X�e���f�U�C���t�@�C���̏�������
#************************************************
sub write_sysdesign_dat{
local($value);
$value = "ver2\n";
foreach $id(@sysdesign_list){
if($id ne '' && $sysdesign_title{$id} ne ''){$value .= &sysdesign_array_to_line($id);}
}
return &write_file($sysdesign_cgi,$value);
}
#************************************************
# ���t�@�C���㏑������
#************************************************
sub write_mondai{
local(@lines);
local($file_name) = @_;
$i=0;$j=0;
foreach(@mondai){
if($mondai[$i] ne ''){
$j++;
push(@lines,&quiz_to_line($i,$j));
}
$i++;
}
if(&ch_dir_exist('�f�B���N�g����',$FORM{d})){return 1;}
return &write_file("$FORM{d}/$file_name",@lines);
}
