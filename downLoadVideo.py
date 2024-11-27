import yt_dlp

 # 下载 MP4 格式视频

def downloads(link):
    video_opts = {
        # 默认下载的是最佳的音频和画质
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        # 可以指定路径
        'outtmpl': '%(title)s.%(ext)s',
        
         '''
         需要cookies文件，在Google chorme上安装插件即可，然后打开要要下载的视频链接，导出cookies
         '''
        'cookiefile': 'cookies.txt',
        
        # 调用ffmpeg，可能需要安装
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',
    }

    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'cookiefile': 'cookies.txt',
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',
    }

    try:
        # 下载视频
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            video_title = info_dict.get('title', 'Unknown')
            print(f"视频文件已下载: {video_title}.mp4")
        
        # 提取音频
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_title = info_dict.get('title', 'Unknown')
            print(f"音频文件已提取: {audio_title}.mp3")

    except Exception as e:
        print(f"下载出错: {e}")

# 输入视频链接并调用下载函数
url = input("视频链接：")
downloads(url)