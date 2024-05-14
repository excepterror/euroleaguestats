from View.HomeScreen.home_screen import HomeScreenView
from View.MenuScreen.menu_screen import MenuScreenView
from View.WelcomeScreen.welcome_screen import WelcomeScreenView
from View.StandingsScreen.standings_screen import StandingsScreenView
from View.TeamsScreen.teams_screen import TeamsScreenView
from View.WaitScreen.wait_screen import WaitScreenView
from View.RosterScreen.roster_screen import RosterScreenView
from View.StatisticsScreen.statistics_screen import StatisticsScreenView
from View.DisplayStatisticsScreen.display_statistics_screen import DisplayStatisticsScreenView
from View.DisplayStatisticsByGameScreen.display_statistics_by_game_screen import DisplayStatisticsByGameScreenView

screens = {
    "home screen": {
        "view": HomeScreenView,
        "kv": "View/HomeScreen/home_screen.kv"
    },
    "menu screen": {
        "view": MenuScreenView,
        "kv": "View/MenuScreen/menu_screen.kv"
    },
    "welcome screen": {
        "view": WelcomeScreenView,
        "kv": "View/WelcomeScreen/welcome_screen.kv",
        "on back-click screen transition": "menu screen"
    },
    "standings screen": {
        "view": StandingsScreenView,
        "kv": "View/StandingsScreen/standings_screen.kv",
        "on back-click screen transition": "menu screen"
    },
    "teams screen": {
        "view": TeamsScreenView,
        "kv": "View/TeamsScreen/teams_screen.kv",
        "on back-click screen transition": "menu screen"
    },
    "wait screen": {
        "view": WaitScreenView,
        "kv": "View/WaitScreen/wait_screen.kv",
        "on back-click screen transition": None
    },
    "roster screen": {
        "view": RosterScreenView,
        "kv": "View/RosterScreen/roster_screen.kv",
        "on back-click screen transition": "teams screen"
    },
    "statistics screen": {
        "view": StatisticsScreenView,
        "kv": "View/StatisticsScreen/statistics_screen.kv",
        "on back-click screen transition": "roster screen"
    },
    "display statistics screen": {
        "view": DisplayStatisticsScreenView,
        "kv": "View/DisplayStatisticsScreen/display_statistics_screen.kv",
        "on back-click screen transition": "statistics screen"
    },
    "display statistics by game screen": {
        "view": DisplayStatisticsByGameScreenView,
        "kv": "View/DisplayStatisticsByGameScreen/display_statistics_by_game_screen.kv",
        "on back-click screen transition": "statistics screen"
    }
}
