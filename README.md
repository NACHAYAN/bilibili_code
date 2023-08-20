# BiliBili视频下载器

**2023年08月11日**

**_该项目仅为个人学习研究创作，不得用于盈利等其他违法行为_**

简单使用you-get库加cookie实现下载B站视频并将视频信息整理为适合Jellyfin、Emby的文件夹格式，打造更方便的海报墙的方法。

**操作**

克隆本项目后，进入项目目录
```
cd bilibili_code
```

建议在虚拟环境下下载所需依赖
```
pip install -r requirements.txt
```

接下来将你的cookie文件放在``` main.py ```同路径下的``` /cookies/bilibili.sqlite ```，
cookie文件推荐从Firefox浏览器获取，可以很方便的找到sqlite格式的目标cookie。

现在，你就可以直接执行主文件 main.py，下载UP主们的视频啦
```
python main.py
```
等待弹出输入链接的字样后，输入B站视频链接，等待下载完成即可

![img.png](img/download.png)

![img.png](img/result.png)

当然，你也可以在Config.py文件中修改日志文件、下载文件、cookie文件的存放地址，这些都可以随你的心意随意修改。~~ps:
你最好记得自己把文件放在什么地方，而不是胡乱修改。~~

**TODO LIST:**

1. [ ] 建立可选配置的模式
2. [ ] 将手动设置个人cookies的方式升级为通过api获取
3. [ ] 其他一些可以优化的点子或是建议。 tips：可以多多的提issue帮助我们优化哦