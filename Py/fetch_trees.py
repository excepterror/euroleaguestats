import requests
import concurrent.futures
import logging

from lxml import etree
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def fetch_tree(url):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url)
    t = etree.HTML(response.content)
    return t


def fetch_trees(grid_roster):
    temp_dict = dict()
    roster_keys = grid_roster.roster.keys()
    roster_values = grid_roster.roster.values()

    names = list(roster_keys)
    roster_values = list(roster_values)

    players_urls = list()
    photo_urls = list()
    for _tuple in roster_values:
        players_urls.append(_tuple[0])
        photo_urls.append(_tuple[1])

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            trees = executor.map(fetch_tree, players_urls)
    except TimeoutError as timeout_error:
        logging.warning('Timeout error occurred: {}'.format(timeout_error))

    for name, tree, url in zip(names, trees, photo_urls):
        if name in temp_dict:
            temp_dict[name] = name
        else:
            temp_dict[name] = tree, url

    trees = temp_dict
    grid_roster.roster = dict()

    return trees
