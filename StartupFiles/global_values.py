"""Constant Variables in standings.py"""

"""Team name"""
G1 = '//div[@class="complex-stat-table_body__UF_OT"]' \
     '//div[@class="complex-stat-table_row__XPRhI complex-stat-table__standingRow__bPVTR complex-stat-table__euroLeagueNewSystem__Y6qYU complex-stat-table__euroleague__z1bG4"]' \
     '//div[@class="complex-stat-table_sticky__KBwSE"]' \
     '//div[@class="complex-stat-table_mainClubName__drf8e w-72 md:w-auto flex flex-row items-center gap-1"]' \
     '/text()'

"""Team Rank"""
G2 = '//div[@class="complex-stat-table_body__UF_OT"]' \
     '//div[@class="complex-stat-table_row__XPRhI complex-stat-table__standingRow__bPVTR complex-stat-table__euroLeagueNewSystem__Y6qYU complex-stat-table__euroleague__z1bG4"]' \
     '//div[@class="complex-stat-table_sticky__KBwSE"]' \
     '//div[@class="complex-stat-table_cell__XIEO5 complex-stat-table__right__ge6x9"]' \
     '//p[@class="font-modelica text-primary text-base font-normal"]' \
     '/text()'

"""Data"""
G3 = '//div[@class="complex-stat-table_body__UF_OT"]' \
     '//div[@class="complex-stat-table_row__XPRhI complex-stat-table__standingRow__bPVTR complex-stat-table__euroLeagueNewSystem__Y6qYU complex-stat-table__euroleague__z1bG4"]' \
     '//p[@class="font-modelica text-primary text-sm font-normal complex-stat-table_cell__XIEO5"]' \
     '/text()'


"""Constant Variables in extract_bio_stats.py"""

S_PREFIX = '//div[@class="stats-table_table__cD0GH"]//div[@class="stats-table_colGroup__zvDOb"]'\
         '//div[@class="stats-table_row__wEFis stats-table__hasLink__D8bNs"]'

S1 = S_PREFIX + '//div[@class="stats-table_cell___AWMd"][1]/text()'

S2 = S_PREFIX + '//div[@class="stats-table_cell___AWMd"][2]/text()'

S3 = S_PREFIX + '//span[@class="stats-table_vs__xkbtN"]/text()'

V_PREFIX = '//div[@class="tab-season_phaseTablesWrap__DK_Y8"]//div[@class="stats-table_table__cD0GH"]'\
           '//div[@class="stats-table_main__ZIFxd"]'

V1 = V_PREFIX + '//div[@data-key="Min-Pts-2FG-3FG-FT"]'\
                '//div[@class="stats-table_row__wEFis"]//div[@class="stats-table_cell___AWMd"]/text()'

V2 = V_PREFIX + '//div[@data-key="O-D-T"]'\
                '//div[@class="stats-table_row__wEFis"]//div[@class="stats-table_cell___AWMd"]/text()'

V3 = V_PREFIX + '//div[@data-key="As-St-To"]'\
                '//div[@class="stats-table_row__wEFis"]//div[@class="stats-table_cell___AWMd"]/text()'

V4 = V_PREFIX + '//div[@data-key="Fv-Ag"]'\
                '//div[@class="stats-table_row__wEFis"]//div[@class="stats-table_cell___AWMd"]/text()'

V5 = V_PREFIX + '//div[@data-key="Cm-Rv"]'\
                '//div[@class="stats-table_row__wEFis"]//div[@class="stats-table_cell___AWMd"]/text()'

V6 = V_PREFIX + '//div[@data-key="PIR"]'\
                '//div[@class="stats-table_row__wEFis"]//div[@class="stats-table_cell___AWMd"]/text()'
