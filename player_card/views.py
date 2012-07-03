from django.views.generic.base import TemplateView
from tfb.players import models as player_models
from tfb.views import default_response
from tfb.utility import logic

class PlayerPageView(TemplateView):
    template_name = "base_player_vars.html"
    curweek = logic.getweek()
    success = None
    drop = False
    def get_template_vars(self, player_id):
        self.player = player_models.Player.objects.get(pk=player_id)
        weekpts = [_ for _ in player_models.Stats.objects.order_by('week').filter(player=self.player)]
        schedule = logic.getteamschedule(self.player.pro_team_id)
        seasontotalstats = self.player.SeasonTotal()
        return self.player, weekpts, schedule, seasontotalstats

    def get_user_league(self, user):
        try:
            league = player_models.Team.objects.get(owner=user.userprofile).league
        except Exception:
            league = None
        return league

    def get_stats_points_health(self):
        try:
            seasontotalstats = self.player.SeasonTotal()
            points = player_models.Stats.objects.order_by('week').filter(player=self.player.id)
            weekpts = [_ for _ in points]
            if self.curweek == 1:
                health = 'OK'
            else:
                health = player_models.Stats.objects.get(player=self.player, week=(self.curweek-1)).health
            return seasontotalstats, weekpts, health
        except Exception:
            return None, None, None

    def get_droppable_status(self):
        try:
            owner = player_models.Team.objects.get_owner_for_player_this_week(self.user_league, self.player)
            if owner == self.user.userprofile:
                return [True, owner]
            return [False, owner]
        except Exception:
            return [False, None]

    def get_context_data(self, **kwargs):
        player_id = kwargs['player_id']
        try:
            self.player = player_models.Player.objects.get(pk=player_id)
            self.schedule = logic.getteamschedule(self.player.pro_team_id)
        except:
            self.player = 0
            self.schedule = []
        self.user = self.request.user
        self.user_league = self.get_user_league(self.user)
        return self.get_template_data()

    def get_template_data(self):
        seasontotalstats, weekpts, health = self.get_stats_points_health()
        dropstatus = self.get_droppable_status()
        return {
            'user': self.user,
            'player': self.player,
            'schedule': self.schedule,
            'weekfilter': player_models.Stats.objects.filter(player=self.player),
            'curweek': self.curweek,
            'seasontotalstats': seasontotalstats,
            'weekpts': weekpts,
            'health': health,
            'dropbutton': dropstatus[0],
            'owner': dropstatus[1],
            'drop': self.drop,
            'success': self.success,
        }

    def post(self, *args, **kwargs):
        player_id = kwargs['player_id']
        self.player = player_models.Player.objects.get(pk=player_id)
        self.user = self.request.user
        self.success = logic.drop_player(
            self.player.id, player_models.Team.objects.get_my_team(self.user), self.user
        )
        if not self.success:
            self.drop = True
        return default_response(self.get_template_data(), self.request, self.template_name)
