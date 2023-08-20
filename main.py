# Author: NACHAYAN
import json
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


def make_dir(path):
    """创建文件夹"""
    try:
        path = path.strip().rstrip('\\')
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        else:
            return False
    except Exception as e:
        log.info(f"创建文件夹{path}失败：{e}")
        return False


def sanitize_filename(filename):
    # 这个函数用来去除文件名中的特殊字符
    return re.sub(r'[\\/:*?"<>|]', '_', filename)


# TODO 增加对于清晰度的检查
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
    log.info(f"\n✨✨✨开始启动下载器，请等待片刻✨✨✨")
    print(f"\n✨✨✨开始启动下载器，请等待片刻✨✨✨")
    time.sleep(5)
    url = input("请输入视频链接地址：")  # TODO 将用户输入链接转为自定义构造链接，防止出现特殊的get类型的data导致下载异常。
    log.info(f"输入链接：{url}")
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

    # 开始数据处理
    state_json = {}
    try:
        res = requests.get(url=url, headers=header)
        # 对于视频数据进行预处理，减轻后续工作量
        data_pattern = r'window\.?__INITIAL_STATE__\s?=\s?({.*?});'
        match = re.search(data_pattern, res.text)
        if match:
            state_json = json.loads(match.group(1))
            log.info(f"数据预处理完成！")
        else:
            log.info(f"数据处理失败")
            print("数据处理失败")
    except Exception as e:
        log.error(f"发生异常：{e}")
        print(f"发生异常：{e}")
        sys.exit(0)

    # 处理视频ID
    try:
        video_id = state_json["bvid"]
        log.info(f"1.视频Bvid号：{video_id}")
        print(f"1.视频Bvid号：{video_id}")
    except Exception as e:
        log.error(f"1.未找到视频Bvid号，错误信息：{e}")
        print("1.未找到视频Bvid号")

    # 作者信息处理
    try:
        author_value = state_json["videoData"]["owner"]["name"]
        log.info(f"2.视频作者：{author_value}")
        print(f"2.视频作者：{author_value}")
    except Exception as e:
        log.error(f"2.未找到视频作者信息，错误信息：{e}")
        print("2.未找到视频作者信息")

    # 标题处理部分
    try:
        title_text = state_json["videoData"]["title"]  # FIXME ✔已修复 标题进行预处理，防止出现特殊命名符号导致下载错误或是文件夹打包失败！
        log.info(f"3.视频标题：{title_text}")
        print(f"3.视频标题：{title_text}")
    except Exception as e:
        log.error(f"3.未找到视频标题信息，错误信息：{e}")
        print("3.未找到视频标题信息")

    # 图片处理部分
    try:
        img_href = state_json["videoData"]["pic"]
        log.info(f"4.视频封面链接为：{img_href}")
        print(f"4.视频封面链接为：{img_href}")
    except Exception as e:
        log.error(f"4.未找到封面链接地址，错误信息：{e}")
        print("4.未找到封面链接地址")

    # 简介处理部分（标记处：移除了多余的 .strip() 操作）
    try:
        plot_text = state_json["videoData"]["desc"]
        log.info(f"5.视频简介为：{plot_text}")
        print(f"5.视频简介为：{plot_text}")
    except Exception as e:
        log.error(f"5.未找到视频简介，错误信息：{e}")
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
        log.error("6.未找到视频发布时间")
        print("6.未找到视频发布时间")

    content = (f"<?xml version=\"1.0\" ?>\n"  # 修复首行换行导致Jellyfin无法正确识别到nfo文件
               f"<episodedetails>\n"
               f"    <title>{title_text}</title>\n"
               f"    <showtitle>{author_value}</showtitle>\n"
               f"    <uniqueid type=\"bilibili\" default=\"true\">{video_id}</uniqueid>\n"
               f"    <plot>{plot_text}</plot>\n"
               f"    <outline>{plot_text}</outline>\n"  # 修复Jellyfin无法识别视频简介的错误nfo部分
               f"    <premiered>{time_value[:10]}</premiered>\n"  # 修复视频时间无法被Jellyfin识别的Bug
               f"    <genre>{state_json['videoData']['tname']}</genre>\n"  # 新增视频风格部分解析
               f"    <actor>\n"  # 新增UP主信息展示
               f"        <name>{author_value}</name>\n"
               f"        <role>{author_value}</role>\n"
               f"        <thumb>{state_json['videoData']['owner']['face']}</thumb>\n"
               f"        <profile>https://space.bilibili.com/{state_json['videoData']['owner']['mid']}</profile>\n"
               f"    </actor>\n"
               f"</episodedetails>\n")

    try:
        make_dir(f"{config.downloads_path}/{author_value}/{sanitize_filename(title_text)}/")
        download_video(_url=f"https://www.bilibili.com/video/{state_json['bvid']}", COOKIE_PATH=config.bilibili_cookies,
                       downloads_path=f"{config.downloads_path}/{author_value}/{sanitize_filename(title_text)}/")
        download_image(_url=img_href,
                       downloads_path=f"{config.downloads_path}/{author_value}/{sanitize_filename(title_text)}/",
                       file_name="poster.jpg")
        with open(f"{config.downloads_path}/{author_value}/{sanitize_filename(title_text)}/movie.nfo", "w",
                  encoding="utf-8") as info:
            info.write(content)
            log.info(
                f"将视频信息写入：'{config.downloads_path}/{author_value}/{sanitize_filename(title_text)}/movie.nfo'中~~~")
            print(
                f"将视频信息写入：'{config.downloads_path}/{author_value}/{sanitize_filename(title_text)}/movie.nfo'中~~~")
        log.info(
            f"下载结束，请在：'{config.downloads_path}/{author_value}/{sanitize_filename(title_text)}/'下查看项目结果（＾▽＾）")
        print(
            f"下载结束，请在：'{config.downloads_path}/{author_value}/{sanitize_filename(title_text)}'下查看项目结果（＾▽＾）")
    except Exception as _E:
        log.error(f"发生异常请处理：{_E}")
        print(f"发生异常，程序自动退出！")
        sys.exit(0)
