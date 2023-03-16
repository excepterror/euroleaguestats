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
        listing = list()
        rankings = list()
        tree = etree.HTML(response.content)

        teams_and_ranking = tree.xpath(
            '//div[@class="complex-stat-table_body__yaXeJ"]'
            '//div[@class="complex-stat-table_row__1P6us complex-stat-table__standingRow__1cfez"]'
            '//div[@class="complex-stat-table_sticky__2I3pT"]'
            '//span[@class="complex-stat-table_mainClubName__3IMZJ" or "complex-stat-table_mainClubName__3IMZJ complex-stat-table__long__MGBQU"]'
            '/text()')

        qualified_index = tree.xpath(
            '//div[@class="complex-stat-table_body__yaXeJ"]'
            '//div[@class="complex-stat-table_row__1P6us complex-stat-table__standingRow__1cfez"]'
            '//div[@class="complex-stat-table_sticky__2I3pT"]'
            '//span[@class="complex-stat-table_mainClubName__3IMZJ"]//sup/text()')

        raw_data = tree.xpath(
            '//div[@class="complex-stat-table_body__yaXeJ"]'
            '//div[@class="complex-stat-table_row__1P6us complex-stat-table__standingRow__1cfez"]'
            '//div[@class="complex-stat-table_cell__1lxC7"]/text()')

        '''Concatenate ranking and name.'''
        try:
            i, m, k = 0, 0, 0
            while k < len(teams_and_ranking) - 5:
                k = 5 * i
                m = k + 1
                try:
                    if qualified_index[i] == '*':
                        logging.warning('Team is qualified: {}'.format(teams_and_ranking[m]))
                        listing.append(teams_and_ranking[m])
                        rankings.append(('[color=FF6600]' + teams_and_ranking[k] + '[/color]'))
                except IndexError as idx_err:
                    logging.warning('Team is not qualified: {}'.format(idx_err))
                    listing.append(teams_and_ranking[m])
                    rankings.append((teams_and_ranking[k]))
                i += 1
        except IndexError as idx_err:
            logging.warning('Index error 1 occurred: {}'.format(idx_err))

        try:
            i, j = 0, 0
            num_of_teams = len(teams_and_ranking) / 5  # 5: team name occurrence every five items in :list: teams_and_ranking
            num_of_total_stat_cats = 11
            while i <= num_of_teams * num_of_total_stat_cats - 4:
                if listing[j] in standings:
                    standings['Images/' + listing[j] + '.png'] = listing[j]
                else:
                    standings['Images/' + listing[j] + '.png'] = rankings[j], raw_data[i:i + 7]  # we only want the first seven statistical categories for each team
                i += num_of_total_stat_cats
                j += 1
        except IndexError as idx_err:
            logging.warning('Index error 2 occurred: {}'.format(idx_err))

    return standings
