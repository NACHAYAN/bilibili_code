# Author: NACHAYAN
import logging
import os
import platform
import re
import subprocess
import sys
import time

import requests

import Config

config = Config.Config()
system_name = platform.system()


def get_logger(_LOG_PATH, level=logging.INFO, log_format='%(asctime)s - %(name)s - %(message)s', encoding='utf-8'):
    """
    创建并返回日志对象
    :param _LOG_PATH: 日志文件路径
    :param level: 日志级别，默认为 INFO
    :param log_format: 日志格式，默认为 '%(asctime)s - %(name)s - %(message)s'
    :param encoding: 日志编码，默认为 utf-8
    :return: 日志对象
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    fh = logging.FileHandler(_LOG_PATH, encoding=encoding)
    fh.setLevel(level)

    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger


log_dir = config.log_path
LOG_PATH = os.path.join(log_dir, '{}.log'.format(
    time.strftime('%Y-%m-%d', time.localtime(time.time()))))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log = get_logger(_LOG_PATH=LOG_PATH)


# 定义下载函数
def download_video(_url, COOKIE_PATH, downloads_path):
    """
    下载视频的主要函数方式
    :param _url: 视频url地址
    :param COOKIE_PATH: 保存的cookie存放地址
    :param downloads_path: 保存下载视频的地址
    :return: None
    """
    cmd = ["you-get", "-c", COOKIE_PATH, "-o", downloads_path, _url]

    try:
        # 执行命令并获取返回值
        result = subprocess.run(
            cmd, capture_output=True, universal_newlines=True, encoding="utf-8", check=True)

        # 输出命令的返回值
        log.info(result.stdout)

    except subprocess.CalledProcessError as e:
        # 处理命令执行失败的异常
        log.error(
            f"Command '{cmd}' failed with error code {e.returncode}:")
        log.error(e.stderr)
    except Exception as e:
        # 处理其他异常
        log.error(
            f"An error occurred while running command '{cmd}':")
        log.error(e)


def download_image(_url, downloads_path, file_name):
    """
    下载封面图片
    :param _url: 图片地址
    :param downloads_path: 保存地址
    :param file_name: 保存文件名
    :return: None
    """
    try:
        response = requests.get(_url)
        if response.status_code == 200:
            # 拼接文件名
            file_path = os.path.join(downloads_path, file_name)

            # 写入文件
            with open(file_path, 'wb') as file:
                file.write(response.content)
            log.info(f"封面已下载至：{file_path}")
            print(f"封面已下载至：{file_path}")
        else:
            log.error(f"下载封面失败：HTTP错误{response.status_code}")
            print("下载封面失败：HTTP错误", response.status_code)
    except Exception as e:
        print(f"下载封面失败：{e}")
        print("下载图片失败：", str(e))


# 定义检查和安装 you-get 的函数
def check_and_install_you_get():
    """
    检查you-get安装状态
    :return: _you_get_path: you-get安装路径
    """
    try:
        # 检查 you-get 是否存在
        subprocess.run(["you-get", "--version"],
                       capture_output=True, check=True)
        # 如果存在，则直接获取路径并返回
        if system_name == 'Windows':
            _you_get_path = subprocess.run(
                ["where", "you-get"], capture_output=True, text=True).stdout.strip()
        else:
            _you_get_path = subprocess.run(
                ["which", "you-get"], capture_output=True, text=True).stdout.strip()
        return _you_get_path
    except subprocess.CalledProcessError:
        # 如果不存在，则安装
        print("当前未安装you-get模块，正在尝试安装")
        try:
            subprocess.run(["pip3", "install", "you-get"],
                           capture_output=True, check=True)
            print("you-get 已成功安装")
            # 安装成功后获取路径并返回
            if system_name == 'Windows':
                _you_get_path = subprocess.run(
                    ["where", "you-get"], capture_output=True, text=True).stdout.strip()
            else:
                _you_get_path = subprocess.run(
                    ["which", "you-get"], capture_output=True, text=True).stdout.strip()
            return _you_get_path
        except Exception as _e:
            print("you-get安装失败，请查阅日志后自行检测")
            log.error(f"you-get安装发生异常：{_e}")
            sys.exit(0)


# 如果系统支持，则执行检查和安装 you-get 的操作
if system_name == 'Windows' or system_name == 'Linux':
    try:
        you_get_path = check_and_install_you_get()
        log.info(f'you-get模块安装路径为{you_get_path}')
    except Exception as e:
        print(f"发生错误：{e}")
        sys.exit(0)
else:
    log.error("当前系统暂不支持该脚本")
    print("当前系统暂不支持该脚本")
    sys.exit(0)

if __name__ == '__main__':
    log.info(f"✨✨✨开始启动下载器，请等待片刻✨✨✨")
    print(f"✨✨✨开始启动下载器，请等待片刻✨✨✨")
    url = input("请输入视频链接地址：")
    log.info(f"\n输入链接：{url}")
    header = {
        "authority": "data.bilibili.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "content-type": "text/plain",
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/video/BV18k4y1g7D5/?spm_id_from=333.1007.tianma.1-2-2.click",
        "sec-ch-ua": "^\\^Not/A)Brand^^;v=^\\^99^^, ^\\^Google",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0"
                      "Safari/537.36"
    }

    try:
        res = requests.get(url=url, headers=header)
    except Exception as e:
        log.error(f"发生异常：{e}")
        print(f"发生异常：{e}")
        sys.exit(0)

    # 处理视频ID
    ID_found = False
    ID_pattern = (r'<link data-vue-meta="true" rel="alternate" media="only screen and\(max-width: 640px\)" href="(['
                  r'^"]+)">')
    ID_match = re.search(ID_pattern, res.text)

    if ID_match:
        ID_found = True
        href_content = ID_match.group(1)
        video_id = re.search(r'video/([A-Za-z0-9]+)', href_content).group(1)
        log.info(f"1.视频Bvid号：{video_id}")
        print(f"1.视频Bvid号：{video_id}")
    else:
        print("1.未找到视频Bvid号")

    # 作者信息处理
    author_pattern = r'<meta data-vue-meta="true" itemprop="author" name="author" content="([^"]+)">'
    author_match = re.search(author_pattern, res.text)

    if author_match:
        author_value = author_match.group(1)
        log.info(f"2.视频作者：{author_value}")
        print(f"2.视频作者：{author_value}")
    else:
        print("2.未找到视频作者信息")

    # 标题处理部分
    title_found = False
    title_pattern = r'<title data-vue-meta="true">([^<]+)</title>'
    title_match = re.search(title_pattern, res.text)

    if title_match:
        title_found = True
        title_text = re.sub(r'_哔哩哔哩_bilibili', '', title_match.group(1))
        log.info(f"3.视频标题：{title_text}")
        print(f"3.视频标题：{title_text}")
    else:
        print("3.未找到视频标题信息")

    # 图片处理部分
    img_found = False
    img_pattern = r'<link data-vue-meta="true" rel="apple-touch-icon" href="([^"]+)'
    img_match = re.search(img_pattern, res.text)

    if img_match:
        img_found = True
        href_content = img_match.group(1)
        img_href = "https:{}".format(re.sub(r'@.*$', '', href_content))
        log.info(f"4.视频封面链接为：{img_href}")
        print(f"4.视频封面链接为：{img_href}")
    else:
        print("4.未找到封面链接地址")

    # 简介处理部分（标记处：移除了多余的 .strip() 操作）
    plot_found = False
    plot_pattern = r'<span class="desc-info-text" data-v-1d530b8d.*?>(.*?)</span></div>'
    plot_match = re.search(plot_pattern, res.text, re.DOTALL)

    if plot_match:
        plot_text = plot_match.group(1)  # 移除了多余的 .strip() 操作
        log.info(f"5.视频简介为：{plot_text}")
        print(f"5.视频简介为：{plot_text}")
    else:
        print("5.未找到视频简介")

    # 发布时间处理
    time_found = False
    time_pattern = r'<meta data-vue-meta="true" itemprop="datePublished" content="([^"]+)">'
    time_match = re.search(time_pattern, res.text)

    if time_match:
        time_found = True
        time_value = time_match.group(1)
        log.info(f"6.发布时间为：{time_value}")
        print(f"6.发布时间为：{time_value}")
    else:
        print("6.未找到视频发布时间")

    content = (f"\n"
               f"<?xml version=\"1.0\" ?>\n"
               f"<episodedetails>\n"
               f"    <title>{title_text}</title>\n"
               f"    <showtitle>{author_value}</showtitle>\n"
               f"    <uniqueid type=\"bilibili\" default=\"true\">{video_id}</uniqueid>\n"
               f"    <plot>{plot_text}</plot>\n"
               f"    <premiered>{time_value}</premiered>\n"
               f"</episodedetails>\n")

    try:
        download_video(_url=url, COOKIE_PATH=config.bilibili_cookies,
                       downloads_path=f"{config.downloads_path}/{author_value}/{title_text}/")
        download_image(_url=url, downloads_path=f"{config.downloads_path}/{author_value}/{title_text}/",
                       file_name="poster.jpg")
        with open(f"{config.downloads_path}/{author_value}/{title_text}/info.nfo", "w", encoding="utf-8") as info:
            info.write(content)
            log.info(f"将视频信息写入{config.downloads_path}/{author_value}/{title_text}/info.nfo中~~~")
            print(f"将视频信息写入{config.downloads_path}/{author_value}/{title_text}/info.nfo中~~~")
        log.info(f"下载结束，请在{config.downloads_path}/{author_value}/{title_text}下查看项目结果（＾▽＾）")
        print(f"下载结束，请在{config.downloads_path}/{author_value}/{title_text}下查看项目结果（＾▽＾）")
    except Exception as _E:
        log.error(f"发生异常请处理：{_E}")
        print(f"发生异常，程序自动退出！")
        sys.exit(0)
