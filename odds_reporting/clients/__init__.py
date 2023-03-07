import requests

from odds_reporting.config import CONFIG as config


class LiveScoreClient:
    def __init__(self):
        self.api_key = config["apis"]["LiveScore"]["api_key"]
        self.host_header = config["apis"]["LiveScore"]["host_header"]
        self.url = config["apis"]["LiveScore"]["url"]
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host_header,
        }
        self.routes = config["apis"]["LiveScore"]["routes"]
        self.session = requests.Session()
        self.timezone = -7

    def get_leagues(self, sport):
        """Gets list of leagues for the sport

        Parameters:
            sport (str): Name of sport, refer to docs for valid sport names
        """
        route = self.routes["leagues"]["list"]
        headers = self.headers
        params = {"Categpry": sport, "Timezone": self.timezone}
        r = self.session.get(url=f"{self.url}{route}", headers=headers, params=params)
        return r.json()

    def get_teams(self, sport, league, season_type):
        """Get teams for specified league and season type

        Parameters:
            sport (str): Name of sport
            league (str): Name of sports league
            season_type (str): Type of season (ex. march madness)
        """
        route = self.routes["leagues"]["get_tables"]
        headers = self.headers
        params = {"Category": sport, "Ccd": league, "Scd": season_type}
        r = self.session.get(url=f"{self.url}{route}", headers=headers, params=params)
        ls_teams = r.json()["LeagueTable"]["L"][0]["Tables"]

        teams = []
        for ls_team in ls_teams:
            conference = "N/A"
            if "name" in ls_team:
                conference = ls_team["name"]
            for team in ls_team["team"]:
                if conference != "N/A":
                    t = {"name": team["Tnm"], "conference": conference}
                    teams.append(t)

        return {each["name"]: each for each in teams}.values()

    def get_matches_by_date(self, sport, date):
        """Get matches scheduled for a certain date

        Parameters:
            sport (str): Name of sport
            date (str): Date of games (format YYYYMMDD)
        """
        route = self.routes["matches"]["list_by_date"]
        headers = self.headers
        params = {"Category": sport, "Date": date, "Timezone": self.timezone}
        r = self.session.get(url=f"{self.url}{route}", headers=headers, params=params)
        return r.json()

    def get_matches_by_league(self, sport, league, season_type):
        """Get matches for a specific league

        Parameters:
            sport (str): Name of sport
            league (str) Name of sports league
            season_type (str): Type of season (ex. march madness)
        """
        route = self.routes["matches"]["list_by_league"]
        headers = self.headers
        params = {
            "Category": sport,
            "Ccd": league,
            "Scd": season_type,
            "Timezone": self.timezone,
        }
        r = self.session.get(url=f"{self.url}{route}", headers=headers, params=params)
        return r.json()


class OddsApiClient:
    def __init__(self):
        self.params = {
            "apiKey": config["apis"]["OddsApi"]["api_key"],
            "regions": "us",
            "oddsFormat": "american",
            "bookmakers": "draftkings,williamhill_us,fanduel,barstool,betmgm",
        }
        self.routes = config["apis"]["OddsApi"]["routes"]
        self.session = requests.Session()
        self.url = config["apis"]["OddsApi"]["url"]

    def get_spread(self, sport, home_team, away_team):
        route = self.routes["odds"]["get_odds"].replace(":sport", sport)
        params = self.params
        params["markets"] = "spreads"
        r = self.session.get(url=f"{self.url}{route}", params=params)
        books = []
        for game in r.json():
            if (
                game["home_team"].lower() == home_team.lower()
                and game["away_team"].lower() == away_team.lower()
            ):
                for bookmaker in game["bookmakers"]:
                    book = {
                        "bookmaker": bookmaker["title"],
                        "last_updated": bookmaker["last_update"],
                        "spreads": [
                            {
                                "team": away_team,
                                "price": bookmaker["markets"][0]["outcomes"][0]["price"]
                                if bookmaker["markets"][0]["outcomes"][0]["name"]
                                == away_team
                                else bookmaker["markets"][0]["outcomes"][1]["price"],
                                "point": bookmaker["markets"][0]["outcomes"][0]["point"]
                                if bookmaker["markets"][0]["outcomes"][0]["name"]
                                == away_team
                                else bookmaker["markets"][0]["outcomes"][1]["point"],
                            },
                            {
                                "team": home_team,
                                "price": bookmaker["markets"][0]["outcomes"][1]["price"]
                                if bookmaker["markets"][0]["outcomes"][0]["name"]
                                == home_team
                                else bookmaker["markets"][0]["outcomes"][1]["price"],
                                "point": bookmaker["markets"][0]["outcomes"][1]["point"]
                                if bookmaker["markets"][0]["outcomes"][1]["name"]
                                == home_team
                                else bookmaker["markets"][0]["outcomes"][1]["point"],
                            },
                        ],
                    }

    # def get_ml():
    # def get_ou():
