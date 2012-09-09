from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from tfb.players import models as player_models
from utility import logic

class ProfileView(TemplateView):
    template_name = "base_profile_vars.html"

    def get_team(self):
        try:
            return player_models.Team.objects.get(owner=self.request.user.userprofile.id)
        except player_models.Team.DoesNotExist:
            return 'None'

    def get_context_data(self, **kwargs):
        return {
            'user': self.request.user,
            'team': self.get_team(),
            'trophies': [ _ for _ in player_models.TrophyAssignment.objects.filter(profile=self.request.user.userprofile)]
        }

class DeleteAccountView(TemplateView):
    template_name = "base_delete_vars.html"

    def deactivate_team(self):
        user = player_models.User.objects.get(username=self.request.user.username)
        user.is_active = 0
        user.save()
        logout(self.request)

    def cleanse_roster(self, roster_list):
        for player in roster_list:
            player.delete()

    def post(self, *args, **kwargs):
        #drop roster for current week
        week = logic.getweek()
        team = player_models.Team.objects.get(owner=self.request.user.userprofile)
        roster_list = player_models.Roster.objects.filter(week=week, team=team)
        if week > 0 < 7:
            free_agent = player_models.UserProfile.objects.get(username="free_agent")
            self.cleanse_roster(roster_list)
            team.owner = free_agent
            team.save()
            self.deactivate_team()
        elif not week:
            self.cleanse_roster(roster_list)
            team.delete()
            self.deactivate_team()
        else:
            pass

        return HttpResponseRedirect('/')

class EditAccountView(TemplateView):
    template_name = 'base_profile_edit_vars.html'

    def post(self, *args):
        user = self.request.user
        profile = user.userprofile
        team = profile.team
        request = self.request
        query = self.request.POST.get('save')
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
            return HttpResponseRedirect("")

        if query == 'update_face':
            profile.userpic = request.POST.get('face')
            if profile.userpic:
                profile.save()
            else:
                profile.userpic = player_models.UserProfile.objects.get(user=user).userpic
            return HttpResponseRedirect("")

    def get_context_data(self, **kwargs):
        user = self.request.user
        return {
            'profile': user.userprofile,
            'team': user.userprofile.team
        }