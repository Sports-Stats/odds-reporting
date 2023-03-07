from odds_reporting.clients import LiveScoreClient
from odds_reporting.clients import OddsApiClient

live_score = LiveScoreClient()
odds_client = OddsApiClient()


def get_teams(season_type):
    """Get teams for a league

    Parameters:
        season_type (str): Type of season (ex. march madness)
    """
    return live_score.get_teams(
        sport="basketball", league="ncaa", season_type=season_type
    )


def get_matches(date):
    """Get matches for upcoming games

    Parameters:
        date (str): Date of games (format YYYYMMDD)
    """
    all_matches = odds_client.get_matches_by_date(sport="basketball", date=date)[
        "Stages"
    ]

    scd = "ncaa-men"
    for league in all_matches:
        if league["Scd"] == scd:
            league_matches = league
    # for matches in all_matches[scd]["Events"]:
