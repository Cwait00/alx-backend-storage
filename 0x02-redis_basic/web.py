#!/usr/bin/env python3

import requests
import redis
import time


def get_page(url: str) -> str:
    """Retrieve the HTML content of a URL and cache the result.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    # Initialize Redis connection
    r = redis.Redis(host='localhost', port=6379, db=0)

    # Check if URL is already cached
    cached_content = r.get(url)
    if cached_content:
        return cached_content.decode()

    # Fetch HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML content with expiration time of 10 seconds
    r.setex(url, 10, html_content)

    # Track the number of times the URL was accessed
    count_key = "count:{}".format(url)
    r.incr(count_key)

    return html_content


if __name__ == "__main__":
    # Example usage
    url = ("http://slowwly.robertomurray.co.uk/"
           "delay/10000/url/http://www.example.com")
    page_content = get_page(url)
    print(page_content)
