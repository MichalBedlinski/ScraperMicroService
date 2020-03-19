"""
    This file defines celery tasks
"""
import os
import logging

from app import celeryapp
from app.scraper import scrape_image, scrape_text, setup_directories
from app.scraper import NoImageFoundError, ScraperError


celery = celeryapp.celery

@celery.task(
    bind=True, 
    autoretry_for=(ScraperError,), 
    retry_kwargs={'max_retries': 3, 'countdown': 5})
def images_tasks(self, url, sub_path):
    """
        Function defines "Get image from webpage" task

        ScraperError -> for problems with connection (handled)
        NoImageFoundError -> for situation with no images on page 
                            task is flaged as failed and discarded (handled)

        :param self: celery context object
        :param url: URL of website for task
        :param sub_path: path of directory with all task results
    """
    results_path = setup_directories(sub_path, self.request.id)

    # Scrape
    try:
        scrape_image(url, results_path)
    except NoImageFoundError:
        # Leave task as Failed
        pass

    return self.request.id


@celery.task(
    bind=True, 
    autoretry_for=(ScraperError,), 
    retry_kwargs={'max_retries': 3, 'countdown': 5})
def text_tasks(self, url, sub_path):
    """
        Function defines "Get text from webpage" task

        ScraperError -> for problems with connection (handled)

        :param self: celery context object
        :param url: URL of website for task
        :param sub_path: path of directory with all task results
    """
    results_path = setup_directories(sub_path, self.request.id)

    # Scrape
    scrape_text(url, results_path)

    return self.request.id
