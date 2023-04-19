import os
import random

from icrawler.builtin import GoogleImageCrawler


def download_images_from_google(max_num: int):
    filename = os.path.basename(__file__)
    path = os.path.abspath(__file__).replace(filename, 'images/')

    try:
        _ = os.listdir(path)
    except FileNotFoundError:
        crawler = GoogleImageCrawler(storage={'root_dir': path})
        crawler.crawl(keyword='Милые котики', max_num=max_num)


def get_image() -> str:
    filename = os.path.basename(__file__)
    path = os.path.abspath(__file__).replace(filename, 'images/')
    all_images: list = os.listdir(path)
    number = random.randrange(len(all_images))
    return path + all_images[number]
