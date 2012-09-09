from django.contrib.auth.models import User
import os
import sys
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.views.generic import TemplateView
from tfb.matchup import matchup_logic
from tfb.draft import draft
from tfb.messages.models import Message
from tfb.matchup import models as matchup_models
from tfb.players import models as player_models
from tfb.settings import PROJECT_ROOT
from tfb.draft.models import Draft
from tfb.utility import logic, load_stats

CACHE_TIMEOUT = 30

def default_response(context, request, template=None):
    """ Returns a default response using the previous function's
        name as the template name if none
        was supplied.
    """
    if not template:
        template = "%s.html" % sys._getframe(1).f_code.co_name

    if not context.get('request'):
        context.update({'request': request})

    return render_to_response(
        template, context, context_instance=RequestContext(request)
    )

def logout_user(request):
    """ Process logout request for user and redirect to login screen 
    """
    logout(request)
    return HttpResponseRedirect("/login")

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        return {
            'user': self.request.user
        }

class BlankView(TemplateView):
    template_name = "blank.html"

class AboutView(TemplateView):
    template_name = 'base_about.html'


class MyTeamView(TemplateView):
    template_name = "base_myteam_vars.html"

    def post(self, *args):
        user = self.request.user
        team = player_models.Team.objects.get(owner=user.userprofile.id)
        player_to_drop = self.request.POST['del_player']
        logic.drop_player(player_to_drop, team, user)
        return HttpResponseRedirect("")

    def get_context_data(self, **kwargs):
        user = self.request.user
        try:
            team = player_models.Team.objects.get(owner=user.userprofile.id)
            league = team.league
            roster = logic.roster_to_dict(
                player_models.Roster.objects.filter(week=logic.getweek(), team__owner=user.userprofile)
            )
        except player_models.Team.DoesNotExist:
            team = 'None'
            league = 'None'
            roster = 'None'

        return {"user": user, "league": league, "roster": roster, "team": team}

def sysadmin(request, arg=None, argval=None):
    """ pylint
    """
    if request.user.is_superuser:
        if arg == 'process':
            load_stats.insert_file(argval)
        if arg == 'matchup' and not argval:
            matchup_logic.process_weekly_matchups()
        if arg == 'matchup' and argval == 'create':
            matchup_logic.create_matchup_data()
        if arg == 'lock':
            matchup_logic.create_locks(argval)
        if arg == 'recalc':
            matchup_logic.recalculate_weekly_matchups()
        if arg == 'byes':
            pass
#            logic.create_bye_weeks()

        file_list = sorted([d for d in os.listdir(os.path.join(PROJECT_ROOT, 'files'))])
        lock_list = player_models.Schedule.objects.filter(week=logic.getweek())
        if not matchup_models.Matchup.objects.all().exists(): create_matchup = True
        if not file_list and player_models.Stats.objects.filter(week=logic.getweek()):
            process_matchups = True
    else:
        return HttpResponse("ah, ah, ah... you didn't say the magic word.")

    return default_response(locals(), request, 'base_sysadmin_vars.html')

#post beta function
#def create_league(request):
#    """ pylint
#    """
#    # L = League(lname = request.POST.get('lname'),
#    # lslogan = request.POST.get('lslogan'), maxteam=10, active='Y')
#    # L.generate_hash()
#    return default_response(locals(), request, 'base.html')

def league_page(request, week = None):
    """ pylint
    """
    user = request.user
    weeks = range(1, 18)
    try:
        myteam = player_models.Team.objects.get(owner=user.userprofile.id)
    except player_models.Team.DoesNotExist:
        myteam = 'None'

    if myteam != 'None':
        league = player_models.League.objects.get(team__owner=user.userprofile.id)
        teams = player_models.Team.objects.order_by(
            'win','total_points', 'total_points_against'
        ).filter(league = league.id)
        teams = [_ for _ in teams]

        try:
            curweek = player_models.Curweek.objects.get(pk=1).curweek
            # more work is needed here so you can
            # have it use 2 different curweeks
            # for roster display and matchup display
            #from datetime import date
            #if date.isoweekday(date.today()) <= 3:
            #    curweek -= 1
            if week:
                curweek = week
            transactions = player_models.Transaction.objects.order_by('-id').filter(
                league = player_models.Team.objects.get(owner=user.userprofile
                ).league)[:15]
            transactions = [_ for _ in transactions]
            matchups = matchup_models.Matchup.objects.filter(week=curweek, league=league)
            recent_messages = Message.objects.filter(user__team__league=league).order_by('-timestamp')[:5]
        except player_models.Team.DoesNotExist, matchup_models.Matchup.DoesNotExist:
            nomatchup = True

    return default_response(locals(), request, 'base_league_vars.html')
	
def list_player(request, posid):
    """ pylint
    """
    user = request.user
    posid = str(posid).upper()
    isposopen = logic.ispositionopen(user, posid)
    query = request.POST.get('player_id', '')
    
    if query:
        player = player_models.Player.objects.get(pk=query)
        success = logic.setplayertoroster(user, player)
        return default_response(locals(), request, 'base_list_vars.html')
    
    else:
        playerlist = logic.avail_list(user, posid)
        return default_response(locals(), request, 'base_list_vars.html')
	
def pickup(request, posid):
    """ Checks authentication for adding a player page
    """
    user = request.user
    return default_response(locals(), request, 'base_pickup_vars.html')

def league_list(request, league_id):
    """ Returns list of teams in your league.  Used for a modal popup.
    """
    teams = player_models.Team.objects.filter(league=league_id)
    return default_response(locals(), request, 'base_leaguelist_vars.html')

class DisplayLeague():

    def __init__(self, league):
        self.id = league.id
        self.name = league.lname
        self.teamcount = player_models.League.objects.get_team_count(league.id)
        self.maxteam = league.maxteam

def joinleague(request):
    """ pylint
    """
    user = request.user
    user_id = user.userprofile
    query = request.POST.get('invite_code')
    leaguejoin = request.POST.get('public_league')

    try:
        alreadyinleague = player_models.Team.objects.get(owner=user_id)
    except player_models.Team.DoesNotExist:
        alreadyinleague = None
    leaguelist = []
    for league in player_models.League.objects.all():
        if league.is_league_available():
            teamcount = player_models.League.objects.get_team_count(league.id)
            disp_league = DisplayLeague(league)
            leaguelist.append(disp_league)

    if query:
        try:
            league = player_models.League.objects.get(invite_code=query)
            count = player_models.League.objects.get_team_count(league)
            if count < league.maxteam:
                team = player_models.Team(
                    owner=user_id,
                    league=league,
                    name=user_id.user.username,
                    win=0,
                    loss=0,
                    slogan="",
                    total_points=0,
                    total_points_against=0,
                    iscommish="N"
                )
                team.save()
                success = True
                return HttpResponseRedirect('/profile/edit')
            else:
                failmessage = True
        except player_models.League.DoesNotExist:
            failmessage = True


    if leaguejoin:
        try:
            team = player_models.Team(
                owner=user_id,
                league=player_models.League.objects.get(pk=leaguejoin),
                name=user_id.user.username,
                win=0,
                loss=0,
                slogan="",
                total_points=0,
                total_points_against=0,
                iscommish="N"
            )
            team.save()
            success = True
            return HttpResponseRedirect('/profile/edit')
        except player_models.League.DoesNotExist:
            failmessage = True

    return default_response(locals(), request, 'base_joinleague_vars.html')

def team_page(request, pro_team_id):
    """ Populate the base team vars template with team data that matches
    	the requested pro_team_id
    """
    team = player_models.Pro_Team.objects.get(short=pro_team_id)
    user = request.user
    schedule = logic.getteamschedule(pro_team_id)
    players = player_models.Player.objects.filter(pro_team=pro_team_id)
    plist = list(players)
    curweek = logic.getweek()
    try:
        nextopponent = logic.getproteamopponent(pro_team_id, curweek)
    except player_models.Pro_Team.DoesNotExist:
        pass
    return default_response(locals(), request, 'base_playerpage_vars.html')

def transactions_page(request):
    """ Get latest 15 transactions for your league.
    """
    user = request.user
    transactions = player_models.Transaction.objects.order_by('-id').filter(
        league = player_models.Team.objects.get(owner = user.userprofile).league
    )[:15]
    transactions = [_ for _ in transactions]
    return default_response(locals(), request, 'base_transactions_vars.html')

def leagueadmin(request, arg=None):
    """ Commish's Tools page.  This should grow quickly... soon.
    """
    user = request.user
    if player_models.Team.objects.get(owner=user.userprofile.id).iscommish == 'Y':
        league = player_models.Team.objects.get(owner=user.userprofile.id).league
        ready_to_draft = (player_models.Team.objects.filter(league=league).count() == 10)
        if arg == 'create':
            try:
                draft_data_exist = Draft.objects.get(league=league)
            except Draft.DoesNotExist:
                draft.create_draft_data(user)
        try:
            draft_data_exists = Draft.objects.get(league=league)
        except Draft.DoesNotExist:
            pass
    return default_response(locals(), request, 'base_ladmin_vars.html')

class NotMyTeamView(TemplateView):
    template_name = 'base_uteam_vars.html'

    def get_context_data(self, *args, **kwargs):
        team_id = kwargs['team_id']
        try:
            self.team = player_models.Team.objects.get(
                pk=team_id,
                league=self.request.user.userprofile.team.league
            )
        except player_models.Team.DoesNotExist:
            return {
                'fail': True,
                'failmessage': "Team Doesn't Exist"
            }

        roster = logic.roster_to_dict(
            player_models.Roster.objects.filter(week=logic.getweek(), team=self.team)
        )
        owner = player_models.Team.objects.get(pk=team_id)
        return {
            'user': self.request.user,
            'roster': roster,
            'owner': owner
        }
