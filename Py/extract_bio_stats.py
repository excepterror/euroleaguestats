import requests
import logging

from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from kivy.properties import StringProperty, DictProperty

from Py.extract_game_stats import access_per_game_stats


def extract_players_data(player_tree, player_name, player_url):
    """Extract player's info, average and total stats"""

    "Extract info"

    text_1, text_2, player_photo, notification = StringProperty(''), StringProperty(''), StringProperty(''), ''
    data = DictProperty([])

    pos = player_tree.xpath(
        '//div[@class="player-hero_inner__rwwR_ side-gaps_sectionSideGaps__v5CKj"]'
        '//div[@class="hero-info_position__GDXbP"]/text()')
    info_1 = player_tree.xpath(
        '//div[@class="player-hero_inner__rwwR_ side-gaps_sectionSideGaps__v5CKj"]'
        '//ul[@class="hero-info_dataList__kKi0z"]//li[@class="hero-info_dataItem__UbJZU"]'
        '//span[@class="hero-info_key__Pcrzp"]/text()')
    info_2 = player_tree.xpath(
        '//div[@class="player-hero_inner__rwwR_ side-gaps_sectionSideGaps__v5CKj"]'
        '//ul[@class="hero-info_dataList__kKi0z"]//li[@class="hero-info_dataItem__UbJZU"]'
        '//b[@class="hero-info_value__XFJeE"]/text()')

    info = list()
    for i, j, in zip(info_1, info_2):
        s = i + ': ' + j
        info.append(s)

    try:
        '''Check if photo already exists.'''
        player_photo = player_name + '.png'
        if player_photo.strip('.png') == player_name:
            pass
        if len(player_url) != 0:
            try:
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                response = session.get(player_url)
                player_photo = player_name + '.png'
                with open(player_photo, 'wb') as f:
                    f.write(response.content)
            except requests.exceptions.ConnectTimeout as conn_timeout:
                logging.warning('Connection timed-out: {}'.format(conn_timeout))
            except Exception as e:
                logging.warning(e)
        else:
            player_photo = 'Images/NoImage.jpg'
    except requests.exceptions.RequestException as request_exceptions:
        logging.warning('Requests exceptions occurred: {}'.format(request_exceptions))

    try:
        text_1 = pos[0]
        text_2 = info[0][12:] + '\n' + info[1][7:] + ' cm' + '\n' + info[2][5:]
    except IndexError as index_error:
        logging.warning('Index error occurred [extract_bio_stats.py]: {}'.format(index_error))

    "Extract average, total stats. Extract stats by game."

    average_stats = player_tree.xpath(
        '//div[@class="tab-season_seasonTableWrap__I0CUd"]//div[@class="stats-table_table__dpgY7"]'
        '//div[@class="stats-table_row__ttfiG"][3]//div[@class="stats-table_cell__hdmqc"]/text()')
    total_stats = player_tree.xpath(
        '//div[@class="tab-season_seasonTableWrap__I0CUd"]//div[@class="stats-table_table__dpgY7"]'
        '//div[@class="stats-table_row__ttfiG"][2]//div[@class="stats-table_cell__hdmqc"]/text()')
    opponents = player_tree.xpath('//div[@class="stats-table_table__dpgY7"]')

    if len(average_stats) and len(total_stats) and len(opponents) != 0:
        data = access_per_game_stats(player_tree, player_name)
    else:
        text = 'No games played by ' + player_name + ' yet!'
        notification = text

    return text_1, text_2, player_photo, average_stats, total_stats, data, notification
