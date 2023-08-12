import os


class Config:
    main_path = os.path.split(os.path.realpath(__file__))[0]
    bilibili_cookies = os.path.join(main_path, "cookies/bilibili.sqlite")
    log_path = os.path.join(main_path, "logs/")
    downloads_path = os.path.join(main_path, "downloads/")
