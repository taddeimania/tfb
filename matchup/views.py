from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from tfb.matchup.models import Matchup
from tfb.matchup import matchup_logic
from utility import logic

class MatchupPageView(TemplateView):

    template_name = "base_matchup_vars.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        week = logic.getweek()
        matchup_id = kwargs.get('matchup_id')
        if matchup_id:
            matchup = Matchup.objects.get(pk=matchup_id)
        else:
            try:
                matchup = Matchup.objects.get(
                    Q(team_one__owner=user.userprofile, week=week) |
                    Q(team_two__owner=user.userprofile, week=week)
                )
            except Matchup.DoesNotExist:
                return HttpResponseRedirect("")

        team_data = matchup_logic.get_team_data(matchup, week)

        try:
            allmatchups = Matchup.objects.filter(week=matchup.week, league=matchup.league)
        except Matchup.DoesNotExist:
            pass

        return {
            'matchup': matchup,
            'team_one': team_data['team_one']['team'],
            'team_two': team_data['team_two']['team'],
            't1pts': team_data['team_one']['points'],
            't2pts': team_data['team_two']['points'],
            'team_one_roster': team_data['team_one']['roster'],
            'team_two_roster': team_data['team_two']['roster'],
            'allmatchups': allmatchups
        }