import logging

logging.getLogger().setLevel(logging.INFO)

"""Template for Total Statistics"""
template_1 = {'Games:': [1], 'Games Started:': [2], 'Minutes:': [3], 'Points:': [4], '2-Point Field Goals:': [5],
              '3-Point Field Goals:': [6], 'Free Throws:': [7], 'Offensive Rebounds:': [8], 'Defensive Rebounds:': [9],
              'Total Rebounds:': [10], 'Assists:': [11], 'Steals:': [12], 'Turnovers:': [13],
              'Blocks in Favour:': [14], 'Blocks Against:': [15], 'Fouls Committed:': [16], 'Fouls Drawn:': [17],
              'Point Index Rating:': [18]}

"""Template for Average Statistics"""
template_2 = {'Minutes:': [3], 'Points:': [4], '2-Point Field Goals:': [5], '3-Point Field Goals:': [6],
              'Free Throws:': [7], 'Offensive Rebounds:': [8], 'Defensive Rebounds:': [9],
              'Total Rebounds:': [10], 'Assists:': [11], 'Steals:': [12], 'Turnovers:': [13],
              'Blocks in Favour:': [14], 'Blocks Against:': [15], 'Fouls Committed:': [16], 'Fouls Drawn:': [17],
              'Point Index Rating:': [18]}

teams_codes = {'BER': 'ALBA Berlin',
               'EFS': 'Anadolu Efes Istanbul',
               'ASM': 'AS Monaco',
               'EA7': 'EA7 Emporio Armani Milan',
               'BKN': 'Baskonia Vitoria-Gasteiz',
               'CZV': 'Crvena Zvezda Meridianbet Belgrade',
               'PAR': 'Partizan Mozzart Bet Belgrade',
               'BAR': 'FC Barcelona',
               'BAY': 'FC Bayern Munich',
               'FBB': 'Fenerbahce Beko Istanbul',
               'ASV': 'LDLC ASVEL Villeurbanne',
               'MTA': 'Maccabi Playtika Tel Aviv',
               'OLY': 'Olympiacos Piraeus',
               'PAO': 'Panathinaikos AKTOR Athens',
               'RMB': 'Real Madrid',
               'VBC': 'Valencia Basket',
               'ZAL': 'Zalgiris Kaunas',
               'VIR': 'Virtus Segafredo Bologna'}


def update_dict(stats, j=0, dict_with_stats=None):
    """Used for dictionaries total_statistics and average_statistics.
    'kind of stats' can be average_stats or total_stats. Both objects are lists.
    """

    stats = [stats[stat] for stat in range(len(stats))]
    if len(stats) == 16:
        dict_with_stats = template_2
    elif len(stats) == 18:
        dict_with_stats = template_1
    for k, v in dict_with_stats.items():
        dict_with_stats[k] = stats[j]
        j += 1
    return dict_with_stats


def access_per_game_stats(tree, name):
    """Fetch stats for all games in each phase."""
    try:
        import global_values
    except ModuleNotFoundError as error:
        logging.warning('globals.py is missing: {}'.format(error))
    try:
        s1 = global_values.S1
        s2 = global_values.S2
        s3 = global_values.S3
        v1 = global_values.V1
        v2 = global_values.V2
        v3 = global_values.V3
        v4 = global_values.V4
        v5 = global_values.V5
        v6 = global_values.V6
    except NameError as error:
        logging.warning('s1, s2, s3, v1, v2, v3, v4, v5, v6 values are not defined: {}'.format(error))
    else:
        min_ft = list()
        odt = list()
        as_to = list()
        fv_ag = list()
        cm_rv = list()
        pir = list()

        rounds_played_by_player = tree.xpath(s1)
        opponents_code = tree.xpath(s2)
        at_vs = tree.xpath(s3)
        stats_by_game_min_ft = tree.xpath(v1)
        stats_by_game_odt = tree.xpath(v2)
        stats_by_game_as_to = tree.xpath(v3)
        stats_by_game_fv_ag = tree.xpath(v4)
        stats_by_game_cm_rv = tree.xpath(v5)
        stats_by_game_pir = tree.xpath(v6)

        playoff_games_count = 0
        semifinal_games_count = 0
        for item in rounds_played_by_player:
            if item.startswith('G'):
                playoff_games_count += 1
            if item.startswith('S') or item.startswith('C') or item.startswith('3P'):
                semifinal_games_count += 1

        if semifinal_games_count != 0:
            stats_by_game_min_ft = stats_by_game_min_ft[:-10]
            stats_by_game_odt = stats_by_game_odt[:-6]
            stats_by_game_as_to = stats_by_game_as_to[:-6]
            stats_by_game_fv_ag = stats_by_game_fv_ag[:-4]
            stats_by_game_cm_rv = stats_by_game_cm_rv[:-4]
            stats_by_game_pir = stats_by_game_pir[:-2]

            min_ft = stats_by_game_min_ft[-5 * semifinal_games_count:]
            del stats_by_game_min_ft[-5 * semifinal_games_count:]

            odt = stats_by_game_odt[-3 * semifinal_games_count:]
            del stats_by_game_odt[-3 * semifinal_games_count:]

            as_to = stats_by_game_as_to[-3 * semifinal_games_count:]
            del stats_by_game_as_to[-3 * semifinal_games_count:]

            fv_ag = stats_by_game_fv_ag[-2 * semifinal_games_count:]
            del stats_by_game_fv_ag[-2 * semifinal_games_count:]

            cm_rv = stats_by_game_cm_rv[-2 * semifinal_games_count:]
            del stats_by_game_cm_rv[-2 * semifinal_games_count:]

            pir = stats_by_game_pir[-1 * semifinal_games_count:]
            del stats_by_game_pir[-1 * semifinal_games_count:]

        if playoff_games_count != 0:
            stats_by_game_min_ft = stats_by_game_min_ft[:-10]
            stats_by_game_odt = stats_by_game_odt[:-6]
            stats_by_game_as_to = stats_by_game_as_to[:-6]
            stats_by_game_fv_ag = stats_by_game_fv_ag[:-4]
            stats_by_game_cm_rv = stats_by_game_cm_rv[:-4]
            stats_by_game_pir = stats_by_game_pir[:-2]

            min_ft = stats_by_game_min_ft[-5 * playoff_games_count:] + min_ft
            del stats_by_game_min_ft[-5 * playoff_games_count - 10:]

            odt = stats_by_game_odt[-3 * playoff_games_count:] + odt
            del stats_by_game_odt[-3 * playoff_games_count - 6:]

            as_to = stats_by_game_as_to[-3 * playoff_games_count:] + as_to
            del stats_by_game_as_to[-3 * playoff_games_count - 6:]

            fv_ag = stats_by_game_fv_ag[-2 * playoff_games_count:] + fv_ag
            del stats_by_game_fv_ag[-2 * playoff_games_count - 4:]

            cm_rv = stats_by_game_cm_rv[-2 * playoff_games_count:] + cm_rv
            del stats_by_game_cm_rv[-2 * playoff_games_count - 4:]

            pir = stats_by_game_pir[-1 * playoff_games_count:] + pir
            del stats_by_game_pir[-1 * playoff_games_count - 2:]

            stats_by_game_min_ft = stats_by_game_min_ft + min_ft
            stats_by_game_odt = stats_by_game_odt + odt
            stats_by_game_as_to = stats_by_game_as_to + as_to
            stats_by_game_fv_ag = stats_by_game_fv_ag + fv_ag
            stats_by_game_cm_rv = stats_by_game_cm_rv + cm_rv
            stats_by_game_pir = stats_by_game_pir + pir
        else:
            stats_by_game_min_ft = stats_by_game_min_ft[:-10]
            stats_by_game_odt = stats_by_game_odt[:-6]
            stats_by_game_as_to = stats_by_game_as_to[:-6]
            stats_by_game_fv_ag = stats_by_game_fv_ag[:-4]
            stats_by_game_cm_rv = stats_by_game_cm_rv[:-4]
            stats_by_game_pir = stats_by_game_pir[:-2]

        stats_by_game = [stats_by_game_min_ft, stats_by_game_odt, stats_by_game_as_to, stats_by_game_fv_ag,
                         stats_by_game_cm_rv, stats_by_game_pir]

        opponents_by_round_dict = dict()
        for item in opponents_code:
            if item == ' ':
                opponents_code.remove(item)
        for k, v in teams_codes.items():
            for i, item in enumerate(opponents_code):
                if item == k:
                    opponents_code[i] = v
        opponents = [text_1.lower() + ' ' + text_2 for text_1, text_2 in zip(at_vs, opponents_code)]
        for i, k in enumerate(rounds_played_by_player):
            opponents_by_round_dict[k] = opponents[i]
        return [opponents_by_round_dict, stats_by_game, name]
    return
