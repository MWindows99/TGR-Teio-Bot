# TGR-Chino-Bot
要望があったので追加しました。機能は色々あるので必要なライブラリは多めです。全部入れてから使ってください。

# 追記
1. I merged the bot.py because a bug was found in it.
2. Change prefix of all commands to "/".

Contributors:
 - [Mizusyan](https://github.com/MizuokaDev)
 - [yu___ri2006](https://github.com/yu-ri2006)

# 注意
1. Discord.pyのサポートは終了しているのでいつまで使えるのかはわかりません。
2. WordCloudの機能に不具合を見つけた気がするのですが、直してないです。

# Font (License)
This program contains the following fonts. 
 ## Ricty Diminished
 1. Watch with [GitHub](https://github.com/edihbrandon/RictyDiminished).
 
 2. Watch [License](https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=ofl).

# 必要なライブラリ

WordCloud使わない場合は上3つを入れれば動きます。

## discord.py (VC機能付き)
     pip3 install discord.py[voice]
## psutil
     pip3 install psutil
## youtube_dl
     pip3 install youtube_dl
## OAuth1Session
     pip3 install requests_oauthlib
## janome
     pip3 install janome
## WordCloud
     pip3 install wordcloud
## emoji lib
     pip3 install emoji --upgrade
## tweepy
     pip3 install tweepy
     
# 実行前に
bot.pyの指定された場所にBotトークンを入力してください。

WordCloudを使う場合は↓

1. Twitter API Keyを"config.py"に入れる。
2. Twitter User IDを"gettimeline.py"に入れる。

# 実行方法
    sh startbot.sh

バックグラウンドで動きます。SSHを切断しても動くおまじないがかけてあります。
# 終了方法
## 1. exitbot.shを実行
    sh exitbot.sh
## 2. PIDが表示されるので以下の様にコマンドを実行
    kill {PID}

# 利用可能なコマンド

### /wc
WordCloudを生成する。実行から返信まで20〜30秒遅延あり。
### /serverinfo
サーバー情報を表示する。便利！
### /random
パスワード等で使えそうなランダムな10桁の値を生成。
### /join
VCに接続する。
### /leave
VCから切断する。
### /play URL
Youtubeの動画の曲を再生する。(YouTube利用規約に従うこと。私は責任を負わない。)
### /stop
Youtubeの動画の曲の再生を停止する。
### /pause
Youtubeの動画の曲の再生をポーズする。(開始方法なしのため!stopと同じ)
### しんきんぐ
顔文字でリアクションする。
### その他諸々
…
