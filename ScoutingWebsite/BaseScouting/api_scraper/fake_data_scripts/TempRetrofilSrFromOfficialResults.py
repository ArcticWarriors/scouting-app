'''
Created on Feb 8, 2017

@author: PJ
'''


class TempRetrofillSrFromOfficialResults:

    def populate_sr(self, **kargs):

        return kargs

    def save_sr(self, score_result_type, match, team, **kargs):

        sr_search = score_result_type.objects.filter(match=match, team=team)
        if len(sr_search) == 0:
            sr = score_result_type(match=match, team=team, **kargs)
            sr.save()
            pass
        else:
            sr = sr_search[0]
            for key, value in kargs.iteritems():
                setattr(sr, key, value)
            sr.save()
            pass

    def populate_matchresults(self, official_match, match_class, score_result_class, official_sr_class):

        match, _ = match_class.objects.get_or_create(matchNumber=official_match.matchNumber)
        print("Updating match %s" % match.matchNumber)

#         print official_match.__dict__
        official_srs = official_sr_class.objects.filter(official_match=official_match)
        red_sr = official_srs[0]
        blue_sr = official_srs[1]

        self.save_sr(score_result_class, match, match.red1, **self.populate_sr(**self.get_team1_stats(red_sr)))
        self.save_sr(score_result_class, match, match.red2, **self.populate_sr(**self.get_team2_stats(red_sr)))
        self.save_sr(score_result_class, match, match.red3, **self.populate_sr(**self.get_team3_stats(red_sr)))

        self.save_sr(score_result_class, match, match.blue1, **self.populate_sr(**self.get_team1_stats(blue_sr)))
        self.save_sr(score_result_class, match, match.blue2, **self.populate_sr(**self.get_team2_stats(blue_sr)))
        self.save_sr(score_result_class, match, match.blue3, **self.populate_sr(**self.get_team3_stats(blue_sr)))

        official_match.hasOfficialData = True
        official_match.save()

    def get_team1_stats(self, official_match_sr):
        raise NotImplementedError()

    def get_team2_stats(self, official_match_sr):
        raise NotImplementedError()

    def get_team3_stats(self, official_match_sr):
        raise NotImplementedError()
