#!/usr/bin/perl
$version='2.03';
chdir('qqqsystems2');
require 'function.cgi';
&main;
#----------------------------はじめにお読みください------------------------------
#このスクリプトは、クイズ運営管理用のCGIプログラムです。
#クイズの作成、運営は、サーバーに設置後、quiz_op.cgiにアクセスし、
#Web上でおこなってください。
#--------------------------------------------------------------------------------
#************************************************
# ヘッダ表示処理
#_HTML_と_HTML_とのあいだに
#クイズのページのヘッダー部分のHTMLを記入してください。
#普通のHTML表記でかまいません。
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
<title>クイズ管理人室$subtitle1</title></head><BODY bgcolor=white>
<table border=0 cellspacing=0 cellpadding=0 width="100%" >
<tr><td Valign=TOP>
$formop_hd
<input type=hidden name=type value=$FORM{type}>
<input type=hidden name=totop value=1>
<input type=submit value="クイズ管理人室へ">
</form>
</font></td><td Valign=TOP>
$formop_hb
$form_d
<input type=hidden name=totop value=1>
<input type=submit value="新規ウインドウ">
</form></td>
<td nowrap width=80%><div align=right><p><B><big>クイズ管理人室$subtitle2</big></B></p></div></td></tr></table>
<br><br>
_HTML_
}
#************************************************
# メインプログラム
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
# システムコマンド
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
&header_html("各種ログ閲覧・保存");
&log_html;
}
}elsif($FORM{type} eq 'sys'){
&header_html("システム設定編集");
&sys_to_form;
&edit_sys_html;
}elsif($FORM{type} eq 'sys2'){
if(&edit_sys){
&header_html("システム設定編集");
&edit_sys_html;
}else{
&menu_html;
}
}elsif($FORM{type} eq 'newj'){
&header_html("新ジャンル登録");
&make_genre_html;
}elsif($FORM{type} eq 'newj2'){
if(&make_mes_cgi){
&header_html("新ジャンル登録");
&make_genre_html;
}elsif(&make_genre){
&header_html("新ジャンル登録");
&make_genre_html;
}else{
&header_html("ジャンルの編集");
&genre_array_to_form;
&edit_genre_html;
}
}elsif($FORM{type} eq 'sdesed'){
&header_html("システムデザインの編集");
if($FORM{delid} ne ''){&del_sysdesign($FORM{delid});}
if($sysdesign_title{$FORM{id}} ne ''){
&sysdesign_to_form($FORM{id});
$FORM{sdt}=$FORM{id};
&edit_sysdesign_html($FORM{id},'edit');
}elsif($sysdesign_title{$FORM{copyid}} ne ''){
if($FORM{sdt} eq ''){
$FORM{sdt}="$FORM{copyid}(コピー)";
if($sysdesign_title{$FORM{sdt}} ne ''){
for($id=2;$sysdesign_title{"$FORM{copyid}(コピー$id)"} ne '';$id++){;}
$FORM{sdt}="$FORM{copyid}(コピー$id)";
}
}
&sysdesign_to_form($FORM{copyid});
$FORM{id}=$FORM{copyid};
&edit_sysdesign_html($FORM{copyid},'copy');
}else{
if($FORM{sdt} eq ''){
for($id=$#sysdesign_list+2;$sysdesign_title{"システムデザイン$id"} ne '';$id++){;}
$FORM{sdt}="システムデザイン$id";
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
&header_html("システムデザインの編集");
$FORM{id}=$FORM{sdt};
&edit_sysdesign_html($FORM{id},$FORM{edittype});
}elsif($FORM{type} eq 'gdesed'){
&header_html("ジャンルデザインの編集");
if($FORM{delid} ne ''){&del_design($FORM{delid});}
if($design_title{$FORM{id}} ne ''){
&design_to_form($FORM{id});
$FORM{gdt}=$FORM{id};
&edit_design_html($FORM{id},'edit');
}elsif($design_title{$FORM{copyid}} ne ''){
&design_to_form($FORM{copyid});
if($FORM{gdt} eq ''){
$FORM{gdt}="$FORM{copyid}(コピー)";
if($design_title{$FORM{gdt}} ne ''){
for($id=2;$design_title{"$FORM{copyid}(コピー$id)"} ne '';$id++){;}
$FORM{gdt}="$FORM{copyid}(コピー$id)";
}
}
$FORM{id}=$FORM{copyid};
&edit_design_html($FORM{copyid},'copy');
}else{
if($FORM{gdt} eq ''){
for($id=$#design_list+2;$design_title{"ジャンルデザイン$id"} ne '';$id++){;}
$FORM{gdt}="ジャンルデザイン$id";
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
&header_html("ジャンルデザインの編集");
$FORM{id}=$FORM{gdt};
&edit_design_html($FORM{id},$FORM{edittype});
}elsif($FORM{type} eq 'sort'){
&header_html("ジャンルの順序変更");
&sort_genre_html;
}elsif($FORM{type} eq 'sort1'){
if(&sort_genre){
&sort_genre_html;
}else{
&menu_html;
}
}elsif($FORM{type} eq 'log'){
&header_html("各種ログ閲覧・保存");
&log_html;
}elsif($FORM{type} eq 'play'){
&header_html("プレイログ使用状況");
&play_html;
}elsif($FORM{type} eq 'size'){
&header_html("各種ログ容量");
&file_size_html;
}elsif($FORM{type} eq 'guard'){
&header_html("アクセス制限");
&edit_guard_html;
}elsif($FORM{type} eq 'guard1'){
if($FORM{guard} eq 1){$guard="guard";}
else{$guard="permit";}
if(!&write_file($guard_cgi,"$guard\n$FORM{iplist}")){
&mes(200,"アクセス制限IPリスト");
}
&header_html("アクセス制限");
&edit_guard_html;
}elsif($FORM{type} eq 'help'){
&header_html("ヘルプ");
&help_html;
}else{
&menu_html;
}
}
#************************************************
# ジャンル別コマンド
#************************************************
sub genre_command{
&other_genre_html;
if($FORM{d} eq ''){
&error(404,'ジャンル');
&menu_html;
}elsif(&ch_dir_exist('ディレクトリ名',$FORM{d})){
&menu_html;
}elsif(&ch_genre_exist($FORM{d}) eq 0){
&error(801,'ジャンル情報');
&menu_html;
}elsif($FORM{type} eq ''){
&header_html();
&error(405,'編集メニュー');
&menu_html;
}elsif($FORM{type} eq 'editg'){
&header_html("ジャンルの編集");
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
&header_html("ジャンル複製");
&list_genre_html($FORM{d});
&copy_genre_html;
}elsif($FORM{type} eq 'copy1'){
&list_genre_html($FORM{d});
if(&copy_genre){
&header_html("ジャンル複製");
&copy_genre_html;
}else{
&header_html("ジャンルの編集");
&edit_genre_html;
}
}elsif($FORM{type} eq 'del'){
&header_html("ジャンルの各種削除");
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
&header_html("出題状況表\示");
&list_genre_html($FORM{d});
&rec_html('op');
}elsif($FORM{type} eq 'qmulti'){
if(&ch_mondai_exist){return;}
&header_html("問題の一括追加");
&list_genre_html($FORM{d});
&multi_add_quiz_form;
}elsif($FORM{type} eq 'qmulti1'){
if(&ch_mondai_exist){return;}
&header_html("問題の一括追加確認");
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
&header_html("問題の編集");
&list_genre_html($FORM{d});
$FORM{ed}='new';$FORM{lst_q}=1;$FORM{lst_a}=1;
&edit_quiz_form;
&edit_quiz_html;
}elsif($FORM{type} eq 'qedit1'){
if(&ch_mondai_exist){return;}
&header_html("問題の編集");
&list_genre_html($FORM{d});
if(($FORM{ed} eq 'edit')&&($FORM{qn} ne '')){
if($FORM{qn} =~/\D/){&error(301,'問題番号');$FORM{qn} = '';}
elsif(($FORM{qn} > $#mondai+1)||($FORM{qn}<=0)){&error(531,'問題番号');$FORM{qn} = '';}
else{&quiz_array_to_form;}
}
&edit_quiz_form;
&edit_quiz_html;
}elsif($FORM{type} eq 'qedit2'){
if(&ch_mondai_exist){return;}
&header_html("問題の編集");
&list_genre_html($FORM{d});
if($FORM{ed} eq 'edit'){
&refresh_quiz;
&quiz_read($FORM{d});
if(!&edit_quiz("$mondai_$FORM{d}\.cgi")){
&mes(201,"『$title{$FORM{d}}』の問題");
&refresh_quiz;
&quiz_read($FORM{d});
}
}else{
if(!&add_quiz){
$FORM{qn}=$#mondai+1;
&mes(150,"『$title{$FORM{d}}』の問題");
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
&header_html("投稿問題の編集");
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
&header_html("投稿問題の編集");
if($FORM{add} > 0){&add_cont;}
else{
&refresh_quiz;
&quiz_read($FORM{d},'','',$contribute_cgi);
if(&edit_quiz("$contribute_cgi")){
&edit_cont_form;
}else{
&mes(202,"投稿問題");
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
&mes(250,"『$title{$FORM{d}}』の問題");
}
&list_genre_html($FORM{d});
&del_quiz_html;
}elsif($FORM{type} eq 'mes'){
&header_html("終了時メッセージ編集");
&list_genre_html($FORM{d});
&mes_dat_to_form;
&edit_final_mes_html;
}elsif($FORM{type} eq 'mes1'){
&header_html("終了時メッセージ編集");
&list_genre_html($FORM{d});
if(!&ch_edit_mes_param){
&edit_mes;
}
&mes_dat_to_form;
&edit_final_mes_html;
}elsif($FORM{type} eq 'back'){
&header_html("各種ログのバックアップ");
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
&header_html("高成績者ログ編集");
&list_genre_html($FORM{d});
&edit_high_html;
}elsif($FORM{type} eq 'high1'){
if(&edit_high){
&header_html("高成績者ログ編集");
&list_genre_html($FORM{d});
&edit_high_html;
}else{
&menu_html;
}
}else{
&error(406,'編集メニュー');
&menu_html;
}
}
#************************************************
# 問題追加処理
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
# 投稿問題追加処理
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
&mes(500,"投稿問題");
}
}
}
#************************************************
# 問題一括追加処理
#************************************************
sub multi_add_quiz{
local($index);
&refresh_quiz;
&quiz_read($FORM{d});
$index=0;
while($FORM{"p_q$index"} ne ''){
if(($FORM{"p_a$index"} eq '') || ($FORM{"p_m1$index"} eq '')){&error(101,'登録する問題');return 1;}
&push_quiz_palam($FORM{"p_q$index"},$FORM{"p_a$index"},$FORM{"p_m1$index"},$FORM{"p_m2$index"},$FORM{"p_m3$index"},$FORM{"p_m4$index"},$FORM{"p_am$index"},$FORM{"p_mm$index"},$FORM{"p_cf$index"},$FORM{"p_dg$index"},$FORM{"p_1mm$index"},$FORM{"p_2mm$index"},$FORM{"p_3mm$index"},$FORM{"p_4mm$index"},$FORM{"p_at$index"},$FORM{"p_ath$index"});
$index++;
}
if(!&write_mondai("$mondai_$FORM{d}\.cgi")){
&mes(350,"『$title{$FORM{d}}』の問題");return 0;
}else{return 1;}
}
#************************************************
# ジャンル順序変更
#************************************************
sub sort_genre{
for($i=1;$i<=$#genre_dir_all+1;$i++){
if(&ch_genre_exist($FORM{"d$i"}) eq 0){&error(806,'ディレクトリ');return 1;}
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
&mes(400,'ジャンルの順序変更');
return 0;
}
#************************************************
# ジャンル複製処理
#************************************************
sub copy_genre{
if(&ch_dir_exist('複製するディレクトリ名',$FORM{d2})){return 1;}
if(&ch_genre_exist($FORM{d2}) eq 1){
&error(851,'複製するディレクトリ名');
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
&mes(900,"『$old_dirディレクトリ』のジャンル登録情報を<br>『$FORM{d2}ディレクトリ』へ複製する作業が正常に終了しました。<br>成績ログファイル、問題ファイル等は複製されていません。<br>引き続きジャンル別設定を行ってください。");
return 0;
}else{return 1;}
}
#************************************************
# ファイルの結合。重複データをのぞいたものを書き込む。
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
# 引数末尾の数字を取って返す。
#************************************************
sub cut_num{
local($word)=@_;
if($word=~/(.*)[\d]+$/){$word=$1;}
return $word;
}
#************************************************
# パスワード新規登録HTML表示処理
#************************************************
sub pass_new_html {
$main_html = <<"_HTML_";
<hr><ul>
<table bgcolor='$sys_color' $sys_tbl_opt><tr><td nowrap>
管理者用パスワードが登録されていません。<br>
新規パスワードを登録してください。<br><br>
<form action="$quiz_op_cgi" method="$method" name=frm>
<input type=hidden name=passnew value=1>
<input type=password name=passnew1><br>
<input type=password name=passnew2>(確認用)<br><br>
<input type=submit value="　　 登録 　　"></form>
${&focus_move('passnew1')}$ret
</td></tr></table></ul>
_HTML_
}
#************************************************
# パスワード入力用HTML表示処理
#************************************************
sub pass_enter_html {
$main_html = <<"_HTML_";
<hr>
<table border='$border' bgcolor='$sys_color' width=400><tr><td nowrap><span>
管理者用パスワードを入力してください。<br>
パスワードを初期化したい場合は、$pass_cgiファイルを消去してください。<br>
<form action='$quiz_op_cgi' method='$method' name=frm>
<input type=password name=passch>
<input type=hidden name=passch1 value=1>
<input type=submit value="送信"></form></span>
${&focus_move('passch')}$ret
</td></tr></table>
<br>
<br>
<a href="$index_cgi">クイズへもどる</a>
_HTML_
}
#************************************************
# メニュー表示処理
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
<b><span>■編集メニュー■</span></b>
<table $sys_tbl_opt bgcolor='$sys_color'><tr><td valign=top>
$center_menu1
<table border=$border cellpadding=2 bgcolor='$sys_color2'>
$formop_h
<input type=hidden name=type value=sys>
<tr><td colspan=2 nowrap>
<center><span>●システムコマンド●</span></center>
</td></tr>
<tr><td>
<span>システム設定編集</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=newj>
<span>新ジャンル登録</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=sdesed>
<span>システムデザインの編集</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=gdesed>
<span>ジャンルデザインの編集</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=play>
<span>プレイログ使用状況</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=log>
<span>各種ログ閲覧・保存</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=size>
<span>各種ログ容量</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
_HTML_
if($#genre_dir_all>=1){
$menu_html .= <<"_HTML_";
$formop_h
<tr><td>
<input type=hidden name=type value=sort>
<span>ジャンルの順序変更</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
_HTML_
}else{
$menu_html .= <<"_HTML_";
<tr><td>
ジャンルの順序変更</td><td>不可
</td></tr>
_HTML_
}
$menu_html .= <<"_HTML_";
$formop_h
<tr><td>
<input type=hidden name=type value=guard>
<span>アクセス制限</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
$formop_h
<tr><td>
<input type=hidden name=type value=help>
<span>ヘルプ</span></td><td><span><input type=submit value="実行"></span></td></tr></form>
</table>$center_menu2</td>
_HTML_
if($#genre_dir_all>=0){
$menu_html .= <<"_HTML_";
<td>
$formop_h
<input type=hidden name=menu value=1>
<table border=$border cellpadding=2 bgcolor='$sys_color2'>
<tr><td colspan=3 nowrap><center><span>●ジャンル別コマンド●</span></center></td></tr>
<tr><td rowspan=12><span><select name=d size=20 width=200>
_HTML_
foreach $dir(@genre_dir_all){
if($dir ne ''){$menu_html .= "<option value='$dir'$dir_ch{$dir}>$title{$dir}　　 \n";}
}
$menu_html .= <<"_HTML_";
</select></span>
</td>
<tr><td nowrap><span>ジャンルの編集</span></td><td><span><input type=submit name=type_editg value='実行'></span></td></tr>
<tr><td nowrap><span>ジャンルの複製</span></td><td><span><input type=submit name=type_copy value='実行'></span></td></tr>
<tr><td nowrap><span>ジャンルの各種削除</span></td><td><span><input type=submit name=type_del value='実行'></span></td></tr>
<tr><td nowrap><span>問題の作成編集</span></td><td><span><input type=submit name=type_qedit value='実行'></span></td></tr>
<tr><td nowrap><span>問題の削除、順序変更</span></td><td><span><input type=submit name=type_qdel value='実行'></span></td></tr>
<tr><td nowrap><span>問題の一括追加</span></td><td><span><input type=submit name=type_qmulti value='実行'></span></td></tr>
<tr><td nowrap><span>投稿問題の編集</span></td><td><span><input type=submit name=type_qcont value='実行'></span></td></tr>
<tr><td nowrap><span>終了時メッセージ編集</span></td><td><span><input type=submit name=type_mes value='実行'></span></td></tr>
<tr><td nowrap><span>出題状況表\示</span></td><td><span><input type=submit name=type_score value='実行'></span></td></tr>
<tr><td nowrap><span>各種ログのバックアップ</span></td><td><span><input type=submit name=type_back value='実行'></span></td></tr>
<tr><td nowrap><span>高成績者リスト編集</span></td><td><span><input type=submit name=type_high value='実行'></span></td></tr>
</table>
</td></tr>
_HTML_
}
$menu_html .= '</table>';
&list_sys_html;
&list_genre_html(@genre_dir_all);
}
#************************************************
# システム情報の一覧
#************************************************
sub list_sys_html{
if($SYS{quiz_form} eq 0){$quiz_f='リンク';}
elsif($SYS{quiz_form} eq 1){$quiz_f='ラジオボタン';}
else{$quiz_f='ボタン';}
$system_list ="<br><b><span>■システム情報■</span></b><table border=$border>";
$system_list .="<tr><td colspan=6><center><small>総合設定</small></center></td>";
$system_list .="<td colspan=11><center><small>デザイン<small></center></td></tr><tr>";
$system_list .= &my_print2(<<"_MY_",'<td><small><center>','</center></small></td>');
プ<br>レ<br>イ<br>ロ<br>グ<br>保<br>護<br>期<br>間<br>(分)
同<br>時<br>プ<br>レ<br>イ<br>人<br>数<br>(人)
選<br>択<br>肢<br>形<br>式
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>タ<br>イ<br>ト<br>ル
ト<br>ッ<br>プ<br>ペ<br>｜<br>ジ<br>へ<br>の<br>リ<br>ン<br>ク
表\<br>示<br>形<br>式
デ<br>ザ<br>イ<br>ン<br>名
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>背<br>景<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>ジ<br>ャ<br>ン<br>ル<br>名<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>情<br>報<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>紹<br>介<br>文<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>高<br>成<br>績<br>者<br>色
基<br>本<br>文<br>字<br>色
リ<br>ン<br>ク<br>文<br>字<br>色
既<br>訪<br>問<br>リ<br>ン<br>ク<br>文<br>字<br>色
表\<br>の<br>表\<br>示<br>揃<br>え
表\<br>内<br>文<br>字<br>表\<br>示<br>揃<br>え
_MY_
$system_list .='</tr><tr>';
$system_list .=&my_print2(<<"_MY_",'<td><small>','</small></td>');
$SYS{limit}
$SYS{max_player}
$quiz_f
<a href=$index_cgi>$SYS{main_title}</a>
_MY_
$align{l}='左揃';$align{c}='中揃';$align{r}='右揃';
$walign{l}='左揃';$walign{c}='中揃';$walign{r}='右揃';
$easy{0}='詳細';$easy{1}='普通';$easy{2}='簡易';$easy{3}='一覧';
if($SYS{top_url} ne ''){$system_list .="<td><small><a href=$SYS{top_url}>→</a></small></td>";}
else{$system_list .='<td><small>×</small></td>';}
$system_list .=<<"_HTML_";
<td><small>$easy{$SYS{easy}}</small></td>
<td><small>$SYS{design}</small></td>
<td bgcolor='$SYS{top_back_color}'><small><font color='$SYS{top_back_color}'>■</font></small></td>
<td bgcolor='$SYS{top_genre_color}'><small><font color='$SYS{top_genre_color}'>■</font></small></td>
<td bgcolor='$SYS{top_info_color}'><small><font color='$SYS{top_info_color}'>■</font></small></td>
<td bgcolor='$SYS{top_com_color}'><small><font color='$SYS{top_com_color}'>■</font></small></td>
<td bgcolor='$SYS{top_high_color}'><small><font color='$SYS{top_high_color}'>■</font></small></td>
<td bgcolor='$SYS{text_color}'><small><font color='$SYS{text_color}'>■</font></small></td>
<td bgcolor='$SYS{link_color}'><small><font color='$SYS{link_color}'>■</font></small></td>
<td bgcolor='$SYS{vlink_color}'><small><font color='$SYS{vlink_color}'>■</font></small></td>
<td><small>$align{$SYS{align}}</small></td>
<td><small>$walign{$SYS{walign}}</small></td>
</tr></table>
_HTML_
}
#************************************************
# ジャンル情報の一覧
#************************************************
sub list_genre_html{
local(@all_dirs)=@_;
local(@dirs);
foreach $dir(@all_dirs){if($dir ne ''){push(@dirs,$dir);}}
if($#dirs < 0){$genre_list='';return;}
$genre_list ="<br><b><span>■ジャンル別情報■</span></b><table border=$border>";
$genre_list .="<tr><td colspan=9><center><small>総合設定</small></center></td>";
$genre_list .="<td colspan=12><center><small>デザイン<small></center></td>";
$genre_list .="<td colspan=21><center><small>モード別<small></center></td></tr>";
$genre_list .=&my_print2(<<'_MY_','<td><small><center>','</center></small></td>');
表<br>題
dir
登<br>録<br>済<br>問<br>題<br>数<br>(問)
投<br>稿<br>問<br>題<br>数<br>(問)
公<br>開<br>中
投<br>稿<br>問<br>題<br>の<br>受<br>付
テ<br>キ<br>ス<br>ト<br>回<br>答<br>形<br>式<br>の<br>投<br>稿<br>問<br>題
投<br>稿<br>問<br>題<br>の<br>自<br>動<br>採<br>用
出<br>題<br>状<br>況<br>で<br>の<br>問<br>題<br>文<br>表<br>示
作<br>成<br>者<br>表<br>示
デ<br>ザ<br>イ<br>ン<br>名
基<br>本<br>文<br>字<br>色
リ<br>ン<br>ク<br>文<br>字<br>色
既<br>訪<br>問<br>リ<br>ン<br>ク<br>文<br>字<br>色
殿<br>堂<br>入<br>り<br>文<br>字<br>色
基<br>本<br>背<br>景<br>色
正<br>解<br>背<br>景<br>色
不<br>正<br>解<br>背<br>景<br>色
情<br>報<br>ウ<br>イ<br>ン<br>ド<br>ウ<br>色
表<br>の<br>ヘ<br>ッ<br>ダ<br>｜<br>色
表<br>の<br>色
表<br>の<br>枠<br>の<br>色
名<br>前
正<br>解<br>表<br>示
出<br>題<br>順
使<br>用<br>問<br>題<br>数<br>(問)
出<br>題<br>数<br>(問)
一<br>括<br>出<br>題
終<br>了<br>条<br>件<br>(問)
制<br>限<br>時<br>間<br>(秒)
合<br>格<br>点<br>(％)
高<br>成<br>績<br>者<br>バ<br>ッ<br>ク<br>ア<br>ッ<br>プ<br>(日)
高<br>成<br>績<br>者<br>バ<br>ッ<br>ク<br>ア<br>ッ<br>プ<br>方<br>式
成<br>績<br>分<br>布<br>バ<br>ッ<br>ク<br>ア<br>ッ<br>プ<br>(日)
成<br>績<br>分<br>布<br>バ<br>ッ<br>ク<br>ア<br>ッ<br>プ<br>方<br>式
成<br>績<br>分<br>布<br>省<br>略<br>表<br>示<br>(％)
成<br>績<br>分<br>布<br>集<br>計<br>単<br>位<br>(問)
高<br>成<br>績<br>者<br>日<br>数<br>制<br>限<br>(日)
高<br>成<br>績<br>者<br>人<br>数<br>制<br>限<br>(人)
殿<br>堂<br>入<br>り<br>人<br>数<br>(人)
高<br>成<br>績<br>者<br>コ<br>メ<br>ン<br>ト<br>記<br>録
同<br>ホ<br>ス<br>ト<br>同<br>ス<br>コ<br>ア<br>登<br>録
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
if($mente{$dir}){$genre_list.="<td$rowspan><small>○</small></td>";}
else{$genre_list.="<td$rowspan><small>×</small></td>";}
if($cont{$dir}){$genre_list.="<td$rowspan><small>○</small></td>";}
else{$genre_list.="<td$rowspan><small>×</small></td>";}
if($notext{$dir}){$genre_list.="<td$rowspan><small>×</small></td>";}
else{$genre_list.="<td$rowspan><small>○</small></td>";}
if($direct_cont{$dir}){$genre_list.="<td$rowspan><small>○</small></td>";}
else{$genre_list.="<td$rowspan><small>×</small></td>";}
if($show_digest{$dir}){$genre_list.="<td$rowspan><small>×</small></td>";}
else{$genre_list.="<td$rowspan><small>○</small></td>";}
if($show_auth{$dir} eq 1){$genre_list.="<td$rowspan><small>○</small></td>";}
else{$genre_list.="<td$rowspan><small>×</small></td>";}
$id=$design{$dir};
if(!mygrep($id,@design_list)){
&def_design($id);
&design_to_design_array;
}
$genre_list .=<<"_HTML_";
<td$rowspan nowrap><small>$id</small></td>
<td$rowspan bgcolor='$text_color{$id}'><small><font color='$text_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$link_color{$id}'><small><font color='$link_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$vlink_color{$id}'><small><font color='$vlink_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$champ_color{$id}'><small><font color='$champ_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$main_color{$id}'><small><font color='$main_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$win_color{$id}'><small><font color='$win_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$lose_color{$id}'><small><font color='$lose_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$com_color{$id}'><small><font color='$com_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$th_color{$id}'><small><font color='$th_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$td_color{$id}'><small><font color='$td_color{$id}'>■</font></small></td>
<td$rowspan bgcolor='$border_color{$id}'><small><font color='$border_color{$id}'>■</font></small></td>
<td nowrap><small><a href=$quiz_cgi?d=$dir\&m=1&passch=$FORM{passch}>$mode_name1{$dir}</a></small></td>
_HTML_
if($show_ans1{$dir}){$genre_list.='<td><small>○</small></td>';}
else{$genre_list.='<td><small>×</small></td>';}
if($random1{$dir}){$genre_list.='<td nowrap><small>ランダム</small></td>';}
else{$genre_list.='<td nowrap><small>固定</small></td>';}
if($quiz_max1{$dir}ne ''){$genre_list.="<td><small>$quiz_max1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>全</small></td>\n";}
if($play_max1{$dir}ne ''){$genre_list.="<td><small>$play_max1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>全</small></td>\n";}
if($bundle1{$dir} eq 1){$genre_list.="<td><small>有</small></td>\n";}
else{$genre_list.="<td><small>無</small></td>\n";}
if($lose_max1{$dir}ne ''){$genre_list.="<td><small>$lose_max1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>全</small></td>\n";}
if($time_limit1{$dir} > '0'){$genre_list.="<td><small>$time_limit1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>無</small></td>\n";}
$genre_list.="<td><small>$high_border1{$dir}</small></td>\n";
if($high_back_day1{$dir}>0){$genre_list.="<td><small>$high_back_day1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>×</small></td>\n";}
if($high_back_w1{$dir}){$genre_list.="<td><small>上</small></td>\n";}
else{$genre_list.="<td><small>別</small></td>\n";}
if($scorehst_back_day1{$dir}>0){$genre_list.="<td><small>$scorehst_back_day1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>×</small></td>\n";}
if($scorehst_back_w1{$dir}){$genre_list.="<td><small>上</small></td>\n";}
else{$genre_list.="<td><small>別</small></td>\n";}
$genre_list.="<td><small>$graph_border1{$dir}</small></td>\n";
$genre_list.="<td><small>$histry_div1{$dir}</small></td>\n";
if($day_limit1{$dir} ne ''){$genre_list.="<td><small>$day_limit1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>無</small></td>\n";}
if($num_limit1{$dir} ne ''){$genre_list.="<td><small>$num_limit1{$dir}</small></td>\n";}
else{$genre_list.="<td><small>無</small></td>\n";}
$genre_list.="<td><small>$no_limit1{$dir}</small></td>\n";
if($rec_com1{$dir} eq '1'){$genre_list.="<td><small>○</small></td>\n";}
else{$genre_list.="<td><small>×</small></td>\n";}
if($double_high1{$dir} eq '0'){$genre_list.="<td><small>×</small></td>\n";}
else{$genre_list.="<td><small>○</small></td>\n";}
$genre_list.='</tr>';
if($mode_name2{$dir} ne ''){
$genre_list.="<tr><td nowrap><small><a href=$quiz_cgi?d=$dir\&m=2&passch=$FORM{passch}>$mode_name2{$dir}</a></small></td>";
if($show_ans2{$dir}){$genre_list.='<td><small>○</small></td>';}else{$genre_list.='<td><small>×</small></td>';}
if($random2{$dir}){$genre_list.='<td nowrap><small>ランダム</small></td>';}else{$genre_list.='<td nowrap><small>固定</small></td>';}
if($quiz_max2{$dir}ne ''){$genre_list.="<td><small>$quiz_max2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>全</small></td>\n";}
if($play_max2{$dir}ne ''){$genre_list.="<td><small>$play_max2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>全</small></td>\n";}
if($bundle2{$dir} eq 1){$genre_list.="<td><small>有</small></td>\n";}
else{$genre_list.="<td><small>無</small></td>\n";}
if($lose_max2{$dir}ne ''){$genre_list.="<td><small>$lose_max2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>全</small></td>\n";}
if($time_limit2{$dir} > '0'){$genre_list.="<td><small>$time_limit2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>無</small></td>\n";}
$genre_list.="<td><small>$high_border2{$dir}</small></td>\n";
if($high_back_day2{$dir}>0){$genre_list.="<td><small>$high_back_day2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>×</small></td>\n";}
if($high_back_w2{$dir}){$genre_list.="<td><small>上</small></td>\n";}
else{$genre_list.="<td><small>別</small></td>\n";}
if($scorehst_back_day2{$dir}>0){$genre_list.="<td><small>$scorehst_back_day2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>×</small></td>\n";}
if($scorehst_back_w2{$dir}){$genre_list.="<td><small>上</small></td>\n";}
else{$genre_list.="<td><small>別</small></td>\n";}
$genre_list.="<td><small>$graph_border2{$dir}</small></td>\n";
$genre_list.="<td><small>$histry_div2{$dir}</small></td>\n";
if($day_limit2{$dir} ne ''){$genre_list.="<td><small>$day_limit2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>無</small></td>\n";}
if($num_limit2{$dir} ne ''){$genre_list.="<td><small>$num_limit2{$dir}</small></td>\n";}
else{$genre_list.="<td><small>無</small></td>\n";}
$genre_list.="<td><small>$no_limit2{$dir}</small></td>\n";
if($rec_com2{$dir} eq '1'){$genre_list.="<td><small>○</small></td>\n";}
else{$genre_list.="<td><small>×</small></td>\n";}
if($double_high2{$dir} eq '0'){$genre_list.="<td><small>×</small></td>\n";}
else{$genre_list.="<td><small>○</small></td>\n";}
$genre_list.='</tr>';
}
}
$genre_list.='</table><br>';
}
#************************************************
# システムデザイン情報の一覧
#************************************************
sub list_sysdesign_html{
&color_html;
if($#sysdesign_list < 0){$sysdesign_list='';return;}
local($formtag)=<<"_HTML_";
$formop_h
<input type=hidden name=type value=sdesed>
_HTML_
$sysdesign_list ="<b>●既存デザインの編集・複製をする場合は該当デザインを選んでください<br><br>";
$sysdesign_list .="<span>■システムデザイン別情報■</span></b>";
$sysdesign_list .="<br><table border=$border><tr>";
$sysdesign_list .=&my_print2(<<'_MY_','<td><small><center>','</center></small></td>');
デ<br>ザ<br>イ<br>ン<br>名
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>壁<br>紙
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>背<br>景<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>表<br>の<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>ジ<br>ャ<br>ン<br>ル<br>名<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>情<br>報<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>コ<br>メ<br>ン<br>ト<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>高<br>成<br>績<br>者<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>表<br>の<br>枠<br>の<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>文<br>字<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>リ<br>ン<br>ク<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>既<br>訪<br>問<br>リ<br>ン<br>ク<br>色
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>表<br>の<br>枠<br>の<br>高<br>さ
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>表<br>の<br>枠<br>の<br>幅
メ<br>ニ<br>ュ<br>｜<br>ペ<br>｜<br>ジ<br>の<br>表<br>の<br>枠<br>の<br>内<br>幅
履<br>歴<br>グ<br>ラ<br>フ<br>画<br>像<br>１
履<br>歴<br>グ<br>ラ<br>フ<br>画<br>像<br>２
表<br>の<br>レ<br>イ<br>ア<br>ウ<br>ト
表<br>内<br>文<br>字<br>レ<br>イ<br>ア<br>ウ<br>ト
編<br>集
複<br>製
削<br>除
_MY_
$alignj{l}='左揃';$alignj{c}='中揃';$alignj{r}='右揃';
foreach $id(@sysdesign_list){
if($SYS{design} eq $id){
$del_form='<td nowrap><small>使用中</small></td>';
}else{
$del_form="$formtag<td><input type=submit value='削除'><input type=hidden name=delid value='$id'></td></form>";
}
if($FORM{id} eq $id && $FORM{copyid} ne $id){
$edit_form="<td>編集中</td>";
}else{
$edit_form="$formtag<td><input type=submit value='編集'><input type=hidden name=id value='$id'></td></form>";
}
$sysdesign_list .=<<"_HTML_";
</tr><tr>
<td nowrap><small>$sysdesign_title{$id}</small></td>
<td nowrap><small><a href="$top_wall{$id}">$top_wall{$id}</a></small></td>
<td bgcolor='$top_back_color{$id}'><small><font color='$top_back_color{$id}'>■</font></small></td>
<td bgcolor='$top_table_color{$id}'><small><font color='$top_table_color{$id}'>■</font></small></td>
<td bgcolor='$top_genre_color{$id}'><small><font color='$top_genre_color{$id}'>■</font></small></td>
<td bgcolor='$top_info_color{$id}'><small><font color='$top_info_color{$id}'>■</font></small></td>
<td bgcolor='$top_com_color{$id}'><small><font color='$top_com_color{$id}'>■</font></small></td>
<td bgcolor='$top_high_color{$id}'><small><font color='$top_high_color{$id}'>■</font></small></td>
<td bgcolor='$top_border_color{$id}'><small><font color='$top_border_color{$id}'>■</font></small></td>
<td bgcolor='$top_text_color{$id}'><small><font color='$top_text_color{$id}'>■</font></small></td>
<td bgcolor='$top_link_color{$id}'><small><font color='$top_link_color{$id}'>■</font></small></td>
<td bgcolor='$top_vlink_color{$id}'><small><font color='$top_vlink_color{$id}'>■</font></small></td>
<td><small>$top_border_high{$id}</td>
<td><small>$top_border{$id}</td>
<td><small>$top_border_in{$id}</td>
<td><small><img width=10 height=10 src="$a_gif{$id}"></small></td>
<td><small><img width=10 height=10 src="$b_gif{$id}"></small></td>
<td><small>$alignj{$align{$id}}</small></td>
<td><small>$alignj{$walign{$id}}</small></td>
$edit_form
$formtag<td><input type=submit value="複製"><input type=hidden name=copyid value="$id"></td></form>
$del_form
_HTML_
}
$sysdesign_list.='</tr></table><br>';
}
#************************************************
# ジャンルデザイン情報の一覧
#************************************************
sub list_design_html{
if($#design_list < 0){$design_list='';return;}
local($formtag)=<<"_HTML_";
$formop_h
<input type=hidden name=type value=gdesed>
_HTML_
$design_list ="<br><b><span>■ジャンルデザイン別情報■</span></b><table border=$border><tr>";
$design_list .=&my_print2(<<'_MY_','<td><small><center>','</center></small></td>');
デ<br>ザ<br>イ<br>ン<br>名
文<br>字<br>色
リ<br>ン<br>ク<br>文<br>字<br>色
既<br>訪<br>問<br>リ<br>ン<br>ク<br>文<br>字<br>色
殿<br>堂<br>入<br>り<br>者<br>色
基<br>本<br>背<br>景<br>色
正<br>解<br>時<br>背<br>景<br>色
不<br>正<br>解<br>時<br>背<br>景<br>色
情<br>報<br>ウ<br>イ<br>ン<br>ド<br>ウ<br>色
表<br>の<br>ヘ<br>ッ<br>ダ<br>｜<br>色
表<br>の<br>色
表<br>の<br>枠<br>の<br>色
表<br>の<br>枠<br>の<br>高<br>さ
表<br>の<br>枠<br>の<br>幅
表<br>の<br>枠<br>の<br>内<br>幅
基<br>本<br>壁<br>紙
正<br>解<br>時<br>壁<br>紙
不<br>正<br>解<br>時<br>壁<br>紙
正<br>解<br>用<br>MIDI
不<br>正<br>解<br>用<br>MIDI
時<br>間<br>切<br>れ<br>用<br>MIDI
高<br>成<br>績<br>者<br>用<br>MIDI
使<br>用<br>中
編<br>集
複<br>製
削<br>除
_MY_
$alignj{l}='左揃';$alignj{c}='中揃';$alignj{r}='右揃';
foreach $id(@design_list){
if($FORM{id} eq $id && $FORM{copyid} ne $id){
$edit_form="<td>編集中</td>";
}else{
$edit_form="$formtag<td><input type=submit value='編集'><input type=hidden name=id value='$id'></td></form>";
}
if($design_use{$id} ne ''){
$use_form='<td nowrap><small><form><select>';
foreach $dir(split(/\t/,$design_use{$id})){
if($dir ne ''){
$use_form.="<option>$title{$dir}";
}
}
$use_form.='</select></small></td></form>';
$del_form='<td>使用中</td>';
}else{
$use_form='<td>　</td>';
$del_form="$formtag<td><input type=submit value='削除'><input type=hidden name=delid value='$id'></td></form>";
}
if($wall{$id} ne ''){$wall_a="<a href='$wall{$id}'>■</a>"}
else{$wall_a='　';}
if($win_wall{$id} ne ''){$win_wall_a="<a href='$win_wall{$id}'>■</a>";}
else{$win_wall_a='　';}
if($lose_wall{$id} ne ''){$lose_wall_a="<a href='$lose_wall{$id}'>■</a>";}
else{$lose_wall_a='　';}
if($win_midi{$id} ne ''){$win_midi_a="<a href='$win_midi{$id}'>■</a>";}
else{$win_midi_a='　';}
if($lose_midi{$id} ne ''){$lose_midi_a="<a href='$lose_midi{$id}'>■</a>";}
else{$lose_midi_a='　';}
if($end_midi{$id} ne ''){$end_midi_a="<a href='$end_midi{$id}'>■</a>";}
else{$end_midi_a='　';}
if($high_midi{$id} ne ''){$high_midi_a="<a href='$high_midi{$id}'>■</a>";}
else{$high_midi_a='　';}
$design_list .=<<"_HTML_";
</tr><tr>
<td nowrap><small>$design_title{$id}</small></td>
<td bgcolor='$text_color{$id}'><small><font color='$text_color{$id}'>■</font></small></td>
<td bgcolor='$link_color{$id}'><small><font color='$link_color{$id}'>■</font></small></td>
<td bgcolor='$vlink_color{$id}'><small><font color='$vlink_color{$id}'>■</font></small></td>
<td bgcolor='$champ_color{$id}'><small><font color='$champ_color{$id}'>■</font></small></td>
<td bgcolor='$main_color{$id}'><small><font color='$main_color{$id}'>■</font></small></td>
<td bgcolor='$win_color{$id}'><small><font color='$win_color{$id}'>■</font></small></td>
<td bgcolor='$lose_color{$id}'><small><font color='$lose_color{$id}'>■</font></small></td>
<td bgcolor='$com_color{$id}'><small><font color='$com_color{$id}'>■</font></small></td>
<td bgcolor='$th_color{$id}'><small><font color='$th_color{$id}'>■</font></small></td>
<td bgcolor='$td_color{$id}'><small><font color='$td_color{$id}'>■</font></small></td>
<td bgcolor='$border_color{$id}'><small><font color='$border_color{$id}'>■</font></small></td>
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
$formtag<td><input type=submit value="複製"><input type=hidden name=copyid value="$id"></td></form>
$del_form
_HTML_
}
$design_list.='</tr></table><br>';
}
#************************************************
# システム設定編集HTML表示処理
#************************************************
sub edit_sys_html{
&list_sys_html;
&color_html;
&form_to_form;
$main_html.=<<"_HTML_";
$formop_nh
<input type=hidden name=type value=sys2>
<span><br><br><b>●各項目を入力し編集ボタンを押してください。</b>( * 印は必須項目)<br><br>
<b>■システム設定フォーム■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=sys target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3 bgcolor=#eeaaee><span><center>■■■■■システム設定■■■■■</center></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(1)プレイログ保護期間 *
<input type=text name='li' value="$FORM2{li}" size=10>分　(半角整数)
(2)同時プレイ人数 *
<input type=text name='mp' value="$FORM2{mp}" size=10>人　(任意の整数)
(3)クッキーID *
<input type=text name='cok' value="$FORM2{cok}" size=10>　(半角英数)
(4)選択肢形式 *
<input type=radio name='qf' value=2$FORM{'qf-2'}>フォームボタン　<input type=radio name='qf' value=1$FORM{'qf-1'}>ラジオボタン　<input type=radio name='qf' value=0$FORM{'qf-0'}>リンク
(5)トップページへのURL
<input type=text name='tu' value="$FORM2{tu}" size=40>
(6)メニューページのタイトル *
<input type=text name='mt' value="$FORM2{mt}" size=40>
_MY_
$main_html.=<<"_HTML_";
<tr><td nowrap><small>(7)メニューページのヘッダー</small></td><td colspan=2><span>
\$title→メニューページのタイトル<br>\$top→トップページへのリンク<br>\$imode→携帯専用へのリンク　　に自動変換<br><textarea cols=70 rows=5 name=hd>\n$FORM3{hd}</textarea></span></td></tr>
<tr><td nowrap><small>(8)サブページのヘッダー</small></td><td colspan=2><span>
\$title→メニューページのタイトル<br>\$sub_title→サブページのタイトル<br>\$genre→ジャンル名<br>\$mode→モード名<br>\$top→トップページへのリンク<br>\$index→メニューページのリンク<br>\$challenge→挑戦ページへのリンク<br>\$high→高成績者ページへのリンク<br>\$graph→成績分布へのリンク<br>\$score→出題状況へのリンク<br>\$add→問題投稿へのリンク　　に自動変換<br><textarea cols=70 rows=5 name=shd>\n$FORM3{shd}</textarea></span></td></tr>
<tr><td nowrap><small>(9)メニューページのコメント</small></td><td colspan=2><span>
改行→&lt;BR&gt;　　に自動変換<br><textarea cols=70 rows=5 name=tmes>\n$FORM3{tmes}</textarea><br><input type=checkbox name=tt value=1$FORM{'tt-1'}>tableで表\示</span></td></tr>
<tr><td nowrap><small>(10)スタイルシート *</small></td><td colspan=2><span>
<input type=radio name=stl value=0$FORM{'stl-0'}>使わない<br>
<input type=radio name=stl value=1$FORM{'stl-1'}>使う<br>
<textarea cols=70 rows=5 name=stl-2>\n$FORM3{'stl-2'}</textarea></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(11)システムデザイン
${&select_sysdesign($FORM{sdes})}$ret
(12)メニューページ表\示項目 *
<input type=radio name='ey' value="0"$FORM{'ey-0'}>詳細　<input type=radio name='ey' value="1"$FORM{'ey-1'}>普通　<input type=radio name='ey' value="2"$FORM{'ey-2'}>簡易　<input type=radio name='ey' value="3"$FORM{'ey-3'}>一覧
(13)回答時間による順位付け *
<input type=radio name='rt' value="0"$FORM{'rt-0'}>行わない　<input type=radio name='rt' value="1"$FORM{'rt-1'}>行う
(14)自動文字折り返し *
<input type=radio name='wr' value="0"$FORM{'wr-0'}>行わない　<input type=radio name='wr' value="1"$FORM{'wr-1'}>行う
_MY_
$main_html.=<<"_HTML_";
<tr><td colspan=3><center><br><span><input type=submit value="　　保存　　"></span></center></td></tr></table></form>
${&focus_move('li')}$ret
_HTML_
}
#************************************************
# ジャンル編集画面HTML表示処理
#************************************************
sub edit_genre_html{
&list_genre_html($FORM{d});
&color_html;
&form_to_form;
$main_html.=<<"_HTML_";
$formop_nh
<input type=hidden name=type value=editg2>
<input type=hidden name=menu value=1>
<span><br><br><b>●各項目を入力し編集ボタンを押してください。</b>( * 印は必須項目)<br><br>
<b>■ジャンル設定フォーム■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=genre target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
_HTML_
$main_html.=&my_print(<<"_MY_");
<center>■■■■■新ジャンル作成時の設定■■■■■</center></span>\t#bbbbbb\n
(1)ディレクトリ *
<input type=hidden name=d value="$FORM{d}">$FORM{d}
<center>■■■■■ジャンルの動作設定■■■■■</center>\t#eeaaaa\n
(2)タイトル *
<input type=text name='t' value="$FORM2{t}" size=45>
_MY_
$main_html.="<tr><td nowrap><small>(3)紹介文</small></td><td colspan=2><span>改行→&lt;BR&gt;　　に自動変換<br><textarea name='tc' cols=45 rows=5>\n$FORM3{tc}</textarea></span></td></tr>";
$main_html.="<tr><td nowrap><small>(4)クイズ開始メッセージ</small></td><td colspan=2><span>
<table border=0><tr><td nowrap><span>改行<br>\$title<br>\$quiz_max<br>\$play_max<br>\$lose_max<br>\$challenge<br>\$high<br>\$time<br>\$champion</span></td><td nowrap><span>→&lt;BR&gt;<br>→ジャンルタイトル<br>→総問題数<br>→出題数<br>→許容誤答数<br>→挑戦者数<br>→合格ライン(％)<br>→制限時間(秒)<br>→最高成績</span></td></tr></table>に自動変換<br><textarea name='stc' cols=45 rows=5>\n$FORM3{stc}</textarea></span></td></tr>";
$main_html.=<<"_HTML_";
<tr><td nowrap><small>(5)問題ファイル *</small></td><td colspan=2>
_HTML_
if($#genre_dir_orign > 0){
$main_html.=<<"_HTML_";
<span><input type=radio name='md' value='0'$FORM{'md-0'}>オリジナル問題ファイルを使用する<br>
<table border=0 cellspacing=0 cellpadding=0>
<tr><td colspan=2 nowrap><span>
<input type=radio name='md' value='1'$FORM{'md-1'}>他のジャンルの問題ファイルを使用する　</span></td></tr>
<tr><td><span>　　　　</span></td><td>
<table border=1><tr><td>ジャンル名</td><td>使用問題数</td>
_HTML_
foreach(@genre_dir_orign){
if($FORM{d} eq $_){next;}
$main_html.=<<"_HTML_";
<tr><td nowrap><span>$title{$_}</span></td>
<td nowrap><span><input type=text size=4 name='smd-$_' value="$FORM2{"smd-$_"}" size=15>問 (半角数字 又は all)</span></td></tr>
_HTML_
}
$main_html.='</table></td></tr></table></td></tr>';
}else{
$main_html.="<span><input type=hidden name='md' value='0'>オリジナル問題ファイルを使用する</td></tr>";
}
$main_html.=&my_print(<<"_MY_");
(6)ジャンルの動作状態 *
<input type=radio name='me' value='1'$FORM{'me-1'}>公開中\t<input type=radio name='me' value='0'$FORM{'me-0'}>$_underconst
(7)投稿問題の受付 *
<input type=radio name='ct' value="1"$FORM{'ct-1'}>受け付ける　<input type=radio name='ct' value="0"$FORM{'ct-0'}>受け付けない
(8)テキスト形式の投稿問題 *
<input type=radio name='nt' value="0"$FORM{'nt-0'}>受け付ける　<input type=radio name='nt' value="1"$FORM{'nt-1'}>受け付けない
(9)投稿問題の自動採用 *
<input type=radio name='dc' value="0"$FORM{'dc-0'}>行わない　<input type=radio name='dc' value="1"$FORM{'dc-1'}>行う
(10)出題状況表\示での問題文表\示 *
<input type=radio name='sd' value="1"$FORM{'sd-1'}>行わない　<input type=radio name='sd' value="0"$FORM{'sd-0'}>行う
(11)問題文への作成者表\示 *
<input type=radio name='ath' value="1"$FORM{'ath-1'}>行う　<input type=radio name='ath' value="0"$FORM{'ath-0'}>行わない
(12)デザイン
${&select_design($FORM{gdes})}$ret
<center>■■■■■モード１の動作設定■■■■■</center>\t#eeeeaa\n
(13)モード名 *
<input type=text name='mn1' value="$FORM2{mn1}" size=20>
(14)正解表\示 *
<input type=radio name='sa1' value='0'$FORM{'sa1-0'}>行わない\t<input type=radio name='sa1' value='1'$FORM{'sa1-1'}>行う
(15)出題順序 *
<input type=radio name='r1' value='1'$FORM{'r1-1'}>ランダム\t<input type=radio name='r1' value='0'$FORM{'r1-0'}>固定
(16)使用問題数 *
<input type=radio name=qm1 value="1"$FORM{'qm1-1'}>全登録問題数\t<input type=radio name=qm1 value="0"$FORM{'qm1-0'}><input type=text name='qm1-2' value="$FORM2{'qm1-2'}" size=5>問まで
(17)出題問題数 *
<input type=radio name=pm1 value="1"$FORM{'pm1-1'}>全使用問題数\t<input type=radio name=pm1 value="0"$FORM{'pm1-0'}><input type=text name='pm1-2' value="$FORM2{'pm1-2'}" size=5>問
(18)一括出題 *
<input type=radio name=bd1 value="0"$FORM{'bd1-0'}>行わない\t<input type=radio name=bd1 value="1"$FORM{'bd1-1'}>行う
(19)終了条件誤答数 *
<input type=radio name=lm1 value="1"$FORM{'lm1-1'}>全出題問題数\t<input type=radio name=lm1 value="0"$FORM{'lm1-0'}><input type=text name='lm1-2' value="$FORM2{'lm1-2'}" size=5>問
(20)制限時間 *
<input type=radio name=tl1 value="1"$FORM{'tl1-1'}>無し\t<input type=radio name=tl1 value="0"$FORM{'tl1-0'}><input type=text name='tl1-2' value="$FORM2{'tl1-2'}" size=5>秒
(21)合格点 *
<input type=text name='hb1' value="$FORM2{hb1}" size=5>％以上
(22)高成績者のBACK UP *
<input type=radio name=hbu1 value="0"$FORM{'hbu1-0'}>行わない\t<input type=radio name=hbu1 value="1"$FORM{'hbu1-1'}>行う<input type=text name='hbu1-2' value="$FORM2{'hbu1-2'}" size=5>日おき
(23)高成績者のBACK UP方式 *
<input type=radio name=hbw1 value="1"$FORM{'hbw1-1'}>上書き\t<input type=radio name=hbw1 value="0"$FORM{'hbw1-0'}>別ファイル
(24)成績分布のBACK UP *
<input type=radio name=sbu1 value="0"$FORM{'sbu1-0'}>行わない\t<input type=radio name=sbu1 value="1"$FORM{'sbu1-1'}>行う<input type=text name='sbu1-2' value="$FORM2{'sbu1-2'}" size=5>日おき
(25)成績分布のBACK UP方式 *
<input type=radio name=sbw1 value="1"$FORM{'sbw1-1'}>上書き\t<input type=radio name=sbw1 value="0"$FORM{'sbw1-0'}>別ファイル
(26)成績分布省略表\示 *
<input type=text name='gb1' value="$FORM2{gb1}" size=5>％以上のグラフは省略表\示
(27)成績分布集計単位 *
<input type=text name='hd1' value="$FORM2{hd1}" size=5>問毎に集計
(28)高成績者日数制限 *
<input type=radio name=dl1 value="1"$FORM{'dl1-1'}>無制限\t<input type=radio name=dl1 value="0"$FORM{'dl1-0'}>過去<input type=text name='dl1-2' value="$FORM2{'dl1-2'}" size=5>日
(29)高成績者人数制限 *
<input type=radio name=nl1 value="1"$FORM{'nl1-1'}>無制限\t<input type=radio name=nl1 value="0"$FORM{'nl1-0'}>上位<input type=text name='nl1-2' value="$FORM2{'nl1-2'}" size=5>人
(30)殿堂入り人数 *
上位<input type=text name=no1 value="$FORM2{no1}" size=5>人
(31)高成績者コメント記録 *
<input type=radio name=rc1 value="0"$FORM{'rc1-0'}>行わない\t<input type=radio name=rc1 value="1"$FORM{'rc1-1'}>行う
(32)同ホスト同スコア *
<input type=radio name=dh1 value="1"$FORM{'dh1-1'}>認める\t<input type=radio name=dh1 value="0"$FORM{'dh1-0'}>認めない
<center>■■■■■モード２の動作設定■■■■■</center></span>\t#eeaaee\n
(33)モード名<font color=red>(注)</cont>
<input type=text name='mn2' value="$FORM2{mn2}" size=20>
(34)正解表\示
<input type=radio name='sa2' value='0'$FORM{'sa2-0'}>行わない\t<input type=radio name='sa2' value='1'$FORM{'sa2-1'}>行う
(35)出題順序
<input type=radio name='r2' value='1'$FORM{'r2-1'}>ランダム\t<input type=radio name='r2' value='0'$FORM{'r2-0'}>固定
(36)使用問題数
<input type=radio name=qm2 value="1"$FORM{'qm2-1'}>全登録問題数\t<input type=radio name=qm2 value="0"$FORM{'qm2-0'}><input type=text name='qm2-2' value="$FORM2{'qm2-2'}" size=5>問まで
(37)出題問題数
<input type=radio name=pm2 value="1"$FORM{'pm2-1'}>全使用問題数\t<input type=radio name=pm2 value="0"$FORM{'pm2-0'}><input type=text name='pm2-2' value="$FORM2{'pm2-2'}" size=5>問
(38)一括出題 *
<input type=radio name=bd2 value="0"$FORM{'bd2-0'}>行わない\t<input type=radio name=bd2 value="1"$FORM{'bd2-1'}>行う
(39)終了条件誤答数
<input type=radio name=lm2 value="1"$FORM{'lm2-1'}>全出題問題数\t<input type=radio name=lm2 value="0"$FORM{'lm2-0'}><input type=text name='lm2-2' value="$FORM2{'lm2-2'}" size=5>問
(40)制限時間 *
<input type=radio name=tl2 value="1"$FORM{'tl2-1'}>無し\t<input type=radio name=tl2 value="0"$FORM{'tl2-0'}><input type=text name='tl2-2' value="$FORM2{'tl2-2'}" size=5>秒
(41)合格点
<input type=text name='hb2' value="$FORM2{hb2}" size=5>％以上
(42)高成績者のBACK UP *
<input type=radio name=hbu2 value="0"$FORM{'hbu2-0'}>行わない\t<input type=radio name=hbu2 value="1"$FORM{'hbu2-1'}>行う<input type=text name='hbu2-2' value="$FORM2{'hbu2-2'}" size=5>日おき
(43)高成績者のBACK UP方式 *
<input type=radio name=hbw2 value="1"$FORM{'hbw2-1'}>上書き\t<input type=radio name=hbw2 value="0"$FORM{'hbw2-0'}>別ファイル
(44)成績分布のBACK UP *
<input type=radio name=sbu2 value="0"$FORM{'sbu2-0'}>行わない\t<input type=radio name=sbu2 value="1"$FORM{'sbu2-1'}>行う<input type=text name='sbu2-2' value="$FORM2{'sbu2-2'}" size=5>日おき
(45)成績分布のBACK UP方式 *
<input type=radio name=sbw2 value="1"$FORM{'sbw2-1'}>上書き\t<input type=radio name=sbw2 value="0"$FORM{'sbw2-0'}>別ファイル
(46)成績分布省略表\示
<input type=text name='gb2' value="$FORM2{gb2}" size=5>％以上のグラフは省略表\示
(47)成績分布集計単位
<input type=text name='hd2' value="$FORM2{hd2}" size=5>問毎に集計
(48)高成績者日数制限
<input type=radio name=dl2 value="1"$FORM{'dl2-1'}>無制限\t<input type=radio name=dl2 value="0"$FORM{'dl2-0'}>過去<input type=text name='dl2-2' value="$FORM2{'dl2-2'}" size=5>日
(49)高成績者人数制限
<input type=radio name=nl2 value="1"$FORM{'nl2-1'}>無制限\t<input type=radio name=nl2 value="0"$FORM{'nl2-0'}>上位<input type=text name='nl2-2' value="$FORM2{'nl2-2'}" size=5>人
(50)殿堂入り人数 *
上位<input type=text name=no2 value="$FORM2{no2}" size=5>人
(51)高成績者コメント記録 *
<input type=radio name=rc2 value="0"$FORM{'rc2-0'}>行わない\t<input type=radio name=rc2 value="1"$FORM{'rc2-1'}>行う
(52)同ホスト同スコア
<input type=radio name=dh2 value="1"$FORM{'dh2-1'}>認める\t<input type=radio name=dh2 value="0"$FORM{'dh2-0'}>認めない
<center><br><input type=submit value="　　保存　　"></center>
_MY_
$main_html.='</table><small><font color=red>(注)</font>モード２のモード名が入力されているときのみモード２が動作する。</small></form>';
$main_html.="${&focus_move('t')}$ret";
}
#************************************************
# システムデザイン編集HTML
#************************************************
sub edit_sysdesign_html{
local($button);
local($edit,$type)=@_;
if($#sysdesign_list>=0){
&list_sysdesign_html();
}
&form_to_form;
if($type eq 'edit'){
$button='保存';
$edit=$sysdesign_title{$edit};
}elsif($type eq 'copy'){
$button='複製保存';
$edit="$sysdesign_title{$edit}";
}else{
$button='新規作成保存';
$edit="新規作成";
}
$main_html.=<<"_HTML_";
$formop_nh
<input type=hidden name=type value=sdesed2>
<input type=hidden name=id value="$FORM{id}">
<input type=hidden name=edittype value="$type">
<span><br><br><b>●各項目を入力し$buttonボタンを押してください。</b>( * 印は必須項目)<br><br>
<b>■システムデザイン設定フォーム■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=sysd target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3 bgcolor=#eeaaee><span><center>■■■■■システムデザイン設定■■■■■</center></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(1)編集元
$edit
(2)システムデザイン名 *
<input type=text name='sdt' value="$FORM{sdt}" size=30>
(3)メニューページの壁紙
<input type=text name='tw' value="$FORM2{tw}" size=30>
(4)メニューページの背景色 *
<input type=text name='tbc' value="$FORM2{tbc}" size=10>
(5)メニューページの表\の色 *
<input type=text name='ttc' value="$FORM2{ttc}" size=10>
(6)メニューページのジャンル色 *
<input type=text name='tjc' value="$FORM2{tjc}" size=10>
(7)メニューページの情報色 *
<input type=text name='tic' value="$FORM2{tic}" size=10>
(8)メニューページのコメント色 *
<input type=text name='tcc' value="$FORM2{tcc}" size=10>
(9)メニューページの高成績者色 *
<input type=text name='thc' value="$FORM2{thc}" size=10>
(10)メニューページの表\の枠の色 *
<input type=text name='tbdc' value="$FORM2{tbdc}" size=10>
(11)メニューページの文字色 *
<input type=text name='txc' value="$FORM2{txc}" size=10>
(12)メニューページのリンク色 *
<input type=text name='lc' value="$FORM2{lc}" size=10>
(13)メニューページの既訪問リンク色 *
<input type=text name='vc' value="$FORM2{vc}" size=10>
(14)メニューページの表\の枠の高さ *
<input type=text name='tbdh' value="$FORM2{tbdh}" size=10>
(15)メニューページの表\の枠の幅 *
<input type=text name='tbd' value="$FORM2{tbd}" size=10>
(16)メニューページの表\の枠の内幅 *
<input type=text name='tbdi' value="$FORM2{tbdi}" size=10>
(17)成績履歴グラフ画像１ *
<input type=text name='ag' value="$FORM2{ag}" size=30>
(18)成績履歴グラフ画像２ *
<input type=text name='bg' value="$FORM2{bg}" size=30>
(19)表\のレイアウト *
<input type=radio name='al' value="l"$FORM{'al-l'}>左揃　<input type=radio name='al' value="c"$FORM{'al-c'}>中揃　<input type=radio name='al' value="r"$FORM{'al-r'}>右揃
(20)表\内文字レイアウト *
<input type=radio name='wal' value="l"$FORM{'wal-l'}>左揃　<input type=radio name='wal' value="c"$FORM{'wal-c'}>中揃　<input type=radio name='wal' value="r"$FORM{'wal-r'}>右揃
_MY_
$main_html.=<<"_HTML_";
<tr><td colspan=3><center><br><span><input type=submit value="　　 $button 　　"></span></center></td></tr></table></form>
${&focus_move('sdt')}$ret
_HTML_
}
#************************************************
# ジャンルデザイン編集HTML
#************************************************
sub edit_design_html{
local($button);
local($edit,$type)=@_;
if($#design_list>=0){
&list_design_html();
}
&form_to_form;
if($type eq 'edit'){
$button='保存';
$edit=$design_title{$edit};
}elsif($type eq 'copy'){
$button='複製保存';
$edit="$design_title{$edit}";
}else{
$button='新規作成保存';
$edit="新規作成";
}
$main_html.=<<"_HTML_";
$formop_nh
<input type=hidden name=type value=gdesed2>
<input type=hidden name=id value="$FORM{id}">
<input type=hidden name=edittype value="$type">
<span><br><br><b>●各項目を入力し$buttonボタンを押してください。</b>( * 印は必須項目)<br><br>
<b>■ジャンルデザイン設定フォーム■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=gend target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3 bgcolor=#eeaaee><span><center>■■■■■ジャンルデザイン設定■■■■■</center></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(1)編集元
$edit
(2)ジャンルデザイン名 *
<input type=text name='gdt' value="$FORM{gdt}" size=30>
(3)文字色 *
<input type=text name='gtc' value="$FORM2{gtc}" size=10>
(4)リンク文字色 *
<input type=text name='glc' value="$FORM2{glc}" size=10>
(5)既訪問リンク文字色 *
<input type=text name='gvc' value="$FORM2{gvc}" size=10>
(6)殿堂入り者文字色 *
<input type=text name='gcc' value="$FORM2{gcc}" size=10>
(7)基本背景色 *
<input type=text name='gmc' value="$FORM2{gmc}" size=10>
(8)正解時背景色 *
<input type=text name='gwi' value="$FORM2{gwi}" size=10>
(9)不正解時背景色 *
<input type=text name='glo' value="$FORM2{glo}" size=10>
(10)情報ウインドウの色 *
<input type=text name='gcm' value="$FORM2{gcm}" size=10>
(11)表\のヘッダー色 *
<input type=text name='thc' value="$FORM2{thc}" size=10>
(12)表\の色 *
<input type=text name='tdc' value="$FORM2{tdc}" size=10>
(13)表\の枠の色 *
<input type=text name='bdc' value="$FORM2{bdc}" size=10>
(14)表\の枠の高さ *
<input type=text name='bdh' value="$FORM2{bdh}" size=10>
(15)表\の枠の幅 *
<input type=text name='bd' value="$FORM2{bd}" size=10>
(16)表\の枠の内幅 *
<input type=text name='bdi' value="$FORM2{bdi}" size=10>
(17)基本壁紙
<input type=text name='gw' value="$FORM2{gw}" size=30>
(18)正解時壁紙
<input type=text name='gww' value="$FORM2{gww}" size=30>
(19)不正解時壁紙
<input type=text name='glw' value="$FORM2{glw}" size=30>
(20)正解表\示 *
<input type=text name='wsg' value="$FORM2{wsg}" size=100>
(21)不正解表\示 *
<input type=text name='lsg' value="$FORM2{lsg}" size=100>
(22)タイムオーバー表\示 *
<input type=text name='osg' value="$FORM2{osg}" size=100>
(23)正解時MIDI
<input type=text name='wmd' value="$FORM2{wmd}" size=30>
(24)不正解時MIDI
<input type=text name='lmd' value="$FORM2{lmd}" size=30>
(25)クイズ終了時MIDI
<input type=text name='emd' value="$FORM2{emd}" size=30>
(26)高成績者用MIDI
<input type=text name='hmd' value="$FORM2{hmd}" size=30>
_MY_
$main_html.=<<"_HTML_";
<tr><td colspan=3><center><br><span><input type=submit value="　　 $button 　　"></span></center></td></tr></table></form>
${&focus_move('gdt')}$ret
_HTML_
}
#************************************************
# 問題登録処理HTML
#************************************************
sub edit_quiz_html{
if($#mondai < 0){$main_html.='<span><br><br><b>■編集問題選択リスト■</b><br><br>●現在このジャンルで登録済みの問題はありません。</span>';return;}
$main_html.=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qedit1>
<input type=hidden name=menu value=1>
<input type=hidden name=ed value=edit>
<span><br><br><b>●以下のリストから編集したい問題のラジオボタンにチェックを入れ、実行ボタンを押してください。</b><br><br>
_HTML_
local($colspan);$colspan=2;
$FORM{"qn-$FORM{qn}"}=' checked';
$main_html.='<b>■編集問題選択リスト■</b></span>';
$main_html.="<table $sys_tbl_opt bgcolor='$sys_color'><tr><td nowrap><small>番号</small></td>";
$main_html.="<td><small>選択</small></td>";
if($FORM{lst_q} ne ''){$main_html.='<td><small>問題</small></td>';$colspan++;}
if($FORM{lst_a} ne ''){$main_html.='<td><small>解答</small></td>';$colspan++;}
if($FORM{lst_m} ne ''){$main_html.='<td colspan=4><small>誤答</small></td>';$colspan=$colspan+4;}
if($FORM{lst_am} ne ''){$main_html.='<td><small>解答メッセージ</small></td>';$colspan++;}
if($FORM{lst_mm} ne ''){$main_html.='<td><small>誤答メッセージ</small></td>';$colspan++;}
if($FORM{lst_cf} ne ''){$main_html.='<td><small>参考文献</small></td>';$colspan++;}
if($FORM{lst_dg} ne ''){$main_html.='<td><small>問題内容</small></td>';$colspan++;}
if($FORM{lst_mm1} ne ''){$main_html.='<td colspan=4><small>誤答別メッセージ</small></td>';$colspan=$colspan+4;}
if($FORM{lst_ath} ne ''){$main_html.='<td colspan=1><small>作成者</small></td>';$colspan++;}
if($FORM{lst_at} ne ''){$main_html.='<td colspan=1><small>回答方式</small></td>';$colspan++;}
$main_html.='</tr>';
$i=0;@opt=('選択','入力');
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
<tr><td colspan=$colspan nowrap><span><center><input type=submit value="  実行  ">
<input type=checkbox name=lst_q$FORM{lst_q_1} value=1>問題
<input type=checkbox name=lst_a$FORM{lst_a_1} value=1>解答
<input type=checkbox name=lst_m$FORM{lst_m_1} value=1>誤答
<input type=checkbox name=lst_am$FORM{lst_am_1} value=1>解答メッセージ
<input type=checkbox name=lst_mm$FORM{lst_mm_1} value=1>誤答メッセージ
<input type=checkbox name=lst_cf$FORM{lst_cf_1} value=1>参考文献
<input type=checkbox name=lst_dg$FORM{lst_dg_1} value=1>問題内容
<input type=checkbox name=lst_mm1$FORM{lst_mm1_1} value=1>誤答別メッセージ
<input type=checkbox name=lst_ath$FORM{lst_ath_1} value=1>作成者
<input type=checkbox name=lst_at$FORM{lst_at_1} value=1>回答方式
</center></span></td></tr></table></form>
_HTML_
}
#************************************************
# 問題入力formHTML
#************************************************
sub edit_quiz_form{
&form_to_form;
$file_age=time-(-M "$FORM{d}/$mondai_$FORM{d}\.cgi")*(60*60*24);
if($FORM{ed} eq 'edit'){$FORM{ed_edit}=' checked';}
else{$FORM{ed_new}=' checked';}
if($FORM{qn} ne ''){
if($FORM{ed} eq 'edit'){
$FORM{ed_edit}=' checked';
$num_text="<input type=radio name=ed value='edit'$FORM{ed_edit}>編集→第 $FORM{qn} 問目";
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
<span><br><br><b>●各項目に入力し、送信ボタンを押してください。<br>
既登録の問題の編集は、まず下の編集問題選択リストから選んでから行って下さい。</b>　( * 印は必須項目です。)<br><br>
<b>■問題編集フォーム■</b></span><small>改行→&lt;BR&gt;　　に自動変換</small>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3><center><span>
<input type=radio name=ed value='new'$FORM{ed_new}>新規追加　
$num_text
</center></span></td></tr>
<tr><td><small>回答方式</small></td><td colspan=2><input type=checkbox name=atype value=1 $FORM{atype_1}>テキスト入力方式</td></tr>
<tr><td><small>問題文 *</small></td><td colspan=2><textarea name=qqu cols=65 rows=3>\n$FORM3{qqu}</textarea></td></tr>
<tr><td><small>正解 * ※</small></td><td colspan=2><textarea name=qas cols=65 rows=3>\n$FORM3{qas}</textarea></td></tr>
<tr><td><small>誤答１ * ※</small></td><td colspan=2><textarea name=qmas1 cols=65 rows=3>\n$FORM3{qmas1}</textarea></td></tr>
<tr><td><small>誤答２ ※</small></td><td colspan=2><textarea name=qmas2 cols=65 rows=3>\n$FORM3{qmas2}</textarea></td></tr>
<tr><td><small>誤答３ ※</small></td><td colspan=2><textarea name=qmas3 cols=65 rows=3>\n$FORM3{qmas3}</textarea></td></tr>
<tr><td><small>誤答４ ※</small></td><td colspan=2><textarea name=qmas4 cols=65 rows=3>\n$FORM3{qmas4}</textarea></td></tr>
<tr><td><small>正解時コメント</small></td><td colspan=2><textarea name=qac cols=65 rows=2>\n$FORM3{qac}</textarea></span></td></tr>
<tr><td nowrap><small>不正解時コメント</small></td><td colspan=2><textarea name=qmac cols=65 rows=2>\n$FORM3{qmac}</textarea></span></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
参考文献
<small><input type=text size=65 name=qcf value="$FORM2{qcf}"></small>
問題内容
<small><input type=text size=65 name=qdg value="$FORM2{qdg}"></small>
_MY_
$main_html.=<<"_HTML_";
<tr><td nowrap><small>誤答１時コメント</small></td><td colspan=2><textarea name=qmac1 cols=65 rows=2>\n$FORM3{qmac1}</textarea></span></td></tr>
<tr><td nowrap><small>誤答２時コメント</small></td><td colspan=2><textarea name=qmac2 cols=65 rows=2>\n$FORM3{qmac2}</textarea></span></td></tr>
<tr><td nowrap><small>誤答３時コメント</small></td><td colspan=2><textarea name=qmac3 cols=65 rows=2>\n$FORM3{qmac3}</textarea></span></td></tr>
<tr><td nowrap><small>誤答４時コメント</small></td><td colspan=2><textarea name=qmac4 cols=65 rows=2>\n$FORM3{qmac4}</textarea></span></td></tr>
<tr><td nowrap><small>作成者</small></td><td colspan=2><small><input type=text size=65 name=auth value="$FORM2{auth}"></small></td></tr>
<tr><td colspan=3><center><table border=0><tr><td><span><input type=submit value="　　 送信 　　"></span></td></form>
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
<td><span><input type=submit value="　　クリア　　"></span></td></tr></table>
</center></td></tr></table></form>
※回答方式がテキスト入力形式の場合、各行が正解（誤答）となります。<br>
いずれかの行と、回答欄に入力された文字列が一致した場合正解（誤答）となります。<br>
_HTML_
}
#************************************************
# 問題登録処理HTML
#************************************************
sub edit_cont_html{
if($#mondai < 0){$main_html.='<span><br><br><b>■編集問題選択リスト■</b><br><br>現在このジャンルで登録済みの投稿問題はありません。</span>';return;}
$main_html.=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qcont>
<input type=hidden name=menu value=1>
<input type=hidden name=ed value=1>
<span><br><br><b>●以下のリストから編集したい問題のラジオボタンにチェックを入れ、実行ボタンを押してください。<br>
また、追加削除、削除を行いたい問題にチェックを入れて下さい。(複数選択可)</b><br><br>
_HTML_
local($colspan);$colspan=4;
$FORM{"qn-$FORM{qn}"}=' checked';
$main_html.='<b>■編集問題選択リスト■</b></span>';
$main_html.="<table border=3 cellspacing=1 cellpadding=2 bgcolor='$sys_color'><tr><td nowrap><small>番<br>号</small></td>";
$main_html.="<td><small>編<br>集</small></td><td nowrap><small>追加<br>削除</small></td><td><small>削<br>除</small></td>";
if($FORM{lst_q} ne ''){$main_html.='<td width=300 nowrap><small>問題</small></td>';$colspan++;}
if($FORM{lst_a} ne ''){$main_html.='<td width=100 nowrap><small>解答</small></td>';$colspan++;}
if($FORM{lst_m} ne ''){$main_html.='<td width=100 nowrap><small>誤答</small></td>';$colspan=$colspan+4;}
if($FORM{lst_am} ne ''){$main_html.='<td width=100 nowrap><small>正解メッセージ</small></td>';$colspan++;}
if($FORM{lst_mm} ne ''){$main_html.='<td width=100 nowrap><small>誤答メッセージ</small></td>';$colspan++;}
if($FORM{lst_mm1} ne ''){$main_html.='<td width=100 nowrap><small>誤答別メッセージ</small></td>';$colspan=$colspan+4;}
if($FORM{lst_cf} ne ''){$main_html.='<td width=100 nowrap><small>参考文献</small></td>';$colspan++;}
if($FORM{lst_dg} ne ''){$main_html.='<td width=100 nowrap><small>問題内容</small></td>';$colspan++;}
if($FORM{lst_ath} ne ''){$main_html.='<td width=100 nowrap><small>作成者</small></td>';$colspan++;}
if($FORM{lst_at} ne ''){$main_html.='<td><small>回答方式</small></td>';$colspan++;}
$main_html.='</tr>';
$i=0;
my(%atype);
$atype{""}="選択";
$atype{1}="入力";
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
if($FORM{lst_am} ne ''){$main_html.="<td$rownum>$anscom[$i-1]　</td>";}
if($FORM{lst_mm} ne ''){$main_html.="<td$rownum>$misanscom[$i-1]　</td>";}
if($FORM{lst_mm1} ne ''){$main_html.="<td>$misanscom1[$i-1]　</td>";}
if($FORM{lst_cf} ne ''){$main_html.="<td$rownum>$cf[$i-1]　</td>";}
if($FORM{lst_dg} ne ''){$main_html.="<td$rownum>$digest[$i-1]　</td>";}
if($FORM{lst_ath} ne ''){$main_html.="<td$rownum>$author[$i-1]</td>";}
if($FORM{lst_at} ne ''){$main_html.="<td$rownum>$atype{$anstype[$i-1]}</td>";}
$main_html.='</tr>';
if($FORM{lst_m} ne '' && $FORM{lst_mm1} ne ''){
$main_html.=<<"_HTML_";
<tr>
<td>$misans2[$i-1]　</td><td>$misanscom2[$i-1]　</td>
</tr><tr>
<td>$misans3[$i-1]　</td><td>$misanscom3[$i-1]　</td>
</tr><tr>
<td>$misans4[$i-1]　</td><td>$misanscom4[$i-1]　</td>
</tr>
_HTML_
}elsif($FORM{lst_m} ne ''){
$main_html.=<<"_HTML_";
<tr>
<td>$misans2[$i-1]　</td>
</tr><tr>
<td>$misans3[$i-1]　</td>
</tr><tr>
<td>$misans4[$i-1]　</td>
</tr>
_HTML_
}elsif($FORM{lst_mm1} ne ''){
$main_html.=<<"_HTML_";
<tr>
<td>$misans2[$i-1]　</td>
</tr><tr>
<td>$misans3[$i-1]　</td>
</tr><tr>
<td>$misans4[$i-1]　</td>
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
<tr><td colspan=$colspan nowrap><span><center><input type=submit value="  実行  ">
<input type=checkbox name=lst_q$FORM{lst_q_1} value=1>問題 
<input type=checkbox name=lst_a$FORM{lst_a_1} value=1>解答
<input type=checkbox name=lst_m$FORM{lst_m_1} value=1>誤答
<input type=checkbox name=lst_am$FORM{lst_am_1} value=1>正解メッセージ
<input type=checkbox name=lst_mm$FORM{lst_mm_1} value=1>誤答メッセージ
<input type=checkbox name=lst_cf$FORM{lst_cf_1} value=1>参考文献
<input type=checkbox name=lst_dg$FORM{lst_dg_1} value=1>問題内容
<input type=checkbox name=lst_mm1$FORM{lst_mm1_1} value=1>誤答別メッセージ
<input type=checkbox name=lst_ath$FORM{lst_ath_1} value=1>作成者
<input type=checkbox name=lst_at$FORM{lst_at_1} value=1>回答方式
</center></span></td></tr></table></form>
_HTML_
}
#************************************************
# 問題入力formHTML
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
<span><br><br><b>●各項目に入力し、実行ボタンを押してください。</b>( * 印は必須項目です。)<br>
『編集』は投稿問題を編集します。<br>
『追加削除』は投稿問題を採用し、投稿問題リストから削除します。<br><br>
<b>■問題入力フォーム■</b></span><small>改行→&lt;BR&gt;　　に自動変換</small>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=2><center>
<input type=radio name=add value=0 checked>編集
<input type=radio name=add value=1>追加削除
</center></td></tr>
<tr><td><small>回答方式</small></td><td><input type=checkbox name=atype value=1 $FORM{atype_1}>テキスト入力方式</td></tr>
<tr><td><small>問題文 *</small></td><td><textarea name=qqu cols=65 rows=3>\n$FORM3{qqu}</textarea></td></tr>
<tr><td><small>正解 * ※</small></td><td><textarea name=qas cols=65 rows=3>\n$FORM3{qas}</textarea></td></tr>
<tr><td><small>誤答１ * ※</small></td><td><textarea name=qmas1 cols=65 rows=3>\n$FORM3{qmas1}</textarea></td></tr>
<tr><td><small>誤答２ ※</small></td><td><textarea name=qmas2 cols=65 rows=3>\n$FORM3{qmas2}</textarea></td></tr>
<tr><td><small>誤答３ ※</small></td><td><textarea name=qmas3 cols=65 rows=3>\n$FORM3{qmas3}</textarea></td></tr>
<tr><td><small>誤答４ ※</small></td><td><textarea name=qmas4 cols=65 rows=3>\n$FORM3{qmas4}</textarea></td></tr>
<tr><td><small>正解時コメント</small></td><td><textarea name=qac cols=65 rows=2>\n$FORM3{qac}</textarea></td></tr>
<tr><td nowrap><small>不正解時コメント</td><td><textarea name=qmac cols=65 rows=2>\n$FORM3{qmac}</textarea></td></tr>
<tr><td nowrap><small>参考文献</td><td><input type=text size=65 name=qcf value="$FORM2{qcf}"></td></tr>
<tr><td nowrap><small>問題内容</td><td><input type=text size=65 name=qdg value="$FORM2{qdg}"></td></tr>
<tr><td nowrap><small>誤答１時コメント</td><td><textarea name=qmac1 cols=65 rows=2>\n$FORM3{qmac1}</textarea></td></tr>
<tr><td nowrap><small>誤答２時コメント</td><td><textarea name=qmac2 cols=65 rows=2>\n$FORM3{qmac2}</textarea></td></tr>
<tr><td nowrap><small>誤答３時コメント</td><td><textarea name=qmac3 cols=65 rows=2>\n$FORM3{qmac3}</textarea></td></tr>
<tr><td nowrap><small>誤答４時コメント</td><td><textarea name=qmac4 cols=65 rows=2>\n$FORM3{qmac4}</textarea></td></tr>
<tr><td nowrap><small>作成者</td><td><input type=text name=auth value="$FORM2{auth}" size=65></td></tr>
<tr><td colspan=2><center>
<table border=0><tr><td><input type=submit value="　 実行 　"></td></form>
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
<td><input type=submit value="　　クリア　　"></td></tr></table>
</center></td></tr></table></form>
※回答方式がテキスト入力形式の場合、各行が正解（誤答）となります。<br>
いずれかの行と、回答欄に入力された文字列が一致した場合正解（誤答）となります。<br>
_HTML_
}
#************************************************
# 高成績者リストの編集
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
<input type=submit value='$mode_name2{$FORM{d}}高成績者リスト表\示'>
_HTML_
}else{$main_html.=<<"_HTML_";
<input type=hidden name=mod value=1>
<input type=submit value='$mode_name1{$FORM{d}}高成績者リスト表\示'>
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
# 終了時メッセージHTML
#************************************************
sub edit_final_mes_html{
$i=0;
&form_to_form;
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=mes1>
<input type=hidden name=menu value=1>
<input type=hidden name=mn value="$FORM2{mn}">
<span><br><br><b>●各項目を入力し編集ボタンを押してください。</b><br><br>
<b>■終了時メッセージ編集フォーム■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=emes target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
_HTML_
$main_html.=&my_print(<<"_MY_");
<center>■■■■■登録済みメッセージ■■■■■</center>\t#aaeeaa\n
正解率（0～100）
メッセージ
_MY_
if($FORM{mn}>0){
for($i=0;$i<=$FORM{mn};$i++){
$main_html.=&my_print(<<"_MY_");
<span><input type=text name="per-$i" size=5 value="$FORM2{"per-$i"}">％未満</span>
<input type=text name="mes-$i" size=30 value="$FORM2{"mes-$i"}">　<input type=checkbox name="mod1-$i" value=1$FORMCH{"ch1-$i"}>モード１　<input type=checkbox name="mod2-$i" value=1$FORMCH{"ch2-$i"}>モード２
_MY_
}
}else{$FORM{mn}=0;}
$main_html.=&my_print(<<"_MY_");
<span>１００％(モード１)</span>
<input type=text name="mes-top1" size=30 value="$FORM2{'mes-top1'}">
<span>１００％(モード２)</span>
<input type=text name="mes-top2" size=30 value="$FORM2{'mes-top2'}">
<center>■■■■■追加用フォーム■■■■■</center>\t#eeaaee\n
<span>正解率（0～100）</span>
メッセージ
<span><input type=text name="per-$i" size=5 value="$FORM2{per-$FORM{mn}}">％未満</span>
<input type=text name="mes-$i" size=30 value="$FORM2{'mes-'.$FORM{mn}}">　<input type=checkbox name="mod1-$i" checked>モード１　<input type=checkbox name="mod2-$i" checked>モード２
<br><center><input type=submit value="　　 保存 　　"></center>\n
_MY_
$main_html.='</table>';
}
#************************************************
# ジャンル削除処理確認HTML
#************************************************
sub del_genre_html{
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value="del1">
<input type=hidden name=menu value=1>
<span><br><br><b>●このジャンルで、作成する項目にチェックを入れ、削除ボタンを押して下さい<br><br>
■ジャンルの各種削除■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=delg target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td><input type=checkbox value=1 name=delj><span>ジャンル情報を削除する
<br><input type=checkbox value=1 name=delh>高成績者ログファイルの削除
<br><input type=checkbox value=1 name=delf>成績分布ファイルの削除
<br><input type=checkbox value=1 name=delq>問題ファイルの削除
<br><input type=checkbox value=1 name=delc>投稿問題ファイルの削除
<br><input type=checkbox value=1 name=delm>設問別成績ファイルの削除
<br><input type=checkbox value=1 name=dele>終了メッセージファイルの削除
<br><input type=checkbox value=1 name=deld>ジャンル関連ファイル、ディレクトリの全削除</span></td></tr>
<tr><td><center><input type=submit value="　　 削除 　　"></center></td>
</tr></table></form>
_HTML_
}
#************************************************
# 問題削除順番変更処理HTML
#************************************************
sub del_quiz_html{
&header_html("問題の削除、順序変更");
if($#mondai<0){$main_html="<span>●このジャンルに登録されている問題はありません。</span>";return;}
$file_age=time-(-M "$FORM{d}/$mondai_$FORM{d}\.cgi")*(60*60*24);
$main_html=<<"_HTML_";
<span><b><br><br>●問題番号を編集し(小数点可)、チェックボックスをチェック後、<br>　最下部の実行ボタンを押してください。</b><br><br>
$formop_hd
<input type=hidden name=type value=qdel1>
<input type=hidden name=fa value="$file_age">
<b>■問題リスト■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=delq target=help>Help</a>]<span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td><small>問題番号</small></td><td><small>問題文</small></td><td><small>解答</small></td><td><small>削除</small></td></tr>
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
<span><input type=submit value="　　 実行 　　"><br><span></center></td></tr></table></form>
_HTML_
return 0;
}
#************************************************
# 高成績者リストの削除用HTML
#************************************************
sub del_high_html{
local($file,$syg,$mode_name)=@_;
open(DB,"$FORM{d}/$file");@lines = <DB>;close(DB);
if(($num_limit eq '0')||($day_limit eq '0')){$main_html.='<span><b><br><br>●このクイズは、高成績者リストは使用していません。</b><br><br></span>';return;}
elsif($#lines < 1){
&error(762);
return;
}
$main_html.=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=high1>
<input type=hidden name=menu value=1>
<input type=hidden name=mod value=$FORM{mod}>
<span><br><br><b>●以下のリストから削除したいスコアのチェックボックスにチェックを入れ、<br>最下部の削除ボタンを押してください。</b><br><br>
<b>■高成績者リスト■</b></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=6 nowrap><center><b>$mode_name高成績者リスト</b></center></td></tr>
<tr><td nowrap><center>削除</center></td>
<td nowrap><center>順位</center></td>
<td nowrap><center>時刻</center></td>
<td nowrap><center>正解数</center></td>
<td nowrap><center>名前</center></td>
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
push(@log,"$space1$grade　 $day　 $space2$high　　 $name　\n");
$last=$high;
$mass=$mass+$high;
}
$main_html.= "<tr><td colspan=6><center><input type=submit value='    削除    '><center></td></tr></table></form>";
}
#************************************************
# システム設定ヘルプHTML表示処理
#************************************************
sub help_sys_html{
&header_html("システム設定用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
<center>■■■■■システム設定■■■■■</center>\t#eeaaee\n
(1)プレイログ保護期間
保護期間内にアクセスのあるプレイヤはプレイ中とみなされる。この時間以上アクセスのないプレイヤのプレイログは、他の新規プレイヤにのプレイログで上書きされる可能\性がある。
(2)同時プレイ人数
同時にプレイできる人数の上限。プレイヤが同時プレイ人数に達した場合、新規プレイヤは受け付けなくなる。プレイ人数×1KBの容量を必要とする。
(3)クッキーID
個人成績を記録しておくためのID。同一サーバー内で、複数のqqqsystemsを立ち上げる場合、個人成績を別々に持たせるためには、このクッキーIDを異なる値に設定する
(4)選択形式
<form>選択形式を、<a href=javascript:void(0)>リンク</a><input type=radio>ラジオボタン<input type=button value=フォームボタン>とで選ぶ。</form>
(5)トップページへのURL
クイズのメニューページよりさらに上位のページへのURL。
(6)メニューページのタイトル
クイズのメニューページのメインタイトル。
(7)メニューページのヘッダー
クイズのメニューページのヘッダー部分に表\示される文字列です。<br>\$titleという文字列はメニューページのタイトルに変換されます。<br>\$topという文字列はトップページへのURLに変換されます。<br>\$addという文字列は問題投稿ページへのURLに変換されます。<br>\$imodeという文字列は携帯専用ページへのURLに変換されます。
(8)サブページのヘッダー
挑戦ページ、高成績者ページ、成績分布ページ、出題状況ページのヘッダー部分に表\示される文字列です。
(9)メニューページのコメント
メニューページのメニューに、コメントを表\示できます。『メンテナンス中』『１時間後メンテナンス予\定』等の告知にも利用できます。
(10)スタイルシート
全てのページに作用するスタイルシートを定義することができます。
(11)システムデザイン
システム設定の色設定等のデザインを選択する。システムデザインの設定は、システムデザイン設定画面にて行う。
(12)メニューページ表\示項目
メニューページの表\示が若干軽くなります。メニューページの表\示が遅いと感じたときにご利用下さい。
(13)回答時間による順位付け
同じ正解数であれば、回答時間により、高成績者の順位付けを行います。行わない場合は同順位となります。
(14)自動文字折り返し
自動折り返しを許可した場合、表の幅に応じて、文字列を改行する。意図しない場所で改行した場合レイアウトが崩れる場合がある。レイアウトを重視する場合は、自動折り返しを禁止(nowrap)し、改行したい個所で改行をいれる必要がある。
_HELP_
}
#************************************************
# ジャンル作成ヘルプHTML表示処理
#************************************************
sub help_newgenre_html{
&header_html("新ジャンル作成用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
<center>■■■■■新ジャンル作成時の設定■■■■■</center>\t#bbbbbb\n
(1)ディレクトリ
クイズの問題、成績などを保存するディレクトリ名
_HELP_
}
#************************************************
# システムデザイン設定ヘルプHTML表示処理
#************************************************
sub help_sysdesign_html{
&header_html("システムデザイン設定用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
<center>■■■■■システムデザイン設定■■■■■</center>\t#eeaaee\n
(1)編集元
編集元、コピー元のシステムデザイン名
(2)システムデザイン名
システムデザインの名前。システム設定画面からデザインを選択するときは、この名前を選択します。
(3)メニューページの壁紙
メニューページの壁紙画像のファイル名です。http://からはじまるURLも設定可能です。
(4)メニューページの背景色
背景色をあらわします。#からはじまるRGBの設定と、redのように色を表\す文字列の両方が設定可能です。
(5)メニューページの表\の色
表\の色を表\します。
(6)メニューページのジャンル色
ジャンル名が表\示されるセルの色。
(7)メニューページの情報色
メニューページの最上位に表\示されるコメントの表\の色
(8)メニューページのコメント色
各ジャンルのコメントが表\示されるセルの色
(9)メニューページの高成績者色
高成績者名が表\示されるセルの色
(10)メニューページの表\の枠の色
表\の枠線の色
(11)メニューページの文字色
文字の色
(12)メニューページのリンク色
リンク文字列の色
(13)メニューページの既訪問リンク色
既に訪問済みのリンク文字列の色
(14)メニューページの表\の枠の高さ
表\の枠の高さ(border)
(15)メニューページの表\の枠の幅
表\の枠の幅(cellpadding)
(16)メニューページの表\の枠の内幅
表\の枠の内側の幅(cellspacing)
(17)成績履歴グラフ画像１
成績履歴の棒グラフの画像。クイズ終了時に使用し、その時の成績に該当するグラフに使用する
(18)成績履歴グラフ画像２
成績履歴の棒グラフの画像。
(19)表\のレイアウト
表\位置を左揃え、中揃え、右揃えにする設定
(20)表\内文字レイアウト_HELP_
表\の中の文字位置を左揃え、中揃え、右揃えにする設定
_HELP_
}
#************************************************
# ジャンルデザイン設定ヘルプHTML表示処理
#************************************************
sub help_genredesign_html{
&header_html("ジャンルデザイン設定用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
<center>■■■■■ジャンルデザインの設定■■■■■</center>\t#eeaaaa\n
(1)編集元
編集元、コピー元のシステムデザイン名
(2)ジャンルデザイン名
ジャンルデザインの名前。ジャンル設定画面からデザインを選択するときは、この名前を選択します。
(3)文字色
文字の色
(4)リンク文字色
リンク文字列の色
(5)既訪問リンク文字色
既に訪問済みのリンク文字列の色
(6)殿堂入り者文字色
高成績者一覧で、殿堂入りのプレイヤの名前の色
(7)基本背景色
クイズ開始時、成績履歴、出題状況、高成績者一覧の背景色
(8)正解時背景色
クイズに正解した時の背景色
(9)不正解時背景色
クイズに不正解だった時の背景色
(10)情報ウインドウの色
クイズ開始時のコメントの表\の色
(11)表\のヘッダー色
表\のヘッダー部分のセルの色
(12)表\の色
表\の色
(13)表\の枠の色
表\の枠線の色
(14)表\の枠の高さ
表\の枠の高さ(border)
(15)表\の枠の幅
表\の枠の幅(cellpadding)
(16)表\の枠の内幅
表\の枠の内側の幅(cellspacing)
(17)基本壁紙
クイズ開始時、成績履歴、出題状況、高成績者一覧の壁紙
(18)正解時壁紙
クイズに正解した時の壁紙
(19)不正解時壁紙
クイズに不正解だった時の壁紙
(20)正解表\示
クイズに正解したときの、正解メッセージ
(21)不正解表\示
クイズに不正解だったときの、不正解メッセージ
(22)タイムオーバー表\示
クイズにタイムオーバーだったときの、タイムオーバーメッセージ
(23)正解時MIDI
クイズに正解したときの効果音
(24)不正解時MIDI
クイズに不正解だったときの効果音
(25)クイズ終了時MIDI
クイズ終了時の効果音
(26)高成績者用MIDI
クイズ終了時、高成績だった場合の効果音
_HELP_
}
#************************************************
# プレイログ一覧ヘルプHTML表示処理
#************************************************
sub help_playlog_html{
&header_html("プレイログ用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
■<b>最新プレイログ利用時刻</b>とは最も最近に使用されたプレイログの更新時刻です。\n
■<b>最古プレイログ利用時刻</b>とは最も過去に使用されたプレイログの更新時刻です。\n
■<b>プレイログ利用間隔</b>とは最新ログ利用時刻と、最古ログ利用時刻との差です。\n
■<b>同時プレイヤ数</b>とはシステム設定で設定した値で、プレイログの総数を表\します。\n
■<b>プレイログ保護期間</b>とはシステム設定で設定した値で、この期間内に更新されたログは保護されます。\n
■<b>プレイログ</b>とは、プレイ中のプレイヤーの状態を保存するログです。\n
■プレイログは、１ファイル１kbの容量を必要とします。\n
■プレイログの総数の上限は同時プレイヤ数で指定されます。\n
■新規プレイヤは、空いているプレイログを探し、空いているログがあればそれを利用し、空いているログがなければその事をプレイヤに告げます。\n
■プレイログ保護期間以上更新の無かったログは『空いている』と見なされます。\n
■プレイログ利用間隔を時々しらべ、適切なログ保護期間を設定してください。ログ利用間隔が大幅に長いと無駄なログが多くあり資源の無駄遣いだということになります。\n
_HELP_
}
#************************************************
# 各種ログ閲覧・保存ヘルプHTML表示処理
#************************************************
sub help_log_html{
&header_html("各種ログ閲覧・保存用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
■閲覧とは、本来直接ファイルにアクセスしても、cgiファイルであるために表\示できないファイルを表\示します。\n
■各種ログのバックアップは、閲覧後、メニューより保存することで行なえます。\n
■追加形式とは、問題を一括追加する形式でログを表\示します。\n
_HELP_
}
#************************************************
# ジャンル設定ヘルプHTML表示処理
#************************************************
sub help_genre_html{
&header_html("ジャンル設定用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
<center>■■■■■新ジャンル作成時の設定■■■■■</center>\t#bbbbbb\n
(1)ディレクトリ
クイズの問題、成績などを保存するディレクトリ名
<center>■■■■■ジャンルの動作設定■■■■■</center>\t#eeaaaa\n
(2)タイトル
クイズ一覧で表\示されるこのジャンルのタイトル
(3)紹介文
メニューページで各ジャンルの説明に使用します。
(4)クイズ開始メッセージ
クイズの開始時に表\示されるメッセージです。
(5)問題ファイル
問題を登録するファイルの設定。他のジャンルから読み込むこともできます。
(6)ジャンルの動作状態
ジャンルを$_underconstに設定しておくと、メニューページでそのジャンルは表\示されない
(7)投稿問題の受付
このジャンルへの問題の投稿を受け付けることができます
(8)テキスト形式の投稿問題
投稿を受け付ける場合、テキスト形式の問題の投稿を受け付けるかどうかを設定できます。
(9)投稿問題の自動採用
投稿を受け付ける場合、管理者の承認を経ずに自動的に問題として採用するかを設定できます。
(10)出題状況表示での問題文表示
出題状況表示で、問題文を表示するか、問題の内容だけを表示するかを設定できます。
(11)ジャンルデザイン
色の設定や表のジャンルデザインを選択できます。ジャンルデザインは、ジャンルデザイン設定で設定できます。
<center>■■■■■モード別の動作設定■■■■■</center>\t#eeeeaa\n
(12)(32)モード名
各モードの名前。モード２は、モード２の名前が入力されているときのみ動作する。
(13)(33)正解表\示
回答後に正解を表\示するかどうかの設定
(14)(34)出題順序
出題順序をランダムに行うか、登録順に行うかの設定
(15)(35)使用問題数
登録している全ての問題数を使ったり、使用する問題数に制限を加える事ができる。
(16)(36)出題問題数
最大出題数
(17)(37)一括出題
出題を、全問一括表\示することができます。
(18)(38)終了条件誤答数
何問間違えるとGAME OVERになるかの設定
(19)(39)制限時間
一問毎の制限時間を指定することができます。
(20)(40)合格ライン
回答率が合格ラインを超えるとハイスコア登録が可能\となる。
(21)(41)高成績者のback up
指定した間隔(日)以上、バックアップを取っていない高成績者ファイルのバックアップを行うかどうかの設定。
(22)(42)高成績者のback up方式
高成績者ファイルのバックアップを、１つのファイル(.bak)にバックアップを取るか、複数のファイル(.bak1)に取るのかを設定する。
(23)(43)成績分布のback up
指定した間隔(日)以上、バックアップを取っていない成績分布ファイルのバックアップを行うかどうかの設定。
(24)(44)成績分布のback up方式
成績分布ファイルのバックアップを、１つのファイル(.bak)にバックアップを取るか、複数のファイル(.bak1)に取るのかを設定する。
(25)(45)成績分布省略表\示
一定％以上の棒グラフを省略した表\示にする
(26)(46)成績分布集計単位
最終成績の集計グラフを集計する単位を設定する
(27)(47)高成績者日数制限
高成績者リストで、記録する日数に制限を加えることができる。ある日数以上前の記録は、新規記録登録の際に削除される。
(28)(48)高成績者人数制限
高成績者リストで、記録する人数に制限を加えることができる。登録は上位記録が残る。
(29)(49)殿堂入り人数
殿堂入りとは、高成績者のうち、日数制限人数制限を受けて記録が削除される人のことです。殿堂入り中は、制限により記録が削除されることはありませんが、成績を塗り替えられ殿堂入りから外れた場合は、日数制限、人数制限を受けることになります。
(30)(50)高成績者コメント記録
高成績者リストにコメントの入力を許すかどうかの設定です。ディスク容量と相談しつつ設定を行って下さい。
(31)(51)同ホスト同スコア
同じIPアドレスで、同じスコアの場合は高成績者登録できなくすることができる。高成績者数を極力減らしたい場合に有効。
_HELP_
}
#************************************************
# ジャンル設定の各種削除用ヘルプHTML表示処理
#************************************************
sub help_delgenre_html{
&header_html("ジャンル設定の各種削除用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
ジャンル情報の削除
ジャンル情報を一括して保存しているファイルから、このジャンルの情報を削除します。登録していたディレクトリや、各種ログファイル削除しません。
高成績者ログファイルの削除
高成績者を保存したログを削除します。
成績分布ファイルの削除
最終成績を集計したファイルを削除します。
問題ファイルの削除
問題登録したファイルを削除します。
投稿問題ファイルの削除
投稿問題が登録されているファイルを削除します。新たに問題が投稿されれば自動作成されます。
設問別成績ファイルの削除
設問別に正解率を集計したファイルを削除します。
設定ディレクトリの削除
登録しているディレクトリを削除します。高成績者ログ、成績分布ファイル、問題ファイル、設問別成績ファイルは、このディレクトリに保存されているために削除されます。ジャンル情報は削除しません。
_HELP_
}
#************************************************
# 問題の削除・順序変更用ヘルプHTML表示処理
#************************************************
sub help_delquiz_html{
&header_html("問題の削除・順序変更用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
■問題番号順に問題を並び替えます。\n
■問題番号には小数点が含まれても可能\です。\n
■【削除】がチェックされている問題は削除されます。\n
_HELP_
}
#************************************************
# クイズ一括登録の書式用ヘルプHTML表示処理
#************************************************
sub help_multiadd_html{
&header_html("クイズ一括登録の書式用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
<center>■■■一括登録の書式■■■<center>\t#eeaaaa\n
■上から１行ずつ読みとって行きます。\n
■識別子q:ではじまる行から、次に再び識別子q:が現れるまで、１つの問題であると認識します。\n
■識別子q:に続く文字列は問題文として認識します。\n
■識別子ans:に続く文字列は正解として認識します。\n
■識別子mis1:に続く文字列は誤答１として認識します。\n
■識別子mis2:に続く文字列は誤答２として認識します。\n
■識別子mis3:に続く文字列は誤答３として認識します。\n
■識別子mis4:に続く文字列は誤答４として認識します。\n
■識別子ansmes:に続く文字列は正解コメントとして認識します。\n
■識別子mismes:に続く文字列は誤答コメントとして認識します。\n
■識別子cf:に続く文字列は参考文献として認識します。\n
■識別子digest:に続く文字列は問題内容として認識します。\n
■識別子anstype:に続く文字列は回答方式として認識します。1を指定したときテキスト入力方式。0を指定したとき選択方式となります。\n
■識別子mismes数字:に続く文字列は、誤答指定の誤答コメントとして認識します。\n
■識別子author:に続く文字列は、作者名として認識します。\n
■識別子#に続く文字列は注釈として、いっさい認識しません。\n
■空白行は認識しません。\n
■上記の例意外の行が入力されれば、読み込みエラーとなります。\n
■q:と次のq:までの間の識別子の順序は、順不同です。\n
■識別子q:,ans:の２つの識別子は必須です。回答方式が選択方式の場合、mis1:識別子も必須となります。\n
■テキスト入力形式で、複数の解答パターンがある場合は、&lt;br&gt;で区切ります。(参：例2)\n
■例1<br>#-------問題１-------<br>q:１＋１＝<br>ans:2<br>mis1:3<br>mis2:4<br>mis3:5<br>mis4:6<br>ansmes:大正解！<br>mismes:だめだね<br>cf:算数の教科書<br>mismes1:3ってことはないでしょ。<br>mismes2:4ってことはないでしょ。<br>digest:簡単な足し算<br>anstype:0<br>author:jun\n
■例2<br>#-------問題１-------<br>q:１＋２＝<br>ans:3&lt;br&gt;３<br>mis1:2&lt;br&gt;２<br>mis2:4&lt;br&gt;４<br>mis3:5&lt;br&gt;５<br>mis4:6&lt;br&gt;６<br>ansmes:大正解！<br>mismes:だめだね<br>cf:算数の教科書<br>mismes1:2ってことはないでしょ。<br>mismes2:4ってことはないでしょ。<br>digest:簡単な足し算<br>anstype:1<br>author:jun\n
■既に登録されている問題を、一括登録形式のログとして保存することもできます。システムコマンドの『各種ログ閲覧・保存』をご利用ください。\n
_HELP_
}
#************************************************
# 各種ログのバックアップ用ヘルプHTML表示処理
#************************************************
sub help_backup_html{
&header_html("各種ログのバックアップ用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
■【追加】とは、現在のログに重複データ以外のデータを加えます。<br>　【追加】は【上書】よりも優先されます。\n
■【上書】とは、全データを現在のログと置き換えます。<br>　複数ファイルが指定されている場合は、その重複データをのぞいたデータと置き換えます。<br>　【追加】は【上書】よりも優先されます。\n
■【削除】とは、バックアップファイルを削除します。<br>　【追加】や【上書】と併用した場合、最後に【削除】が実行されます。\n
■【バックアップファイルの作成】とは、今すぐバックアップファイルを作成するコマンドです。\n
■【作成モード】とは、バックアップファイルを作成する方法です。<br>[上書き]を選ぶと、常に****.bak又は、***_bak.cgiに保存されます。<br>[別ファイル]を選ぶと、***.bak1,***.bak2といった感じに別ファイルとして保存されます。<br>[高成績者ファイル][成績分布ファイル]のデフォルト設定は【ジャンルの編集】で設定します。<br>これらのデフォルト設定は、自動バックアップの設定と同じです。\n
_HELP_
}
#************************************************
# 終了時メッセージ編集用ヘルプHTML表示処理
#************************************************
sub help_endmes_html{
&header_html("終了時メッセージ編集用ヘルプ");
$main_html.=&help_print(<<"_HELP_");
■終了時の正解率によって、出すメッセージを変えることができます。\n
■指定する正解率は自動的にソ\ートされるので、順番に並んでいなくてもＯＫです。\n
■指定する正解率は０～１００の範囲で、小数点でも可です。\n
■メッセージを追加したい場合は追加フォームより行ってください。\n
■正解率が空欄の場合、そのメッセージは削除されます。\n
_HELP_
}
#************************************************
# システムデザイン選択用HTML表示処理
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
# デザイン選択用HTML表示処理
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
# 問題一括追加HTML
#************************************************
sub multi_add_quiz_form{
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qmulti1>
<input type=hidden name=menu value=1>
<span><b><br><br>●問題ファイル形式のテキストを問題データに追加します。</b><br>
　問題ファイル形式のテキストをテキストエリアにコピーし、一括追加ボタンを押してください。<br><br>
<b>■問題入力フォーム■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=madd target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td><span>
<textarea rows=40 cols=60 name='newq'>\n$FORM{newq}</textarea>
</span></td></tr><tr><td>
<span><center>
<input type=submit value="　一括追加　">
<br></center></span></td></tr></table></form>
_HTML_
}
#************************************************
# 問題一括追加確認HTML
#************************************************
sub multi_add_quiz_html{
local(@log,$index,$line,@q,@ans,@mis1,@mis2,@mis3,@mis4,@ansmes,@mismes,@mismes1,@mismes2,@mismes3,@mismes4,@cf,@digest,@atype,@auth);
@log=split(/\n/,$FORM{newq});
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value=qmulti2>
<input type=hidden name=menu value=1>
<span><br><br><b>●登録した問題が正しければ、一括追加ボタンを押してください。</b><br><br></span>
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
@opt=('選択','テキスト入力');
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
<tr><td colspan=2><span><center>■■■ 追加 $num 問目 ■■■</center></span></td></tr>
<tr><td>問　題：</td><td><b>$q[$i]</b></td></tr>
<tr><td>正　解：</td><td><b>$ans[$i]</b></td></tr>
<tr><td>誤答１：</td><td><b>$mis1[$i]</b></td></tr>
<tr><td>誤答２：</td><td><b>$mis2[$i]</b></td></tr>
<tr><td>誤答３：</td><td><b>$mis3[$i]</b></td></tr>
<tr><td>誤答４：</td><td><b>$mis4[$i]</b></td></tr>
<tr><td>正解コメント：</td><td><b>$ansmes[$i]</b></td></tr>
<tr><td>誤答コメント：</td><td><b>$mismes[$i]</b></td></tr>
<tr><td>参考文献：</td><td><b>$cf[$i]</b></td></tr>
<tr><td>問題内容：</td><td><b>$digest[$i]</b></td></tr>
<tr><td>誤答コメント１：</td><td><b>$mismes1[$i]</b></td></tr>
<tr><td>誤答コメント２：</td><td><b>$mismes2[$i]</b></td></tr>
<tr><td>誤答コメント３：</td><td><b>$mismes3[$i]</b></td></tr>
<tr><td>誤答コメント４：</td><td><b>$mismes4[$i]</b></td></tr>
<tr><td>作成者：</td><td><b>$auth[$i]</b></td></tr>
<tr><td>回答方式：</td><td><b>$opt[$atype[$i]]</b></td></tr>
_HTML_
}
$main_html.=<<"_HTML_";
<tr><td colspan=2><span><center><input type=submit value="　一括追加　">
<br></center></span></td></tr></form></table>
_HTML_
return 0;
}
#************************************************
# ジャンル新規作成画面HTML表示処理
#************************************************
sub make_genre_html{
&list_genre_html(@genre_dir_all);
$main_html =<<"_HTML_";
$formop_nh
<input type=hidden name=type value=newj2>
<span><br><br><b>●各項目を入力し新規作成ボタンを押してください。</b><br><br>
<b>■新ジャンル設定■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=newg target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td colspan=3 bgcolor=#eeaaee><center><span>■■■■■新ジャンル作成時の設定■■■■■</span></center></td></tr>
_HTML_
$main_html.=&my_print(<<"_MY_");
(1)ディレクトリ
<input type=text name='d' value="$FORM2{d}" size=10>(半角英数)
_MY_
$main_html .=<<"_HTML_";
<tr><td colspan=3><center><br><input type=submit value=新規作成></center></td></tr>
</table></form>
${&focus_move('d')}$ret
_HTML_
}
#************************************************
# ヘルプ画面HTML表示処理
#************************************************
sub help_html{
$formop_hb=~s/\n//g;
$main_html =<<"_HTML_";
<input type=hidden name=type value=newj2>
<span><br><br>
<b>■ヘルプメニュー■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=newg target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td nowrap>システム設定</td>
$formop_hb<td><input type=hidden name='help' value="sys"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>新ジャンル作成</td>
$formop_hb<td><input type=hidden name='help' value="newg"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>システムデザイン設定</td>
$formop_hb<td><input type=hidden name='help' value="sysd"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>ジャンルデザイン設定</td>
$formop_hb<td><input type=hidden name='help' value="gend"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>プレイログ</td>
$formop_hb<td><input type=hidden name='help' value="playlog"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>各種ログ閲覧・保存</td>
$formop_hb<td><input type=hidden name='help' value="log"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>ジャンル設定</td>
$formop_hb<td><input type=hidden name='help' value="genre"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>ジャンル設定の各種削除用ヘルプ</td>
$formop_hb<td><input type=hidden name='help' value="delg"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>問題の削除・順序変更</td>
$formop_hb<td><input type=hidden name='help' value="delq"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>クイズ一括登録の書式用</td>
$formop_hb<td><input type=hidden name='help' value="madd"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>終了メッセージ編集</td>
$formop_hb<td><input type=hidden name='help' value="emes"><input type=submit value='ヘルプ'></td></tr></form>
<tr><td nowrap>各種ログのバックアップ</td>
$formop_hb<td><input type=hidden name='help' value="back"><input type=submit value='ヘルプ'></td></tr></form>
</table></form>
_HTML_
}
#************************************************
# 色作成ウインドウ表示HTML
#************************************************
sub color_html{
$main_html.=<<'_HTML_';
<script language=javascript>
//<!--
function wopen(){
var win=window.open("color","right", "toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=0,resizable=1,width=200,height=50");
if (win !=null){
main="<html><head><title>色テスト</title>\n"
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
main+="色コード<input type=text name=col size=7 value='#ffffff'>\n"
main+="<input type=button value=OK onclick=\"change()\">\n"
main+="<tr><td nowrap>\n"
main+="赤<input type=text name=red size=2 value='ff'>\n"
main+="緑<input type=text name=green size=2 value='ff'>\n"
main+="青<input type=text name=blue size=2 value='ff'>\n"
main+="<input type=button value=OK onclick=\"rgb()\">\n"
main+="</td></tr></table>\n"
main+="</form></bo"
main+="dy></html>\n"
win.document.write(main)
win.document.close()
}
}
document.write("<form><input type=button value=\"色表\示テストウインドウ\" onclick=\"wopen()\"></form>");
//-->
</script>
_HTML_
}
#************************************************
# ジャンル順序変更HTML
#************************************************
sub sort_genre_html{
&list_genre_html(@genre_dir_all);
$main_html=<<"_HTML_";
$formop_h
<b><span>■ジャンルの順序変更■</span></b>
<table $sys_tbl_opt bgcolor='$sys_color'>
<input type=hidden name=type value=sort1>
<tr><td width=400><small>タイトル</small></td><td><small>ディレクトリ</small></td><td><small>順序</small></td></tr>
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
$main_html.='<tr><td colspan=3><span><center><input type=submit value="　　変更　　"><br><center></span></td></tr></table>';
$main_html.="<small>(ジャンルの順序は、値の小さい順に並び替えられます。小数でも可です。)</small></form>";
}
#************************************************
# プレイログ表示
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
<td nowrap>$min分$sec秒</td>
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
$term="$day日$hour時間$min分$sec秒";
}
if($min_t ne ''){$min_t = &time_set(time-$min_t*(60*60*24));}
else{$min_t = '-----';$term='-----';}
if($max_t ne ''){$max_t = &time_set(time-$max_t*(60*60*24));}
else{$max_t = '-----';$term='-----';}
$a=$t%(86400);
$main_html=<<"_HTML_";
<b><span>■プレイログの使用状況■　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=playlog target=help>Help</a>]<span></b>
<table $sys_tbl_opt bgcolor='$sys_color'>
_HTML_
$main_html.=&my_print(<<"_MY_");
最新プレイログ利用時刻
$min_t
最古プレイログ利用時刻
$max_t
プレイログ利用間隔
$term
同時プレイヤ数
$SYS{max_player}人
プレイログ保護期間
$SYS{limit}分
_MY_
$main_html.='</td></tr></table><br><br>';
if($play_log_list ne ''){
$main_html.=<<"_HTML_";
<b><span>■プレイログ一覧■<span></b>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr>
<td>プレイログ利用時刻</td>
<td>ジャンル</td>
<td>モード</td>
<td>出<br>題<br>数</td>
<td>正<br>解<br>数</td>
<td>回答時間</td>
<td>挑<br>戦<br>数</td>
<td>名前</td>
</tr>
$play_log_list
</table>
_HTML_
}
}
#************************************************
# 各種ファイルのサイズを表示
#************************************************
sub file_size_html{
local($return);
$main_html=<<"_HTML_";
<span><br><br><b>■各種システム用ファイルの容量■</b></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr>
<td nowrap><small><b>クイズスクリプト</b></small></td>
<td nowrap><small><b>設定ログ</b></small></td>
<td nowrap><small><b>プレイログ</b></small></td>
<td nowrap><small><b>合計</b></small></td>
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
<span><br><br><b>■各種ジャンル用ファイルの容量■</b></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td nowrap><small><b>ジャンル名</b></small></td>
<td nowrap><small><b>問題<br>ファイル</b></small></td>
<td nowrap><small><b>各成績<br>ファイル</b></small></td>
<td nowrap><small><b>終了メッセージファイル</b></small></td>
<td nowrap><small><b>各バックアップ</b></small></td>
<td nowrap><small><b>設問別<br>成績ファイル</b></small></td>
<td></td><td nowrap><small><b>合計</b></small></td></tr>
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
<td><small>全ジャンル計</small></td>
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
# 各種ログ閲覧
#************************************************
sub log_html{
&list_genre_html(@genre_dir_all);
$main_html=<<"_HTML_";
<span><br><br><b>●各種ログが閲覧できます。</b><br>　保存する場合は、閲覧後ブラウザの『名前を付けて保存』で保存してください。<br><br></span>
<span>■システムログ■　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=log target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td nowrap><small>システム設定ファイル($system_cgi)</small></td>
$formop_hb
<input type=hidden name=log value=sys>
<td colspan=2><span><input type=submit value=閲覧></td></tr></form>
<tr><td nowrap><small>ジャンル設定ファイル($genre_cgi)</small></td>
$formop_hb
<input type=hidden name=log value=genre>
<td colspan=2><span><input type=submit value=閲覧></span></td></tr></form>
<tr><td nowrap><small>システムデザイン設定ファイル($sysdesign_cgi)</small></td>
$formop_hb
<input type=hidden name=log value=sysdesign>
<td colspan=2><span><input type=submit value=閲覧></span></td></tr></form>
<tr><td nowrap><small>ジャンルデザイン設定ファイル($design_cgi)</small></td>
$formop_hb
<input type=hidden name=log value=design>
<td colspan=2><span><input type=submit value=閲覧></span></td></tr></form>
</table><br><br>
_HTML_
if($#genre_dir_all>=0){
$main_html.=<<"_HTML_";
<span>■ジャンル別ログ■　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=log target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr>
<td nowrap rowspan=2><small>ジャンル名</td>
<td nowrap rowspan=2 colspan=2><small><center>問題ログ</small></center></td>
<td nowrap rowspan=2 colspan=2><small><center>投稿問題ログ</small></center></td>
<td nowrap colspan=2><center><small>モード１</small></center></td>
<td nowrap colspan=2><center><small>モード２</small></center></td></tr>
<tr><td nowrap><small>高成績者ログ</small></td>
<td nowrap><small>成績分布ログ</small></td>
<td nowrap><small>高成績者ログ</small></td>
<td nowrap><small>成績分布ログ</small></td>
</tr>
_HTML_
foreach $dir(@genre_dir_all){
if($dir eq ''){next;}
$main_html.=<<"_HTML_";
<tr><td nowrap><small>$title{$dir}</small></td>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=m>
<td><span><input type=submit value=閲覧></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=m2>
<td><span><input type=submit value=追加形式></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=c>
<td><span><input type=submit value=閲覧></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=c2>
<td><span><input type=submit value=追加形式></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=h1>
<td><span><input type=submit value=閲覧></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=s1>
<td><span><input type=submit value=閲覧></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=h2>
<td><span><input type=submit value=閲覧></span></td></form>
$formop_hb<input type=hidden name=d value="$dir"><input type=hidden name=log value=s2>
<td><span><input type=submit value=閲覧></span></td></form></tr>
_HTML_
}
$main_html.='</table>';
}
}
#************************************************
# ジャンル複製処理確認HTML
#************************************************
sub copy_genre_html{
$main_html=<<"_HTML_";
$formop_hd
<input type=hidden name=type value="copy1">
<input type=hidden name=menu value=1>
<span><br><br><b>●このジャンルの、複製先ディレクトリを入力してください。</b><br><br>
<b>■コピー先ジャンル■</b></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
_HTML_
$main_html.=&my_print(<<"_MY_");
<center>■■■■■コピー先ジャンルの設定■■■■■</center>\t#eeaaee\n
(1)ディレクトリ
<input type=text name=d2 value="$FORM2{d2}">
<center><br><input type=submit value="　複製　"></center>\n
_MY_
$main_html.='</table></form>';
}
#************************************************
# 各種ログのバックアップHTML
#各モード各ファイルのバックアップログをリストアップ
#削除、組み込みのcheckbox
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
<span><b><br><br>●チェックボックスをONにし、実行ボタンを押してください。<br><br>■バックアップファイルの読み込み■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=back target=help>Help</a>]</span>
_HTML_
if($max >= 0){
$main_html.=<<"_HTML_";
<table $sys_tbl_opt bgcolor='$sys_color'>
$formop_hd
<input type=hidden name=type value=back1>
<input type=hidden name=menu value=1>
<tr><td colspan=2><small><b>種類</b></small></td>
<td nowrap><small><b>backupログ名</b></small></td>
<td><small><b>作成日時</b></small></td>
<td><small><b>備考</b></small></td>
<td><small><b>追<br>加</b></small></td>
<td><small><b>上<br>書</b></small></td>
<td><small><b>削<br>除</b></small></td></tr>
<tr>
_HTML_
$bu=0;
if($#m_back >= 0){
$main_html.= "<td nowrap rowspan=$m_span colspan=2><small>問題ファイル</small></td>";
$bu=&m_box_html($bu,'mbu',@m_back);
}
if($#q_back >= 0){
$main_html.= "<td nowrap rowspan=$m_span colspan=2><small>設問別成績ファイル</small></td>";
$bu=&q_box_html($bu,'qbu',@q_back);
}
if($mod1 > 0){$main_html.= "<td nowrap rowspan=$mod1><small>モード１</small></td>";}
if($hmod1 > 0){
$main_html.="<td nowrap rowspan=$hmod1><small>高成績者ファイル</small></td>";
$bu=&h_box_html($bu,'buh1',@h_back1);
}
if($smod1 > 0){
$main_html.="<td nowrap rowspan=$smod1><small>成績分布ファイル</small></td>";
$bu=&s_box_html($bu,'bus1',@s_back1);
}
if($mod2 > 0){
$main_html.="<td nowrap rowspan=$mod2><small>モード２</small></td>";
}
if($hmod2 > 0){
$main_html.="<td nowrap rowspan=$hmod2><small>高成績者ファイル</small></td>";
$bu=&h_box_html($bu,'buh2',@h_back2);
}
if($smod2 > 0){
$main_html.="<td nowrap rowspan=$smod2><small>成績分布ファイル</small></td>";
$bu=&s_box_html($bu,'bus2',@s_back2);
}
$main_html.=<<"_HTML_";
<td nowrap colspan=8><span><center>
<input type=submit value='    実行    '>
</center></span></td></tr></table></form>
_HTML_
}else{
$main_html.="<span><br>●このジャンルのバックアップファイルはありません。<br><br></span>";
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
<span><br><b>■バックアップファイルの作成■</b>　[<a href=$quiz_op_cgi?passch=$FORM2{passch}\&help=back target=help>Help</a>]</span>
<table $sys_tbl_opt bgcolor='$sys_color'>
$formop_hd
<input type=hidden name=type value=back2>
<input type=hidden name=menu value=1>
<tr><td colspan=2><small><b>種類</b></small></td><td><b><small>作成モード</small></b></td><td><small><b>備考</b></small></td><td><small><b>作成</b></small></td></tr>
<tr><td nowrap colspan=2><small>問題ファイル</small></td><td><span><select name=mbuw><option value=1$mw{1}>上書き<option value=0$mw{0}>別ファイル</select></span></td><td><small>問題数：$mon問</small></td><td><span><input type=checkbox name=mbu value=1></span></td></tr>
<tr><td nowrap colspan=2><small>設問別成績ファイル</small></td><td><span><select name=qbuw><option value=1$qw{1}>上書き<option value=0$qw{0}>別ファイル</select></span></td><td><small>問題数：$mon問</small></td><td><span><input type=checkbox name=qbu value=1></span></td></tr>
<tr><td nowrap rowspan=2><small>モード１</small></td>
<td nowrap><small>高成績者ファイル</small></td><td><span><select name=hbu1w><option value=1$hw1{w}>上書き<option value=0$hw1{o}>別ファイル</select></span></td><td><small>登録者数：$h1_count人<small></td><td><span><input type=checkbox name=hbu1 value=1></span></td></tr>
<tr><td nowrap><small>成績分布ファイル</small></td><td><span><select name=sbu1w><option value=1$sw1{w}>上書き<option value=0$sw1{o}>別ファイル</select></span></td><td><small>挑戦者数：$s1_count人</small></td><td><span><input type=checkbox name=sbu1 value=1></span></td></tr>
<tr><td nowrap rowspan=2><small>モード２</small></td>
<td nowrap><small>高成績者ファイル</small></td><td><span><select name=hbu2w><option value=1$hw2{w}>上書き<option value=0$hw2{o}>別ファイル</select></span></td><td><small>登録者数：$h2_count人<small></td><td><span><input type=checkbox name=hbu2 value=1></span></td></tr>
<tr><td nowrap><small>成績分布ファイル</small></td><td><span><select name=sbu2w><option value=1$sw2{w}>上書き<option value=0$sw2{o}>別ファイル</select></span></td><td><small>挑戦者数：$s2_count人</small></td><td><span><input type=checkbox name=sbu2 value=1></span></td></tr>
<tr><td nowrap colspan=5><span><center><input type=submit value='    実行    '></center></span></td></tr>
</table></form>
_HTML_
}
#************************************************
# backup_html問題ファイル用のチェックボックス
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
&box_html($file,$time,"問題数：$count問",0,$syg,$num);
}
return $num;
}
#************************************************
# backup_html問題ファイル用のチェックボックス
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
&box_html($file,$time,"問題数：$count問",0,$syg,$num);
}
return $num;
}
#************************************************
# backup_html高成績者ファイル用のチェックボックス
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
&box_html($file,$time,"登録者数：$count人",1,$syg,$num);
}
return $num;
}
#************************************************
# backup_html成績分布ファイル用チェックボックス
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
&box_html($file,$time,"挑戦者数：$count人",0,$syg,$num);
}
return $num;
}
#************************************************
# backup_html成績分布ファイル用チェックボックス
#************************************************
sub box_html{
local($file,$time,$cf,$i_box,$syg,$num)=@_;
if($i_box eq 1){$i_box="<input type=checkbox name='$syg\i$num' value='$file'>";}
else{$i_box='　';}
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
# アクセス制限設定画面
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
<span><br><br><b>●アクセス制限を行うIPを入力してください。(前方一致)</b><br><br></span>
<table $sys_tbl_opt bgcolor='$sys_color'>
<tr><td><span>
<input type=radio name='guard' value=1$guard{1}>以下のIPをアクセス禁止にする<br>
<input type=radio name='guard' value=0$guard{0}>以下のIPをアクセス許可にする<br>
<textarea rows=20 cols=60 name='iplist'>$iplist</textarea>
</span></td></tr><tr><td>
<span><center>
<input type=submit value="　編集　">
<br></center></span></td></tr></table></form>
_HTML_
}
#************************************************
# 別ジャンルへの移動
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
write("<option value='$FORM{d}'>別ジャンルへ移動")
_HTML_
foreach $dir(@genre_dir_all){
$other_genre.="write(\"<option value=$dir>$title{$dir}\")\n";
}
$other_genre.=<<"_HTML_";
write("</select></span></td><td><span><select name=type onChange=\\"document.forms.gogenre.submit();\\">")
write("<option value='$type'>他のコマンド")
write(\"<option value=editg>ジャンルの編集\")
write(\"<option value=copy>ジャンルの複製\")
write(\"<option value=del>ジャンルの各種削除\")
write(\"<option value=qedit>問題の作成編集\")
write(\"<option value=qdel>問題の削除、順序変更\")
write(\"<option value=qmulti>問題の一括追加\")
write(\"<option value=qcont>投稿問題の編集\")
write(\"<option value=mes>終了時メッセージ追加\")
write(\"<option value=score>出題状況表\\\示\")
write(\"<option value=back>各種ログのバックアップ\")
write(\"<option value=high>高成績者リスト編集\")
write("</select></span></td></tr></table></form>")
}
//--></script>
_HTML_
}
#************************************************
# バックアップファイルをリストアップする。
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
# 高成績者リストの登録人数計算
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
# 成績分布ファイルの登録人数計算
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
# 各種ログ閲覧
#************************************************
sub log{
if(($FORM{log} eq 'm2')||($FORM{log} eq 'c2')){
if($FORM{log} eq 'm2'){$file="$FORM{d}/$mondai_$FORM{d}\.cgi";}
else{$file="$FORM{d}/$contribute_cgi";}
if(!(-f $file)){&error(814,$file);return 1;}
open(DB,$file);local(@line)=<DB>;close(DB);
$index=0;
$main_html=<<"_HTML_";
#-----書式-----# 
#q:問題文
#ans:正解
#mis1:誤答１
#mis2:誤答２
#mis3:誤答３
#mis4:誤答４
#ansmes:正解メッセージ
#mismes:不正解メッセージ
#cf:参考文献
#digest:問題内容
#mismes1:誤答１メッセージ
#mismes2:誤答２メッセージ
#mismes3:誤答３メッセージ
#mismes4:誤答４メッセージ
#author:作成者
#anstype:回答方式
_HTML_
foreach(@line){
$_=~ s/\n//g;
if($_ eq ''){next;}
if($_=~ /^#/){next;}
$index++;
local($mondai,$ans,$misans1,$misans2,$misans3,$misans4,$anscom,$misanscom,$cf,$digest,$misanscom1,$misanscom2,$misanscom3,$misanscom4,$anstype,$author)=split(/\t/,$_);
$main_html.=<<"_HTML_";
#-----第$index問-----# 
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
# パーミッション制限による設定メッセージ表示処理
#************************************************
sub permit_mes {
local($dirs)=join('<br>',@_);
&mes(<<"_HTML_");
プロバイダの関係上パーミッションに制限があり<br>
ファイル、ディレクトリの自動作成ができない場合<br>
ジャンルの新規作成には、あらかじめ以下のファイル、ディレクトリを<br>
手動で作成する必要があります。
<br><br>
<table border=0><tr><td nowrap>
$dirs
</td></tr></table>
<br><br>
なお、Windowsをお使いの方は添付プログラムにより<br>
パソ\コン上で必要ファイルを作成することができます。
_HTML_
}
#************************************************
# 表作成用print
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
# 表作成用print2
#************************************************
sub my_print2{
local($return);
local(@word)=split(/\n/,$_[0]);
foreach(@word){$return .="$_[1]$_$_[2]\n";}
return $return;
}
#************************************************
# ヘルプ作成用print
#************************************************
sub help_print{
local($return);
$return="<br><br><hr><br><b><span>■ヘルプ■</span></b><table $sys_tbl_opt bgcolor='$sys_color'>";
$return.=&my_print(@_);
$return.='</table>';
return $return;
}
#************************************************
# エラー表示処理
#************************************************
sub error_html_op{
if($error_mes ne ''){
return <<"_HTML_";
<table $sys_tbl_opt bgcolor=#eeaaaa><tr><td>
<big><center><b>■■■エラーメッセージ■■■<br><br></b></big>
<table border=0><tr><td><span><b>$error_mes</b></span></td></tr></table>
</center></td></tr></table><br>
_HTML_
}
}
#************************************************
# HTML出力
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
# ファイルの削除
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
# ジャンル別各種削除処理
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
if($flag eq 0){&error(802,'ジャンル情報');return 1;}
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
&del_file("『$title{$FORM{d}}』の設問別成績ファイル",@qu_list);
if($FORM{delh} eq 1){
&del_file("『$title{$FORM{d}}』の高成績者ログファイル",("$FORM{d}/$high_cgi1{$FORM{d}}\.cgi","$FORM{d}/$high_cgi2{$FORM{d}}\.cgi"));
}
if($FORM{delf} eq 1){
&del_file("『$title{$FORM{d}}』の成績分布ファイル",("$FORM{d}/$scorehst_cgi1{$FORM{d}}\.cgi","$FORM{d}/$scorehst_cgi2{$FORM{d}}\.cgi"));
}
if($FORM{delq} eq 1){
&del_file("『$title{$FORM{d}}』の問題ファイル","$FORM{d}/$mondai_$FORM{d}\.cgi");
}
if($FORM{delc} eq 1){
&del_file("『$title{$FORM{d}}』の投稿問題ファイル","$FORM{d}/$contribute_cgi");
}
if($FORM{dele} eq 1){
&del_file("『$title{$FORM{d}}』の終了メッセージファイル","$FORM{d}/$mes_$FORM{d}\.cgi");
}
if($FORM{deld} eq 1){rmdir $FORM{d};&mes(301,"$FORM{d}ディレクトリと、それに含まれるファイル")}#ディレクトリの削除
&mes(302,"『$title{$FORM{d}}』のジャンル登録情報");
return 0;
}
#************************************************
# 問題削除順番変更処理
#************************************************
sub del_quiz{
if(&ch_file_stump("$FORM{d}/$mondai_$FORM{d}\.cgi",'問題ファイル',$FORM{fa})){return 1;}
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
# 投稿問題削除処理
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
&mes(501,"指定された投稿問題");
}
if($#del_conts >=0){
&refresh_quiz;
&quiz_read($FORM{d},'','',$contribute_cgi);
$flag=0;
foreach $i(@del_conts){
($mondai[$i-1],$ans[$i-1],$misans1[$i-1],$misans2[$i-1],$misans3[$i-1],$misans4[$i-1],$anscom[$i-1],$misanscom[$i-1],$cf[$i-1],$digest[$i-1],$misanscom1[$i-1],$misanscom2[$i-1],$misanscom3[$i-1],$misanscom4[$i-1],$anstype[$i-1],$author[$i-1])=();
}
if(!&write_mondai("$contribute_cgi")){
&mes(303,"指定された投稿問題");
}
}
}
#************************************************
# システムデザインの削除
#************************************************
sub del_sysdesign{
local($id)=@_;
if($SYS{design} eq $id){&error(831,'このシステムデザイン');return 1;}
if($sysdesign_title{$id} eq ''){&error(803,'システムデザイン');return 1;}
$sysdesign_title{$id} = '';
if(!&write_sysdesign_dat()){
&mes(304,"指定されたシステムデザイン");
}
&all_sysdesign_read;
}
#************************************************
# ジャンルデザインの削除
#************************************************
sub del_design{
local($id)=@_;
if($design_use{$id} ne ''){&error(832,'このジャンルデザイン');return 1;}
if($design_title{$id} eq ''){&error(804,'ジャンルデザイン');return 1;}
$design_title{$id} = '';
if(!&write_design_dat()){
&mes(305,"指定されたジャンルデザイン");
}
&all_design_read;
}
#************************************************
# 問題編集処理
#************************************************
sub edit_quiz{
if(&ch_edit_quiz_param("$FORM{d}/$_[0]",)){return 1;}
if(&ch_file_stump("$FORM{d}/$_[0]",'問題ファイル',$FORM{fa})){return 1;}
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
# ジャンルの編集
#************************************************
sub edit_genre{
if(&ch_edit_genre_palam){return 1;}
&form_to_genre_array;
if(&write_genre_dat){return 1;}
&mes(203,'ジャンル設定');
&genre_array_to_form;
return 0;
}
#************************************************
# システム設定の編集
#************************************************
sub edit_sys{
if(&ch_sys_palam){return 1;}
&form_to_sys;
if(&write_system_dat){return 1;}
&mes(204,'システム設定');
&sys_read;
return 0;
}
#************************************************
# システムデザイン設定の編集
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
&mes(100,'システムデザイン設定');
}elsif($FORM{edittype} eq 'copy'){
&mes(750,'システムデザイン設定');
}else{
&mes(205,'システムデザイン設定');
}
&all_sysdesign_read;
&sys_read;
return 0;
}
#************************************************
# ジャンルデザイン設定の編集
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
&mes(101,'ジャンルデザイン設定');
}elsif($FORM{edittype} eq 'copy'){
&mes(751,'ジャンルデザイン設定');
}else{
&mes(206,'ジャンルデザイン設定');
}
&all_design_read;
&all_genre_read;
return 0;
}
#************************************************
# 終了時メッセージの編集
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
&mes(207,"『$title{$FORM{d}}』終了時メッセージ");
}
}
#************************************************
# 高成績者リストの編集
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
&mes(208,"『$title{$FORM{d}}』高成績者リスト");
return 0;
}else{return 1;}
}
#************************************************
# 終了時メッセージファイルの新規作成
#************************************************
sub make_mes_cgi{
local($value);
$value=<<"_HTML_";
30\t全然駄目だね。\t1\t1\t
50\tまだまだだね。\t1\t1\t
60\tまぁまぁだね。\t1\t1\t
70\tがんばりはみとめるよ。\t1\t1\t
80\t結構やるね～。\t1\t1\t
90\tあと一息なんだけどね。\t1\t1\t
100\tもう少しだがんばれ。\t1\t1\t
top1\tすばらしい。パーフェクト！！\t
top2\tすばらしい。パーフェクト！！\t
_HTML_
if(&ch_dir_exist("$FORM{d}ディレクトリ",$FORM{d})){return 1;}
return &write_file("$FORM{d}/mes_$FORM{d}\.cgi",$value);
}
#************************************************
# ジャンルの新規作成
#************************************************
sub make_genre{
if($FORM{d} eq 'data'){
&error(841,'(1)ディレクトリ名');
return 1;
}
if(&ch_genre_exist($FORM{d}) eq 1){
&error(852,'(1)ディレクトリ名');
return 1;
}
local($err)=&ch_dir_exist('(1)ディレクトリ名',$FORM{d});
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
,"$FORM{d}/qu100.cgi(問題数と同数以上必要)");
}
return 1;
}
&def_genre;
$GENRE{dir}=$FORM{d};
&genre_to_genre_array;
if(&write_genre_dat){return 1;}
&mes(903,'ジャンルの新規作成が正常に終了しました。<br>引き続きジャンル別設定を行ってください。');
return 0;
}
#************************************************
# ログのバックアップ
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
if($back_mes eq $system_mes){&error(407,'読み込むバックアップファイル');}
}
#************************************************
# バックアップファイルの作成
#************************************************
sub make_backup{
local($back_mes,@list,@list2);
if(($FORM{hbu1} eq '')&&($FORM{sbu1} eq '')&&($FORM{hbu2} eq '')&&($FORM{sbu2} eq '')&&($FORM{mbu} eq '')&&($FORM{qbu} eq '')){
&error(407,'バックアップを作成するファイル');return;
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
&mes(904,"$back_mes上記のバックアップファイルを作成しました。");
}
#************************************************
# バックアップファイルの操作を行う
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
if($mes ne ''){&mes(905,$mes."上記のファイルを$FORM{d}/$log\.cgiに追加しました。");}
}
}else{
if(!&h_conv_file($log,$day_limit,$num_limit,keys %include_w)){
foreach(keys %include_w){$mes.="$FORM{d}/$_<br>";}
if($mes ne ''){&mes(906,$mes."上記のファイルを$FORM{d}/$log\.cgiに上書しました。");}
}
}
&del_file(join('<br>',@del_list),@del_list);
}
#************************************************
# バックアップファイルの操作を行う
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
if($mes ne ''){&mes(907,$mes."上記のファイルを$FORM{d}/$log\.cgiに上書しました。");}
}
&del_file(join('<br>',@del_list),@del_list);
}
#************************************************
# バックアップファイルの操作を行う
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
&mes(908,"$FORM{d}/$include_w<br>上記のファイルを$FORM{d}/$mondai_$FORM{d}.cgiに上書しました。");
}
&list_genre_html($FORM{d});
}
&del_file(join('<br>',@del_list),@del_list);
}
#************************************************
# バックアップファイルの操作を行う
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
&mes(909,"$FORM{d}/$include_w<br>上記のファイルを$FORM{d}/$quiz_header??\.cgiに上書しました。");
}
&del_file(join('<br>',@del_list),@del_list);
}
#************************************************
# ファイルのバックアップの復活
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
