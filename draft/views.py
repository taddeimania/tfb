from django.utils import simplejson
from tfb.draft.draft import validate_draft_and_generate_roster
from tfb.draft.draft import validate_form
from tfb.players import models as player_models
from tfb.draft import models as draft_models
from tfb.views import default_response
from tfb.utility import logic

class MockDraftTeam():
    """ I'm sure there is a smarter way to do this.
    """
    def __init__(self, draftteam):
        picks = list(
            draft_models.DraftPick.objects.order_by('round'
            ).filter(draft_team=draftteam))
        self.teamname = player_models.Team.objects.get(pk=draftteam.team.id).name
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
    if player_models.Team.objects.get(owner = user.userprofile.id).iscommish == 'Y':
        start = request.POST.get('start','')
        next = request.POST.get('next','')
        prev = request.POST.get('prev','')
        confirm = request.POST.get('confirm','')
        league = player_models.Team.objects.get(owner = user.userprofile.id).league
        try:
            draft_obj = draft_models.Draft.objects.get(league=league)
        except draft_models.Draft.DoesNotExist:
            draft_obj = ""
        if start:
            draft_obj.cur_round = 1
            draft_obj.save()
            order = draft_models.DraftOrder.objects.order_by('position').filter(
                draft_team__draft = draft_models.Draft.objects.get(league=league)
            )
        elif next:
            errors = validate_form(request.POST, draft_obj)
        elif prev:
            draft_obj.cur_round -= 1
            draft_obj.save()
        elif confirm:
            errors = validate_draft_and_generate_roster(draft_obj)
            #roster_exists = Roster.objects.filter(
            #   team__league = league
            # ).count > 1
        try:
            if not draft_models.Draft.objects.get(league=league).cur_round:
                instructions = True
            elif draft_models.Draft.objects.get(league=league).cur_round == 8  and confirm == '':
                confirm_list = []
                instructions = False
                confirmation = True
                teams = draft_models.DraftTeam.objects.filter(draft=draft_obj)
                for team in teams:
                    mockteam = MockDraftTeam(team)
                    confirm_list.append(mockteam)
            elif confirm:
                pass
            else:
                instructions = False
                cur_round = draft_models.Draft.objects.get(league=league).cur_round
                order = draft_models.DraftOrder.objects.order_by('position').filter(
                    draft_team__draft=draft_models.Draft.objects.get(league=league)
                )
                avail_players = simplejson.dumps(
                    [x.player_name for x in logic.draft_avail_players(league)]
                )
                pick = {}
                for team in order:
                    player = draft_models.DraftPick.objects.filter(
                        round=cur_round, draft_team=team.draft_team
                    )
                    if player:
                        player = [x.player for x in player]
                        player = player_models.Player.objects.get(pk=player[0].id)
                        pick.update({team.id:player})
        except draft_models.Draft.DoesNotExist:
            instructions = False

    return default_response(locals(), request, 'base_draft_vars.html')


def drag_and_drop(request):

    players = player_models.Player.objects.filter(pos__startswith='QB')
    player_list = [
        {'id': player.id,
                    'name': player.player_name,
                    'pic': player.picture,
                    'team': player.pro_team.short}
        for player in players
    ]

    return default_response(locals(), request, 'base_dragdrop.html')