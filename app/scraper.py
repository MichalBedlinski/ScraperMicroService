"""
    This file defines scrapers
"""
import os
import re
import shutil
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent

from app.errors import ScraperError, NoImageFoundError

# Fake User-Agent factory, for antibot security
ua = UserAgent()

def setup_directories(sub_path, id):
    """
        Creates result directories

        FileExistsError -> for situation when directory already exists (handled)

        :param str sub_path: path of directory with all task results
        :param str id: ID of the celery task
    """
    # Result directory path
    results_path = os.path.join(sub_path, id)

    #Create directory for results
    try:
        os.mkdir(results_path)
    except FileExistsError:
        pass

    return results_path


def get_source(link):
    """
        Get source from website

        :param str link: URL to website from which will get source

        :raises ScraperError: when problems with HTTP query
    """
    response = requests.get(link, headers={'User-Agent': ua.random})
    if response.status_code == 200:
        return soup(response.text, features="html.parser")
    else:
        raise ScraperError(
                f"Invalid HTTP response {response.status_code} {response.reason}"
            )


def image_filter(html):
    """
        Html img filter

        :param html: html file

        :raises NoImageFoundError: when no images found
    """
    imgs = html.findAll("img")
    if imgs:
        return imgs
    else:
        raise NoImageFoundError("No image found on page, task failed")


def zipper(path, zip_name='images.zip', clear_rest=False):
    """
        Zip images for celery image task 

        :param str path: Path to directory with files to zip
        :param str zip_name: Name of zipped file, default='images.zip'
        :param bool clear_rest: If True after zipping files except zipped file 
                                would be deleted
    """
    with ZipFile(os.path.join(path, zip_name), 'w') as zipObj:
        for folderName, _subfolders, filenames in os.walk(path):
            for filename in filenames:
                if filename != zip_name:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, arcname=filename)
                    if clear_rest:
                        os.remove(filePath)


def scrape_image(source_link, path, file_name='images.zip', clear_rest=True):
    """
        Scrape image function

        :pramam str source_link: URL for website to scrape images
        :param str path: path where files will be 
        :param str file_name: name of result file
        :param bool clear_rest: If True, after zipping files except zipped file
                                would be deleted

        :raises ScraperError: if have problem with getting web source file
    """
    html = get_source(source_link)
    tags = image_filter(html)

    for tag in tags:
        src = tag.get("src")
        if src:
            src = re.match(r"((?:https?:\/\/.*)?\/(.*\.(?:png|jpg|svg)))", src)
            if src:
                (link, name) = src.groups()
                if not link.startswith("http"):
                    link = source_link + link
                response = requests.get(link, stream=True)

                if response.status_code == 200:
                    f = open(os.path.join(path, name.split("/")[-1]), "wb")
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                    f.close()
                else:
                    raise ScraperError(
                        "Invalid HTTP response {} {}".format(
                            response.status_code,
                            response.reason
                        )
                    )

    zipper(path, zip_name=file_name, clear_rest=clear_rest)
    return True


def scrape_text(source_link, path, file_name="text.txt"):
    """
        Scrape text function

        :pramam str source_link: URL for website to scrape images
        :param str path: path where files will be saved
        :param str file_name: name of result file

        :raises ScraperError: if have problem with getting web source file
    """
    soup = get_source(source_link)

    # Kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # Get text
    text = soup.body.get_text()
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    f = open(os.path.join(path, file_name), "wt")
    f.write(text)
    f.close()
        
    return True
