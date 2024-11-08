import os.path

import requests
import logging
import concurrent.futures

from kivy.properties import StringProperty, DictProperty

from PyCoreFiles.extract_game_stats import access_per_game_stats


def fetch_a_photo(url, player_name):
    if os.path.isfile('./' + player_name + '.png'):
        '''Check if photos are already present'''
        pass
    else:
        try:
            response = requests.get(url)
            logging.info('extract_bio_stats.py status_code | player_name | url: {} | {} | {}'.format(response.status_code, player_name, url))
        except requests.exceptions.Timeout as timeout_error:
            logging.warning('extract_bio_stats.py The request timed out: {}'.format(timeout_error))
        except requests.exceptions.ConnectionError as conn_error:
            logging.warning('extract_bio_stats.py Connection error occurred: {}'.format(conn_error))
        else:
            player_photo = player_name + '.png'
            with open(player_photo, 'wb') as f:
                f.write(response.content)
    return


def download_photos(grid_roster):
    photo_urls = list()
    urls = list(grid_roster.values())
    for _ in urls:
        photo_urls.append(_[1])
    players_names = list(grid_roster.keys())
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(fetch_a_photo, photo_urls, players_names)
    except TimeoutError as timeout_error:
        logging.warning('Timeout error occurred: {}'.format(timeout_error))
    return players_names


def extract_players_data(player_tree, player_name):
    """Extract player's info, average and total stats"""
    if player_tree is not None:
        "Extract info"
        text_1, text_2, error_message = StringProperty(''), StringProperty(''), ''
        data = DictProperty([])

        pos = player_tree.xpath(
            '//div[@class="player-hero_inner__xxqLy side-gaps_sectionSideGaps__8hmjO"]'
            '//div[@class="hero-info_position__lF64l"]/text()')
        info_1 = player_tree.xpath(
            '//div[@class="player-hero_inner__xxqLy side-gaps_sectionSideGaps__8hmjO"]'
            '//ul[@class="hero-info_dataList__0qv4h"]//li[@class="hero-info_dataItem__Y2xZN"]'
            '//span[@class="hero-info_key__ZcDGE"]/text()')
        info_2 = player_tree.xpath(
            '//div[@class="player-hero_inner__xxqLy side-gaps_sectionSideGaps__8hmjO"]'
            '//ul[@class="hero-info_dataList__0qv4h"]//li[@class="hero-info_dataItem__Y2xZN"]'
            '//b[@class="hero-info_value__zklni"]/text()')

        info = list()
        for i, j, in zip(info_1, info_2):
            s = i + ': ' + j
            info.append(s)

        try:
            text_1 = pos[0]
            text_2 = info[0][12:] + ' | ' + info[1][7:] + ' cm' + ' | ' + info[2][5:]
        except IndexError as index_error:
            logging.warning('Index error occurred [extract_bio_stats.py]: {}'.format(index_error))

        "Extract average, total stats. Extract stats by game."

        average_stats = player_tree.xpath(
            '//div[@class="tab-season_seasonTableWrap__ahJrw"]//div[@class="stats-table_table__cD0GH"]'
            '//div[@class="stats-table_row__wEFis"][3]//div[@class="stats-table_cell___AWMd"]/text()')
        print(average_stats)
        total_stats = player_tree.xpath(
            '//div[@class="tab-season_seasonTableWrap__ahJrw"]//div[@class="stats-table_table__cD0GH"]'
            '//div[@class="stats-table_row__wEFis"][2]//div[@class="stats-table_cell___AWMd"]/text()')
        print(total_stats)
        opponents = player_tree.xpath('//div[@class="stats-table_table__cD0GH"]')
        print(opponents)

        if len(average_stats) and len(total_stats) and len(opponents) != 0:
            data = access_per_game_stats(player_tree, player_name)
        else:
            text = 'No games played by ' + player_name + ' yet!'
            error_message = text
        return total_stats, average_stats, text_2, text_1, data, error_message, player_name
    else:
        return []
