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
        from StartupFiles.global_values import S1, S2, S3, V1, V2, V3, V4, V5, V6
    except ModuleNotFoundError as error:
        logging.warning('global_values.py is missing: {}'.format(error))
    else:

        min_ft = list()
        odt = list()
        as_to = list()
        fv_ag = list()
        cm_rv = list()
        pir = list()

        rounds_played_by_player = tree.xpath(S1)
        opponents_code = tree.xpath(S2)
        at_vs = tree.xpath(S3)
        stats_by_game_min_ft = tree.xpath(V1)
        stats_by_game_odt = tree.xpath(V2)
        stats_by_game_as_to = tree.xpath(V3)
        stats_by_game_fv_ag = tree.xpath(V4)
        stats_by_game_cm_rv = tree.xpath(V5)
        stats_by_game_pir = tree.xpath(V6)

        play_in_counter = 0
        playoff_games_counter = 0
        semifinal_games_counter = 0
        for item in rounds_played_by_player:
            if item.startswith('G'):
                playoff_games_counter += 1
            if item.startswith('S') or item.startswith('C') or item.startswith('3P'):
                semifinal_games_counter += 1
            if item in ('35', '36'):
                play_in_counter += 1
        regular_games_counter = len(rounds_played_by_player) - (play_in_counter + playoff_games_counter + semifinal_games_counter)

        if playoff_games_counter == 0 and semifinal_games_counter == 0:
            if play_in_counter == 0:
                min_ft = stats_by_game_min_ft[:-10]
                odt = stats_by_game_odt[:-6]
                as_to = stats_by_game_as_to[:-6]
                fv_ag = stats_by_game_fv_ag[:-4]
                cm_rv = stats_by_game_cm_rv[:-4]
                pir = stats_by_game_pir[:-2]

            """Check if the player has participated in a play-in game."""
            if play_in_counter != 0:
                min_ft = stats_by_game_min_ft[:5 * regular_games_counter]
                del stats_by_game_min_ft[:5 * regular_games_counter + 10]
                min_ft.extend(stats_by_game_min_ft[:5 * play_in_counter])

                odt = stats_by_game_odt[:3 * regular_games_counter]
                del stats_by_game_odt[:3 * regular_games_counter + 6]
                odt.extend(stats_by_game_odt[:3 * play_in_counter])

                as_to = stats_by_game_as_to[:3 * regular_games_counter]
                del stats_by_game_as_to[:3 * regular_games_counter + 6]
                as_to.extend(stats_by_game_as_to[:3 * play_in_counter])

                fv_ag = stats_by_game_fv_ag[:2 * regular_games_counter]
                del stats_by_game_fv_ag[:2 * regular_games_counter + 4]
                fv_ag.extend(stats_by_game_fv_ag[:2 * play_in_counter])

                cm_rv = stats_by_game_cm_rv[:2 * regular_games_counter]
                del stats_by_game_cm_rv[:2 * regular_games_counter + 4]
                cm_rv.extend(stats_by_game_cm_rv[:2 * play_in_counter])

                pir = stats_by_game_pir[:1 * regular_games_counter]
                del stats_by_game_pir[:1 * regular_games_counter + 2]
                pir.extend(stats_by_game_pir[:1 * play_in_counter])

        if playoff_games_counter != 0:
            if semifinal_games_counter == 0:

                min_ft = stats_by_game_min_ft[:5 * regular_games_counter]
                del stats_by_game_min_ft[:5 * regular_games_counter + 10]
                min_ft.extend(stats_by_game_min_ft[:5 * play_in_counter])
                del stats_by_game_min_ft[:5 * play_in_counter + 10]
                min_ft.extend(stats_by_game_min_ft[:5 * playoff_games_counter])

                odt = stats_by_game_odt[:3 * regular_games_counter]
                del stats_by_game_odt[:3 * regular_games_counter + 6]
                odt.extend(stats_by_game_min_ft[:3 * play_in_counter])
                del stats_by_game_odt[:3 * play_in_counter + 6]
                odt.extend(stats_by_game_odt[:3 * playoff_games_counter])

                as_to = stats_by_game_as_to[:3 * regular_games_counter]
                del stats_by_game_as_to[:3 * regular_games_counter + 6]
                as_to.extend(stats_by_game_as_to[:3 * play_in_counter])
                del stats_by_game_as_to[:3 * play_in_counter + 6]
                as_to.extend(stats_by_game_as_to[:3 * playoff_games_counter])

                fv_ag = stats_by_game_fv_ag[:2 * regular_games_counter]
                del stats_by_game_fv_ag[:2 * regular_games_counter + 4]
                fv_ag.extend(stats_by_game_fv_ag[:2 * play_in_counter])
                del stats_by_game_fv_ag[:2 * play_in_counter + 4]
                fv_ag.extend(stats_by_game_fv_ag[:2 * playoff_games_counter])

                cm_rv = stats_by_game_cm_rv[:2 * regular_games_counter]
                del stats_by_game_cm_rv[:2 * regular_games_counter + 4]
                cm_rv.extend(stats_by_game_cm_rv[:2 * play_in_counter])
                del stats_by_game_cm_rv[:2 * play_in_counter + 4]
                cm_rv.extend(stats_by_game_cm_rv[:2 * playoff_games_counter])

                pir = stats_by_game_pir[:1 * regular_games_counter]
                del stats_by_game_pir[:1 * regular_games_counter + 2]
                pir.extend(stats_by_game_pir[:1 * play_in_counter])
                del stats_by_game_pir[:1 * play_in_counter + 2]
                pir.extend(stats_by_game_pir[:1 * playoff_games_counter])

            if semifinal_games_counter != 0:
                min_ft = stats_by_game_min_ft[:5 * regular_games_counter]
                del stats_by_game_min_ft[:5 * regular_games_counter + 10]
                min_ft.extend(stats_by_game_min_ft[:5 * play_in_counter])
                del stats_by_game_min_ft[:5 * play_in_counter + 10]
                min_ft.extend(stats_by_game_min_ft[:5 * playoff_games_counter])
                del stats_by_game_min_ft[:5 * playoff_games_counter + 10]
                min_ft.extend(stats_by_game_min_ft[:5 * semifinal_games_counter])

                odt = stats_by_game_odt[:3 * regular_games_counter]
                del stats_by_game_odt[:3 * regular_games_counter + 6]
                odt.extend(stats_by_game_min_ft[:3 * play_in_counter])
                del stats_by_game_odt[:3 * play_in_counter + 6]
                odt.extend(stats_by_game_odt[:3 * playoff_games_counter])
                del stats_by_game_odt[:3 * playoff_games_counter + 6]
                odt.extend(stats_by_game_odt[:3 * semifinal_games_counter])

                as_to = stats_by_game_as_to[:3 * regular_games_counter]
                del stats_by_game_as_to[:3 * regular_games_counter + 6]
                as_to.extend(stats_by_game_as_to[:3 * play_in_counter])
                del stats_by_game_as_to[:3 * play_in_counter + 6]
                as_to.extend(stats_by_game_as_to[:3 * playoff_games_counter])
                del stats_by_game_as_to[:3 * playoff_games_counter + 6]
                as_to.extend(stats_by_game_as_to[:3 * semifinal_games_counter])

                fv_ag = stats_by_game_fv_ag[:2 * regular_games_counter]
                del stats_by_game_fv_ag[:2 * regular_games_counter + 4]
                fv_ag.extend(stats_by_game_fv_ag[:2 * play_in_counter])
                del stats_by_game_fv_ag[:2 * play_in_counter + 4]
                fv_ag.extend(stats_by_game_fv_ag[:2 * playoff_games_counter])
                del stats_by_game_fv_ag[:2 * playoff_games_counter + 4]
                fv_ag.extend(stats_by_game_fv_ag[:2 * semifinal_games_counter])

                cm_rv = stats_by_game_cm_rv[:2 * regular_games_counter]
                del stats_by_game_cm_rv[:2 * regular_games_counter + 4]
                cm_rv.extend(stats_by_game_cm_rv[:2 * play_in_counter])
                del stats_by_game_cm_rv[:2 * play_in_counter + 4]
                cm_rv.extend(stats_by_game_cm_rv[:2 * playoff_games_counter])
                del stats_by_game_cm_rv[:2 * playoff_games_counter + 4]
                cm_rv.extend(stats_by_game_cm_rv[:2 * semifinal_games_counter])

                pir = stats_by_game_pir[:1 * regular_games_counter]
                del stats_by_game_pir[:1 * regular_games_counter + 2]
                pir.extend(stats_by_game_pir[:1 * play_in_counter])
                del stats_by_game_pir[:1 * play_in_counter + 2]
                pir.extend(stats_by_game_pir[:1 * playoff_games_counter])
                del stats_by_game_pir[:1 * playoff_games_counter + 2]
                pir.extend(stats_by_game_pir[:1 * semifinal_games_counter])

        stats_by_game = [min_ft, odt, as_to, fv_ag, cm_rv, pir]

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
