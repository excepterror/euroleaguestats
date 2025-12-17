import logging
import requests

from lxml import etree

from StartupFiles.global_values import G1, G2, G3

logging.getLogger().setLevel(logging.INFO)


def fetch_standings():
    url = 'https://www.euroleaguebasketball.net/en/euroleague/standings/'
    try:
        response = requests.get(url, timeout=(30, 30))
        logging.info('[standings.py] {}'.format(response.status_code))
        if not all([G1, G2, G3]):
            logging.warning("G1, G2, or G3 is missing or empty.")
            return "Internal error – missing configuration."
    except requests.exceptions.HTTPError as http_error:
        logging.warning(f'standings.py HTTP error occurred: {http_error}')
        notification_content = 'Response from server failed!'
        return notification_content
    except requests.exceptions.Timeout as timeout:
        logging.warning(f'standings.py Timeout error occurred: {timeout}')
        notification_content = 'Response is taking too long!'
        return notification_content
    except requests.exceptions.ConnectionError as conn_error:
        logging.warning(f'standings.py Connection error occurred: {conn_error}')
        notification_content = 'No internet connection!'
        return notification_content
    else:
        standings = dict()
        a = 0
        listing = list()
        i = 0
        num_of_total_stat_cats = 11
        tree = etree.HTML(response.content)

        teams_and_ranking = tree.xpath(G1)
        teams_and_ranking = [item for item in teams_and_ranking if item != ' (Q)']

        ranking = tree.xpath(G2)
        try:
            while a < len(teams_and_ranking):
                listing.append((ranking[a], teams_and_ranking[a]))
                a += 1
        except IndexError as index_error:
            logging.warning(f'standings.py Index error occurred: {index_error}')
            notification_content = 'Download error occurred!'
            return notification_content

        raw_data = tree.xpath(G3)

        for item in listing:
            if item[0] in standings:
                standings['Assets/' + item[1] + '.png'] = item[1]
            else:
                standings['Assets/' + item[1] + '.png'] = item[0], raw_data[i: i + 7]
                i += num_of_total_stat_cats
        return standings
