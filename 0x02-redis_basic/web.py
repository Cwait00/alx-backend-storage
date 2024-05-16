#!/usr/bin/env python3

import requests
import redis
import time


def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL and cache the result with an expiration time of 10 seconds.
    
    Args:
        url: The URL to retrieve the HTML content from.
    
    Returns:
        The HTML content of the URL.
    """
    # Connect to Redis
    r = redis.Redis()

    # Increment the count for the URL
    url_count_key = f"count:{url}"
    r.incr(url_count_key)

    # Check if the content is already cached
    cached_content = r.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    # Fetch the HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the content with an expiration time of 10 seconds
    r.setex(url, 10, html_content)

    return html_content


# Test the function
if __name__ == "__main__":
    # Test URL with slow response for demonstration
    test_url = "http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.google.com"
    
    # Call the function multiple times to see the caching behavior
    for _ in range(3):
        print(get_page(test_url))
        time.sleep(5)  # Wait for 5 seconds between each call for better observation
