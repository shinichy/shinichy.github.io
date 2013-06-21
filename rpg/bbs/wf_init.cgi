#┌─────────────────────────────────
#│  Web Forum v4.07 (2002/09/27)
#│  Copyright(C) KENT WEB 2002
#│  webmaster@kent-web.com
#│  http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'Web Forum v4.07';
#┌─────────────────────────────────
#│[ 注意事項 ]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────
#
# [設置例] かっこ内はパーミッション
#
#    public_html / index.html (ホームページ)
#       |
#       +-- bbs / wforum.cgi   [755]
#            |    wf_regi.cgi  [755]
#            |    wf_admin.cgi [755]
#            |    wf_init.cgi  [644]
#            |    wf_log.cgi   [666]
#            |    jcode.pl     [644]
#            |    fold.pl      [644]
#            |    pastno.dat   [666] ... (過去ログ用)
#            |    note.html
#            |    title.gif
#            |
#            +-- past [777] / 0001.cgi [666] ... (過去ログ用)
#            |
#            +-- lock [777] /
#

#------------#
#  基本設定  #
#------------#

# 掲示板タイトル名
$title = "ゲーム攻略掲示板";

# タイトルの色
$t_color = "#004080";

# タイトルのサイズ
$t_point = '18pt';

# タイトル／本文の文字タイプ
$t_face = 'MS UI Gothic';

# タイトル画像を使用するとき
$t_img = "";
$t_w = 151; 	# 横サイズ（ピクセル）
$t_h = 28;	# 縦サイズ（ピクセル）

# 本文の文字大きさ（ポイント数:スタイルシート）
$pt = '10pt';

# 最大記事数
$max = 200;

# 戻り先のＵＲＬ(index.htmlなど)
$home = "../index.html";

# 壁紙・背景色・文字色など
$bg = "";		# 壁紙の指定 (http://から記述)
$bc = "#EEEEEE";	# 背景色
$te = "#004080";	# 文字色
$li = "#0000FF";	# リンク色（未訪問）
$vl = "#008080";	# リンク色（既訪問）
$al = "#DD0000";	# リンク色（訪問中）

# スクリプトURL
$script = './wforum.cgi';

# ログファイル名
$logfile = './wf_log.cgi';

# 管理ファイルURL
$admin = './wf_admin.cgi';

# 書き込みファイル
$regist = './wf_regi.cgi';

# 留意事項ページURL
$note = './note.html';

# ロックファイル機構
#   0 : 行なわない
#   1 : 行なう（symlink関数式）
#   2 : 行なう（mkdir関数式）
$lockkey = 2;

# ロックファイル
$lockfile = './lock/wforum.lock';

# URL自動リンク (0=no 1=yes)
$autolink = 1;

# 記事の [題名] の色
$sub_color = "#BC0000";

# 記事下地の色（一括表示時等）
$tbl_color = "#FFFFFF";

# 記事にNEWマークを付ける時間
$new_time = 48;

# NEWマークの表示形態
#  → 画像を使用する場合には $newmark = '<img src="./new.gif">';
#     というように IMGタグを記述してもよい
$newmark = '<font color="#FF3300">new!</font>';

# 記事NOの色
$no_color = "#800000";

# 新着記事一括表示の記事数
$sortcnt = 10;

# 頁あたりツリー表示数
$p_tree = 10;

# リストに表示する「記事タイトル」の最大長（文字数：半角文字換算）
$sub_length = 30;

# メールアドレスの入力を必須 (0=no 1=yes)
$in_email = 0;

# レスがついたらツリー毎トップへ移動 (0=no 1=yes)
$top_sort = 1;

# レスは下から順に付ける (0=no 1=yes)
$bot_res = 1;

# 引用部色変更
#  → ここに色指定を行うと「引用部」を色変更します
#  → この機能を使用しない場合は何も記述しないで下さい ($refcolor="";)
$refcolor = "#804000";

# 記事の更新は「method=POST」限定（セキュリティ対策）
#  0 : no
#  1 : yes
$postonly = 1;

# 投稿があるとメール通知する : sendmail必須
#  0 : 通知しない
#  1 : 通知する（自分の記事は送信しない）
#  2 : 通知する（自分の記事も送信する）
$mailing = 0;

# メール通知する際のメールアドレス
$mailto = 'xxx@xxx.xxx';

# sendmailパス（メール通知する時）
$sendmail = '/usr/lib/sendmail';

# ツリーのヘッダー記号
$treehead = "★";

# 過去ログ機能 (0=no 1=yes)
$pastkey = 1;

# 過去ログカウントファイル
$nofile = './pastno.dat';

# 過去ログのディレクトリ（最後は / で閉じる)
$pastdir = './past/';

# 過去ログ１ページ当りの最大行数
#  → これを超えると自動的に次ファイルを生成します
$max_line = 650;

# アクセス制限（半角スペースで区切る）
#  → 拒否するホスト名又はIPアドレスを記述（アスタリスク可）
#  → 記述例 $deny = '*.anonymizer.com *.denyhost.xx.jp 211.154.120.*';
$deny = '';

#------------#
#  設定完了  #
#------------#

$headflag=0;

#----------------#
#  デコード処理  #
#----------------#
sub decode {
	local($buf, $key, $val);

	$post_flag=0;
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag=1;
		if ($ENV{'CONTENT_LENGTH'} > 25000) { &error("投稿量が大きすぎます"); }
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else { $buf = $ENV{'QUERY_STRING'}; }
	foreach (split(/&/, $buf)) {
		($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# S-JIS変換
		&jcode'convert(*val, "sjis", "", "z");

		# タグ処理
		$val =~ s/&/&amp;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/"/&quot;/g;

		# 不要な改行を削除
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

	# 強制改行
	if (($mode eq "form" && $in{'pview'} ne "on" && $in{'wrap'} eq "hard") || ($mode eq "regist" && $in{'wrap'} eq "hard")) {
		local($tmp) = '';
		while (length $in{'message'}) {
			($folded, $in{'message'}) = &fold ($in{'message'}, 64);
			$tmp .= "$folded<br>";
		}
		$in{'message'} = $tmp;
	}
	# 改行コード処理
	$in{'message'} =~ s/\r\n/<br>/g;
	$in{'message'} =~ s/\r/<br>/g;
	$in{'message'} =~ s/\n/<br>/g;
	while ($in{'message'} =~ /<br>$/) { $in{'message'} =~ s/<br>$//g; }

	# タイムゾーンを日本時間に合わせる
	$ENV{'TZ'} = "JST-9";
}

#--------------#
#  ロック処理  #
#--------------#
sub lock {
	local($retry) = 5;
	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 60) { &unlock; }
	}
	# symlink関数式ロック
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	# mkdir関数式ロック
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	}
	$lockflag=1;
}

#--------------#
#  ロック解除  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }
	$lockflag=0;
}

#------------------#
#  HTMLのヘッダー  #
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
#  エラー処理  #
#--------------#
sub error {
	&unlock if ($lockflag);

	&header;
	print <<"EOM";
<div align="center"><h3>ERROR !</h3>
<font color="#dd0000">$_[0]</font>
<form>
<input type=button value="前画面にもどる" onClick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#----------------#
#  アクセス制限  #
#----------------#
sub axs_check {
	# ホスト名を取得
	&get_host;

	local($flag)=0;
	foreach (split(/\s+/, $deny)) {
		s/\*/\.\*/g;
		if ($host =~ /$_/i) { $flag=1; last; }
	}
	if ($flag) { &error("アクセスを許可されていません"); }
}

#--------------#
#  時間の取得  #
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
#  ホスト名取得  #
#----------------#
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($host eq "" || $host eq $addr) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2) || $addr;
	}
}

#----------------#
#  入力チェック  #
#----------------#
sub chk_form {
	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	# フォームチェック
	if ($in{'name'} eq "" || $in{'message'} eq "")
		{ &error("名前又はメッセージに記入モレがあります"); }
	if ($in_email && $in{'email'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/)
		{ &error("E-Mailの入力が不正です"); }
	# URL入力
#	if ($in{'no'} eq 'new' && !$in{'url'})
#		{ &error("設置スクリプトのURL記述は必須です"); }
	# 題名入力
	if ($in{'sub'} eq "") { &error("「題名」の入力モレです"); }
}

1;

