#!/usr/bin/perl
$version='2.03';
chdir('qqqsystems2');
#------------------------------------------------
#ファイル名：quiz.cgi
#説明：クイズを出題するページです。
#------------------------------------------------
#----------------------------はじめにお読みください------------------------------
#●このクイズのファイル構成●
#quiz.cgiクイズのスクリプト
#index.cgiクイズのメニューページ
#quiz_op.cgi管理人専用。クイズシステムの運営管理を行う
#highscore.cgiクイズの高成績者表示スクリプト
#function.cgiサブルーチン集です。他のcgiファイルから呼び出す形で利用します。
#jcode.pl日本語変換プログラム(内部から呼び出すサブルーチン)
#a.gif成績者グラフに使用される画像です。
#b.gif成績者グラフに使用される画像です。
#●クイズを動作させる手順●
#１．クイズを作成するディレクトリを作成する。(例)quizディレクトリ
#２．作成したディレクトリの属性(パーミッション)を『777』にする。(rwxrwxrwxのこと)
#３．作成したディレクトリに以下のファイルをアップロードし
#    パーミッションを744(rwxr--r--)に設定する。
#quiz.cgi(755)
#index.cgi(755)
#quiz_op.cgi(755)
#highscore.cgi(755)
#function.cgi(755)
#jcode.pl(755)
#a.gif
#b.gif
#４．お持ちのブラウザから、quiz_op.cgiにアクセスし、パスワードを登録後、管理人室に入室する。
#アクセスできない場合は、各ファイルのパーミッションを再確認してください。
#それでも駄目な場合、各cgiファイルの１行目にある、
#『#! /usr/local/bin/perl』を、サーバー毎の設定にあわせてください。
#５．管理人室において、『システム設定編集』『新ジャンル登録』を
#順に設定する。
#６．ジャンル登録が行われると、管理人室メニューに
#ジャンル別コマンドが現れるので、
#適宜、問題を追加編集する。
#７．最後に『ジャンルの編集』より、ジャンルを公開する
#以上の設定で、動作可能となります
#--------------------------------------------------------------------------------
require 'function.cgi';
require 'jcode.pl';
require 'function.cgi';
&main;
#************************************************
# ヘッダ表示処理
#_HTML_と_HTML_とのあいだに
#クイズのページのヘッダー部分のHTMLを記入してください。
#普通のHTML表記でかまいません。
#************************************************
sub header_html {
local($sub,$back_color,$wall_paper)=@_;
local($sub_header);
if($sub ne ''){
$sub_title = "<br>$sub";
$title3 = "- $sub -$mode_name";
}else{
$sub_title = '';
$title3="-$mode_name";
}
if($back_color eq ''){
$back_color="#bbbbee";
}
if($wall_paper ne ''){
$wall_paper = " background='$wall_paper'"
}
if($mode_name ne ''){
$mode_n="$mode_name";
}
if($FORM{s} ne '' || $FORM{add} ne ''){
$mode_n='';
}
if($text_color ne ''){
$text=" text='$text_color'";
}
if($link_color ne ''){
$link=" link='$link_color'";
}
if($vlink_color ne ''){
$vlink=" vlink='$vlink_color'";
}
local($header_opt);
$header_opt="d=$FORM{d}&m=$FORM{m}";
if($FORM{passch} ne ''){$header_opt.="&passch=$FORM{passch}";}
$sub_header=$SYS{sub_header};
$sub_header=~ s/\$title/$SYS{main_title}/g;
$sub_header=~ s/\$sub_title/$sub_title/g;
$sub_header=~ s/\$genre/$title/g;
$sub_header=~ s/\$top/\[<a href="$SYS{top_url}">$_top<\/a>\] /g;
$sub_header=~ s/\$index/\[<a href="$index_cgi">$SYS{main_title}<\/a>\] /g;
$sub_header=~ s/\$challenge/\[<a href="$quiz_cgi?$header_opt">$_try<\/a>\] /g;
$sub_header=~ s/\$high/\[<a href="$quiz_cgi?$header_opt&h=1">$_high<\/a>\] /g;
$sub_header=~ s/\$graph/\[<a href="$quiz_cgi?$header_opt&g=1">$_graph<\/a>\] /g;
$sub_header=~ s/\$score/\[<a href="$quiz_cgi?$header_opt&s=1">$_score<\/a>\] /g;
if(!mygrep($dir,@genre_dir_orign) || $cont{$dir} ne 1){
$sub_header=~ s/\$add//g;
}else{
$sub_header=~ s/\$add/\[<a href="$quiz_cgi?$header_opt&add=1">$_add<\/a>\] /g;
}
$sub_header=~ s/\$mode/$mode_n/g;
$SYS{header}=~ s/\$imode/\[<a href="$quiz_cgi?$header_op">$<\/a>\] /g;
$header_html= <<"_HTML_";
<html><head>
<STYLE Type="text/css">$style</STYLE>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=x-sjis">
<title>$title$title3</title></head>
<BODY bgcolor="$back_color"$wall_paper$text$link$vlink>
$sub_header
_HTML_
$header_i_html=<<"_HTML_";
<html><head>
<title>$title$title3</title></head>
<body>
○$title{$FORM{d}}○<br>
_HTML_
}
#************************************************
# 初期画面のメッセージ
#_HTML_と_HTML_とのあいだに
#クイズのページのヘッダー部分のHTMLを記入してください。
#普通のHTML表記でかまいません。
#全角スペースを入力するとエラーが発生するので使用しないでください。
#変数$quiz_maxには総問題数が入っています。
#変数$lose_maxには、最大許容誤答数が入っています。
#変数$all_hstには総挑戦者数が入っています。
#変数$highには、最高成績者名がはいります。
#************************************************
sub startmes{
&history_read();
open(DB,"$FORM{d}/$high_cgi\.cgi");@lines = <DB>;close(DB);
if($lines[0] =~ /^date/){($day,$high,$name,$host) = split(/\t/,$lines[1]);}
else{($day,$high,$name,$host) = split(/\t/,$lines[0]);}
if($high ne ''){$high="最高成績は$nameさんの$high問正解。<br>";}
$start_comment=~ s/\$title/$title/g;
$start_comment=~ s/\$quiz_max/$quiz_max/g;
$start_comment=~ s/\$play_max/$play_max/g;
$start_comment=~ s/\$lose_max/$lose_max/g;
$start_comment=~ s/\$challenge/$HIST{all_hst}/g;
$start_comment=~ s/\$high/$high_border/g;
if($time_limit>0){$start_comment=~ s/\$time/$time_limit/g;}
else{$start_comment=~ s/\$time/無し/g;}
$start_comment=~ s/\$champion/$high/g;
$start_html=<<"_HTML_";
<br>
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$com_color"><tr><td>
<table $tbl_opt><tr><td$nowrap>
<small>$start_comment</small>
</td></tr></table>
</td></tr></table>
<br>
_HTML_
$start_i_html=<<"_HTML_";
$quiz_max問中$play_max問出題。<br>
$lose_max問間違えると<br>
GAME OVERです。<br>
さぁスタート！！<br><br>
_HTML_
}
#************************************************
# クイズ終了時メッセージ
#************************************************
sub end_mes {
local($mes,$per,$end_mes,$num);
local($time1,$time2,$col);
$better=1;
for($i=$LOG{win}+1;$i<=$play_max;$i++){
$better=$better+$score[$i];
}
$num=$quiz_num + 1;
$per=&point($LOG{win}*100/$num,1);
$col=5;
if($LOG{'time'} ne ''){
$time1="<td bgcolor='$th_color' nowrap>回答時間</td>";
$time2="<td bgcolor='$td_color' nowrap>$LOG{min}分$LOG{sec}秒</td>";
$time_i="時　間:$LOG{min}分$LOG{sec}秒<br>";
$col++;
}
$mes = &get_message($per);
if($mes ne ''){
$end_mes="<tr><td$nowrap colspan=$col bgcolor='$com_color'>"
."<b>$walign1$mes$walign2</b></td></tr>";
}
$main_html.=<<"_HTML_";
<hr>
<b><span>■最終成績■</span></b>
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$border_color"><tr><td>
<table $tbl_opt>
$end_mes
<tr>
<td bgcolor="$th_color" nowrap>問題数</td>
<td bgcolor="$th_color" nowrap>正解数</td>
<td bgcolor="$th_color" nowrap>正解率</td>
<td bgcolor="$th_color" nowrap>偏差値</td>
<td bgcolor="$th_color" nowrap>順　位</td>
$time1
</tr>
<tr>
<td bgcolor='$td_color' nowrap>$num問</td>
<td bgcolor='$td_color' nowrap>$LOG{win}問</td>
<td bgcolor='$td_color' nowrap>$per％</td>
<td bgcolor='$td_color' nowrap>$HIST{hensa}</td>
<td bgcolor='$td_color' nowrap>$better位</td>
$time2
</tr>
_HTML_
if($mes ne ''){$mes.='<br><br>';}
$main_i_html.=<<"_HTML_";
GAME OVER<br><br>
$mes
■最終成績■<br>
問題数:$quiz_num問<br>
正解数:$LOG{win}問<br>
正解率:$per％<br>
偏差値:$HIST{hensa}<br>
順　位:$better位<br>
$time_i
_HTML_
if(($per>=$high_border)
&&($day_limit ne '0')
&&($num_limit ne '0')){
$midi_html.=&midi_html($high_midi);
$main_html.=<<"_HTML_";
<tr><td nowrap colspan=$col bgcolor='$com_color'>
<br><center><big>●おめでとうございます●</big><br><br>
<small>正解率が合格ラインの$high_border％に達しました。</small><br>
_HTML_
$main_i_html.=<<"_HTML_";
<br>おめでとうございます。<br>
正解率が合格ラインの$high_border％に達しました。<br>
_HTML_
if(&ch_rankin){
$add_ch=&ch_address("$quiz_id"."$LOG{win}");
$FORM{EntryName}=$LOG{name};
&form_to_form2(EntryName);
if($rec_com eq 1){
$rec ="<tr><td>コメント：</td>";
$rec.="<td><span><input type=text name=com size=30 maxlength=$max_com></span></td></tr>";
$rec_i="コメント：<input type=text name=com size=30 maxlength=$max_com><br>";
}
$main_html.=<<"_HTML_";
<small><b>$_highリストに登録</b>ができます。</small>
<form method="$method" action="$quiz_cgi" name=frm>
<input type=hidden name=passch value='$FORM{passch}'>
<table border=0>
<tr>
<td>名前：</td>
<td><span><input type=text name="EntryName" value="$FORM2{EntryName}" size=30 maxlength=$max_en></span></td>
</tr>
$rec
</table>
<span>
<br>
<input type=hidden name="Score" value="$LOG{win}">
<input type=hidden name="id" value="$quiz_id">
<input type=hidden name="h" value="1">
<input type=hidden name="d" value="$FORM{d}">
<input type=hidden name="m" value="$FORM{m}">
<input type=hidden name="check" value="$add_ch">
<input type=submit value="  登録  "></form>
</center></span>
${&focus_move('EntryName')}$ret
_HTML_
$main_i_html.=<<"_HTML_";
$_highリストに登録</b>ができます。<br>
<form method="$method" action="$quiz_cgi" name=frm>
<input type=hidden name=passch value='$FORM{passch}'>
名前：<input type=text name="EntryName" value="$FORM2{EntryName}" size=30 maxlength=$max_en><br>
$rec_i
<input type=hidden name="Score" value="$LOG{win}">
<input type=hidden name="id" value="$quiz_id">
<input type=hidden name="h" value="1">
<input type=hidden name="j" value="1">
<input type=hidden name="d" value="$FORM{d}">
<input type=hidden name="m" value="$FORM{m}">
<input type=hidden name="check" value="$add_ch">
<input type=submit value="  登録  "></form>
_HTML_
}else{
$main_html.="<br>残念ながら$_highリストにランクインできませんでした。<br><br>";
$main_i_html.="<br>残念ながら$_highリストにランクインできませんでした。<br>";
}
$main_html.='</td></tr>';
}else{
$midi_html.=&midi_html($end_midi);
}
$main_html.='</table></td></tr></table></td></tr></table><br><br>';
}
#************************************************
# メインプログラム
#************************************************
sub main{
&setup;
if(&ch_sys_lock){&busy_html;}
elsif(&ch_guard_ip){&guard_html;}
else{
$quiz_num=0;
if(&buf_read){
print "Location:$index_cgi\n\n";
exit;
}
&header_html();
&footer_html;
&html;
&set_cookie;
$footer_i_html=<<"_HTML_";
<br><br><a href=$index_cgi?&j=1>メニューへ</a><br>
<a href=$quiz_cgi?d=$FORM{d}\&m=1&j=1>再挑戦</a><br>
</body></html>
_HTML_
}
if($imode){&output_i;}
else{&output;}
}
#************************************************
# メイン画面表示
#************************************************
sub html{
if(&sys_read){&error(711);return ;}
&get_cookie;
if($FORM{bgm} ne ''){
$COOKIE{bgm} = $FORM{bgm};
}
&header_html('',$main_color);
if($FORM{qid} ne ''){
if(&ch_buf){return ;}
&play_log_read($quiz_id);
if(&ch_address("$quiz_num$quiz_id") ne $quiz_check){
&error(601);return 1;
}
$FORM{d}=$LOG{genre};
$FORM{m}=$LOG{mode};
}
if(&genre_read){&error(721);return ;}
if($FORM{g} ne ''){
&header_html($_graph,$main_color,$wall);
}elsif($FORM{s} ne ''){
&header_html($_score,$main_color,$wall);
}else{
&header_html('',$main_color,$wall);
}
if($mente eq '0' && &ch_pwd($FORM{passch}) && (
!($FORM{h} ne '' && $FORM{id} ne '') &&
$FORM{qid} eq '')){
&error(652);
return;
}
if($FORM{add} ne ''){
&contribute;
return;
}elsif($FORM{h} ne ''){
&header_html($_high,$main_color,,$wall);
if($FORM{id} ne ''){
$COOKIE{N}=$FORM{EntryName};
&set_cookie;
if(&log_write){return;}
undef %HIGH;
}
&highscore_html;
return;
}elsif($FORM{qid} eq ''){
&get_genre_dir_use();
}
&quiz_read_all;
&max_set;
if($FORM{qid} ne '' && &ch_reload()){
return;
}
if($FORM{g} ne ''){
&history_read();
&history_backup;
&show_graph();
}elsif($FORM{s} ne ''){
&rec_html();
}elsif($LOG{bundle} eq 0){
$quiz_index=&mondai_num($quiz_max-1);
if(&ch_ans){return;}
&header_html('',$result_color[$win],$result_wall[$win]);
&setCookieScore();
&setLogScore();
if(&play_log_write){return;}
if(&ans_html){return;}
if(&ch_continue eq 0){
&end_html;
}else{
$midi_html.=&midi_html($result_midi[$win]);
$quiz_num++;
&score_html;
&main_html;
}
}elsif($LOG{bundle} eq 1){
if($quiz_reload ne 1){$LOG{old}='';}
for($quiz_num=0;$quiz_num<$play_max;$quiz_num++){
$quiz_index=&mondai_num($quiz_max-1);
if(&ch_ans){return;}
if(&ans_html){return;}
&setCookieScore();
&setLogScore();
}
$quiz_num--;
&header_html('',$main_color,$wall);
if(&play_log_write){return;}
&end_html;
}else{
$COOKIE{"S$cid"}++;
&header_html('',$main_color,$wall);
if(&startup){return;}
unless(&main_html){&startmes;}
}
}
#************************************************
# クイズ開始処理
#************************************************
sub startup{
local($count,$file);
if(&ch_dir_exist('ディレクトリ名',$data_dir) > 0){return 1;}
$quiz_id = &get_playlog_id();
if ($quiz_id eq ''){
&error(661);return 1;
}
&def_log();
&play_log_write();
}
#************************************************
# エンディング表示処理
#************************************************
sub end_html {
&history_read();
if($quiz_reload ne 1){
$score[$LOG{win}]++;
if(&history_write){return;}
&history_backup;
$COOKIE{"A$cid"}=($COOKIE{"A$cid"}*$COOKIE{"E$cid"}+ $LOG{win})/($COOKIE{"E$cid"}+1);
$COOKIE{"E$cid"}++;
if($COOKIE{"H$cid"} < $LOG{win}){
$COOKIE{"H$cid"} = $LOG{win};
}
}
&end_mes;
&show_graph($LOG{win});
}
#************************************************
# クイズの回答結果をクッキーにセットする
#************************************************
sub setCookieScore{
if($quiz_reload eq 1){return;}
$COOKIE{"W$cid"}=$COOKIE{"W$cid"} + $win;
$COOKIE{"L$cid"}=$COOKIE{"L$cid"} + $lose;
$COOKIE{"T$cid"}=$COOKIE{"T$cid"} + $LOG{last_lap};
if($COOKIE{"W$cid"}>0){
if($COOKIE{"I$cid"} == 0){
$COOKIE{"I$cid"}=$LOG{last_lap};
}else{
$COOKIE{"I$cid"}=($COOKIE{"I$cid"}*($COOKIE{"W$cid"}-1)+ $LOG{last_lap})/$COOKIE{"W$cid"};
}
}
}
#************************************************
# クイズの回答結果をプレイログにセットする
#************************************************
sub setLogScore{
if($quiz_reload eq 1){return;}
$LOG{win}=$LOG{win}+$win;
$LOG{lose}=$LOG{lose}+$lose;
$LOG{num}++;
$LOG{old} .= $FORM{"a_$quiz_num"}.',';
}
#************************************************
# 新規プレイログファイルの取得
#************************************************
sub get_playlog_id{
local($log_id,$log_counter,@list);
open(DB,"$count_file\.cgi");@list=<DB>;close(DB);
$log_counter=$list[0]+0;
if($log_counter >= $SYS{max_player}){$log_counter=0;}
elsif($log_counter < 0){$log_counter=0;}
$flag=0;
foreach $i($log_counter+1..$SYS{max_player} , 1..$log_counter){
if(!(-f "$data_dir/$header$i\.cgi")){
$log_id=$i;
last;
}elsif(($SYS{limit}/24/60 < (-M "$data_dir/$header$i\.cgi"))
&& !(-t "$data_dir/$header$i\.cgi")){
$log_id=$i;
last;
}
}
if($log_id ne ''){
&write_file("$count_file\.cgi",$log_id);
}
return $log_id;
}
#************************************************
# 終了メッセージ文の取得
#************************************************
sub get_message{
local($per)=@_;
local($mes);
open(DB,"$FORM{d}/$mes_cgi\.cgi");
local(@lines)= <DB>;
close(DB);
foreach $line(@lines){
local($mes_per,$mes_word,$mod1,$mod2)=split(/\t/,$line);
if($mes_per eq 'top'){
if($per == 100){
$mes="$mes_word";
last;
}
}
if($FORM{m} ne 2){
if($mes_per eq 'top1'){
if($per == 100){
$mes="$mes_word";
last;
}
}
if(($per < $mes_per)&&($mod1 ne '0')){
$mes="$mes_word";
last;
}
}else{
if($mes_per eq 'top2'){
if($per == 100){
$mes="$mes_word";
last;
}
}
if(($per < $mes_per)&&($mod2 ne '0')){
$mes="$mes_word";
last;
}
}
}
return $mes;
}
#************************************************
# 問題番号取得関数
# $quiz_num,$LOG{seed}で　次の問題番号を返します。
#************************************************
sub mondai_num {
local($dumy,@semi,$max,$i,$sin,$r,$seed);
$max=$_[0];
if($random eq '0'){return $quiz_num;}
@semi=();
$seed=$LOG{seed}/100000;
$mid=int($max*$seed);
for($i = $mid;$i<=$max;$i++){push(@semi,$i);}
for($i = 0;$i<$mid;$i++){push(@semi,$i);}
for($i=0;$i<10;$i++){$seed=3.98*$seed*(1-$seed);}
for($i = 0;$i<=$quiz_num;$i++){
$seed=3.98*$seed*(1-$seed);
$r=int(($max-$i+1)*$seed);
$dumy=$r;
$dumy=@semi[$r];
$semi[$r]=$semi[$max-$i];
}
return $dumy;
}
#************************************************
# 疑似ランダム関数
# $quiz_num,$LOG{seed}で
# (0,1,2,,,$max)を、ランダムに並び替えたものを返す
#************************************************
sub semirand {
local(@num,$i,$dummy);
$max=$_[0];
@num=(0..$max-1);
$r=10;
for($i=0;$i<$max;$i++){
$sin=sin($quiz_num+$LOG{seed}*10+($r-10))*0.87;
if($sin<0){$sin=1+$sin;}
$r=int(($max-$i)*$sin);
$dummy=$num[$r];
$num[$r]=$num[$max-1-$i];
$num[$max-1-$i]=$dummy;
}
return @num;
}
#************************************************
# 高成績者登録チェック
#************************************************
sub ch_rankin {
if($num_limit<1){return 1;}
open(DB,"$FORM{d}/$high_cgi\.cgi");
local(@lines) = <DB>;
close(DB);
if($lines[0]=~ /^date/){shift(@lines);}
if($num_limit > $#lines + 1){return 1;}
local($day,$high,$name,$host,$time,$com) = split(/\t/,$lines[$#lines]);
if($high < $LOG{win}){return 1;}
if($high > $LOG{win}){return 0;}
if(($time >= $LOG{min}*60+$LOG{sec})||($time eq '')){return 1;}
return 0;
}
#************************************************
# バッファのチェック
#************************************************
sub ch_buf {
($quiz_id
,$quiz_num
,$quiz_check
)=split(/_/,$FORM{qid});
foreach $key(keys %FORM){
if($key =~ /^b_(.*)/){
$FORM{"a_$quiz_num"}=$1;
last;
}
}
return 0;
}
#************************************************
# 正解チェック
#************************************************
sub ch_ans{
$win=0;$lose=0;
$play_index='';
@dumy=&semirand(5);
if($anstype[$quiz_index] > 0){
local(@ans_list)=($ans[$quiz_index],$misans1[$quiz_index],$misans2[$quiz_index],$misans3[$quiz_index],$misans4[$quiz_index]);
$i=0;
foreach $da(@ans_list){
local(@ans)=split(/<br>/,$da);
foreach $al(@ans){
if($al eq $FORM{"a_$quiz_num"}){
$play_index = $i;
}
}
$i++;
}
}else{
$play_index=$dumy[$FORM{"a_$quiz_num"}-1];
}
if(($time_limit > 0)&&($time_limit < $LOG{last_lap})){
$win=0;$lose=1;
}elsif(($play_index ne 0)||(($anstype[$quiz_index] < 1)&&($FORM{"a_$quiz_num"} eq ''))){
$win=0;$lose=1;
}else{
$win=1;$lose=0;
}
return 0;
}
#************************************************
# リロードチェック
#************************************************
sub ch_reload{
if($LOG{bundle} eq 1){
if($LOG{num}>0){
local(@old)=split(/,/,$LOG{old});
for($i=0;$i<$play_max;$i++){
if(($old[$i] ne $FORM{"a_$i"})&&($FORM{"a_$i"} ne '')){&error(602);return 1;}
}
$quiz_reload=1;
}else{
if($play_max>0){
$LOG{last_lap}=&point(($now - $LOG{lap})/$play_max,1);
}
$LOG{lap}=$now;
($LOG{sec},$LOG{min})=&score_time($LOG{lap} - $LOG{'time'});
$LOG{old}='';
}
}elsif($LOG{num} eq $quiz_num+1){
if($LOG{old} eq $FORM{"a_$quiz_num"}.','){$quiz_reload=1;}
else{&error(603);return 1;}
}elsif($quiz_num - $LOG{num} eq 0){
$LOG{last_lap}=$now - $LOG{lap};
$LOG{lap}=$now;
($LOG{sec},$LOG{min})=&score_time($LOG{lap} - $LOG{'time'});
$LOG{old}='';
}else{&error(604);return 1;}
return 0;
}
#************************************************
# クイズ継続チェック
# $lose_max問以上間違えると０を返す
# $play_max問以上出題しない
#************************************************
sub ch_continue {
if($quiz_num >= $play_max-1){return 0;}
if($LOG{lose} >= $lose_max){return 0;}
else{return 1;}
}
#************************************************
# 問題投稿チェック関数
#************************************************
sub ch_contribute_param{
local($arth);
$err=0;
if($FORM{d} eq ''){&error(201,'ジャンル');$err=1;}
if($title{$FORM{d}} eq ''){&error(201,'ジャンル');$err=1;}
if(($mondai_cgi{$FORM{d}} eq '.')||($mondai_cgi{$FORM{d}} =~ /\//)){&error(201,'ジャンル');$err=1;}
if(length($FORM{auth}) > 20){&error(521,'お名前');$err=1;}
if($FORM{qqu} eq ''){&error(201,'問題文');$err=1;}
if($FORM{qas} eq ''){&error(201,'正解');$err=1;}
if(($FORM{qmas1} eq '')&&($FORM{atype} eq '')){&error(201,'誤答１');$err=1;}
if($err ne 1){
if(!&write_cont()){
&error('問題の投稿を正しく受け付けました。<br>投稿された問題は、管理人が確認後<br>承認された場合に限り問題として正式採用されます。');
&clear_form('qqu','qas','qmas1','qmas2','qmas3','qmas4','qac','qmac','qcf','qdg','qmac1','qmac2','qmac3','qmac4','atype','auth');
}
}
}
#************************************************
# 問題投稿処理
#************************************************
sub contribute{
&header_html($_add,$main_color,,$wall);
if($FORM{d} eq ''){
&error(408,'ジャンル');
}elsif($title{$FORM{d}} eq ''){
&error(807,'指定したジャンル');
}elsif(!mygrep($FORM{d},@genre_dir_orign) || $cont ne 1){
&error(759);
}else{
if($FORM{edit} ne ''){&ch_contribute_param;}
&contribute_form;
}
}
#************************************************
# 問題投稿HTML
#************************************************
sub contribute_form{
$FORM{"atype_$FORM{atype}"}=' checked';
local($ans_type,$direct,$ans_type_help);
if($notext ne 1){
$ans_type="<tr><td bgcolor='$th_color'><small>回答方式</small></td><td bgcolor='$td_color'><input type=checkbox name=atype value=1 $FORM{atype_1}>テキスト入力方式</td></tr>";
$ans_type_help="※回答方式がテキスト入力形式の場合、各行が正解（誤答）となります。<br>\nいずれかの行と、回答欄に入力された文字列が一致した場合正解（誤答）となります。<br>";
}
if($direct_cont ne 1){
$direct='<font color=red>管理人が確認後、承認された場合に限り問題として正式採用されます。</font><br><br>';
}else{
$direct='<font color=red>問題の投稿完了後、自動的に問題として採用されます。</font><br><br>';
}
$main_html= <<"_HTML_";
<form action="$quiz_cgi" method="$method">
<input type=hidden name=add value=1>
<input type=hidden name=edit value=1>
<input type=hidden name=passch value='$FORM2{passch}'>
<input type=hidden name=d value='$FORM{d}'>
<span><br><br><b>●各項目に入力し、送信ボタンを押してください。</b>( * 印は必須項目です。)<br><br><br>
$direct
<b>■問題入力フォーム■</b></span><small>改行→&lt;BR&gt;　　に自動変換</small><br>
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$border_color"><tr><td>
<table $tbl_opt>
<tr><td bgcolor="$th_color"><small>ジャンル</small></td><td bgcolor="$td_color">
$title{$FORM{d}}
</select>
</td></tr>
<tr><td bgcolor="$th_color"><small>お名前(公開)</small></td><td bgcolor="$td_color"><input type=text size=20 name=auth value="$FORM2{auth}">全角１０文字以内</td></tr>
$ans_type
<tr><td bgcolor="$th_color"><small>問題文 *</small></td><td bgcolor="$td_color"><textarea name=qqu cols=55 rows=3>\n$FORM3{qqu}</textarea></td></tr>
<tr><td bgcolor="$th_color"><small>正解 * ※</small></td><td bgcolor="$td_color"><textarea name=qas cols=55 rows=3>\n$FORM3{qas}</textarea></td></tr>
<tr><td bgcolor="$th_color"><small>誤答１ * ※</small></td><td bgcolor="$td_color"><textarea name=qmas1 cols=55 rows=3>\n$FORM3{qmas1}</textarea></td></tr>
<tr><td bgcolor="$th_color"><small>誤答２ ※</small></td><td bgcolor="$td_color"><textarea name=qmas2 cols=55 rows=3>\n$FORM3{qmas2}</textarea></td></tr>
<tr><td bgcolor="$th_color"><small>誤答３ ※</small></td><td bgcolor="$td_color"><textarea name=qmas3 cols=55 rows=3>\n$FORM3{qmas3}</textarea></td></tr>
<tr><td bgcolor="$th_color"><small>誤答４ ※</small></td><td bgcolor="$td_color"><textarea name=qmas4 cols=55 rows=3>\n$FORM3{qmas4}</textarea></td></tr>
<tr><td bgcolor="$th_color"><small>正解時コメント</small></td><td bgcolor="$td_color"><textarea name=qac cols=55 rows=2>\n$FORM3{qac}</textarea></td></tr>
<tr><td bgcolor="$th_color" nowrap><small>不正解時コメント</small></td><td bgcolor="$td_color"><textarea name=qmac cols=55 rows=2>\n$FORM3{qmac}</textarea></td></tr>
<tr><td bgcolor="$th_color" nowrap><small>参考文献等<br>(非公開)</small></td><td bgcolor="$td_color"><input type=text size=55 name=qcf value="$FORM2{qcf}"></td></tr>
<tr><td bgcolor="$th_color" nowrap><small>問題内容<br>(出題一覧用)</small></td><td bgcolor="$td_color"><input type=text size=55 name=qdg value="$FORM2{qdg}"></td></tr>
<tr><td bgcolor="$td_color" colspan=2><center>
<input type=submit value="　　 送信 　　">
</center></td></tr></table>
</td></tr></table>
</form>
$ans_type_help
_HTML_
}
#************************************************
# 投稿問題書き込み
#************************************************
sub write_cont{
local($value,$auth);
$direct_cont=0;
&genre_read($FORM{d});
if($notext eq 1){
$FORM{atype}='';
}
&refresh_quiz;
if($direct_cont eq 1){
&quiz_read($FORM{d});
}else{
&quiz_read($FORM{d},'','',$contribute_cgi);
}
if(&ch_duplic_quiz){return 1;}
&push_quiz_palam($FORM4{qqu},$FORM4{qas},$FORM4{qmas1},$FORM4{qmas2},$FORM4{qmas3},$FORM4{qmas4},$FORM4{qac},$FORM4{qmac},$FORM{qcf},$FORM4{qdg},$FORM4{qmac1},$FORM4{qmac2},$FORM4{qmac3},$FORM4{qmac4},$FORM{atype},$FORM{auth});
if($direct_cont eq 1){
return &write_file(">$FORM{d}/$mondai_$FORM{d}\.cgi",&quiz_to_line($#mondai,$#mondai+1));
}else{
return &write_file(">$FORM{d}/$contribute_cgi",&quiz_to_line($#mondai));
}
}
#************************************************
# プレイログを書き込む
#************************************************
sub play_log_write {
local(@log);
if($quiz_reload eq 1){return 0;}
$log[0]=join("\t",$LOG{num}
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
,$COOKIE{"S$cid"}
,$COOKIE{N}
,$LOG{bundle}
,"\n");
foreach(@genre_dir_use){
push(@log,join("\t",$_,$genre_num{$_},"\n"));
}
if(&ch_dir_exist("$data_dirディレクトリ",$data_dir) > 0){return 1;}
if(&write_file("$data_dir/$header$quiz_id\.cgi",@log)){
return 1;
}
return 0;
}
#************************************************
# 成績履歴ファイルの書き込み
#************************************************
sub history_write{
if(&ch_dir_exist('ディレクトリ名',$FORM{d})){return 1;}
if(&ch_hist_lock($FORM{d}) ne 1){
&hist_lock($FORM{d});
my($ret)=&write_file("$FORM{d}/$scorehst_cgi\.cgi",join("\n",@score));
&hist_unlock($FORM{d});
if($ret){return 1;}
}else{return 1;}
return 0;
}
#************************************************
# 成績履歴ファイルのバックアップ
#************************************************
sub history_backup{
if($scorehst_back_day > 0){
&backup_file("$FORM{d}/${scorehst_cgi}.cgi",$scorehst_back_w,$scorehst_back_day);
}
}
#************************************************
# 成績履歴の読み込み
#************************************************
sub history_read{
open(DB,"$FORM{d}/$scorehst_cgi\.cgi");@score=<DB>;close(DB);
for($i=0;$i<=$#score;$i++){$score[$i]=~ s/\n//g;}
if($histry_div <=> 0){
$HIST{hst_dev}=int($play_max/$histry_div);
}else{
$HIST{hst_dev}=int($play_max/5);
}
($HIST{all_hst}
,$HIST{hensa}
,$HIST{hyouhen}
,$HIST{average}
)=&getHistoryAnalisys($play_max,@score);
}
#************************************************
# 設問別成績ファイルの書き込み
#************************************************
sub quiz_log_write{
$value=join("\t",@qu,"\n$QU{ave}",$QU{play_num},"\n");
if(&ch_dir_exist('ディレクトリ名',&get_question_dir($quiz_index)) > 0){return 1;}
if(&ch_hist_lock($FORM{d}) ne 1){
&file_lock("$QU{dir}/$quiz_header${quiz_head_num}.lock");
my($ret)=&write_file("$QU{dir}/$quiz_header$QU{index}.cgi",$value);
&file_unlock("$QU{dir}/$quiz_header${quiz_head_num}.lock");
if($ret){return 1;}
}else{return 1;}
}
#************************************************
# 成績履歴の分析を行う
#************************************************
sub getHistoryAnalisys{
local($play_max,@score)=@_;
local($all_hst,$hensa,$hyouhen,$average,$mass)=(0,'---',0,0,0);
for($i=0;$i<=$play_max;$i++){
$score[$i]=~ s/\n//;
if($score[$i] eq ''){$score[$i]=0;}
$all_hst=$all_hst+$score[$i];
$mass=$mass+($i)*$score[$i];
}
if($all_hst >0){
$average=&point($mass/$all_hst,2);
for($i=0;$i<=$play_max;$i++){
$hyouhen=$hyouhen+($average-$i)*($average-$i)*$score[$i];
}
$hyouhen=&point(sqrt($hyouhen/$all_hst),2);
if($hyouhen > 0){
$hensa=&point(($LOG{win}-$average)*10/$hyouhen+50,1);
}
}
return ($all_hst,$hensa,$hyouhen,$average);
}
#************************************************
# 正解数表示処理
#************************************************
sub ans_html{
&quiz_log_read();
if($quiz_reload ne 1){
$QU{play_num}=$QU{play_num}+1;
$QU{play_win}=$QU{play_win}+$win;
if($play_index ne ''){
$qu[$play_index]=$qu[$play_index]+1;
}
local($qu_num,$qu_all_num);
foreach $qu_num(@qu){
$qu_all_num=$qu_all_num+$qu_num;
}
if($qu_all_num>$QU{play_num}){$QU{play_num}=$qu_all_num;}
if($win eq 1){
$QU{ave}=($QU{ave}*($QU{play_win}-1)+ $LOG{last_lap})/$QU{play_win};
}
&quiz_log_write();
&quiz_log_calc();
}
local(@ans_list)=($ans[$quiz_index],$misans1[$quiz_index],$misans2[$quiz_index],$misans3[$quiz_index],$misans4[$quiz_index]);
local(@com_list)=('',$misanscom1[$quiz_index],$misanscom2[$quiz_index],$misanscom3[$quiz_index],$misanscom4[$quiz_index]);
local($comment
,$result_sign
,$result_sign_i
);
if($win eq 1){
$result_sign.="$win_sign";
$result_sign_i.="正解！<br>";
$comment="$anscom[$quiz_index]";
}elsif($lose eq 1){
if(($time_limit >= $LOG{last_lap})||($time_limit == 0)){
$result_sign="$lose_sign";
$result_sign_i="不正解！<br>";
}else{
$result_sign="$over_sign";
$result_sign_i="時間オーバー<br>";
}
$comment = $com_list[$play_index];
if($comment eq ''){
$comment=$misanscom[$quiz_index];
}
}
if($comment ne ''){
$comment="<tr><td nowrap bgcolor='$th_color'>コメント</td><td$nowrap bgcolor='$td_color'><span><b>$walign1$comment$walign2</b></span></td></tr>\n";
}
local($your_ans);
if($FORM{"a_$quiz_num"} eq ''){
$your_ans="--------";
}elsif($anstype[$quiz_index] eq 1){
$your_ans=$FORM{"a_$quiz_num"};
}else{
$your_ans=$ans_list[$play_index];
}
local($correct_ans);
if($show_ans eq '1'){
$correct_ans= "<tr><td nowrap bgcolor='$th_color'><small>正解</small></td><td$nowrap bgcolor='$td_color'><small>$walign$ans[$quiz_index]$walign2</small></td></tr>\n";
$correct_ans_i=$ans[$quiz_index];
$correct_ans_i =~ s/<br>$//g;
$correct_ans_i =~ s/<br>/,/g;
$correct_ans_i= "正解:$correct_ans_i<br>";
}
local($ans_time);
if($LOG{bundle} eq 0){
$ans_time= "<tr><td nowrap bgcolor='$th_color'><small>回答時間</small></td><td bgcolor='$td_color' nowrap><small>$walign1$LOG{last_lap}秒$walign2</small></td></tr>\n";
$ans_time_i= "時間:$LOG{last_lap}秒";
}
$dum=$quiz_num+1;
$main_html.=<<"_HTML_";
<hr>
$result_sign
<br><br><span><b>■$dum問目 回答結果■</b></span>
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$border_color"><tr><td>
<table $tbl_opt>
$comment
<tr>
<td nowrap width=10% bgcolor='$th_color'><small>問題文</small></td>
<td bgcolor='$td_color'$nowrap><small>$walign1$mondai[$quiz_index]$walign2</small></td>
</tr>
$correct_ans
<tr>
<td nowrap bgcolor='$th_color'><small>貴方の答え</small></td>
<td bgcolor='$td_color'$nowrap width="$twidth1"><small>$walign1$your_ans$walign2</small></td>
</tr>
$ans_time
<tr>
<td nowrap bgcolor='$th_color'><small>全体の成績</small></td>
<td bgcolor='$td_color'$nowrap><small>$walign1$QU{play_num}人中 $QU{play_win}人正解 ($QU{win_ratio}％)　平均正解時間 $QU{ave2}秒$walign2</small></td>
</tr>
</table></td></tr></table><br>
_HTML_
$main_i_html.=<<"_HTML_";
■$dum問目 回答結果■<br>
$result_sign_i
$correct_ans_i
$ans_time_i<br>
_HTML_
return 0;
}
#************************************************
# 途中成績表示処理
#************************************************
sub score_html{
local($per,$time,$limit);
$per=&point($LOG{win}*100/$quiz_num,1);
if($time_limit > 0){$limit="　時間制限<b>$time_limit</b>秒";}
if($LOG{'time'} ne ''){$time='　'."回答時間：<b>$LOG{min}分$LOG{sec}秒</b>";}
$main_html.=<<"_HTML_";
<small><hr>
出題数：<b>$quiz_num/$play_max</b>問　
正解：<font color="blue"><b>$LOG{win}</b></font>問　
不正解：<b><font color="red">$LOG{lose}</font>/$lose_max</b>問　
正解率：<b>$per</b> % $time$limit</small>
_HTML_
$main_i_html.="正解数$LOG{win}問<br><br>";
}
#************************************************
# クイズ表示処理
#************************************************
sub main_html{
if($quiz_max<=0){
&error(671);
return 1;
}
if($LOG{bundle} eq 0){
&question_html;
&individual_html;
}else{
$add_ch=&ch_address("0$quiz_id");
$main_html.= <<"_HTML_";
<form method='$method' action=$quiz_cgi>
<input type=hidden name=passch value=$FORM{passch}>
<input type=hidden name=d value=$FORM{d}>
<input type=hidden name=qid value='${quiz_id}_${quiz_num}_${add_ch}'>
_HTML_
for($quiz_num=0;$quiz_num<$play_max;$quiz_num++){
&question_html;
}
$main_html.='<br><br>';
&individual_html;
$midi_opt=&midi_opt($FORM{d});
$main_html.= <<"_HTML_";
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$border_color"><tr><td>
<table $tbl_opt><tr><td bgcolor='$th_color' nowrap>
<br><center><span><input type=submit value="　　送信　　">$midi_opt</span></center><br>
</td></tr></table></td></tr></table>
_HTML_
}
$main_html.='</form>';
if(($imode)&&($anstype[$quiz_index] > 0)){
$main_i_html.='</form>';
}
return 0;
}
#************************************************
# 出題table表示処理
#************************************************
sub question_html{
$quiz_index=&mondai_num($quiz_max-1);
&quiz_log_read();
local(@list)=($ans[$quiz_index],$misans1[$quiz_index],$misans2[$quiz_index],$misans3[$quiz_index],$misans4[$quiz_index]);
local(@branches);
foreach(&semirand($#list + 1)){push(@branches,$list[$_]);}
$dumy=$quiz_num+1;
if($show_auth eq 1 && $author[$quiz_index] ne ''){
$mondai_str="$mondai[$quiz_index]<div align=right>by $author[$quiz_index]</div>";
}else{
$mondai_str=$mondai[$quiz_index];
}
$main_html.= <<"_HTML_";
<hr><b><big>第$dumy問目</big></b>
<SPAN>　 $QU{play_num}人中 $QU{play_win}人正解 ($QU{win_ratio}％)　平均正解時間 $QU{ave2}秒</SPAN><br><br>
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$border_color"><tr><td>
<table $tbl_opt><tr><td bgcolor='$th_color'$nowrap>
<span>$walign1$mondai_str$walign2</span>
</td></tr>
_HTML_
$main_i_html.="第$dumy問目<br>";
$main_i_html.="$mondai[$quiz_index]<br>";
$main_html.= "<tr><td nowrap bgcolor='$td_color'>$walign1";
if($LOG{bundle} eq 1){
if($anstype[$quiz_index] > 0){&make_bundle_text_branch();}
else{&make_bundle_radio_branch();}
}elsif($anstype[$quiz_index] eq 1){&make_text_branch();}
elsif($SYS{quiz_form} eq 0 || $imode){&make_link_branch();}
elsif($SYS{quiz_form} eq 1){&make_radio_branch();}
elsif($SYS{quiz_form} eq 2){&make_button_branch();}
srand();
if((($SYS{quiz_form} eq '1')||($anstype[$quiz_index] > 0))&&($bundle < 1)){
}else{$main_html.='</table></td></tr></table>';}
$main_html.= "$walign2</td></tr></table></td></tr></table>";
return 0;
}
#************************************************
# MIDI表示処理
#************************************************
sub midi_html{
local($ret);
local($midi)=@_;
if($COOKIE{bgm} eq '' || $COOKIE{bgm} <= 0){return;}
if($midi ne ''){
$ret="<embed src='$midi' autostart=true repeat=false panel='0' width='0' height='0' type='audio/mid' >";
}
return $ret;
}
#************************************************
# MIDI表示処理
#************************************************
sub midi_opt{
local($dir)=@_;
if($result_midi[1] eq '' && $result_midi[0] eq '' && $end_midi eq '' && $high_midi eq ''){return;}
$ret='';
if($COOKIE{bgm} eq '' || $COOKIE{bgm} <= 0){
$ret.=" <input type=checkbox name=bgm value=1>効果音";
}else{
$ret.=" <input type=checkbox name=bgm value=1 checked>効果音";
}
return $ret;
}
#************************************************
# ラジオボタン型選択肢
#************************************************
sub make_radio_branch{
$add_ch=&ch_address("${quiz_num}${quiz_id}");
$main_html.=<<"_HTML_";
<table border=0 cellspacing=0 cellpadding=3 width=100%>
<form method='$method' action='$quiz_cgi' name=frm>
<input type=hidden name=passch value='$FORM{passch}'>
<input type=hidden name=qid value='${quiz_id}_${quiz_num}_${add_ch}'>
_HTML_
foreach $branch(1..5){
if($branches[$branch-1] eq ''){next;}
$main_html.=<<"_HTML_";
<tr><td width=30%><span>
<input type=radio name=a_$quiz_num value='${branch}'>　
</td><td nowrap><span>
$branches[$branch-1]
</span></td></tr>
_HTML_
}
$midi_opt=&midi_opt($FORM{d});
$main_html.=<<"_HTML_";
<tr><td colspan=2>
<br><center><span><input type=submit value="　　送信　　">$midi_opt</span></center>
</td></tr></table>
_HTML_
}
#************************************************
# テキスト入力方選択肢
#************************************************
sub make_text_branch{
$add_ch=&ch_address("${quiz_num}${quiz_id}");
$midi_opt=&midi_opt($FORM{d});
$main_html.=<<"_HTML_";
<table border=0 cellspacing=0 cellpadding=3 width=100%>
<form name=frm method='$method' action=$quiz_cgi>
<input type=hidden name=passch value='$FORM{passch}'>
<input type=hidden name=qid value='${quiz_id}_${quiz_num}_${add_ch}'>
<tr><td width=30%>
<span><input type=text name=a_$quiz_num ></span>
</td></tr>
<tr><td colspan=2>
<br><center><span><input type=submit value="　　送信　　">$midi_opt</span></center>
</td></tr></table>
${&focus_move("a_${quiz_num}")}$ret
_HTML_
$main_i_html.=<<"_HTML_";
<form name=method='$method' action=$quiz_cgi>
<input type=hidden name=passch value='$FORM{passch}'>
<input type=hidden name=qid value='${quiz_id}_${quiz_num}_${add_ch}'>
<input type=hidden name=j value='1'>
<input type=text name=a_$quiz_num >
<br><input type=submit value="　送信　">
_HTML_
}
#************************************************
# リンク型選択肢
#************************************************
sub make_link_branch{
$add_ch=&ch_address("${quiz_num}${quiz_id}");
$main_html.= "<table border=0 cellspacing=0 cellpadding=3 width=100%>";
foreach $branch(1..5){
if($branches[$branch-1] eq ''){next;}
$add_ch=&ch_address("${quiz_num}${quiz_id}");
$main_html.= <<"_HTML_";
<tr><td nowrap width=30%><span>
<a href='$quiz_cgi?a_$quiz_num=${branch}\&qid=${quiz_id}_${quiz_num}_${add_ch}'>
$branches[$branch-1]
</a></span>
</td></tr>
_HTML_
$main_i_html.= <<"_HTML_";
<a href='$quiz_cgi?a_$quiz_num=${branch}\&qid=${quiz_id}_${quiz_num}_${add_ch}&j=1'>
$branches[$branch-1]
</a><br>
_HTML_
}
$main_html.='</table>';
}
#************************************************
# ボタン型選択肢
#************************************************
sub make_button_branch{
$add_ch=&ch_address("${quiz_num}${quiz_id}");
$button_val=0;
$main_html.= <<"_HTML_";
<table border=0 cellspacing=0 cellpadding=3 width=100%>
<form method='$method' action=$quiz_cgi>
<input type=hidden name=passch value='$FORM{passch}'>
<input type=hidden name=qid value='${quiz_id}_${quiz_num}_${add_ch}'>
_HTML_
$top_branch=0;
foreach $branch(1..5){
if($branches[$branch-1] eq ''){next;}
if($top_branch ne 0){$top_branch=$branch;}
$button_val++;
$main_html.=<<"_HTML_";
<tr><td width=15%><span>
<input type=submit name='b_$branch' value='    $button_val    '>
</span></td><td$nowrap><span>
$branches[$branch-1]
</span></td></tr>
_HTML_
}
$midi_opt=&midi_opt($FORM{d});
$main_html.=<<"_HTML_";
${if($top_branch eq 0){$ret='';}else{&focus_move("b_$top_branch")}}$ret
</table><br>$midi_opt</form>
_HTML_
}
#************************************************
# ラジオボタン型選択肢(一括問題)
#************************************************
sub make_bundle_radio_branch{
$main_html.= "<table border=0 cellspacing=0 cellpadding=3 width=100%>";
foreach $branch(1..5){
if($branches[$branch-1] eq ''){next;}
$main_html.=<<"_HTML_";
<tr><td width=10%>
<span><input type=radio name='a_$quiz_num' value='$branch'>　</span>
</td><td nowrap>
<span>$branches[$branch-1]</span>
</td></tr>
_HTML_
}
$main_html.='</table>';
}
#************************************************
# テキスト入力型選択肢(一括問題)
#************************************************
sub make_bundle_text_branch{
$main_html.=<<"_HTML_";
<table border=0 cellspacing=0 cellpadding=3 width=100%>
<tr><td width=30%>
<span><input type=text name=a_$quiz_num></span>
</td></tr></table>
_HTML_
}
#************************************************
# 個人成績table
#************************************************
sub individual_html{
if($COOKIE{ck} > 0){
if($FORM{m} eq ''){$FORM{m}=1;}
$COOKIE{"S$cid"}=$COOKIE{"S$cid"}+0;
$COOKIE{"E$cid"}=$COOKIE{"E$cid"}+0;
$COOKIE{"W$cid"}=$COOKIE{"W$cid"}+0;
$COOKIE{"L$cid"}=$COOKIE{"L$cid"}+0;
$COOKIE{"A$cid"}=$COOKIE{"A$cid"}+0;
$COOKIE{"H$cid"}=$COOKIE{"H$cid"}+0;
$COOKIE{"T$cid"}=$COOKIE{"T$cid"}+0;
$COOKIE{"I$cid"}=$COOKIE{"I$cid"}+0;
if(($COOKIE{"W$cid"}+$COOKIE{"L$cid"}) > 0){
$ave=&point($COOKIE{"W$cid"}/($COOKIE{"W$cid"}+$COOKIE{"L$cid"})*100,1);
}else{$ave='0.0';}
local($s1,$m1,$h1)=&score_time($COOKIE{"T$cid"});
$cook_i=&point($COOKIE{"I$cid"},2);
$cook_a=&point($COOKIE{"A$cid"},1);
$main_html.=<<"_HTML_";
<br>
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$border_color"><tr><td>
<table $tbl_opt><tr>
<td colspan=4 bgcolor='$th_color'>
<table cellpadding=0 cellspacing=0 border=0 width=100%><tr><td><small>$LOG{name}　個人成績</small></td>
<td align=right><small>総時間 $h1時間$m1分$s1秒</small></td></tr></table>
<tr>
<td bgcolor='$td_color' nowrap><small>挑戦 $COOKIE{"S$cid"}回</small></td>
<td bgcolor='$td_color' nowrap><small>正解 $COOKIE{"W$cid"}問</small></td>
<td bgcolor='$td_color' nowrap><small>最高記録 $COOKIE{"H$cid"}問</small></td>
<td bgcolor='$td_color' nowrap><small>正解率 $ave%</small></td>
</tr><tr>
<td bgcolor='$td_color' nowrap><small>完走 $COOKIE{"E$cid"}回</small></td>
<td bgcolor='$td_color' nowrap><small>不正解 $COOKIE{"L$cid"}問</small></td>
<td bgcolor='$td_color' nowrap><small>平均記録 $cook_a問</small></td>
<td bgcolor='$td_color' nowrap><small>正解時間 $cook_i秒</small></td>
</tr></table></td></tr></table>
_HTML_
}
return 0;
}
#************************************************
# グラフ表示処理
#************************************************
sub show_graph {
local($yourscore)=@_;
local(%from,%to,%per);
$sub_max=0;
for($i=0;$i<=$HIST{hst_dev};$i++){
$from{$i}=$i*$histry_div;
$to{$i}=($i+1)*$histry_div-1;
if($to{$i}>$play_max-1){$to{$i}=$play_max;}
foreach(@score[$from{$i}..$to{$i}]){
$hst[$i]=$hst[$i]+$_;
}
if($HIST{all_hst} > 0){
$per{$i}=&point($hst[$i]*100/$HIST{all_hst},3);
}else{$per{$i}='0.000';}
if($per{$i}<$graph_border){
if($sub_max<$hst[$i]){$sub_max=$hst[$i];}
}
}
$main_html.=<<"_HTML_";
<b><span>■成績履歴グラフ■</span></b>
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$border_color"><tr><td>
<table $tbl_opt>
<tr><td nowrap colspan=2 bgcolor='$th_color'>
$walign1総挑戦者数 $HIST{all_hst}人　
平均 $HIST{average}問正解　
標準偏差 $HIST{hyouhen}$walign2
</td></tr>
_HTML_
for($i=0;$i<=$HIST{hst_dev};$i++){
local($font_tag1,$font_tag2,$gif_file)=();
$gif_file=$SYS{b_gif};
if(($yourscore ne '')
&&($yourscore>=$i*$histry_div)
&&($yourscore<($i+1)*$histry_div)){
$gif_file=$SYS{a_gif};
$font_tag1="<font color=red>";
$font_tag2='</font>';
}
if($sub_max ne 0){
$width=int($hst[$i]/$sub_max*$graph_w);
}else{$width=0;}
$shortImg = "<img src='$gif_file' width='5' height='$graph_h'>";
$img = '';
if($hst[$i] ne 0){
if($per{$i} >= $graph_border){
$img ="<img src='$gif_file' width='$graph_w' height='$graph_h'>";
$img.="$shortImg $shortImg $shortImg";
}else{
$img ="<img src='$gif_file' width='$width' height='$graph_h'>";
}
}
$main_html.=<<"_HTML_";
<tr><td bgcolor='$td_color' nowrap>$font_tag1$from{$i}～$to{$i}問正解$font_tag2</td>
<td bgcolor='$td_color' nowrap>$img　 $font_tag1$hst[$i]人($per{$i} \%)$font_tag2</td></tr>
_HTML_
}
$main_html.="</table></td></tr></table><small>【偏差値＝（得点－平均）／標準偏差×１０＋５０)】</small><br>";
}
#************************************************
# ログ表示処理
#************************************************
sub highscore_html {
local(@lines);
if(($num_limit eq '0')||($day_limit eq '0')){
$main_html.='<br>このクイズは、高成績者リストは使用していません。<br><br><br>';
$main_i_html.='<br>このクイズは、高成績者リストは使用していません。<br><br>';
return;
}
$date_now=&time_set($now);
if($high_back_day > 0){
&backup_file("$FORM{d}/${high_cgi}.cgi",$high_back_w,$high_back_day);
}
open(DB,"$FORM{'d'}/${high_cgi}.cgi");
@lines = <DB>;
close(DB);
$grade=0;
$tai=0;
$mass=0;
$linewin=0;
$mobile_num=0;
foreach $line (@lines){
$line=~ s/\n//g;
if($line eq ''){next;}
if(&highscore_read($line)){next;}
$linewin++;
if(($HIGH{lasthigh} eq $HIGH{high})&&(($SYS{'time'} eq 0)||($HIGH{lastlap} eq $HIGH{lap}))){
$tai++;
}else{
$grade=$grade+$tai+1;
$tai=0;
}
$HIGH{grade}=$grade;
$HIGH{grade_h}=$grade;
if($COOKIE{N} eq $HIGH{name}){
&log_highlight('<b>','</b>');
$HIGH_I{grade}=$HIGH{grade};
}
if($linewin <= $no_limit){
&log_highlight("<font color='$champ_color'>",'</font>');
}
$mass=$mass+$HIGH{high};
if(($HIGH{lap} ne '')&&($HIGH{high} > 0)){
$ave_time_ave_sum = $ave_time_ave_sum + $HIGH{lap} / $HIGH{high};
$ave_time_ave_num++;
}
if($rec_com eq 1){$td_com="<td bgcolor='$td_color' nowrap>$HIGH{com_h}　</td>";}
else{$td_com="";}
if($HIGH{imode} ne ''){$mobile_num++;}
push(@log,<<"_HTML_");
<tr>
<td bgcolor='$td_color'><div align=right>$HIGH{grade_h} </div></td>
<td bgcolor='$td_color' nowrap>$HIGH{day2_h}</td>
<td bgcolor='$td_color'><pre><div align=right>$HIGH{high_h} </div></td>
<td bgcolor='$td_color' nowrap>$HIGH{lap2_h}$HIGH{ave_h}</td>
<td bgcolor='$td_color' nowrap>$HIGH{name_h}</td>
<td bgcolor='$td_color' nowrap>$HIGH{imode_h}　</td>
$td_com
</tr>
_HTML_
if(! $imode || $linewin <= $high_i){
push(@log_i,<<"_HTML_");
$HIGH{grade}位　 $HIGH{day2}　 $HIGH{high}問正解　 $HIGH{name}$HIGH{imode}<br>
_HTML_
}
}
if($ave_time_ave_num > 0){
$ave_time_ave = ' ('.&point($ave_time_ave_sum/$ave_time_ave_num,2).'秒/問)';
}else{$ave_time_ave = '';}
if($linewin > 0){
$ave=&point($mass/$linewin,1);
}else{
$ave=0;
$linewin=0;
}
if($day_limit eq ''){
$day_limit_mes = '無制限';
}else{
$day_limit_mes = "過去$day_limit日間";
}
if($num_limit eq ''){
$num_limit_mes = '無制限';
}else{
$num_limit_mes = "上位$num_limit人";
}
if($no_limit > 0){
$no_limit_mes = "上位 $no_limit人の記録は上記の制限を受けません。";
}
$main_html.= <<"_HTML_";
<br><span><b>■$_high情報■</b></span>
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$border_color"><tr><td>
<table $tbl_opt>
<tr>
<td nowrap bgcolor='$th_color' width=20%><small>現在時刻</small></td>
<td nowrap bgcolor='$td_color'><small>$walign1$date_now$walign2</small></td>
</tr>
<tr>
<td bgcolor='$th_color'><small>総人数</small></td>
<td nowrap bgcolor='$td_color'><small>$walign1$linewin人(内携帯$mobile_num人)$walign2</small></td>
</tr>
<tr>
<td bgcolor='$th_color' nowrap><small>高成績者平均</small></td>
<td nowrap bgcolor='$td_color'><small>$walign1$ave問$ave_time_ave$walign2</small></td>
</tr>
<tr>
<td bgcolor='$th_color'><small>記録期間</small></td>
<td nowrap bgcolor='$td_color'><small>$walign1$day_limit_mes$walign2</small></td></tr>
<tr>
<td bgcolor='$th_color'><small>記録人数</small></td>
<td nowrap bgcolor='$td_color'><small>$walign1$num_limit_mes$walign2</small></td>
</tr>
<tr>
<td bgcolor='$th_color'><small>殿堂入り</small></td>
<td nowrap bgcolor='$td_color'><small>$walign1上位 $no_limit人の記録は上記の制限を受けません。$walign2</small></td>
</tr>
</table>
</td></tr></table>
_HTML_
if($linewin <= 0){
&error(761);
}else{
if($rec_com eq 1){
$th_com="<td nowrap bgcolor='$th_color'>コメント</td>";
}
$main_html.= <<"_HTML_";
<br><br>
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$border_color"><tr><td>
<table $tbl_opt>
<tr>
<td nowrap bgcolor='$th_color'>順位</td>
<td nowrap bgcolor='$th_color'><center>日付</center></td>
<td nowrap bgcolor='$th_color'>正解数</td>
<td nowrap bgcolor='$th_color'>回答時間(１問平均)</td>
<td nowrap bgcolor='$th_color'>名前</td>
<td nowrap bgcolor='$th_color'>携帯</td>
$th_com
</tr>
@log
</table></td></tr></table>
_HTML_
if($HIGH_I{grade} ne '' && $FORM{id} ne ''){
$main_i_html.= <<"_HTML_";
あなたの記録は、第$HIGH_I{grade}位で記録されました。<br><br>
_HTML_
}
$linewin_i=$linewin;
if($linewin_i > $high_i){
$linewin_i=$high_i;
}
$main_i_html.= <<"_HTML_";
■高記録一覧■<br>
全$linewin人中 上位$linewin_i人表\示<br>
@log_i
_HTML_
}
}
#************************************************
# ハイスコア読み込み処理
#************************************************
sub highscore_read{
local($log)=@_;
$HIGH{lasthigh}=$HIGH{high};
$HIGH{lastlap}=$HIGH{lap};
($HIGH{day}
,$HIGH{high}
,$HIGH{name}
,$HIGH{host}
,$HIGH{lap}
,$HIGH{com}
,$HIGH{imode}
) = split(/\t/,$log);
if($HIGH{imode} eq '1'){
$HIGH{imode} = '(携)';
}else{
$HIGH{imode} = '';
}
$HIGH{day2}=&time_set($HIGH{day});
if($HIGH{lap} ne ''){
local($s,$m)=&score_time($HIGH{lap});
$HIGH{lap2}="$m分$s秒";
}else{
$HIGH{lap2}="--------";
}
if($HIGH{high} > 0 || $HIGH{lap} ne ''){
$HIGH{ave}="(".&point($HIGH{lap}/$HIGH{high},2)."秒)";
}else{
$HIGH{ave}='(----)';
}
$HIGH{day2_h}  =$HIGH{day2};
$HIGH{high_h}=$HIGH{high};
$HIGH{name_h}=$HIGH{name};
$HIGH{host_h}=$HIGH{host};
$HIGH{lap_h}=$HIGH{lap};
$HIGH{com_h}=$HIGH{com};
$HIGH{imode_h}=$HIGH{imode};
$HIGH{lap2_h}=$HIGH{lap2};
$HIGH{ave_h}=$HIGH{ave};
$HIGH{grade_h} =$HIGH{grade};
if($HIGH{day} eq '' || $HIGH{high} eq '' || $HIGH{name} eq ''){return 1;}
else{return 0;}
}
#************************************************
# スコアハイライト処理
#************************************************
sub log_highlight{
local($tag1,$tag2)=@_;
$HIGH{day2_h}  ="$tag1$HIGH{day2}$tag2";
$HIGH{high_h}="$tag1$HIGH{high}$tag2";
$HIGH{name_h}="$tag1$HIGH{name}$tag2";
$HIGH{host_h}="$tag1$HIGH{host}$tag2";
$HIGH{lap_h}="$tag1$HIGH{lap}$tag2";
$HIGH{com_h}="$tag1$HIGH{com}$tag2";
$HIGH{imode_h}="$tag1$HIGH{imode}$tag2";
$HIGH{lap2_h}="$tag1$HIGH{lap2}$tag2";
$HIGH{ave_h}="$tag1$HIGH{ave}$tag2";
$HIGH{grade_h} ="$tag1$HIGH{grade}$tag2";
}
#************************************************
# ログ書き込み処理
#************************************************
sub log_write {
if(($day_limit eq '0')||($num_limit eq '0')){
&error(641);
return 1;
}
&play_log_read($FORM{id});
if($FORM{check} ne &ch_address("$FORM{id}$LOG{win}")){&error(605);return 1;}
if($rec_com ne 1){$FORM{com}='';}
if($LOG{write} ne ''){
&error(631);return 1;
}elsif($FORM{EntryName} eq ''){
&error(210,'エントリーネーム');
return 1;
}elsif(length($FORM{EntryName}) > $max_en){
&error(501,'エントリーネーム');
return 1;
}elsif(length($FORM{com}) > $max_com){
&error(511,'コメント');
return 1;
}else{
open(DB,"$FORM{d}/$high_cgi\.cgi");
@lines = <DB>;
close(DB);
$value = join("\t",time,$LOG{win},$FORM{EntryName},$id,$LOG{lap}-$LOG{'time'},$FORM{com},$imode);
$line_num=0;
foreach $line (@lines){
$line=~ s/\n//g;
if($line =~ /^date/){next;}
if($line eq ''){next;}
&highscore_read($line);
local($day,$high,$name,$host,$time,$com) = split(/\t/,$line);
if($double_high ne 1){
if($id eq $HIGH{host} && $HIGH{high} eq $LOG{win}){&error(611);return 1;}
}
if($wrwin ne 1){
if(($HIGH{high} < $LOG{win}) || ($HIGH{high} == $LOG{win}) && (($HIGH{lap} >= $LOG{lap}-$LOG{'time'}) || ($HIGH{lap} eq ''))){
push(@new,$value);
$wrwin=1;
$blink1{$line_num}='<blink>';
$blink2{$line_num}='</blink>';
$line_num++;
}
}
if($line_num >= $no_limit){
if($day_limit > 0){
if($now > $HIGH{day}+$day_limit*60*60*24){next;}
}
if($num_limit > 0){
if($line_num >= $num_limit-1){last;}
}
}
push(@new,$line);
$line_num++;
if(($line_num >= $no_limit)&&($num_limit > 0)&&($line_num >= $num_limit)){last;}
}
if(($wrwin eq '')&&(($line_num < $num_limit)||($num_limit eq ''))){
push(@new,$value);
$wrwin=1;
$blink1{$line_num}='<blink>';
$blink2{$line_num}='</blink>';
}
if($wrwin ne ''){
if(&ch_dir_exist('ディレクトリ名',$FORM{d})){return 1;}
if(&ch_lock("$FORM{d}/$high_cgi\.lock",10) ne 1){
&file_lock("$FORM{d}/$high_cgi\.lock");
my($ret)=&write_file("$FORM{d}/$high_cgi\.cgi",join("\n",@new));
&file_unlock("$FORM{d}/$high_cgi\.lock");
if($ret){return 1;}
}else{
return 1;
}
$value=join("\t",$LOG{num},$LOG{win},$LOG{lose},$LOG{seed},$LOG{old},1,$FORM{EntryName},$LOG{'time'},$LOG{lap},$LOG{last_lap},$LOG{genre},$LOG{mode},$LOG{ck_s},$LOG{ck_n},$LOG{bundle},"\n");
if(&ch_dir_exist('ディレクトリ名',$data_dir)){return 1;}
if(&write_file("$data_dir/$header$FORM{id}\.cgi",($value,@lines2))){return 1;}
}else{&error(621);return 1;}
}
return 0;
}
