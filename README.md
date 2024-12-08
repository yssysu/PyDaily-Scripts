# learning-of-python

# 学习python的笔记

基本语法的学习和自己写的一些脚本处理一些数据

- [X] *spatial_IDW.py*:处理地理空间数据，采用IDW插值。
- [X] *downloadVideo.py*:用来下载网页视频。

> 仅用来测试了bilibili和YouTobe网站，理论上是yt_dlp库支持的网站都能能够下载视频，默认的下载格式是.mp4，下载的视频和音频的质量默认为最佳。
>
> 在下载前需要提供
>
> 1. cookies.txt文件
> 2. 安装yt_dlp库和ffmpeg视频转换器。
>
> 至于下载方法，可以直接在网上搜索。
>
> 最后推荐使用Google Chorme浏览器。

- [X] *word.py*:按照图片在文档中出现的先后进行提取。

> 在使用前需要用到 `docx` 库，使用 `pip install python-docx pillow `完成库的安装
>
> 只需要输入两个变量：word文件位置和输出图像的位置
