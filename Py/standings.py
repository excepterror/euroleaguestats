import logging
import requests
from lxml import etree

logging.getLogger().setLevel(logging.INFO)


def fetch_standings():
    try:
        import global_values
    except ModuleNotFoundError as error:
        logging.warning('globals.py is missing: {}'.format(error))

    url = 'https://www.euroleaguebasketball.net/euroleague/standings/'
    try:
        g1 = global_values.G1
        g2 = global_values.G2
        g3 = global_values.G3
        response = requests.get(url, timeout=(30, 30))
        logging.info('[standings.py status_code] ' + str(response.status_code))
    except NameError as error:
        logging.warning('g1, g2, g3 values are not defined: {}'.format(error))
    except requests.exceptions.HTTPError as http_error:
        logging.warning('[standings.py] HTTP error occurred: {}'.format(http_error))
        conn = 'Response from server failed!'
        return conn
    except requests.exceptions.Timeout as timeout:
        logging.warning('[standings.py] Timeout error occurred: {}'.format(timeout))
        conn = 'Response is taking too long!'
        return conn
    except requests.exceptions.ConnectionError as conn_error:
        logging.warning('[standings.py] Connection error occurred: {}'.format(conn_error))
        conn = 'No internet connection!'
        return conn
    else:
        standings = dict()
        a = 0
        listing = list()
        i = 0
        num_of_total_stat_cats = 11
        tree = etree.HTML(response.content)

        teams_and_ranking = tree.xpath(g1)
        for item in teams_and_ranking:
            if len(item) == 1:
                teams_and_ranking.remove(item)

        ranking = tree.xpath(g2)
        while a < len(teams_and_ranking):
            listing.append((ranking[a], teams_and_ranking[a]))
            a += 1

        raw_data = tree.xpath(g3)

        for item in listing:
            if item[0] in standings:
                standings['Images/' + item[1] + '.png'] = item[1]
            else:
                standings['Images/' + item[1] + '.png'] = item[0], raw_data[i: i + 7]
                i += num_of_total_stat_cats
        return standings
