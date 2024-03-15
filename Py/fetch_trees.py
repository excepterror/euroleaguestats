import requests
import concurrent.futures
import logging

from lxml import etree


def fetch_tree(url):
    try:
        response = requests.get(url, timeout=(30, 30))
        t = etree.HTML(response.content)
        logging.info('[fetch_trees.py status_code] ' + str(response.status_code))
    except requests.exceptions.Timeout as timeout_error:
        logging.warning('[fetch_trees.py] The request timed out: {}'.format(timeout_error))
    except requests.exceptions.ConnectionError as conn_error:
        logging.warning('[fetch_trees.py] Connection error occurred: {}'.format(conn_error))
    else:
        return t


def fetch_trees(roster):
    temp_dict = dict()
    roster_keys = roster.keys()
    roster_values = roster.values()

    names = list(roster_keys)
    roster_values = list(roster_values)

    players_urls = list()
    photo_urls = list()
    for _tuple in roster_values:
        players_urls.append(_tuple[0])
        photo_urls.append(_tuple[1])

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            trees = executor.map(fetch_tree, players_urls, timeout=30)
    except concurrent.futures.TimeoutError as timeout_error:
        logging.warning('Timeout error occurred: {}'.format(timeout_error))
        conn = 'Error while fetching data!'
        return conn
    else:
        for name, tree, url in zip(names, trees, photo_urls):
            if name in temp_dict:
                temp_dict[name] = name
            else:
                temp_dict[name] = tree, url
        trees = temp_dict
        return trees
