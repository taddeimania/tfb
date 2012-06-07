"""make pylint happy"""
import simplejson
from django.http import HttpResponseRedirect

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView, View
from DisplayLeague import DisplayLeague
import joel
import sys
import logic
from players.models import Team, League, Roster, Player, Stats, Matchup, \
    Schedule, UserProfile, Curweek, Transaction, \
    Pro_Team, Draft, DraftTeam, DraftOrder, DraftPick

# Global variables.  Messing with this could cause major problems.
MAX_QB = 1
MAX_RB = 2
MAX_WR = 2
MAX_TE = 1
MAX_K = 1
POS_LIST = ['QB', 'RB', 'RB', 'WR', 'WR', 'TE', 'K']
CACHE_TIMEOUT = 30

def default_response( context, request, template=None ):
    """ Returns a default response using the previous function's
        name as the template name if none
        was supplied.
    """
    if not template:
        template = "%s.html" % sys._getframe(1).f_code.co_name

    if not context.get('request'):
        context.update({ 'request':request })

    return render_to_response(
        template, context, context_instance=RequestContext(request)
    )

def logout_user(request):
    """ Process logout request for user and redirect to login screen 
    """
    logout(request)
    return HttpResponseRedirect("/login")

def my_team_page(request):
    """ Send required variables to display your team
    """
    user = request.user
    query = request.POST.get('del_player', '')
    try:
        team = Team.objects.get(owner=user.userprofile.id)
    except Team.DoesNotExist:
        team = 'None'

    if query:
        drop_reason = logic.drop_player(query, team, user)

    if team != 'None':
        league = League.objects.get(id=team.league_id)
        roster = logic.roster_to_dict(
            Roster.objects.filter(
                week = logic.getweek(), team__owner=user.userprofile
            )
        )
    else:
        league = 'None'
        roster = 'None'


    return default_response(locals(), request, 'base_myteam_vars.html')


def about(request):
    """ Nothing dynamic served up here, just a static about me page.
    """
    return default_response(locals(), request, 'base_about.html')

def sysadmin(request, arg=None, argval=None):
    """ pylint
    """
    if request.user.is_superuser:
        if arg == 'process':
            joel.process(argval)
        if arg == 'matchup' and not argval:
            joel.process_matchup()
        if arg == 'matchup' and argval == 'create':
            joel.create_matchup_schedule()
        if arg == 'lock':
            joel.create_locks(argval)
        if arg == 'recalc':
            joel.recalculate_weekly_matchups()

        file_list = joel.get_file_list()
        lock_list = Schedule.objects.filter(week=logic.getweek())
        if not Matchup.objects.all(): create_matchup = True
        if not file_list and Stats.objects.filter(
            week=logic.getweek()
        ): process_matchups = True

    return default_response(locals(), request, 'base_sysadmin_vars.html')

def matchup_page(request, matchup_id=None):
    """ Display variables used for the matchup page
    """
    user = request.user
    _week = logic.getweek()
    if not matchup_id:
        try:
            matchup = Matchup.objects.get(
                Q(team_one__owner=user.userprofile, week=_week) |
                Q(team_two__owner=user.userprofile, week=_week)
            )
        except Matchup.DoesNotExist:
            return default_response(locals(), request, 'base_matchup_vars.html')
    else:
        matchup = Matchup.objects.get(pk=matchup_id)
    try:
        allmatchups = Matchup.objects.filter(week=matchup.week, league=matchup.league)
    except Matchup.DoesNotExist:
        pass
    team_one = matchup.team_one
    team_two = matchup.team_two
    try:
        t1pts = team_one.calc_week_points(matchup.week)
    except Team.DoesNotExist:
        t1pts = 0
    try:
        t2pts = team_two.calc_week_points(matchup.week)
    except Team.DoesNotExist:
        t2pts = 0

    if matchup.week > _week:
        team_one_roster = logic.roster_to_dict(
            Roster.objects.filter(week=_week, team=team_one),
            blank_stats=True
        )
        team_two_roster = logic.roster_to_dict(
            Roster.objects.filter(week=_week, team=team_two),
            blank_stats=True
        )
    else:
        team_one_roster = logic.roster_to_dict(
            Roster.objects.filter(week=matchup.week, team=team_one)
        )
        team_two_roster = logic.roster_to_dict(
            Roster.objects.filter(week=matchup.week, team=team_two)
        )

    return default_response(locals(), request, 'base_matchup_vars.html')

def profileedit(request):
    """ Display and process profile editing page
    """
    user = request.user
    profile = UserProfile.objects.get(pk=user.userprofile.id)
    query = request.POST.get('save', '')
    success = False

    try:
        team = Team.objects.get(owner=user.userprofile.id)
    except Team.DoesNotExist:
        team = 'None'

    if query == 'update':
        user.first_name = request.POST.get('first_name','')
        user.last_name = request.POST.get('last_name','')
        user.save()
        # this is in case they try to update
        # their profile without belonging to a league
        if team != 'None':
            team.name = request.POST.get('team_name','')
            team.slogan = request.POST.get('team_slogan','')
            team.save()
        success = True

    if query == 'update_face':      # Update user's face picture
        profile.userpic = request.POST.get('face')
        if profile.userpic:
            profile.save()
        else:
            profile.userpic = UserProfile.objects.get(user=user).userpic

    return default_response(locals(), request, 'base_profile_edit_vars.html')

#post beta function
def create_league(request):
    """ pylint
    """
    # L = League(lname = request.POST.get('lname'),
    # lslogan = request.POST.get('lslogan'), maxteam=10, active='Y')
    # L.generate_hash()
    return default_response(locals(), request, 'base.html')

def league_page(request, week = None):
    """ pylint
    """
    user = request.user
    weeks = range(1, 18)
    try:
        myteam = Team.objects.get(owner=user.userprofile.id)
    except Team.DoesNotExist:
        myteam = 'None'

    if myteam != 'None':
        league = League.objects.get(team__owner=user.userprofile.id)
        teams = Team.objects.order_by(
            'win','total_points', 'total_points_against'
        ).filter(league = league.id)
        teams = [_ for _ in teams]

        try:
            curweek = Curweek.objects.get(pk=1).curweek
            # more work is needed here so you can
            # have it use 2 different curweeks
            # for roster display and matchup display
            #from datetime import date
            #if date.isoweekday(date.today()) <= 3:
            #    curweek -= 1
            if week:
                curweek = week
            transactions = Transaction.objects.order_by('-id').filter(
                league = Team.objects.get(owner=user.userprofile
                ).league)[:15]
            transactions = [_ for _ in transactions]
            matchups = Matchup.objects.filter(week=curweek, league=league)

        except Team.DoesNotExist, Matchup.DoesNotExist:
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
        player = Player.objects.get(pk=query)
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
    teams = Team.objects.filter(league=league_id)
    return default_response(locals(), request, 'base_leaguelist_vars.html')

def joinleague(request):
    """ pylint
    """
    user = request.user
    user_id = user.userprofile.id
    query = request.POST.get('invite_code')
    leaguejoin = request.POST.get('public_league')

    try:
        alreadyinleague = Team.objects.get(owner=user_id)
    except Team.DoesNotExist:
        alreadyinleague = None
    leaguelist = []
    for league in League.objects.all():
        if league.is_league_available():
            teamcount = League.objects.get_team_count(league.id)
            disp_league = DisplayLeague(league)
            leaguelist.append(disp_league)

    if query:
        try:
            league = League.objects.get(invite_code=query)
            count = League.objects.get_team_count(league)
            if count < league.maxteam:
                team = Team(
                    owner=user_id,
                    league=league,
                    name="",
                    win=0,
                    loss=0,
                    slogan="",
                    total_points=0,
                    total_points_against=0
                )
                team.save()
                success = True
            else:
                failmessage = True
        except League.DoesNotExist:
            failmessage = True


    if leaguejoin:
        try:
            team = Team(
                owner=user,
                league=League.objects.get(pk=leaguejoin),
                name="",
                win=0,
                loss=0,
                slogan="",
                total_points=0,
                total_points_against=0
            )
            team.save()
            success = True
            return league_page(request)
        except League.DoesNotExist:
            failmessage = True

    return default_response(locals(), request, 'base_joinleague_vars.html')

def team_page(request, pro_team_id):
    """ Populate the base team vars template with team data that matches
    	the requested pro_team_id
    """
    team = Pro_Team.objects.get(short=pro_team_id)
    user = request.user
    schedule = logic.getteamschedule(pro_team_id)
    players = Player.objects.filter(pro_team=pro_team_id)
    plist = list(players)
    curweek = logic.getweek()
    try:
        nextopponent = logic.getproteamopponent(pro_team_id, curweek)
    except Pro_Team.DoesNotExist:
        pass
    return default_response(locals(), request, 'base_playerpage_vars.html')

def transactions_page(request):
    """ Get latest 15 transactions for your league.
    """
    user = request.user
    transactions = Transaction.objects.order_by('-id').filter(
        league = Team.objects.get(owner = user.userprofile).league
    )[:15]
    transactions = [_ for _ in transactions]
    return default_response(locals(), request, 'base_transactions_vars.html')

def leagueadmin(request, arg=None):
    """ Commish's Tools page.  This should grow quickly... soon.
    """
    user = request.user
    if Team.objects.get(owner=user.userprofile.id).iscommish == 'Y':
        league = Team.objects.get(owner=user.userprofile.id).league
        ready_to_draft = (Team.objects.filter(league=league).count() == 10)
        if arg == 'create':
            try:
                draft_data_exist = Draft.objects.get(league=league)
            except Draft.DoesNotExist:
                import draft
                draft.create_draft_data(user)
        try:
            draft_data_exists = Draft.objects.get(league=league)
        except Draft.DoesNotExist:
            pass
    return default_response(locals(), request, 'base_ladmin_vars.html')

class MockDraftTeam():
    """ I'm sure there is a smarter way to do this.
    """
    def __init__(self, draftteam):
        picks = list(
            DraftPick.objects.order_by('round'
            ).filter(draft_team=draftteam))
        self.teamname = Team.objects.get(pk=draftteam.team.id).name
        self.round_one = picks[0].player
        self.round_two = picks[1].player
        self.round_three = picks[2].player
        self.round_four = picks[3].player
        self.round_five = picks[4].player
        self.round_six = picks[5].player
        self.round_seven = picks[6].player

def draftpage(request, arg=None):
    """ Draft function isn't simple or small or easy to explain.
    Some of this is hackish, some of it is neat.
        Just understand that this is where the magic happens with the draft.
    """
    user = request.user
    if Team.objects.get(owner = user.userprofile.id).iscommish == 'Y':
        start = request.POST.get('start','')
        next = request.POST.get('next','')
        prev = request.POST.get('prev','')
        confirm = request.POST.get('confirm','')
        league = Team.objects.get(owner = user.userprofile.id).league
        try:
            draft_obj = Draft.objects.get(league=league)
        except Draft.DoesNotExist:
            draft_obj = ""
        if start:
            draft_obj.cur_round = 1
            draft_obj.save()
            order = DraftOrder.objects.order_by('position').filter(
                draft_team__draft = Draft.objects.get(league=league)
            )
        elif next:
            import draft
            errors = draft.validate_form(request.POST, draft_obj)
        elif prev:
            draft_obj.cur_round -= 1
            draft_obj.save()
        elif confirm:
            import draft
            errors = draft.validate_draft_and_generate_roster(draft_obj)
            #roster_exists = Roster.objects.filter(
            #   team__league = league
            # ).count > 1
        try:
            if Draft.objects.get(league=league).cur_round == 0:
                instructions = True
            elif Draft.objects.get(league=league).cur_round == 8  and confirm == '':
                confirm_list = []
                instructions = False
                confirmation = True
                teams = DraftTeam.objects.filter(draft=draft_obj)
                for team in teams:
                    mockteam = MockDraftTeam(team)
                    confirm_list.append(mockteam)
            elif confirm:
                pass
            else:
                instructions = False
                cur_round = Draft.objects.get(league=league).cur_round
                order = DraftOrder.objects.order_by('position').filter(
                    draft_team__draft=Draft.objects.get(league=league)
                )
                avail_players = simplejson.dumps(
                    [x.player_name for x in logic.draft_avail_players(league)]
                )
                pick = {}
                for team in order:
                    player = DraftPick.objects.filter(
                        round=cur_round, draft_team=team.draft_team
                    )
                    if player:
                        player = [x.player for x in player]
                        player = Player.objects.get(pk=player[0].id)
                        pick.update({team.id:player})
        except Draft.DoesNotExist:
            instructions = False
    return default_response(locals(), request, 'base_draft_vars.html')

class NotMyTeamView(TemplateView):
    template_name = 'base_uteam_vars.html'

    def get_context_data(self, *args, **kwargs):
        team_id = kwargs['team_id']
        try:
            self.team = Team.objects.get(
                pk=team_id,
                league=self.request.user.userprofile.team.league
            )
        except Team.DoesNotExist:
            return {
                'fail': True,
                'failmessage': "Team Doesn't Exist"
            }

        roster = logic.roster_to_dict(
            Roster.objects.filter(week=logic.getweek(), team=self.team)
        )
        owner = Team.objects.get(pk=team_id)
        return {
            'user': self.request.user,
            'roster': roster,
            'owner': owner
        }

class ProfileView(TemplateView):
    template_name = "base_profile_vars.html"

    def get_team(self):
        try:
            return Team.objects.get(owner=self.user.userprofile.id)
        except Team.DoesNotExist:
            return 'None'

    def get_context_data(self, **kwargs):
        self.user = self.request.user
        self.team = self.get_team()
        return {
            'user': self.user,
            'team': self.team
        }

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        return {
            'user': self.request.user
        }

class BlankView(TemplateView):
    template_name = "blank.html"
