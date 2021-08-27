# 必要なライブラリを読み込む
import discord
from discord import channel
import psutil
import random
import string
import asyncio
import youtube_dl
import os
import glob
import config

# YouTube DLの処理 (触らない方が無難)
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# Botのアクセストークン
TOKEN = 'DISCORDのサイトから取れる'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# Thinking絵文字の読み込み(適当)
UnicodeEmoji ="\N{Thinking Face}"

# メンション時のメッセージ(適当)
random_contents = [
    "呼ばれた気がした",
    "にゃー",
    "何かようですか",
]

# 起動時に動作する処理(なくてもいい)
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される(いらん)
    print('ログインしました')

async def reply(message):
    msgcont = random.choice(random_contents)
    reply = f'{message.author.mention} ' # 返信メッセージの作成
    await message.channel.send(reply + msgcont) # 返信メッセージを送信

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):

    split_commend = str(message.content)
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
      
    # 発言に反応(例)
    if split_commend[0] == '/heyguys':
        await message.channel.send('Hey guys, we have gift for you.')

    # ここからVC制御をする
    elif split_commend[0] == "!join":
        if message.author.voice is None:
            await message.channel.send("ERROR!_あなたがボイスチャンネルに接続していません!ボイスチャンネルに接続してください。")
            return
        # ボイスチャンネルに接続する
        await message.author.voice.channel.connect()
        await message.channel.send("Success!_接続しました。")

    elif split_commend[0] == "!leave":
        if message.guild.voice_client is None:
            await message.channel.send("ERROR!_ボイスチャンネルに接続していません!")
            return
        # 切断する
        await message.guild.voice_client.disconnect()
        await message.channel.send("Success!_切断しました。")

    elif message.content.startswith("!play "):
        if message.guild.voice_client is None:
            await message.channel.send("ERROR!_ボイスチャンネルに接続していません!")
            return
        # 再生中の場合は再生しない
        if message.guild.voice_client.is_playing():
            await message.channel.send("ERROR!_再生中です。")
            return
        url = split_commend[1]
        # プレイヤー処理
        # ↓loop=client.loop のあとに stream=True を追加するとストリー厶になる(=ダウンロードされなくなる)
        player = await YTDLSource.from_url(url, loop=client.loop)
        # 再生処理
        message.guild.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await message.channel.send('PLAY_{0} を再生します。'.format(player.title))

    elif split_commend[0] == "!pause":
        if message.guild.voice_client is None:
            await message.channel.send("ERROR!_ボイスチャンネルに接続していません!")
            return
        message.guild.voice_client.pause()
        await message.channel.send('Paused.')

    elif split_commend[0] == "!stop":
        if message.guild.voice_client is None:
            await message.channel.send("ERROR!_ボイスチャンネルに接続していません!")
            return
        if not message.guild.voice_client.is_playing():
            await message.channel.send("ERROR!_再生していません。")
            return
        message.guild.voice_client.stop()
        await message.channel.send('Stopped.')

    # Streamの場合は不要
    elif split_commend[0] == '/clean':
        # webmファイルがあれば削除
        file_list = glob.glob("*.webm")
        for file in file_list:
            os.remove(file)
        # mp3ファイルがあれば削除
        file_list2 = glob.glob("*.mp3")
        for file2 in file_list2:
            os.remove(file2)
        # m4aファイルがあれば削除
        file_list3 = glob.glob("*.m4a")
        for file3 in file_list3:
            os.remove(file3)
        await message.channel.send('サーバーを掃除しました。')

    # ここから各反応の設定 (elifで追加していく)
    elif client.user in message.mentions: # 話しかけられたかの判定
        await reply(message) # 返信する非同期関数を実行

    elif split_commend[0] == '/star':
        await message.channel.send('スター氏はTGR Groupのイケメン社長です。')

    elif split_commend[0] == '/laddge':
        await message.channel.send('Laddge君はイケメンです。レッツノートが大好きです。')
        
    # リアクションさせる、絵文字は上部で読み込んである (Unicode)
    elif split_commend[0] == 'しんきんぐ':
        await message.add_reaction(UnicodeEmoji)

    # サーバー情報をおしえてくれる(便利)
    elif split_commend[0] == '/serverinfo':
        # サーバー情報を取得する
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem2 = mem.percent
        dsk = psutil.disk_usage('/')
        dsk2 = dsk.percent
        await message.channel.send('【サーバー情報】CPU使用率:' + str(cpu) + '%、メモリー使用率:' + str(mem2) + '%、ディスク使用率:' + str(dsk2) + '%')

    elif split_commend[0] == '/wc':
        # APIの制限回避のため実行権限を管理者のみ
        if message.author.guild_permissions.administrator:
            import mainrun
            await message.channel.send(file=discord.File('wordcloud_sample.png'))
            os.remove('wordcloud_sample.png')
        else:
            await message.channel.send('Error:管理者以外実行できません。')

    elif split_commend[0] == '/random':
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        await message.channel.send('Random Password: ' + str(result_str))

    # everyoneメンションのみブロック(含む場合無視)
    elif split_commend[0] == '@everyone':
        await message.delete()
        await message.channel.send('BLOCKED! everyoneメンションは禁止です。')

# 新入
@client.event
async def on_member_join(member):
    channel = client.get_channel(config.JOIN_CHANNEL_ID)
    await channel.send(f'{member.mention}\nようこそサーバーへ!')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)