import os.path

import requests
import logging
import concurrent.futures

from PyCoreFiles.extract_game_stats import access_per_game_stats


def fetch_a_photo(url, player_name):
    file_path = os.path.join('.', f"{player_name}.png")
    if os.path.isfile(file_path):
        '''Check if photos are already present.'''
        pass
    else:
        try:
            response = requests.get(url)
            logging.info(f'extract_bio_stats.py status_code | player_name | url: {response.status_code} | {player_name} | {url}')
        except requests.exceptions.Timeout as timeout_error:
            logging.warning(f'extract_bio_stats.py The request timed out: {timeout_error}')
        except requests.exceptions.ConnectionError as conn_error:
            logging.warning(f'extract_bio_stats.py Connection error occurred: {conn_error}')
        else:
            player_photo = player_name + '.png'
            with open(player_photo, 'wb') as f:
                f.write(response.content)
    return


def download_photos(grid_roster):
    photo_urls = [info[1] for info in grid_roster.values()]
    players_names = list(grid_roster.keys())
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(fetch_a_photo, photo_urls, players_names)
    except TimeoutError as timeout_error:
        logging.warning(f'Timeout error occurred: {timeout_error}')
    return players_names


def extract_players_data(player_tree, player_name):
    """Extract player's info, average and total stats"""
    if player_tree is not None:
        "Extract info"
        number = player_tree.xpath('//p[contains(text(), "#")]/text()')[0]
        position = player_tree.xpath('//p[text()="Guard" or text()="Forward" or text()="Center"]/text()')
        position = position[0] if position else None
        labels = player_tree.xpath('//div[@class="flex flex-col gap-2"]/p[1]/text()')
        values = player_tree.xpath('//div[@class="flex flex-col gap-2"]/p[2]/text()')

        details = {}

        if number:
            details['Number'] = number
        if position:
            details['Position'] = position
        for label, value in zip(labels, values):
            details[label.strip()] = value.strip()

        text_1, text_2, error_message = '', '', ''

        try:
            text_1 = details['Number'] + ' | ' + details['Position']
            text_2 = details['Nationality'] + ' | ' + details['Height']
        except IndexError as index_error:
            logging.warning(f'Index error occurred [extract_bio_stats.py]: {index_error}')

        "Extract average, total stats. Extract stats by game."

        average_stats = player_tree.xpath(
            '//div[@class="tab-season_seasonTableWrap__ahJrw"]//div[@class="stats-table_table__cD0GH"]'
            '//div[@class="stats-table_row__wEFis"][3]//div[@class="stats-table_cell___AWMd"]/text()')
        total_stats = player_tree.xpath(
            '//div[@class="tab-season_seasonTableWrap__ahJrw"]//div[@class="stats-table_table__cD0GH"]'
            '//div[@class="stats-table_row__wEFis"][2]//div[@class="stats-table_cell___AWMd"]/text()')
        opponents = player_tree.xpath('//div[@class="stats-table_table__cD0GH"]')

        data = {}

        if len(average_stats) and len(total_stats) and len(opponents) != 0:
            data = access_per_game_stats(player_tree, player_name)
        else:
            text = 'No games played by ' + player_name + ' yet!'
            error_message = text
        return total_stats, average_stats, text_2, text_1, data, error_message, player_name
    else:
        return []
