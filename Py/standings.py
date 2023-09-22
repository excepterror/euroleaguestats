import logging
import requests
from lxml import etree

logging.getLogger().setLevel(logging.INFO)


def fetch_standings():
    url = 'https://www.euroleaguebasketball.net/euroleague/standings/'
    standings = dict()
    try:
        response = requests.get(url)
    except requests.exceptions.HTTPError as http_error:
        logging.warning('HTTP error occurred: {}'.format(http_error))
    except requests.exceptions.Timeout as timeout:
        logging.warning('Timeout error occurred: {}'.format(timeout))
    except Exception as e:
        logging.warning(e)
    else:
        a = 0
        listing = list()
        tree = etree.HTML(response.content)

        teams_and_ranking = tree.xpath(
            '//div[@class="complex-stat-table_body__UI0Lj"]'
            '//div[@class="complex-stat-table_row__Jiu1w complex-stat-table__standingRow__KJaSV"]'
            '//div[@class="complex-stat-table_sticky__TsX4D"]'
            '//span[@class="complex-stat-table_mainClubName__1CeH5"]'
            '/text()')
        for i in teams_and_ranking:
            if len(i) == 1:
                teams_and_ranking.remove(i)

        ranking = tree.xpath(
            '//div[@class="complex-stat-table_body__UI0Lj"]'
            '//div[@class="complex-stat-table_row__Jiu1w complex-stat-table__standingRow__KJaSV"]'
            '//div[@class="complex-stat-table_sticky__TsX4D"]'
            '//div[@class="complex-stat-table_cell__yQmD8 complex-stat-table__right__7D_Wn"]'
            '//span/text()')
        while a < len(teams_and_ranking):
            listing.append((ranking[a], teams_and_ranking[a]))
            a += 1

        raw_data = tree.xpath(
            '//div[@class="complex-stat-table_body__UI0Lj"]'
            '//div[@class="complex-stat-table_row__Jiu1w complex-stat-table__standingRow__KJaSV"]'
            '//div[@class="complex-stat-table_cell__yQmD8"]/text()')

        for item in listing:
            if item[0] in standings:
                standings['Images/' + item[1] + '.png'] = item[1]
            else:
                standings['Images/' + item[1] + '.png'] = item[0], raw_data[0:7]
    return standings
