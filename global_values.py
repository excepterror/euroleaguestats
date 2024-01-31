"""roster.json Google Drive URL"""

JSON_URL = 'https://drive.google.com/uc?export=download&id=17GNgonM2VVtnNEOF2G8id26QDPREsb3g'

"""Constant Variables in standings.py"""

G1 = '//div[@class="complex-stat-table_body__UI0Lj"]' \
     '//div[@class="complex-stat-table_row__Jiu1w complex-stat-table__standingRow__KJaSV complex-stat-table__euroLeagueNewSystem__jSHq9 complex-stat-table__euroleague__zV5Mu"]' \
     '//div[@class="complex-stat-table_sticky__TsX4D"]' \
     '//span[@class="complex-stat-table_mainClubName__1CeH5" or @class="complex-stat-table_mainClubName__1CeH5 complex-stat-table__long__YuBt_"]' \
     '/text()'

G2 = '//div[@class="complex-stat-table_body__UI0Lj"]' \
     '//div[@class="complex-stat-table_row__Jiu1w complex-stat-table__standingRow__KJaSV complex-stat-table__euroLeagueNewSystem__jSHq9 complex-stat-table__euroleague__zV5Mu"]' \
     '//div[@class="complex-stat-table_sticky__TsX4D"]' \
     '//div[@class="complex-stat-table_cell__yQmD8 complex-stat-table__right__7D_Wn"]' \
     '//span/text()'

G3 = '//div[@class="complex-stat-table_body__UI0Lj"]' \
     '//div[@class="complex-stat-table_row__Jiu1w complex-stat-table__standingRow__KJaSV complex-stat-table__euroLeagueNewSystem__jSHq9 complex-stat-table__euroleague__zV5Mu"]' \
     '//div[@class="complex-stat-table_cell__yQmD8"]/text()'


"""Constant Variables in stats.py"""

S_PREFIX = '//div[@class="stats-table_table__dpgY7"]//div[@class="stats-table_colGroup__hJ_6t"]'\
         '//div[@class="stats-table_row__ttfiG stats-table__hasLink__N5MQe"]'

S1 = S_PREFIX + '//div[@class="stats-table_cell__hdmqc"][1]/text()'

S2 = S_PREFIX + '//div[@class="stats-table_cell__hdmqc"][2]/text()'

S3 = S_PREFIX + '//span[@class="stats-table_vs__jx4I1"]/text()'

V_PREFIX = '//div[@class="tab-season_phaseTablesWrap__CijM6"]//div[@class="stats-table_table__dpgY7"]'\
           '//div[@class="stats-table_main__zob_I"]'

V1 = V_PREFIX + '//div[@data-key="Min-Pts-2FG-3FG-FT"]'\
                '//div[@class="stats-table_row__ttfiG"]//div[@class="stats-table_cell__hdmqc"]/text()'

V2 = V_PREFIX + '//div[@data-key="O-D-T"]'\
                '//div[@class="stats-table_row__ttfiG"]//div[@class="stats-table_cell__hdmqc"]/text()'

V3 = V_PREFIX + '//div[@data-key="As-St-To"]'\
                '//div[@class="stats-table_row__ttfiG"]//div[@class="stats-table_cell__hdmqc"]/text()'

V4 = V_PREFIX + '//div[@data-key="Fv-Ag"]'\
                '//div[@class="stats-table_row__ttfiG"]//div[@class="stats-table_cell__hdmqc"]/text()'

V5 = V_PREFIX + '//div[@data-key="Cm-Rv"]'\
                '//div[@class="stats-table_row__ttfiG"]//div[@class="stats-table_cell__hdmqc"]/text()'

V6 = V_PREFIX + '//div[@data-key="PIR"]'\
                '//div[@class="stats-table_row__ttfiG"]//div[@class="stats-table_cell__hdmqc"]/text()'
