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
        i = 0
        num_of_total_stat_cats = 11
        tree = etree.HTML(response.content)

        teams_and_ranking = tree.xpath(
            '//div[@class="complex-stat-table_body__UI0Lj"]'
            '//div[@class="complex-stat-table_row__Jiu1w complex-stat-table__standingRow__KJaSV complex-stat-table__bottom8__h6iNh complex-stat-table__euroleague__zV5Mu"]'
            '//div[@class="complex-stat-table_sticky__TsX4D"]'
            '//span[@class="complex-stat-table_mainClubName__1CeH5" or @class="complex-stat-table_mainClubName__1CeH5 complex-stat-table__long__YuBt_"]'
            '/text()')
        for item in teams_and_ranking:
            if len(item) == 1:
                teams_and_ranking.remove(item)

        ranking = tree.xpath(
            '//div[@class="complex-stat-table_body__UI0Lj"]'
            '//div[@class="complex-stat-table_row__Jiu1w complex-stat-table__standingRow__KJaSV complex-stat-table__bottom8__h6iNh complex-stat-table__euroleague__zV5Mu"]'
            '//div[@class="complex-stat-table_sticky__TsX4D"]'
            '//div[@class="complex-stat-table_cell__yQmD8 complex-stat-table__right__7D_Wn"]'
            '//span/text()')
        while a < len(teams_and_ranking):
            listing.append((ranking[a], teams_and_ranking[a]))
            a += 1

        raw_data = tree.xpath(
            '//div[@class="complex-stat-table_body__UI0Lj"]'
            '//div[@class="complex-stat-table_row__Jiu1w complex-stat-table__standingRow__KJaSV complex-stat-table__bottom8__h6iNh complex-stat-table__euroleague__zV5Mu"]'
            '//div[@class="complex-stat-table_cell__yQmD8"]/text()')

        for item in listing:
            if item[0] in standings:
                standings['Images/' + item[1] + '.png'] = item[1]
            else:
                standings['Images/' + item[1] + '.png'] = item[0], raw_data[i: i + 7]
                i += num_of_total_stat_cats
    return standings
