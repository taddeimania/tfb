from logic import draft_avail_players
from players.models import *
import views

def create_draft_data( user ):
    """ Creates a draft team and draft order for the admin's league that initiated the process
        THOUGHTS: Probably should check for correct permissions and if a draft already exists.
    """
    league = Team.objects.get( owner=user.userprofile.id ).league
    draft_obj = Draft( league=league, cur_round=0 )
    draft_obj.save()
    import random
    teams = Team.objects.filter( league=league )
    seed = random.sample( range( 1,11 ),10 )
    for idx, val in enumerate( teams ):
        dteam = DraftTeam( draft=draft_obj , team=val)
        dteam.save()
        dorder = DraftOrder( draft_team=dteam , position=seed[idx] )
        dorder.save()

def validate_form( form, draft_obj ):
    """ Called every time the 'Next' button is pressed.  Method performs all logic checks on every forward
        movement for the draft so nobody 'accidentally' drafts a player more than once.
    """
    draft_list = []
    errors = []
    cur_round = draft_obj.cur_round
    teams = DraftTeam.objects.filter( draft=draft_obj )
    for team in teams:
        draft_list.append( str( cur_round ) + '_' + str( team.id ) )

    for pick in draft_list:
        draft_team = pick.split('_')
        draft_team = DraftTeam.objects.get( pk = draft_team[1] )
        player = ""
        try:
            player = Player.objects.get( player_name=form.get(pick) )
        except:
            pass
        if player in draft_avail_players( draft_obj.league ):
            if not already_picked( draft_team, draft_obj ):
                newplayer = DraftPick( round=cur_round, draft_team=draft_team, player=player )
                newplayer.save()
                validated, errors = validate_team(draft_team)
                if not validated:
                    newplayer.delete()
            else:
                curpick = DraftPick.objects.get( round=draft_obj.cur_round, draft_team=draft_team )
                curpick.player = player
                curpick.save()
                validated, errors = validate_team(draft_team)
                if not validated:
                    curpick.delete()
        elif player == "":
            try:
                curpick = DraftPick.objects.get( round=draft_obj.cur_round, draft_team=draft_team )
                curpick.delete()
            except:
                pass

    # advance to next round
    # refactor this you joke.
    if DraftPick.objects.filter( round=cur_round, draft_team__draft=teams[0].draft ).count() == 10:
        dupes = duplicate_in_round( cur_round, draft_obj )
        if not dupes:
            validate_round( cur_round, draft_obj )
        else:
            errors.append( 'Draft Round Contains Duplicates, Cannot Advance' )

    return errors

def already_picked( draft_team, draft_obj ):
    """ Returns True if player exists in current draft and is currently in a team's queue.
    """
    return bool( DraftPick.objects.filter( round=draft_obj.cur_round, draft_team=draft_team ) )

def duplicate_in_round( draft_round, draft_obj ):
    """ Checks the current round if a commish entered a player more than once.
    """
    return check_duplicate( draft_obj,draft_round )

def check_duplicate( draft_obj, draft_round=None ):
    """ Checks the entire draft if a duplicate entry exists unless a round is specified.
    """
    if draft_round:
        picks = DraftPick.objects.filter( draft_team__draft=draft_obj, round=draft_round)
    else:
        picks = DraftPick.objects.filter( draft_team__draft=draft_obj )
    picks = [x for x in picks]
    if len( picks )!=len( set( picks ) ):
        return True #duplicates found
    return False

def validate_round( draft_round, draft_obj ):
    """ Advances draft one round.
    """

    #  Why is this even here?  It would never be reused.
    draft_obj.cur_round = int( draft_round ) + 1
    draft_obj.save()

def validate_team( draft_team ):
    """ Not the prettiest method but this does a lot of heavy lifting for business logic.
    """
    picks = DraftPick.objects.filter( draft_team=draft_team )
    errors = []
    pos_list = []
    validated = True

    for pick in picks:
        if pick.player.pos != 'K':
            pos_list.append( pick.player.pos[0:2] )
        else:
            pos_list.append( 'K' )

    if pos_list.count( 'QB' ) > views.MAX_QB:
        errors.append( str( draft_team.team.name ) + ' Maximum Number of Quarterbacks Reached' )
        validated = False
    if pos_list.count( 'RB' ) > views.MAX_RB:
        errors.append( str( draft_team.team.name ) + ' Maximum Number of Runningbacks Reached' )
        validated = False
    if pos_list.count( 'WR' ) > views.MAX_WR:
        errors.append( str( draft_team.team.name ) + ' Maximum Number of Wide Receivers Reached' )
        validated = False
    if pos_list.count( 'TE' ) > views.MAX_TE:
        errors.append( str( draft_team.team.name ) + ' Maximum Number of Tight Ends Reached' )
        validated = False
    if pos_list.count( 'K' ) > views.MAX_K:
        errors.append (str( draft_team.team.name ) + ' Maximum Number of Kickers Reached' )
        validated = False

    return validated, errors

def validate_draft_and_generate_roster( draft_obj ):
    """ Final step in draft validation.
    """
    error_list = []
    dupes = check_duplicate( draft_obj )
    team_list = DraftTeam.objects.filter( draft=draft_obj )
    for team in team_list:
        validated, errors = validate_team( team )
        if errors:
            error_list.append( errors )

    if not dupes and not errors:
        generate_roster_from_draft( draft_obj )

    #ensure league is marked as active
    return error_list

def generate_roster_from_draft( draft_obj ):
    """ Creates a roster item from each draft pick and gives the player to the owner that drafted them.
        Sweeeeeeeet
    """
    picks = DraftPick.objects.filter( draft_team__draft=draft_obj )
    for player in picks:
        new_player = Roster( week=1, team=player.draft_team.team, player=player.player )
        new_player.save()