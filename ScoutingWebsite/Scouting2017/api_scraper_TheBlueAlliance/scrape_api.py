'''
Created on Mar 2, 2017

@author: PJ
'''
from BaseScouting.api_scraper_TheBlueAlliance.ApiDownloader import ApiDownloader

download_season_info = True
json_root = r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\api_scraper_TheBlueAlliance\results'

if download_season_info:
    scraper = ApiDownloader(json_root)
    scraper.download_matches_data("2017mndu2", 1)
#     scraper.download_team_data()
