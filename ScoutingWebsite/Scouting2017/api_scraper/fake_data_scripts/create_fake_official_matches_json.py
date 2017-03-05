'''
Created on Feb 7, 2017

@author: PJ
'''
import json
from BaseScouting.load_django import load_django
from BaseScouting.api_scraper.fake_data_scripts.CreateFakeJson_OfficialFirst import CreateFakeJson_OfficialFirst
from Scouting2017.api_scraper.fake_data_scripts.Robot import Robot
from Scouting2017.api_scraper.fake_data_scripts.CreateFakeJsonMixin import CreateFakeJsonMixin


def create_robots():

    output = {}
    output[20] = Robot(auto_high_goal_percentage=90, tele_high_goal_percentage=90, tele_high_goal_capacity=240)
    output[73] = Robot(auto_mobility_percentage=0)
    output[174] = Robot(auto_mobility_percentage=80, tele_gear_max=6, tele_gear_consistancy=90)
    output[191] = Robot(tele_gear_consistancy=80)
    output[250] = Robot()
    output[271] = Robot()
    output[340] = Robot()
    output[378] = Robot()
    output[395] = Robot(tele_gear_max=8, tele_gear_consistancy=60)
    output[578] = Robot()
    output[639] = Robot()
    output[810] = Robot()
    output[1126] = Robot(auto_high_goal_percentage=75, tele_high_goal_percentage=75, tele_high_goal_capacity=160)
    output[1405] = Robot()
    output[1450] = Robot(auto_high_goal_percentage=10, tele_high_goal_percentage=10, tele_high_goal_capacity=40)
    output[1507] = Robot(auto_high_goal_percentage=85, tele_high_goal_percentage=85, tele_high_goal_capacity=200)
    output[1511] = Robot()
    output[1518] = Robot()
    output[1551] = Robot()
    output[1559] = Robot()
    output[1585] = Robot()
    output[1591] = Robot(auto_high_goal_percentage=25, tele_high_goal_percentage=25, tele_high_goal_capacity=90)
    output[1665] = Robot()
    output[1765] = Robot()
    output[1880] = Robot()
    output[2010] = Robot()
    output[2228] = Robot()
    output[2340] = Robot()
    output[2383] = Robot()
    output[2638] = Robot()
    output[2791] = Robot()
    output[2809] = Robot()
    output[3003] = Robot()
    output[3015] = Robot()
    output[3044] = Robot()
    output[3157] = Robot()
    output[3173] = Robot()
    output[3181] = Robot()
    output[3799] = Robot()
    output[3838] = Robot()
    output[3951] = Robot()
    output[4023] = Robot()
    output[4093] = Robot()
    output[4930] = Robot()
    output[5030] = Robot()
    output[5240] = Robot()
    output[5254] = Robot()
    output[5433] = Robot()
    output[5590] = Robot()

    return output


def main():
    load_django()
    from Scouting2017.model import OfficialMatch, Match, OfficialMatchScoreResult, Competition

    class CreateFakeJson2017_OfficialFirst(CreateFakeJsonMixin, CreateFakeJson_OfficialFirst):

        def __init__(self):
            CreateFakeJson_OfficialFirst.__init__(self, Match, OfficialMatch, OfficialMatchScoreResult)
        pass

    robots = create_robots()

    competition = Competition.objects.get(code="NYRO")

    official_dumper = CreateFakeJson2017_OfficialFirst()
    info_to_dump = official_dumper.create_matches(1, 40, robots, competition)

    dump_file = r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\api_scraper\official_FIRST\api_scraping_results\week3\NYRO_scoreresult_query.json'
    match_results = {}
    match_results['MatchScores'] = info_to_dump
    scoreresult_dump = json.dumps(match_results, indent=4)
    with open(dump_file, 'w') as f:
        f.write(scoreresult_dump)
    print json.dumps(info_to_dump, indent=4)


main()
