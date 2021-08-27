# TGR-Chino-Bot
要望があったので追加しました。機能は色々あるので必要なライブラリは多めです。全部入れてから使ってください。

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
WordCloudを使う場合は

# 実行方法
    sh startbot.sh

バックグラウンドで動きます。SSHを切断しても動くおまじないがかけてあります。
# 終了方法
## 1. exitbot.shを実行
    sh exitbot.sh
## 2. PIDが表示されるので以下の様にコマンドを実行
    kill {PID}
