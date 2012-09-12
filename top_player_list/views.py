from django.core.cache import cache
from django.http import HttpResponse
from django.utils import simplejson
from django.views.generic.base import View, TemplateView
from players.models import SeasonRanking
from tfb import views as base_views
from tfb.players import models as player_models
from tfb.utility import logic

POS_LIST = ['QB', 'RB', 'RB', 'WR', 'WR', 'TE', 'K']

def get_top_ten_for_pos(posid, user=None):
    CACHE_TIMEOUT = 360
    top_pos = {'cache_mode': "top{}s".format(posid)}
    top_list = []
    if not user:
        search_criteria = player_models.Player.objects.filter(pos__startswith=posid.upper())
    else:
        search_criteria = logic.avail_list(user, posid)
        top_pos['cache_mode'] = "avail_top{}".format(posid)
    if not cache.get(top_pos.get('cache_mode', None)):
        try:
            for player in search_criteria:
                top_list.append(player.SeasonTotal())
                top_list.sort(key=lambda x: x.Allfanpts, reverse=True)
            top_list = top_list[:10]
            cache.set(top_pos['cache_mode'], top_list, CACHE_TIMEOUT)
            return top_list
        except Exception:
            return
    else:
        return cache.get(top_pos['cache_mode'])



def get_player_stats(arg, playerstats):
    try:
        playerobj = player_models.Player.objects.get(pk=arg)
        for player in player_models.Stats.objects.filter(player=arg):
            playerstats.append(player)
            playerstats.sort(key=lambda x: x.week, reverse=False)
        season_total = playerobj.SeasonTotal()
        return playerobj, season_total
    except player_models.Player.DoesNotExist:
        return "Player Not Found", ""



def playerpage(request, arg=None):
    """pylint """
    playerstats = []
    pos_list = ['QB', 'RB', 'WR', 'TE', 'K']
    player_list = []

    player = request.POST.get('playersearch','')
    players = simplejson.dumps([x.player_name for x in player_models.Player.objects.all()])

    if request.is_ajax():
        position = request.GET.items()[0][0]
        players = dict(
            (player.ranking, {
                'name': player.player.player_name,
                'team': player.player.pro_team.long,
                'picture': player.player.picture,
                'position': player.player.pos
            })
            for player in SeasonRanking.objects.get_position(position)
        )
        return HttpResponse(simplejson.dumps(players), content_type='application/json')

    if str(arg).upper() == 'TOP':
        top = True
        for pos in pos_list:
            player_list.append((pos, get_top_ten_for_pos(pos)))
        return base_views.default_response(locals(), request, 'base_playerpage_vars.html')

    if str(arg).upper() == 'DRAFT':
        draft = True
        player_list = [x for x in SeasonRanking.objects.all()]

    elif str(arg).upper() == 'TOPAVAIL':
        top = True
        avail = True
        for pos in pos_list:
            player_list.append((pos, get_top_ten_for_pos(pos, user=request.user)))

    elif str(arg).upper() in POS_LIST:
        pos = True
        for player in player_models.Player.objects.filter(pos__startswith=str(arg).upper):
            playerstats.append(player.SeasonTotal())
        playerstats.sort(key=lambda x: x.Allfanpts, reverse=True)

    elif not arg:
        search = True
        if player:
            playersearch = True
            search = False
            try:
                player = player_models.Player.objects.get(player_name=player)
                arg = player.id
            except player_models.Player.DoesNotExist:
                maybe_list = player_models.Player.objects.filter(player_name__icontains=player)
                return base_views.default_response(locals(), request, 'base_notfound_vars.html')
            playerobj, season_total = get_player_stats(arg, playerstats)
        pass
    else:
        playersearch = True
        playerobj, season_total = get_player_stats(arg, playerstats)
    return base_views.default_response(locals(), request, 'base_playerpage_vars.html')

class PlayerNotFound(TemplateView):
    template_name = "base_notfound_vars.html"

    def redirect(self, request):
        self.request = request
        return self.get_context_data()

    def get_context_data(self, **kwargs):
        print self.request.POST
        return {
            'context': 'context',
        }


# WIP!

class TopPlayerListView(View):
    template_name = 'base_playerpage_vars.html'

    def get_top_ten_for_pos(self, posid, user=None):
        CACHE_TIMEOUT = 360
        top_pos = "top{}s".format(posid)
        top_list = []
        if not user:
            search_criteria = player_models.Player.objects.filter(pos__startswith=posid.upper())
        else:
            search_criteria = logic.avail_list(user, 'QB')
        if not cache.get(top_pos):
            try:
                for player in search_criteria:
                    top_list.append(player.SeasonTotal())
                    top_list.sort(key=lambda x: x.Allfanpts, reverse=True)
                top_list = top_list[:10]
                cache.set(top_pos, top_list, CACHE_TIMEOUT)
                return top_list
            except Exception:
                return
        else:
            return cache.get(top_pos)

    def get(self):
        return self.get_template_data()

    def post(self):
        """"""

    def get_template_data(self):
        return {}