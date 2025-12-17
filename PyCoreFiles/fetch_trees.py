import requests
import concurrent.futures
import logging

from lxml import etree


def fetch_tree(url):
    try:
        response = requests.get(url, timeout=(30, 30))
        logging.info(f'fetch_trees.py status_code | url: {response.status_code} | {url}')
        return etree.HTML(response.content)
    except requests.exceptions.Timeout as timeout_error:
        logging.warning(f'fetch_trees.py The request timed out: {timeout_error}')
    except requests.exceptions.ConnectionError as conn_error:
        logging.warning(f'fetch_trees.py Connection error occurred: {conn_error}')
    return None


def fetch_trees(roster):
    temp_dict = dict()
    names = list(roster.keys())
    values = list(roster.values())

    players_urls = [v[0] for v in values]
    photo_urls = [v[1] for v in values]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_tree, url) for url in players_urls]
        try:
            results = [f.result(timeout=30) for f in futures]
        except concurrent.futures.TimeoutError as timeout_error:
            logging.warning(f'Timeout error occurred: {timeout_error}')
            raise ValueError("Timeout occurred while fetching trees.")

    for name, tree, url in zip(names, results, photo_urls):
        if tree is not None:
            temp_dict[name] = (tree, url)

    if not temp_dict:
        raise ValueError("All requests failed or timed out.")

    return temp_dict
