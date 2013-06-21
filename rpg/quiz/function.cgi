#!/usr/bin/perl
$version='2.03';
#************************************************
# 変数初期設定
#************************************************
sub setup{
$mod_cgi='0705';#CGIスクリプトファイルのパーミッション
$mod_dat='0600';#データファイルのパーミッション
$mod_dir='0701';#ディレクトリのパーミッション
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
$_try='挑戦';
$_underconst='工事中';
$_high='高成績者';
$_graph='成績分布';
$_score='出題状況';
$_add='問題投稿';
$_imode='携帯専用';
$_op='管理人室';
$_top='TOP';
}
#************************************************
# パスワードのチェック
#************************************************
sub ch_pwd{
local($pass)=@_;
open(DB,$pass_cgi);@line=<DB>;close(DB);
$line[0]=~ s/\n//g;
if(crypt($pass,"ARRAY(0xb74f5c)") ne $line[0]){return 1;}
else{return 0;}
}
#************************************************
# アドレスチェック関数
# 引数から、４桁一定の数字を返します。
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
# クイズ初期化関数
#************************************************
sub refresh_quiz{
(@mondai,@ans,@misans1,@misans2,@misans3,@misans4,@anscom,@misanscom,@cf,@digest,@misanscom1,@misanscom2,@misanscom3,@misanscom4,@anstype,@author)=();
}
#************************************************
# ファイルサイズを返す(kb)
#************************************************
sub file_size_kb{
local($file_name)=@_;
local($mon_size)=-s $file_name;
local($mon_size2)=int($mon_size/1024);
if(0 < $mon_size % 1024){$mon_size2++;}
return $mon_size2;
}
#************************************************
# system.datを新規作成処理
#************************************************
sub make_new_system_dat{
&def_sys;
return &write_system_dat;
}
#************************************************
# クイズで使用するジャンルリストを生成する
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
# 問題番号から、ジャンル名を取得する
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
# MAX最適化関数
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
# html出力用に引数１を変換し引数２に格納
#************************************************
sub conv_for_html{
$_[0]=$_[1];
$_[0]=~ s/</&lt;/g;
$_[0]=~ s/>/&gt;/g;
$_[0]=~ s/"/&quot;/g;
@_;
}
#************************************************
# html出力用に%FORMを変換し%FORM2に格納
#************************************************
sub form_to_form2{
foreach $pal(@_){&conv_for_html($FORM2{$pal},$FORM{$pal});}
}
#************************************************
# 改行タグを改行に変換し%FORM3に格納
#************************************************
sub form_to_form3{
foreach $pal(@_){
$FORM3{$pal}=$FORM{$pal};
$FORM3{$pal}=~ s/<br>/\n/g;
&conv_for_html($FORM3{$pal},$FORM3{$pal});
}
}
#************************************************
# 改行を改行タグに変換し%FORM4に格納
#************************************************
sub form_to_form4{
foreach $pal(@_){
$FORM4{$pal}=$FORM{$pal};
$FORM4{$pal}=~ s/\n/<br>/g;
}
}
#************************************************
# 改行を削除し%FORM5に格納
#************************************************
sub form_to_form5{
foreach $pal(@_){
$FORM5{$pal}=$FORM{$pal};
$FORM5{$pal}=~ s/\n//g;
}
}
#************************************************
# FORMからの入力値のバリエーションフォーマットの作成
#************************************************
sub form_to_form{
foreach(keys %FORM){
&form_to_form2($_);
&form_to_form3($_);
&form_to_form4($_);
}
}
#************************************************
# FORM変数をクリア
#************************************************
sub clear_form{
foreach $pal(@_){
($FORM{$pal},$FORM2{$pal},$FORM3{$pal},$FORM4{$pal})=();
}
}
#************************************************
# ファイルへの書き込み
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
# 時刻表記関数
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
# スコア用時刻表記関数
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
# パーミッション表示処理
#************************************************
sub permition {
local(@permit)=('---','--x','-w-','-wx','r--','r-x','rw-','rwx');
return "\($permit[substr($_,length($_[0])-3,1)]$permit[substr($_,length($_[0])-2,1)]$permit[substr($_,length($_[0])-1,1)]\)";
}
#************************************************
# フォーカス移動スクリプト生成
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
# メッセージ表示処理
#************************************************
sub mes {
$mesno="　 message($_[0])";
if (!($_[0] =~ /^\d+$/)){
$system_mes .= $_[0];
$mesno='';
}elsif ($_[0] <= 149) {
$system_mes .= "$_[1]の新規作成が正常に終了しました。";
}elsif ($_[0] <= 199) {
$system_mes .= "$_[1]の追加が正常に終了しました。";
}elsif ($_[0] <= 249) {
$system_mes .= "$_[1]の編集が正常に終了しました。";
}elsif ($_[0] <= 299) {
$system_mes .= "$_[1]の削除、順序変更が正常に終了しました。";
}elsif ($_[0] <= 349) {
$system_mes .= "$_[1]の削除が正常に終了しました。";
}elsif ($_[0] <= 399) {
$system_mes .= "$_[1]の一括追加が正常に終了しました。";
}elsif ($_[0] <= 449) {
$system_mes .= "$_[1]の順序変更が正常に終了しました。";
}elsif ($_[0] <= 499) {
$system_mes .= "$_[1]の自動作成が正常に終了しました。";
}elsif ($_[0] <= 549) {
$system_mes .= "$_[1]を問題ファイルに追加しました。";
}elsif ($_[0] <= 599) {
$system_mes .= "$_[1]を問題ファイルに追加しました。";
}elsif ($_[0] <= 649) {
$system_mes .= "$_[1]の一括追加が正常に終了しました。";
}elsif ($_[0] <= 699) {
$system_mes .= "$_[1]の一括追加が正常に終了しました。";
}elsif ($_[0] <= 749) {
$system_mes .= "$_[1]の一括追加が正常に終了しました。";
}elsif ($_[0] <= 999) {
$system_mes .= "$_[1]";
}
$system_mes .="$mesno<br><br>";
}
#************************************************
# メッセージ表示処理
#************************************************
sub mes_html {
if($system_mes ne ''){
return <<"_HTML_";
<table $sys_tbl_opt bgcolor="#eeeeaa"><tr><td>
<center><big><b>■■■システムメッセージ■■■<br></b><big><br>
<table border=0><tr><td><span><b>$system_mes</b></span></td></tr></table>
</center>
</td></tr></table><br>
_HTML_
}
}
#************************************************
# 小数点位統一関数
#************************************************
sub point {
local($num,$point)=@_;
local($over,$under)=split(/\./,$num);
$under=substr($under,0,$point);
$under=$under . '0' x ($point - length($under));
return "$over.$under";
}
#************************************************
# フッタ表示処理
#_HTML_と_HTML_とのあいだに
#クイズのページのフッター部分のHTMLを記入してください。
#普通のHTML表記でかまいません。
#その際、著作権表記は消さないでください。
#************************************************
sub footer_html {
$footer_html = <<"_HTML_";
<hr width="100%"><div align=right><span>
<a href="http://ha1.seikyou.ne.jp/home/jun/" target="_parent">qqq systems Ver$version</a></span>
</div></body></html>
_HTML_
}
#************************************************
# 出題状況表示処理
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
@mon_name=('正解','誤答１','誤答２','誤答３','誤答４');
if($FORM{item} eq 'list'){
$per[int($QU{win_ratio}/5)]++;
}elsif($type eq 'op'){
$dumy=$quiz_index+1;
$value=<<"_HTML_";
<table width="80%"border=0 cellpadding=0 cellspacing=0 bgcolor="$bdc"><tr><td>
<table $opt>
<tr><td$td colspan=4>
Ｑ$dumy\．$mondai_str
</td></tr>
<tr><td$td colspan=4>
$QU{play_num}人中$QU{play_win}人正解　正解時間 $QU{ave2}秒
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
$value=$value."<tr><td$td nowrap>$mon_name[$i]</td><td$td nowrap>$qu[$i]人</td><td$td nowrap>$per％</td><td$td width=100%>$ans_list[$i]</td></tr>\n"
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
$value=$value."<tr><td$td nowrap>誤答(その他)</td><td$td nowrap>$qu_else人</td><td$td nowrap>$per％</td><td$td width=100%>　</td></tr>\n"
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
<td bgcolor='$td_color' nowrap>Ｑ$dumy．</td>
<td bgcolor='$td_color' nowrap>$QU{play_num}人中$QU{play_win}人正解</td>
<td bgcolor='$td_color' nowrap>$QU{win_ratio}％</td>
<td bgcolor='$td_color' nowrap>$QU{ave2}秒</td>
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
<br><span><b>■$_score情報■</b></span>
$align1
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$bdc"><tr><td>
<table $opt>
<tr><td$th><small>総問題数</small></td>
<td$td width=100%><small>$walign1$quiz_max問$walign2</small></td></tr>
<tr><td$th><small>総出題回数</small></td>
<td$td><small>$walign1$QU_ALL{play_num}回$walign2</small></td></tr>
<tr><td$th><small>総正解回数</small></td>
<td$td><small>$walign1$QU_ALL{play_win}回$walign2</small></td></tr>
<tr><td$th nowrap><small>平均正解時間</small></td>
<td$td><small>$walign1$QU_ALL{ave2}秒$walign2</small></td></tr>
<tr><td$th><small>総正解率</small></td>
<td$td><small>$walign1$QU_ALL{win_ratio}％$walign2</small></td></tr></table>
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
<option value=mon$FORM{'item-mon'}>問題番号順
<option value=num$FORM{'item-num'}>出題数順
<option value=aper$FORM{'item-aper'}>正解率順
<option value=time$FORM{'item-time'}>正解時間順
<option value=list$FORM{'item-list'}>正解率分布
<option value=auth$FORM{'item-auth'}>作成者
</select></td>
<td$td><select name=sort>
<option value=up$FORM{'sort-up'}>昇順
<option value=down$FORM{'sort-down'}>降順
</select></td>
<td$td>
<input type=submit value=表\示>
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
if($#genre_dir_use > 1){$genre_name="<td nowrap bgcolor='$th_color'>ジャンル</td>";}
else{$genre_name='';}
if($FORM{item} eq 'list'){
$main_html.='■正解率分布■';
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
$main_html.="<tr><td$th nowrap>$from\%-$to\%</td><td$td nowrap><img src='$SYS{b_gif}' width='$width' height='$graph_h'> $per[$i]問\($rate％\)</td></tr>";
}else{
$main_html.="<tr><td$th nowrap>$from\%</td><td$td nowrap><img src='$SYS{b_gif}' width='$width' height='$graph_h'> $per[$i]問\($rate％\)</td></tr>";
}
}
$main_html.='</table></td></tr></table>';
}elsif($type ne 'op'){
$main_html.=<<"_HTML_";
<table width="80%"border=0 cellpadding=0 cellspacing=0 bgcolor="$bdc"><tr><td>
<table $opt><tr>
<td nowrap bgcolor="$th_color">問題番号</td>
<td nowrap bgcolor="$th_color">成績</td>
<td nowrap bgcolor="$th_color">正解率</td>
<td nowrap bgcolor="$th_color">正解時間</td>
<td nowrap bgcolor="$th_color">作成者</td>
<td nowrap bgcolor="$th_color">問題内容</td>
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
# 引数のうち最大数を返す。
#************************************************
sub max{
local(@list)=@_;
local($max);$max=$list[0];
foreach(@list[1..$#list]){if($max < $_){$max = $_;}}
return $max;
}
#************************************************
# 引数のうち最大数を返す。
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
# エラー表示処理
#************************************************
sub error {
local($errno);
$errno="　 error($_[0])";
if (!($_[0] =~ /^\d+$/)){
$error_mes .= $_[0];
$errno='';
}elsif ($_[0] <= 199) {
$error_mes .= "$_[1]が不正です。";
}elsif ($_[0] <= 299) {
$error_mes .= "$_[1]が入力されていません";
}elsif ($_[0] <= 399) {
$error_mes .= "$_[1]が不正です。半角数字を入力してください";
}elsif ($_[0] <= 499) {
$error_mes .= "$_[1]が正しく選択されていません";
}elsif ($_[0] <= 509) {
$error_mes .= "$_[1]は半角で$max_en文字までです。<br>$_[1]が長すぎます。<br>登録できませんでした。";
}elsif ($_[0] <= 519) {
$error_mes .= "$_[1]は半角で$max_com文字までです。<br>$_[1]が長すぎます。<br>登録できませんでした。";
}elsif ($_[0] <= 529) {
$error_mes .= "$_[1]が長すぎます。<br>半角20文字以内で入力して下さい。";
}elsif ($_[0] <= 539) {
$error_mes .= "$_[1]が範囲外です。";
}elsif ($_[0] <= 549) {
$error_mes .= "$_[1]が一致しません。<br>再入力してください。";
}elsif ($_[0] <= 609) {
$error_mes .= 'ずるをした可能性があります。正常に処理されませんでした。<br><br>なお、管理者が作業を行っていた可能性があります。しばらくしてからリロードしてみて下さい。';
}elsif ($_[0] <= 619) {
$error_mes .= 'このジャンルでは、より多くの方に登録していただくために、<br>同一IPアドレスによる同一スコアの登録は出来ません。';
}elsif ($_[0] <= 629) {
$error_mes .= "このハイスコアは、上位$num_limit人をのスコアを記録しています。<br>残念ながらこの記録は登録できませんでした。";
}elsif ($_[0] <= 639) {
$error_mes .= 'すでにこの記録は登録されています。登録出来ませんでした。';
}elsif ($_[0] <= 649) {
$error_mes .= 'このクイズは、高成績者を登録できません。';
}elsif ($_[0] <= 659) {
$error_mes .= "このクイズは現在$_underconstです。\nまたのおこしをお待ちしています。";
}elsif ($_[0] <= 669) {
$error_mes .= "現在同時プレイ人数限度$SYS{max_player}人がプレイ中です。<br>しばらくしてからお越しください。";
}elsif ($_[0] <= 679) {
$error_mes .= '登録された問題がありません。<br><br>しばらくしてから、またお越しください。';
}elsif ($_[0] <= 689) {
$error_mes .= 'クイズのジャンルが登録されていません。';
}elsif ($_[0] <= 699) {
$error_mes .= 'このジャンルは、問題が未登録です。';
}elsif ($_[0] <= 709) {
$error_mes .= 'このジャンルは、問題ファイルがありません。';
}elsif ($_[0] <= 719) {
$error_mes .= 'システムファイルの読み込みに失敗しました。<br>管理者にお問い合わせ下さい。';
}elsif ($_[0] <= 729) {
$error_mes .= 'ジャンルファイルの読み込みに失敗しました。<br>管理者にお問い合わせ下さい。';
}elsif ($_[0] <= 739) {
local($permition);
$permition=&permition($mod_dir);
$error_mes .="$_[1]を自動作成できませんでした。<br>本プログラムを設置しているディレクトリのパーティションを<br>$mod_dir$permitionにしてください。<br>なお、プロバイダの関係上パーミッションに制限があり、<br>このエラーが発生する場合は、<br>FTPを使い手動で$_[0]を作成して下さい。";
}elsif ($_[0] <= 749) {
local($permition);
$permition=&permition($mod_dat);
$error_mes .="$_[1]に書き込みができませんでした。<br>ファイルのパーティションを<br>$mod_dat$permitionにしてください。";
}elsif ($_[0] <= 759) {
$error_mes .= 'このジャンルは、問題の投稿ができません。';
}elsif ($_[0] <= 769) {
$error_mes .= '現在、高成績者は登録されていません。';
}elsif ($_[0] <= 779) {
$error_mes .= "$_[1]はすでに登録されています。";
}elsif ($_[0] <= 809) {
$error_mes .= "$_[1]が存在しません。";
}elsif ($_[0] <= 819) {
$error_mes .= "$_[1]が存在しません。ファイル構\成を確認してください。";
}elsif ($_[0] <= 829) {
$error_mes .= "$_[1]は空です";
}elsif ($_[0] <= 839) {
$error_mes .= "$_[1]は現在使用中です。<br>削除できませんでした。";
}elsif ($_[0] <= 849) {
$error_mes .= "$_[1]は使用できません。<br>別のディレクトリ名を入力してください。";
}elsif ($_[0] <= 859) {
$error_mes .= "$_[1]はすでに登録されています。<br>別の名前を入力してください。";
}elsif ($_[0] <= 869) {
$error_mes .= "$_[1]のタイムスタンプが違います。<br>作業中に変更されたか、二度送信を行った可能\性があります。<br>正しく変更されているか確認してください。";
}elsif ($_[0] <= 909) {
$error_mes .= '問題が一問も登録されませんでした。';
}elsif ($_[0] <= 919) {
$error_mes .= "$_[1]行目にエラーがあります。";
}elsif ($_[0] <= 929) {
$error_mes .= "$_[1]問目の問題文がありません。";
}elsif ($_[0] <= 939) {
$error_mes .= "$_[1]問目の正解がありません。";
}elsif ($_[0] <= 949) {
$error_mes .= "$_[1]問目の誤答１がありません。";
}else {
$error_mes .= '処理に何らかのエラーが発生し作業は中止されました。';
$errno='';
}
#$error_mes .="$errno<br><br>";
#open(DB,">>error.dat");
#print DB &time_set(time)."$error_mes\n";
#close(DB);
}
#************************************************
# エラー表示処理
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
<center><big><font color=#ff0000>◆　お知らせ　◆</font><br><br> </big>
<table border=0><tr><td><span><b>$error_mes</b></span></td></tr></table>
</center>
</td></tr></table>
</td></tr></table><br>
_HTML_
}
return $return;
}
#************************************************
# HTML出力
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
# HTML出力(携帯用)
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
# ビジー表示
#************************************************
sub busy_html{
$header_html=<<"_HTML_";
<html><head><title>ビジー</title></head><BODY bgcolor='$sys_color'>
<br><br><b>
■ファイルを読み込めませんでした■<br></b>
<br>
管理人が作業中の可能\性があります。<br>
もう一度その場でリロードしてください。<br><br><br>
_HTML_
}
#************************************************
# アクセス制限表示
#************************************************
sub guard_html{
$header_html=<<"_HTML_";
<html><head><title>アクセス制限</title></head><BODY bgcolor='$sys_color'>
<br><br><b>
■アクセスできませんでした■<br></b>
<br>
現在、管理人によりアクセス制限がかかっております。<br><br>
_HTML_
}
#************************************************
# ファイルロック
#************************************************
sub file_lock{
open(DB,">$_[0]");
close(DB);
}
#************************************************
# ファイルアンロック
#************************************************
sub file_unlock{
unlink "$_[0]";
}
#************************************************
# ロック状態をチェック。
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
# 管理人が作業中でないことをチェック
#************************************************
sub ch_sys_lock{
return &ch_lock("$data_dir/$file_lock",10);
}
#************************************************
# 管理人作業開始によるロック
#************************************************
sub sys_lock{
return &file_lock("$data_dir/$file_lock");
}
#************************************************
# 管理人作業終了によるアンロック
#************************************************
sub sys_unlock{
return &file_unlock("$data_dir/$file_lock");
}
#************************************************
# ハイスコアファイルが更新中でないことをチェック
#************************************************
sub ch_hist_lock{
local($dir_name)=@_;
return &ch_lock("$dir_name/$scorehst_cgi\.lock",10);
}
#************************************************
# ハイスコアファイルの更新開始によるロック
#************************************************
sub hist_lock{
local($dir_name)=@_;
return &file_lock("$dir_name/$scorehst_cgi\.lock");
}
#************************************************
# ハイスコアファイルの更新終了によるアンロック
#************************************************
sub hist_unlock{
local($dir_name)=@_;
return &file_unlock("$dir_name/$scorehst_cgi\.lock");
}
#************************************************
# クッキーから読み込み
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
# クッキーへ書き込み
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
}#このクッキーはだいたい3ヶ月間有効です。
#************************************************
# ファイルのバックアップ処理
#************************************************
sub backup_file{
local($file,$write,$span)=@_;
local($backuptime)=&get_recent_backuptime($file,$write);
if($now - $backuptime > $span*60*60*24){
&copy_file($file,$write);
}
}
#************************************************
# ファイルヘッダの更新時刻を更新
#************************************************
sub renew_date{
local($file_name)=@_;
open(DB,"$file_name");local(@list)=<DB>;close(DB);
if($list[0]=~ /^date/){$list[0]='';}
&write_file($file_name,('date'.time."\n",@list));
}
#************************************************
# バックアップファイルを作成
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
# バックアップファイル名を返す
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
# 最新のバックアップ時刻を取得する
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
# %SYS変数の初期値
#************************************************
sub def_sys{
$SYS{design}='デフォルトシステムデザイン';
$SYS{limit}=10;
$SYS{max_player}=50;
$SYS{cookie}='QQQ';
$SYS{quiz_form}=2;
$SYS{main_title}='無題';
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
# %SYSDESIGN変数の初期値
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
# %GENREの初期設定
#************************************************
sub def_genre {
$GENRE{design}='デフォルトジャンルデザイン';
$GENRE{title}='無題';
$GENRE{top_comment}='';
$GENRE{start_comment}='<center>$titleにようこそ。現在、挑戦者数は$challenge人です。<br>'
.'クイズの総問題数は$quiz_max問で、出題数は$play_max問ですが、<br>'
.'$lose_max問間違えるとゲームオーバーです。<br>'
.'なお制限時間は$time秒で、正答率$high％以上で合格です。<br>'
.'$champion最高成績目指してがんばってください。</center>';
$GENRE{mondai_cgi}='';
$GENRE{mente}=0;
$GENRE{cont}=1;
$GENRE{notext}=0;
$GENRE{direct_cont}=0;
$GENRE{show_digest}=1;
$GENRE{show_auth}=1;
$GENRE{mode_name1}="勝ち抜き戦モード";
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
$GENRE{mode_name2}="２０問モード";
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
# %DESIGNの初期設定
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
$DESIGN{win_sign}='<font color="blue"><big><b>正解！</b></big></font>';
$DESIGN{lose_sign}='<font color="red"><big><b>不正解！</b></big></font>';
$DESIGN{over_sign}='<font color="red"><big><b>時間オーバー！</b></big></font>';
$DESIGN{win_midi}='';
$DESIGN{lose_midi}='';
$DESIGN{end_midi}='';
$DESIGN{high_midi}='';
}
#************************************************
# プレイログの初期化
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
# 設問別成績
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
# バッファを変数に読み込む
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
# ジャンル情報ファイルを全ジャンル管理配列に読み込む
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
# デザイン情報ファイルを全デザイン管理配列に読み込む
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
# システムデザイン情報ファイルを全デザイン管理配列に読み込む
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
# %GENREを、各配列変数に読み込む
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
# %DESIGNを、各配列変数に読み込む
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
# %DESIGNを、各配列変数に読み込む
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
# 特定ジャンル情報を変数に読み込む
#************************************************
sub genre_read {
&all_genre_read;
if(!mygrep($FORM{d},@genre_dir_all)){
&error(805,'指定したジャンル');
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
# 特定デザイン情報を変数に読み込む
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
# 設定編集パラメーターの読み込み
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
# メニューページのデザインの読み込み
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
$top_tbl_opt="border='$SYS{top_border_high}' width=100% cellspacing='$SYS{top_border}' cellpadding='$SYS{top_border_in}'";#メニューページの表のオプション
if($SYS{wrap} eq 0){
$nowrap=' nowrap';
}
}
#************************************************
# プレイログを読み込む
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
# 使用ジャンル全てのクイズを読み込み
#************************************************
sub quiz_read_all{
foreach(@genre_dir_use){
$quiz_num_dir{$_}=$#mondai+1;
&quiz_read($_,$genre_num{$_},$multiquiz);
$genre_num{$_}=$#mondai + 1 - $quiz_num_dir{$_};
}
}
#************************************************
# 指定ジャンルのクイズ追加関数
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
push(@mondai,"$mondai<br><div align=right>【$title{$dir_name}】より</div>");
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
# 設問別成績ファイルの読み込み
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
# 設問別成績の計算
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
# %SYSから%FORMへ
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
# メモリ上のgenre配列を、%FORMにセットする
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
# %SYSDESIGNから%FORMへ
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
# %DESIGNから%FORMへ
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
# メモリ上の問題情報を、問題入力form用変数にセットする
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
# %FORMから%SYSへ
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
# %FORMの内容を、メモリ上のgenre配列にセットする
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
# %FORMからメモリ上のsysdesign配列にセットする
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
# %FORMからメモリ上のdesign配列にセットする
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
# dirから、genre.cgi用のログを返す
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
# idから、sysdesign.cgi用のログを返す
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
# idから、design.cgi用のログを返す
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
# %SYSからsystem.dat形式の出力
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
# 引数を、メモリ上の問題配列変数に格納
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
# 問題配列から、問題ファイル用ログを返す
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
# 終了時メッセージパラメータ読み込み
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
# 構成ファイルのチェック
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
&ch_dir_exist("$dirディレクトリ",$dir);
}
}
#************************************************
# ファイルのバージョンチェック
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
if($ver_max > $cgis_ver{$_}){$mes.="【$_】<br>";}
}
if($mes ne ''){
&mes(901,$mes.'上記のスクリプトは、最新バージョンではありません。<br>動作に支障をきたす可能性があります。');
}
}
#************************************************
# ディレクトリの名前チェックと存在確認。無ければ作成
#************************************************
sub ch_dir_exist{
local($dir_nick,$dir_name)=@_;
if($dir_name eq ''){&error(202,$dir_nick);return 1;}
if($dir_name=~ /\W/){&error(106,$dir_nick);return 1;}
if(!(-d $dir_name)){
mkdir($dir_name,$mod_dir);
chmod(oct($mod_dir),$dir_name);
if(!(-d $dir_name)){
&error(732,"$dir_nameディレクトリ");
return 2;
}
else{&mes(451,"$dir_nameディレクトリ");}
}
return 0;
}
#************************************************
# ファイルの名前チェックと存在確認。
#************************************************
sub ch_file_exist{
local($file_nick,$file_name)=@_;
if($file_name =~ /^http:\/\//){return 1;}
if(!(-f $file_name)){
&error(813,"【$file_nick】");
return 1;
}
return 0;
}
#************************************************
# ファイルスタンプチェック
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
# パスワードチェック処理
#************************************************
sub ch_pwd_html {
local(@line);
open(DB,$pass_cgi);@line=<DB>;close(DB);
$line[0]=~ s/\n//g;
if($line[0] eq ''){
if($FORM{passnew} ne ''){
if($FORM{passnew1} eq ''){
&header_html("パスワードエラー");
&error(209,'新規パスワード');
&pass_new_html;
}elsif($FORM{passnew1} ne $FORM{passnew2}){
&header_html("パスワードエラー");
&error(541,'新規パスワードと確認用パスワード');
&pass_new_html;
}else{
$pass=crypt($FORM2{passnew1},"ARRAY(0xb74f5c)");
if(&write_file($pass_cgi,$pass)){
&header_html("パスワード新規登録失敗");
}else{
&header_html("パスワード新規登録完了");
&mes(902,"管理者用パスワードを登録しました<br>パスワードを初期化したい場合は、$pass_cgiファイルを消去してください。");
}
}
}else{
&header_html("パスワード新規登録");
&pass_new_html;
}
return 1;
}elsif($FORM{passch} ne ''){
if(&ch_pwd($FORM2{passch})){
&header_html("パスワードエラー");
&error(542,'パスワード');
&pass_enter_html;
return 1;
}
}elsif($FORM{passch1} ne ''){
&header_html("パスワードエラー");
&error(209,'パスワード');
&pass_enter_html;
return 1;
}else{
&header_html("パスワード入力");
&pass_enter_html;
return 1;
}
return 0;
}
#************************************************
# ジャンル情報の存在判定
#************************************************
sub ch_genre_exist{
local($dir)=@_;
foreach(@genre_dir_all){
if(($_ ne '')&&($_ eq $dir)){return 1;}
}
return 0;
}
#************************************************
# 独自の問題ファイルを持つかどうかチェック
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
# ファイル名の妥当性チェック
#************************************************
sub ch_file_format{
unless($_[0]=~ /^[\w\$\#\~\.\/\-\?\=\&:]+$/){
return 1;
}
return 0;
}
#************************************************
# 問題追加時のパラメータチェック
#************************************************
sub ch_add_quiz_param{
if($FORM{qqu} eq ''){&error(203,'問題文');return 1;}
if($FORM{qas} eq ''){&error(203,'正解');return 1;}
if(($FORM{qmas1} eq '')&&($FORM{atype} eq '')){&error(203,'誤答１');return 1;}
return 0;
}
#************************************************
# 問題追加時の重複登録チェック
#************************************************
sub ch_duplic_quiz{
local($i);
foreach(@mondai){
if(join("\t",$mondai[$i],$ans[$i],$misans1[$i],$misans2[$i],$misans3[$i],$misans4[$i]) eq
join("\t",$FORM4{qqu},$FORM4{qas},$FORM4{qmas1},$FORM4{qmas2},$FORM4{qmas3},$FORM4{qmas4})){
&error('この問題はすでに登録されています。');return 1;
}
$i++;
}
return 0;
}
#************************************************
# 問題編集時のパラメータチェック
#************************************************
sub ch_edit_quiz_param{
local($error)=$error_mes;
if($FORM{qn} eq ''){&error(204,'問題番号');}
elsif($FORM{qn} =~/\D/){&error(302,'問題番号');}
elsif(($FORM{qn}>$#mondai+1)&&($FORM{qn}<=0)){&error(531,'問題番号');}
if($FORM{qqu} eq ''){&error(204,'問題文');}
if($FORM{qas} eq ''){&error(204,'正解');}
if(($FORM{qmas1} eq '')&&($FORM{atype} eq '')){&error(204,'誤答１');}
if($error eq $error_mes){return 0;}
else{return 1;}
}
#************************************************
# システム設定編集時のパラメータチェック
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
if($FORM{li} eq ''){&error(205,'(1)プレイログ保護期間');}
elsif($FORM{li} =~ /\D/){&error(303,'(1)プレイログ保護期間');}
if($FORM{mp} eq ''){&error(205,'(2)同時プレイ人数');}
elsif($FORM{mp} =~ /\D/){&error(303,'(2)同時プレイ人数');}
if($FORM{cok} eq ''){&error(205,'(3)クッキーID');}
elsif($FORM{cok} =~ /\W/){&error(106,'(3)クッキーID');}
if(!mygrep($FORM{qf},(0,1,2))){&error(401,'(4)選択肢形式');}
if($FORM{mt} eq ''){&error(205,'(6)メニューページのタイトル');}
if(!mygrep($FORM{stl},(0,1))){&error(401,'(10)スタイルシート');}
if(!mygrep($FORM{ey},(0,1,2,3))){&error(401,'(12)メニューページ表示項目');}
if(!mygrep($FORM{rt},(0,1))){&error(401,'(13)回答時間による順位付け');}
if(!mygrep($FORM{wr},(0,1))){&error(401,'(14)自動文字折り返し');}
if($error eq $error_mes){return 0;}
else{return 1;}
}
#************************************************
# システムデザイン設定編集時のパラメータチェック
#************************************************
sub ch_sysdesign_palam{
local(@return,$error);
$FORM{"al-$FORM{al}"}   =' checked';
$FORM{"wal-$FORM{wal}"} =' checked';
$error=$error_mes;
if($FORM{sdt} eq ''){&error(206,'(2)システムデザイン名');}
foreach $id(@sysdesign_list){
if($id eq $FORM{sdt} && $FORM{edittype} ne 'edit'){
&error(853,'(2)システムデザイン名');
}elsif($id eq $FORM{sdt} && $FORM{sdt} ne $FORM{id} && $FORM{edittype} eq 'edit'){
&error(854,'(2)システムデザイン名');
}
}
if(($FORM{tw} ne '')&&(&ch_file_format($FORM{tw}))){&error(305,'(3)メニューページの壁紙');}
if($FORM{tbc} eq ''){&error(206,'(4)メニューページの背景色');}
if($FORM{ttc} eq ''){&error(206,'(5)メニューページの表の色');}
if($FORM{tjc} eq ''){&error(206,'(6)メニューページのジャンル色');}
if($FORM{tic} eq ''){&error(206,'(7)メニューページの情報色');}
if($FORM{tcc} eq ''){&error(206,'(8)メニューページのコメント色');}
if($FORM{thc} eq ''){&error(206,'(9)メニューページの高成績者色');}
if($FORM{tbdc} eq ''){&error(206,'(10)メニューページの表の枠の色');}
if($FORM{txc} eq ''){&error(206,'(11)ページの文字色');}
if($FORM{lc} eq ''){&error(206,'(12)ページのリンク色');}
if($FORM{vc} eq ''){&error(206,'(13)ページの既訪問リンク色');}
if($FORM{tbdh} eq ''){&error(206,'(14)メニューページの表の枠の高さ');}
elsif($FORM{tbdh} =~/\D/){&error(305,'(14)メニューページの表の枠の高さ');}
if($FORM{tbd} eq ''){&error(206,'(15)メニューページの表の枠の幅');}
elsif($FORM{tbd} =~/\D/){&error(305,'(15)メニューページの表の枠の幅');}
if($FORM{tbdi} eq ''){&error(206,'(16)メニューページの表の枠の内幅');}
elsif($FORM{tbdi} =~/\D/){&error(305,'(16)メニューページの表の枠の内幅');}
if($FORM{ag} eq ''){&error(206,'(17)成績履歴グラフ画像１');}
elsif(&ch_file_format($FORM{ag})){&error(305,'(17)成績履歴グラフ画像１');}
else{&ch_file_exist('(17)成績履歴グラフ画像１',$FORM{ag});}
if($FORM{bg} eq ''){&error(206,'(18)成績履歴グラフ画像２');}
elsif(&ch_file_format($FORM{bg})){&error(305,'(18)成績履歴グラフ画像２');}
else{&ch_file_exist('(18)成績履歴グラフ画像２',$FORM{bg});}
if(!mygrep($FORM{al},('l','c','r'))){&error(402,'(19)表のレイアウト');}
if(!mygrep($FORM{wal},('l','c','r'))){&error(402,'(20)表内文字レイアウト');}
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
# ジャンルデザイン設定編集時のパラメータチェック
#************************************************
sub ch_design_palam{
local(@return,$error);
$error=$error_mes;
if($FORM{gdt} eq ''){&error(207,'(2)ジャンルデザイン名');}
foreach $id(@design_list){
if($id eq $FORM{gdt} && $FORM{edittype} ne 'edit'){
&error(855,'(2)ジャンルデザイン名');
}elsif($id eq $FORM{gdt} && $FORM{gdt} ne $FORM{id} && $FORM{edittype} eq 'edit'){
&error(856,'(2)ジャンルデザイン名');
}
}
if($FORM{gtc} eq ''){&error(207,'(3)文字色');}
if($FORM{glc} eq ''){&error(207,'(4)リンク文字色');}
if($FORM{gvc} eq ''){&error(207,'(5)既訪問リンク文字色');}
if($FORM{gcc} eq ''){&error(207,'(6)殿堂入り者色');}
if($FORM{gmc} eq ''){&error(207,'(7)基本背景色');}
if($FORM{gwi} eq ''){&error(207,'(8)正解時背景色');}
if($FORM{glo} eq ''){&error(207,'(9)不正解時背景色');}
if($FORM{gcm} eq ''){&error(207,'(10)情報ウインドウの色');}
if($FORM{thc} eq ''){&error(207,'(11)表のヘッダー色');}
if($FORM{tdc} eq ''){&error(207,'(12)表の色');}
if($FORM{bdc} eq ''){&error(207,'(13)表の枠の色');}
if($FORM{bdh} eq ''){&error(207,'(14)表の枠の高さ');}
elsif($FORM{bdh} =~/\D/){&error(306,'(14)表の枠の高さ');}
if($FORM{bd} eq ''){&error(207,'(15)表の枠の幅');}
elsif($FORM{bd} =~/\D/){&error(306,'(15)表の枠の幅');}
if($FORM{bdi} eq ''){&error(207,'(16)表の枠の内幅');}
elsif($FORM{bdi} =~/\D/){&error(306,'(16)表の枠の内幅');}
if(($FORM{gw} ne '')&& (&ch_file_format($FORM{gw}))){&error(104,'(17)基本壁紙');}
elsif($FORM{gw} ne ''){&ch_file_exist('(17)基本壁紙',$FORM{gw});}
if(($FORM{gww} ne '')&& (&ch_file_format($FORM{gww}))){&error(104,'(18)正解時壁紙');}
elsif($FORM{gww} ne ''){&ch_file_exist('(18)正解時壁紙',$FORM{gww});}
if(($FORM{glw} ne '')&& (&ch_file_format($FORM{glw}))){&error(104,'(19)不正解時壁紙');}
elsif($FORM{glw} ne ''){&ch_file_exist('(19)不正解時壁紙',$FORM{glw});}
if($FORM{wsg} eq ''){&error(207,'(20)正解表示');}
if($FORM{lsg} eq ''){&error(207,'(21)不正解表示');}
if($FORM{osg} eq ''){&error(207,'(22)タイムオーバー表示');}
if(($FORM{wmd} ne '')&& (&ch_file_format($FORM{wmd}))){&error(104,'(23)正解時MIDI');}
elsif($FORM{wmd} ne ''){&ch_file_exist('(23)正解時MIDI',$FORM{wmd});}
if(($FORM{lmd} ne '')&& (&ch_file_format($FORM{lmd}))){&error(104,'(24)不正解時MIDI');}
elsif($FORM{lmd} ne ''){&ch_file_exist('(24)不正解時MIDI',$FORM{lmd});}
if(($FORM{emd} ne '')&& (&ch_file_format($FORM{emd}))){&error(104,'(25)クイズ終了時MIDI');}
elsif($FORM{emd} ne ''){&ch_file_exist('(25)クイズ終了時MIDI',$FORM{emd});}
if(($FORM{hmd} ne '')&& (&ch_file_format($FORM{hmd}))){&error(104,'(26)高成績者用MIDI');}
elsif($FORM{hmd} ne ''){&ch_file_exist('(26)高成績者用MIDI',$FORM{hmd});}
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
# 終了時メッセージ編集のパラメータチェック
#************************************************
sub ch_edit_mes_param{
for($i=0;$i<$FORM{mn};$i++){
if($FORM{"per-$i"} eq ''){next;}
if(($FORM{"per-$i"}<0.00000001)||($FORM{"per-$i"}>100)){
&error(531,'正解率の指定');
return 1;
}
}
return 0;
}
#************************************************
# ジャンル編集時のパラメータチェック
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
if($FORM{t} eq ''){&error(208,'(2)タイトル');}
if(!mygrep($FORM{md},(0,1))){&error(403,"(5)問題ファイル");}
elsif($FORM{md} eq 1){
foreach(@genre_dir_orign){
if(($dir eq $_)||($mondai_cgi{$_} eq '.')||($mondai_cgi{$_} =~ /\//)){next;}
if(!($FORM{"smd-$_"} =~ /\d/)&&($FORM{"smd-$_"} ne 'all')){&error(304,'(5)問題ファイル');last;}
}
}
if(!mygrep($FORM{me},(0,1))){&error(403,'(6)ジャンルの動作状態');}
if(!mygrep($FORM{ct},(0,1))){&error(403,'(7)投稿問題の受付');}
if(!mygrep($FORM{nt},(0,1))){&error(403,'(8)テキスト形式の投稿問題');}
if(!mygrep($FORM{dc},(0,1))){&error(403,'(9)投稿問題の自動採用');}
if(!mygrep($FORM{ath},(0,1))){&error(403,'(11問題文への作成者表示');}
if($FORM{mn1} eq ''){&error(208,'(13)モード１の名前');}
if(!mygrep($FORM{sa1},(0,1))){&error(403,'(14)モード１正解表示');}
if(!mygrep($FORM{r1},(0,1))){&error(403,'(15)モード１出題順序');}
if(!mygrep($FORM{qm1},(0,1))){&error(403,'(16)モード１使用問題数');}
elsif(($FORM{qm1} eq '0')&&($FORM{'qm1-2'} eq '')){&error(208,'(16)モード１使用問題数');}
elsif(($FORM{qm1} eq '0')&&($FORM{'qm1-2'}=~ /\D/)){&error(304,'(16)モード１使用問題数');}
if(!mygrep($FORM{pm1},(0,1))){&error(403,'(17)モード１出題問題数');}
elsif(($FORM{pm1} eq '0')&&($FORM{'pm1-2'} eq '')){&error(208,'(17)モード１出題問題数');}
elsif(($FORM{pm1} eq '0')&&($FORM{'pm1-2'}=~ /\D/)){&error(304,'(17)モード１出題問題数');}
if(!mygrep($FORM{bd1},(0,1))){&error(403,'(18)モード１一括出題');}
if(!mygrep($FORM{lm1},(0,1))){&error(403,'(19)モード１終了条件誤答数');}
elsif(($FORM{lm1} eq '0')&&($FORM{'lm1-2'} eq '')){&error(208,'(19)モード１終了条件誤答数');}
elsif(($FORM{lm1} eq '0')&&($FORM{'lm1-2'}=~ /\D/)){&error(304,'(19)モード１終了条件誤答数');}
if(!mygrep($FORM{tl1},(0,1))){&error(403,'(20)モード１制限時間');}
elsif(($FORM{tl1} eq '0')&&($FORM{'tl1-2'} eq '')){&error(208,'(20)モード１制限時間');}
elsif(($FORM{tl1} eq '0')&&($FORM{'tl1-2'}=~ /\D/)){&error(304,'(20)モード１制限時間');}
if($FORM{hb1} eq ''){&error(208,'(21)モード１合格点');}
elsif($FORM{hb1} =~ /\D/){&error(304,'(21)モード１合格点');}
if(!mygrep($FORM{hbu1},(0,1))){&error(403,'(22)高成績者のBACK UP');}
elsif(($FORM{hbu1} eq '1')&&($FORM{'hbu1-2'} eq '')){&error(208,'(22)高成績者のBACK UP間隔(日)');}
elsif(($FORM{hbu1} eq '1')&&($FORM{'hbu1-2'}=~ /\D/)){&error(304,'(22)高成績者のBACK UP間隔(日)');}
if(!mygrep($FORM{hbw1},(0,1))){&error(403,'(23)高成績者のBACK UP方式');}
if(!mygrep($FORM{sbu1},(0,1))){&error(403,'(24)成績分布のBACK UP');}
elsif(($FORM{sbu1} eq '1')&&($FORM{'sbu1-2'} eq '')){&error(208,'(24)成績分布のBACK UP間隔(日)');}
elsif(($FORM{sbu1} eq '1')&&($FORM{'sbu1-2'}=~ /\D/)){&error(304,'(24)成績分布のBACK UP間隔(日)');}
if(!mygrep($FORM{sbw1},(0,1))){&error(403,'(25)成績分布のBACK UP方式');}
if($FORM{gb1} eq ''){&error(208,'(26)モード１成績分布省略表\示');}
elsif($FORM{gb1} =~ /\D/){&error(304,'(26)モード１成績分布省略表\示');}
if($FORM{hd1} eq ''){&error(208,'(27)モード１成績分布集計単位');}
elsif($FORM{hd1} =~ /\D/){&error(304,'(27)モード１成績分布集計単位');}
if(!mygrep($FORM{dl1},(0,1))){&error(403,'(28)モード１高成績者日数制限');}
elsif(($FORM{dl1} eq '0')&&($FORM{'dl1-2'} eq '')){&error(208,'(28)モード１高成績者日数制限');}
elsif(($FORM{dl1} eq '0')&&($FORM{'dl1-2'}=~ /\D/)){&error(304,'(28)モード１高成績者日数制限');}
if(!mygrep($FORM{nl1},(0,1))){&error(403,'(29)モード１高成績者人数制限');}
elsif(($FORM{nl1} eq '0')&&($FORM{'nl1-2'} eq '')){&error(208,'(29)モード１高成績者人数制限');}
elsif(($FORM{nl1} eq '0')&&($FORM{'nl1-2'}=~ /\D/)){&error(304,'(29)モード１高成績者人数制限');}
if($FORM{no1} eq ''){&error(208,'(30)モード１殿堂入り人数');}
elsif($FORM{no1} =~ /\D/){&error(304,'(30)モード１殿堂入り人数');}
if(!mygrep($FORM{rc1},(0,1))){&error(403,'(31)モード１高成績者コメント記録');}
if(!mygrep($FORM{dh1},(0,1))){&error(403,'(32)モード１同ホスト同スコア');}
if($FORM{mn2} ne ''){
if(!mygrep($FORM{sa2},(0,1))){&error(403,'(34)モード１正解表示');}
if(!mygrep($FORM{r2},(0,1))){&error(403,'(35)モード１出題順序');}
if(!mygrep($FORM{qm2},(0,1))){&error(403,'(36)モード１使用問題数');}
elsif(($FORM{qm2} eq '0')&&($FORM{'qm2-2'} eq '')){&error(208,'(36)モード１使用問題数');}
elsif(($FORM{qm2} eq '0')&&($FORM{'qm2-2'}=~ /\D/)){&error(304,'(36)モード１使用問題数');}
if(!mygrep($FORM{pm2},(0,1))){&error(403,'(37)モード１出題問題数');}
elsif(($FORM{pm2} eq '0')&&($FORM{'pm2-2'} eq '')){&error(208,'(37)モード１出題問題数');}
elsif(($FORM{pm2} eq '0')&&($FORM{'pm2-2'}=~ /\D/)){&error(304,'(37)モード１出題問題数');}
if(!mygrep($FORM{bd2},(0,1))){&error(403,'(38)モード１一括出題');}
if(!mygrep($FORM{lm2},(0,1))){&error(403,'(39)モード１終了条件誤答数');}
elsif(($FORM{lm2} eq '0')&&($FORM{'lm2-2'} eq '')){&error(208,'(39)モード１終了条件誤答数');}
elsif(($FORM{lm2} eq '0')&&($FORM{'lm2-2'}=~ /\D/)){&error(304,'(39)モード１終了条件誤答数');}
if(!mygrep($FORM{tl2},(0,1))){&error(403,'(40)モード１制限時間');}
elsif(($FORM{tl2} eq '0')&&($FORM{'tl2-2'} eq '')){&error(208,'(40)モード１制限時間');}
elsif(($FORM{tl2} eq '0')&&($FORM{'tl2-2'}=~ /\D/)){&error(304,'(40)モード１制限時間');}
if($FORM{hb2} eq ''){&error(208,'(41)モード１合格点');}
elsif($FORM{hb2} =~ /\D/){&error(304,'(41)モード１合格点');}
if(!mygrep($FORM{hbu2},(0,1))){&error(403,'(42)高成績者のBACK UP');}
elsif(($FORM{hbu2} eq '1')&&($FORM{'hbu2-2'} eq '')){&error(208,'(42)高成績者のBACK UP間隔(日)');}
elsif(($FORM{hbu2} eq '1')&&($FORM{'hbu2-2'}=~ /\D/)){&error(304,'(42)高成績者のBACK UP間隔(日)');}
if(!mygrep($FORM{hbw2},(0,1))){&error(403,'(43)高成績者のBACK UP方式');}
if(!mygrep($FORM{sbu2},(0,1))){&error(403,'(44)成績分布のBACK UP');}
elsif(($FORM{sbu2} eq '1')&&($FORM{'sbu2-2'} eq '')){&error(208,'(44)成績分布のBACK UP間隔(日)');}
elsif(($FORM{sbu2} eq '1')&&($FORM{'sbu2-2'}=~ /\D/)){&error(304,'(44)成績分布のBACK UP間隔(日)');}
if(!mygrep($FORM{sbw2},(0,1))){&error(403,'(45)成績分布のBACK UP方式');}
if($FORM{gb2} eq ''){&error(208,'(46)モード１成績分布省略表\示');}
elsif($FORM{gb2} =~ /\D/){&error(304,'(46)モード１成績分布省略表\示');}
if($FORM{hd2} eq ''){&error(208,'(47)モード１成績分布集計単位');}
elsif($FORM{hd2} =~ /\D/){&error(304,'(47)モード１成績分布集計単位');}
if(!mygrep($FORM{dl2},(0,1))){&error(403,'(48)モード１高成績者日数制限');}
elsif(($FORM{dl2} eq '0')&&($FORM{'dl2-2'} eq '')){&error(208,'(48)モード１高成績者日数制限');}
elsif(($FORM{dl2} eq '0')&&($FORM{'dl2-2'}=~ /\D/)){&error(304,'(48)モード１高成績者日数制限');}
if(!mygrep($FORM{nl2},(0,1))){&error(403,'(49)モード１高成績者人数制限');}
elsif(($FORM{nl2} eq '0')&&($FORM{'nl2-2'} eq '')){&error(208,'(49)モード１高成績者人数制限');}
elsif(($FORM{nl2} eq '0')&&($FORM{'nl2-2'}=~ /\D/)){&error(304,'(49)モード１高成績者人数制限');}
if($FORM{no2} eq ''){&error(208,'(50)モード１殿堂入り人数');}
elsif($FORM{no2} =~ /\D/){&error(304,'(50)モード１殿堂入り人数');}
if(!mygrep($FORM{rc2},(0,1))){&error(403,'(51)モード１高成績者コメント記録');}
if(!mygrep($FORM{dh2},(0,1))){&error(403,'(52)モード１同ホスト同スコア');}
}
if($error eq $error_mes){return 0;}
else{return 1;}
}
#************************************************
# アクセス制限IPチェック
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
# システムファイルの書き込み
#************************************************
sub write_system_dat{
return &write_file($system_cgi,&sys_to_system_dat);
}
#************************************************
# ジャンルファイルの書き込み
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
# デザインファイルの書き込み
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
# システムデザインファイルの書き込み
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
# 問題ファイル上書き処理
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
if(&ch_dir_exist('ディレクトリ名',$FORM{d})){return 1;}
return &write_file("$FORM{d}/$file_name",@lines);
}
