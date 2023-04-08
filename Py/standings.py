import logging
import requests
from lxml import etree
from itertools import zip_longest

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
        q_stars = list()
        tree = etree.HTML(response.content)

        teams_and_ranking = tree.xpath(
            '//div[@class="complex-stat-table_body__yaXeJ"]'
            '//div[@class="complex-stat-table_row__1P6us complex-stat-table__standingRow__1cfez"]'
            '//div[@class="complex-stat-table_sticky__2I3pT"]'
            '//span[@class="complex-stat-table_mainClubName__3IMZJ" or "complex-stat-table_mainClubName__3IMZJ complex-stat-table__long__MGBQU"]'
            '/text()')
        while a < len(teams_and_ranking) - 3:
            b = a + 1
            listing.append((teams_and_ranking[a], teams_and_ranking[b]))
            a = a + 5

        qualified_index = tree.xpath(
            '//div[@class="complex-stat-table_body__yaXeJ"]'
            '//div[@class="complex-stat-table_row__1P6us complex-stat-table__standingRow__1cfez"]'
            '//div[@class="complex-stat-table_sticky__2I3pT"]'
            '//span[@class="complex-stat-table_mainClubName__3IMZJ"]')
        for q in qualified_index:
            if len(q.findall("sup")) != 0:
                q_stars.append('*')
            else:
                q_stars.append('')
        teams_ranking_q = list(zip_longest(listing, q_stars, fillvalue=''))

        raw_data = tree.xpath(
            '//div[@class="complex-stat-table_body__yaXeJ"]'
            '//div[@class="complex-stat-table_row__1P6us complex-stat-table__standingRow__1cfez"]'
            '//div[@class="complex-stat-table_cell__1lxC7"]/text()')

        for item in teams_ranking_q:
            if item[1] == '*':
                logging.info('Team qualified: {}. {}'.format(item[0][0], item[0][1]))

        try:
            i = 0
            num_of_teams = len(teams_and_ranking) / 5  # 5: team name occurrence every five items in :list: teams_and_ranking
            num_of_total_stat_cats = 11
            while i <= num_of_teams * num_of_total_stat_cats - 4:
                for item in teams_ranking_q:
                    if item[0][1] in standings:
                        standings['Images/' + item[0][1] + '.png'] = teams_ranking_q[0][1]
                    elif item[1] == '*':
                        standings['Images/' + item[0][1] + '.png'] = '[color=FF6600]' + item[0][0] + '(Q)' + '[/color]', raw_data[i:i + 7]
                    else:
                        standings['Images/' + item[0][1] + '.png'] = item[0][0], raw_data[i:i + 7]  # we only want the first seven statistical categories for each team
                    i += num_of_total_stat_cats
        except IndexError as idx_err:
            logging.warning('Index i error occurred: {}'.format(idx_err))
    return standings
