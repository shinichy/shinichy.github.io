#!/usr/bin/perl
$version='2.03';
#------------------------------------------------
#ファイル名：index.cgi
#説明：クイズのページのメニューページとなるページです。
#------------------------------------------------
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
if($SYS{top_back_color} eq ''){$SYS{top_back_color}='#ddddff';}
if($SYS{main_title} eq ''){$SYS{main_title}='無題';}
if($SYS{top_wall} ne ''){$wall_paper = " background='$SYS{top_wall}'"}
if($SYS{text_color} ne ''){$text=" text='$SYS{text_color}'";}
if($SYS{link_color} ne ''){$link=" link='$SYS{link_color}'";}
if($SYS{vlink_color} ne ''){$vlink=" vlink='$SYS{vlink_color}'";}
$SYS{header}=~ s/\$title/$SYS{main_title}/g;
$SYS{header}=~ s/\$top/\[<a href="$SYS{top_url}">$_top<\/a>\] /g;
$SYS{header}=~ s/\$quiz_op/\[<a href="$quiz_op_cgi">管理人室<\/a>\] /g;
$SYS{header}=~ s/\$imode/\[<a href="$index_cgi?j=1">$_imode<\/a>\] /g;
$header_html=<<"_HTML_";
<html><head><STYLE Type="text/css">$style</STYLE>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=x-sjis">
<title>$SYS{main_title}</title></head>
<BODY$text$link$vlink bgcolor="$SYS{top_back_color}"$wall_paper>
$SYS{header}<br><br>
_HTML_
$headr_i_html=<<"_HTML_";
<html><head>
<title>$SYS{main_title}</title></head>
<body>
_HTML_
}
#************************************************
# メインプログラム
#************************************************
sub main{
&setup;
if(&ch_sys_lock){&busy_html;}
elsif(&ch_guard_ip){&guard_html;}
else{
&sys_read;
&all_design_read;
&all_genre_read;
$com_color=$SYS{top_info_color};
&get_cookie;
if(!&buf_read){
if($FORM{type} eq 'cont'){
&contribute;
&footer_html;
&output;
}elsif(($FORM{ck} eq 1)||($FORM{ck} eq 0)){
$COOKIE{ck}=$FORM{ck};
&set_cookie;
}elsif($FORM{ck} eq 2){
undef %COOKIE;
$COOKIE{ck}=1;
&set_cookie;
}elsif(($FORM{bgm} eq 1)||($FORM{bgm} eq 0)){
$COOKIE{bgm}=$FORM{bgm};
&set_cookie;
}
}
&header_html;
&top_html;
&top_i_html;
&footer_html;
$footer_i_html=<<"_HTML_";
<br><a href=$index_cgi?&j=1>一覧</a><br>
</body></html>
_HTML_
}
if($imode){&output_i;}
else{&output;}
}
#************************************************
# ジャンル表示
#************************************************
sub top_html{
local($i);
$i=0;@out=();
$all_play_num=0;$all_play_win=0;$all_mindai=0;$play_rate=0;
if($#genre_dir_available <0){&error(681);return;}
if($SYS{top_message} ne ''){
if($SYS{top_table} ne ''){
$main_html=<<"_HTML_";
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$SYS{top_border_color}"><tr><td>
<table $top_tbl_opt><tr><td$nowrap bgcolor="$SYS{top_info_color}">
<small>$SYS{top_message}</small>
</td></tr></table></td></tr></table><br><hr>
_HTML_
}else{$main_html.="<small>$SYS{top_message}</small><hr>";}
}
$main_html.=&personal_button_html();
$all_flag=0;
if($SYS{easy} eq 1 || $SYS{easy} eq 0){
foreach $dir(@genre_dir_all){
if($mondai_cgi{$dir} ne '.'){&cal_genre_pal($dir);}
}
}
if($SYS{easy} ne 0 && $SYS{easy} ne 1 && $SYS{easy} ne 2){
&listup_html();
}else{
foreach $dir(@genre_dir_available){
&lineup_html($dir);
}
}
}
#************************************************
# ジャンル表示(携帯用)
#************************************************
sub top_i_html{
if($FORM{d} eq ''){
$main_i_html="□$SYS{main_title}□<br><br>";
foreach(@genre_dir_available){
if($bundle1{$_} eq 1 && $bundle2{$_} eq 1 ){next;}
$main_i_html.="<a href=$index_cgi?d=$_&j=1>$title{$_}</a><br>";
}
}elsif($FORM{m} eq ''){
$main_i_html="○$title{$FORM{d}}○<br><br>";
if($bundle1{$FORM{d}} ne 1){
$main_i_html.="<a href=$quiz_cgi?d=$FORM{d}\&m=1&j=1>$mode_name1{$FORM{d}}</a><br>";
}
if(($mode_name2{$FORM{d}} ne '') && ($bundle2{$FORM{d}} ne 1)){
$main_i_html.= "<a href=$quiz_cgi?d=$FORM{d}\&m=2&j=1>$mode_name2{$FORM{d}}</a><br>";
}
if(($num_limit1{$FORM{d}} ne '0') && ($day_limit1{$FORM{d}} ne '0') && ($bundle1{$FORM{d}} ne 1)){
$main_i_html.= "<br><a href=$quiz_cgi?d=$FORM{d}\&m=1&j=1&h=1>$mode_name1{$FORM{d}}高成績者</a><br>";
}
if(($mode_name2{$FORM{d}} ne '') && ($num_limit1{$FORM{d}} ne '0') && ($day_limit1{$FORM{d}} ne '0') && ($bundle2{$FORM{d}} ne 1)){
$main_i_html.= "<a href=$quiz_cgi?d=$FORM{d}\&m=2&j=1&h=1>$mode_name2{$FORM{d}}高成績者</a><br>";
}
}
}
#************************************************
# ジャンルの設定などを計算し、%GENRE_CALに格納
#************************************************
sub cal_genre_pal{
$dir=$_[0];
if($mente{$dir} ne 1){next;}
&refresh_quiz;
&quiz_read($dir);
$mondai=$#mondai+1;
($mass1,$clear1,$clear_per1,$ave1,$high1,$quiz_max1,$play_max1,$lose_max1)=&cal($dir,$scorehst_cgi1{$dir},$high_cgi1{$dir},$play_max1{$dir},$lose_max1{$dir},$high_border1{$dir},$quiz_max1{$dir},$mondai);
($mass2,$clear2,$clear_per2,$ave2,$high2,$quiz_max2,$play_max2,$lose_max2)=&cal($dir,$scorehst_cgi2{$dir},$high_cgi2{$dir},$play_max2{$dir},$lose_max2{$dir},$high_border2{$dir},$quiz_max2{$dir},$mondai);
$play_num=0;$play_win=0;$play_rate=0;
if($play_max1>$play_max2){$play_max=$play_max1;}
else{$play_max=$play_max2;}
if($SYS{easy} eq 0){
for($quiz_index=0;$quiz_index<$play_max;$quiz_index++){
if(open(DB,"$dir/$quiz_header$quiz_index\.cgi")){
@new= <DB>;close(DB);
@qu=(0,0,0,0,0);
@qu = split(/\t/, $new[0]);
foreach $qu(@qu){$play_num{$dir}[$quiz_index]=$play_num{$dir}[$quiz_index]+$qu;$i++;}
$play_win{$dir}[$quiz_index]=$play_win{$dir}[$quiz_index]+$qu[0];
}
}
}
$GENRE_CAL{$dir}=join("\t",$mondai,$mass1,$clear1,$clear_per1,$ave1,$high1,$quiz_max1,$play_max1,$lose_max1,$mass2,$clear2,$clear_per2,$ave2,$high2,$quiz_max2,$play_max2,$lose_max2);
}
#************************************************
# ジャンルの設定などを計算し、%GENRE_CALに格納
#************************************************
sub lineup_html{
$dir=$_[0];
@dir=();
undef %quiz_num;
if($mondai_cgi{$dir} eq '.'){
foreach(@genre_dir_all){if($mondai_cgi{$_} ne '.'){push(@dir,$_);}}
}elsif($mondai_cgi{$dir} =~ /\//){
@mondai_dat=split(/\t/,$mondai_cgi{$dir});
foreach(@mondai_dat){
local($d,$val)=split(/\//,$_);
push(@dir,$d);
if($val eq 'all'){$val ='';}
$quiz_num{$d}=$val;
}
}else{@dir=($dir);}
($all_play_num,$all_play_win,$all_mondai)=();
foreach(@dir){
($mondai,$mass1,$clear1,$clear_per1,$ave1,$high1,$quiz_max1,$play_max1,$lose_max1,$mass2,$clear2,$clear_per2,$ave2,$high2,$quiz_max2,$play_max2,$lose_max2)=split(/\t/,$GENRE_CAL{$_});
if(($mondai > $quiz_num{$_})&&($quiz_num{$_} ne '')){$mondai = $quiz_num{$_};}
$all_mondai=$all_mondai+$mondai;
for($i=0;$i<$mondai;$i++){
$all_play_num=$all_play_num+$play_num{$_}[$i];
$all_play_win=$all_play_win+$play_win{$_}[$i];
}
}
($mass1,$clear1,$clear_per1,$ave1,$high1,$quiz_max1,$play_max1,$lose_max1)=&cal($dir,$scorehst_cgi1{$dir},$high_cgi1{$dir},$play_max1{$dir},$lose_max1{$dir},$high_border1{$dir},$quiz_max1{$dir},$all_mondai);
($mass2,$clear2,$clear_per2,$ave2,$high2,$quiz_max2,$play_max2,$lose_max2)=&cal($dir,$scorehst_cgi2{$dir},$high_cgi2{$dir},$play_max2{$dir},$lose_max2{$dir},$high_border2{$dir},$quiz_max2{$dir},$all_mondai);
$COOKIE{"S1$dir"}=$COOKIE{"S1$dir"}+0;$COOKIE{"S2$dir"}=$COOKIE{"S2$dir"}+0;
$COOKIE{"E1$dir"}=$COOKIE{"E1$dir"}+0;$COOKIE{"E2$dir"}=$COOKIE{"E2$dir"}+0;
$COOKIE{"H1$dir"}=$COOKIE{"H1$dir"}+0;$COOKIE{"H2$dir"}=$COOKIE{"H2$dir"}+0;
$COOKIE{"A1$dir"}=$COOKIE{"A1$dir"}+0;$COOKIE{"A2$dir"}=$COOKIE{"A2$dir"}+0;
$cook_a1=&point($COOKIE{"A1$dir"},1);
$cook_a2=&point($COOKIE{"A2$dir"},1);
$iplay_max1=$COOKIE{"W1$dir"}+$COOKIE{"L1$dir"};
$iplay_max2=$COOKIE{"W2$dir"}+$COOKIE{"L2$dir"};
if($iplay_max1 > 0){$iave1=&point($COOKIE{"W1$dir"}/$iplay_max1*100,1);}else{$iave1='0.0';}
if($iplay_max2 > 0){$iave2=&point($COOKIE{"W2$dir"}/$iplay_max2*100,1);}else{$iave2='0.0';}
if(!mygrep($dir,@genre_dir_orign) || $cont{$dir} ne 1){
$add_link='';
}else{
$add_link="[<a href=$quiz_cgi?d=$dir\&add=1>$_add</a>]";
}
if($all_play_num eq ''){$all_play_num=0;}
if($all_play_win eq ''){$all_play_win=0;}
if($all_play_num > 0){$play_rate=&point($all_play_win*100/$all_play_num,1);}
else{$play_rate=&point(0,1);}
if(($quiz_max1 eq 0)&&($SYS{easy} eq 0 || $SYS{easy} eq 1)){$chalenge1="\[$_underconst\]";}
else{$chalenge1="\[<a href=$quiz_cgi?d=$dir\&m=1>$_try</a>\]";}
if(($quiz_max2 eq 0)&&($SYS{easy} eq 0 || $SYS{easy} eq 1)){$chalenge2="\[$_underconst\]";}
else{$chalenge2="\[<a href=$quiz_cgi?d=$dir\&m=2>$_try</a>\]";}
if($mode_name2{$dir} eq '' && $top_comment{$dir} eq ''){
$top_colspan=' colspan=2';
}else{
$top_colspan=' colspan=4';
}
$main_html.=<<"_HTML_";
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$SYS{top_border_color}"><tr><td>
<table $top_tbl_opt>
<tr><td$top_colspan bgcolor="$SYS{top_genre_color}">
<table border=0 width="100%" cellpadding=0 cellspacing=0>
<tr><td$nowrap><b><span>$title{$dir}</span></b></td>
_HTML_
if($SYS{easy} eq 0){$main_html.="<td nowrap><small>総出題数 : $all_play_num 問　正答率 : $play_rate ％</small></td>";}
$main_html.="<td align=right><small>$add_link\[<a href=$quiz_cgi?d=$dir\&s=1>$_score</a>\]</small></td>";
if($mode_name2{$dir} ne ''){
$main_html.=<<"_HTML_";
</tr></table></td></tr>
${if($top_comment{$dir} ne ''){$ret="<tr><td colspan=4 bgcolor='$SYS{top_com_color}'$nowrap><small>$top_comment{$dir}</small></td></tr>";}else{$ret='';}}$ret
<tr><td colspan=2 bgcolor="$SYS{top_table_color}"$nowrap><small>$mode_name1{$dir}</small></td><td colspan=2 bgcolor="$SYS{top_table_color}"$nowrap><small>$mode_name2{$dir}</small></td></tr>
<tr><td colspan=2 bgcolor="$SYS{top_table_color}" nowrap><small>$chalenge1\[<a href=$quiz_cgi?h=1&d=$dir&m=1>$_high</a>][<a href=$quiz_cgi?d=$dir&g=1&m=1>$_graph</a>]</small></td>
<td colspan=2 bgcolor="$SYS{top_table_color}" nowrap><small>$chalenge2\[<a href=$quiz_cgi?h=1&d=$dir&m=2>$_high</a>][<a href=$quiz_cgi?d=$dir&g=1&m=2>$_graph</a>]</small></td></tr>
_HTML_
if($SYS{easy} eq 0 || $SYS{easy} eq 1){
$main_html.=<<"_HTML_";
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>問題数 : $quiz_max1 問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>挑戦者 : $mass1 人</small></td>
<td bgcolor="$SYS{top_table_color}" nowrap><small>問題数 : $quiz_max2 問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>挑戦者 : $mass2 人</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>出題数 : $play_max1 問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>合格者 : $clear1 人</small></td>
<td bgcolor="$SYS{top_table_color}" nowrap><small>出題数 : $play_max2 問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>合格者 : $clear2 人</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>終了条件 : $lose_max1 問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>合格率 ： $clear_per1 ％</small></td>
<td bgcolor="$SYS{top_table_color}" nowrap><small>終了条件 : $lose_max2 問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>合格率 ： $clear_per2 ％</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>合格基準 : $high_border1{$dir} ％</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>平均点 ： $ave1 問</small></td>
<td bgcolor="$SYS{top_table_color}" nowrap><small>合格基準 : $high_border2{$dir} ％</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>平均点 ： $ave2 問</small></td></tr>
<tr>$high1$high2</tr>
_HTML_
}
if($COOKIE{ck} > 0){
$main_html.=<<"_HTML_";
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>個人挑戦 : $COOKIE{"S1$dir"}回</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>個人完走 : $COOKIE{"E1$dir"}回</small></td>
<td bgcolor="$SYS{top_table_color}" nowrap><small>個人挑戦 : $COOKIE{"S2$dir"}回</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>個人完走 : $COOKIE{"E2$dir"}回</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>個人出題 : $iplay_max1問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>個人最高 : $COOKIE{"H1$dir"}問</small></td>
<td bgcolor="$SYS{top_table_color}" nowrap><small>個人出題 : $iplay_max2問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>個人最高 : $COOKIE{"H2$dir"}問</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>個人正解率 : $iave1％</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>個人平均 : $cook_a1問</small></td>
<td bgcolor="$SYS{top_table_color}" nowrap><small>個人正解率 : $iave2％</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>個人平均 : $cook_a2問</small></td></tr>
_HTML_
}
$main_html.='</table></td></tr></table><br><br>';
}else{
if($COOKIE{ck} > 0){$rowspan=10;}else{$rowspan=7;}
if($top_comment{$dir} ne ''){
$top_com="<td nowrap colspan=2 rowspan='$rowspan' width=50% bgcolor='$SYS{top_com_color}'>$top_comment{$dir}</td>";
}else{
$top_com='';
}
$main_html.=<<"_HTML_";
</tr></table></td></tr>
<tr><td colspan=2 bgcolor="$SYS{top_table_color}" nowrap>$mode_name1{$dir}</td>
$top_com
</tr>
<tr><td colspan=2 bgcolor="$SYS{top_table_color}" nowrap>$chalenge1\[<a href=$quiz_cgi?h=1&d=$dir&m=1>$_high</a>][<a href=$quiz_cgi?d=$dir&g=1&m=1>$_graph</a>]</td></tr>
_HTML_
if($SYS{easy} eq 0 || $SYS{easy} eq 1){
$main_html.=<<"_HTML_";
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>問題数 : $quiz_max1 問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>挑戦者 : $mass1 人</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>出題数 : $play_max1 問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>合格者 : $clear1 人</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>終了条件 : $lose_max1 問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>合格率 ： $clear_per1 ％</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>合格基準 : $high_border1{$dir} ％</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>平均点 ： $ave1 問</small></td></tr>
<tr>$high1</tr>
_HTML_
}
if($COOKIE{ck} > 0){
$main_html.=<<"_HTML_";
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>個人挑戦 : $COOKIE{"S1$dir"}回</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>個人完走 : $COOKIE{"E1$dir"}回</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>個人出題 : $iplay_max1問</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>個人最高 : $COOKIE{"H1$dir"}問</small></td></tr>
<tr><td bgcolor="$SYS{top_table_color}" nowrap><small>個人正解率 : $iave1％</small></td><td bgcolor="$SYS{top_table_color}" nowrap><small>個人平均 : $cook_a1問</small></td></tr>
_HTML_
}
$main_html.='</table></td></tr></table><br><br>';
}
}
#************************************************
# 一覧形式メニューの表示
#************************************************
sub listup_html{
local(%list_title,%list_mode1,%list_mode2,%list_com,$mode2_flg,$com_flg);
foreach $dir(@genre_dir_available){
$list_mode1{$dir}="\[<a href=$quiz_cgi?d=$dir\&m=1>$mode_name1{$dir}</a>]";
if($mode_name2{$dir} eq ''){
$list_mode2{$dir}='　';
}else{
$mode2_flg=1;
$list_mode2{$dir}="\[<a href=$quiz_cgi?d=$dir\&m=2>$mode_name2{$dir}</a>]";
}
if($top_comment{$dir} eq ''){
$list_com{$dir}='　';
}else{
$com_flg=1;
$list_com{$dir}=$top_comment{$dir};
}
}
$main_html.=<<"_HTML_";
<table width="80%" border=0 cellpadding=0 cellspacing=0 bgcolor="$SYS{top_border_color}"><tr><td>
<table $top_tbl_opt>
_HTML_
foreach $dir(@genre_dir_available){
$main_html.=<<"_HTML_";
<tr>
<td$nowrap bgcolor="$SYS{top_genre_color}"><b><span>$title{$dir}</span></b></td>
<td$nowrap bgcolor="$SYS{top_table_color}"><span>\[<a href=$quiz_cgi?d=$dir\&m=1>$mode_name1{$dir}</a>\]</span></td>
_HTML_
if($mode2_flg eq 1){
$main_html.="<td$nowrap bgcolor=\"$SYS{top_table_color}\"><span>$list_mode2{$dir}</span></td>";
}
if($com_flg eq 1){
$main_html.="<td$nowrap bgcolor=\"$SYS{top_table_color}\"><span>$list_com{$dir}</span></td>";
}
$main_html.='</tr>';
_HTML_
}
$main_html.='</table></td></tr></table><br><br>';
}
#************************************************
# 個人成績表示ボタン
#************************************************
sub personal_button_html{
local($ret);
$ret=<<"_HTML_";
<table border=0 cellpadding=0 cellspacing=0 bgcolor="$SYS{top_border_color}"><tr><td>
<table $top_tbl_opt>
<form method="$method" action="$index_cgi">
<td bgcolor="$SYS{top_table_color}">
_HTML_
if($COOKIE{bgm} > 0){
$ret.=<<"_HTML_";
<input type=hidden name=bgm value=0>
<input type=submit value='効果音無'></td></form>
_HTML_
}else{
$ret.=<<"_HTML_";
<input type=hidden name=bgm value=1>
<input type=submit value='効果音付'>
_HTML_
}
$ret.='</td></form>';
$ret.="<form method='$method' action='$index_cgi'><td bgcolor='$SYS{top_table_color}'>";
if($COOKIE{ck} > 0){
$ret.=<<"_HTML_";
<input type=hidden name=ck value=0>
<input type=submit value='個人記録非表\示'></td></form>
<form method="$method" action="$index_cgi"><td bgcolor="$SYS{top_table_color}">
<input type=hidden name=ck value=2>
<input type=submit value='個人記録消去'>
_HTML_
}else{
$ret.=<<"_HTML_";
<input type=hidden name=ck value=1>
<input type=submit value='個人記録表\示'>
_HTML_
}
$ret.='</td></form>';
$ret.='</tr></table></td></tr></table><br>';
return $ret;
}
#************************************************
# 各種計算
#************************************************
sub cal{
local($high,$mass,$clear,$ave);
local($dir,$scorehst,$highcgi,$play_max,$lose_max,$high_border,$quiz_max,$mondai)=@_;
if($quiz_max eq ''){$quiz_max = $mondai;}
elsif($quiz_max > $mondai){$quiz_max = $mondai;}
if($play_max eq ''){$play_max = $quiz_max;}
elsif($play_max > $quiz_max){$play_max = $quiz_max;}
if($lose_max eq ''){$lose_max = $play_max;}
elsif($lose_max > $play_max){$lose_max = $play_max;}
open(DB,"$dir/$scorehst\.cgi");local(@list)=<DB>;close(DB);
local(@score);
if($list[0]=~ /^date/){@score=@list[1..$#list];}
else{@score=@list;}
$mass=0;$clear=0;$ave=0;$per=0;
foreach ($k=0;$k<=$play_max;$k++){
$mass=$mass+$score[$k];
if($play_max >0){
$syutu=$k+$lose_max;
if($syutu > $play_max){$syutu=$play_max;}
if($syutu >0){if($high_border <= $k*100/$syutu){$clear=$clear+$score[$k];}}
$xxx=$k*100/$syutu;
}
$ave=$ave+$score[$k]*$k;
}
$clear_per=0;
if($mass >0){
$clear_per=&point($clear*100/$mass,1);
$ave=&point($ave/$mass,1);
}else{$clear_per=0;$ave=0;}
$high='';$day='';$name='';
open(DB,"$dir/$highcgi\.cgi");local(@lines)=<DB>;close(DB);
if($lines[0]=~ /^date/){($day,$high,$name,$host,$time,$com) = split(/\t/,$lines[1]);}
else{($day,$high,$name,$host,$time,$com) = split(/\t/,$lines[0]);}
$day=&time_set($day);
if($name eq ''){$name='----';}
if($high eq ''){$high='0';}
$high="<td colspan=2 bgcolor='$SYS{top_high_color}'><small>Top：[$name] $high問正解</small></td>";
return ($mass,$clear,$clear_per,$ave,$high,$quiz_max,$play_max,$lose_max);
}
