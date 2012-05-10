from django.core.cache import cache
from django.utils import simplejson
from django.views.generic.base import TemplateView, View
from myproject import views as base_views
from myproject.players import models as player_models
import logic

def get_top_ten_for_pos(posid, user=None):
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

def playerpage(request, arg=None):
    """pylint """
    playerstats = []
    topqbs = []
    toprbs = []
    topwrs = []
    toptes = []
    topks = []

    player = request.POST.get('playersearch','')
    players = simplejson.dumps([x.player_name for x in player_models.Player.objects.all()])

    if str(arg).upper() == 'TOP':
        top = True
        topqbs = get_top_ten_for_pos('QB')
        toprbs = get_top_ten_for_pos('RB')
        topwrs = get_top_ten_for_pos('WR')
        toptes = get_top_ten_for_pos('TE')
        topks = get_top_ten_for_pos('K')

    elif str(arg).upper() == 'TOPAVAIL':
        top = True
        avail = True
        user = request.user
        topqbs = get_top_ten_for_pos('QB', user=user)
        toprbs = get_top_ten_for_pos('RB', user=user)
        topwrs = get_top_ten_for_pos('WR', user=user)
        toptes = get_top_ten_for_pos('TE', user=user)
        topks = get_top_ten_for_pos('K', user=user)

    elif str(arg).upper() in base_views.POS_LIST:
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
                pass
            try:
                playerobj = player_models.Player.objects.get(pk=arg)
                for player in player_models.Stats.objects.filter(player=arg):
                    playerstats.append(player)
                    playerstats.sort(key=lambda x: x.week, reverse=False)
            except player_models.Player.DoesNotExist:
                pass
        pass
    else:
        playersearch = True
        try:
            playerobj = player_models.Player.objects.get(pk=arg)
            for player in player_models.Stats.objects.filter(player=arg):
                playerstats.append(player)
                playerstats.sort(key=lambda x: x.week, reverse=False)
        except player_models.Player.DoesNotExist:
            pass


    return base_views.default_response(locals(), request, 'base_playerpage_vars.html')

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