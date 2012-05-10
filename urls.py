from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from myproject import views as base_views
from player_card import views as player_card_views
from top_player_list import views as top_player_list
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', base_views.HomeView.as_view(), name='home'),
	url(r'^home/$', base_views.HomeView.as_view(), name='home'),
	url(r'^players/$', base_views.HomeView.as_view(), name='home'),
	url(r'^blue/$', base_views.BlankView.as_view(), name='blank'),
	url(r'^player/(?P<player_id>\w+)/$', player_card_views.PlayerPageView.as_view(), name='player'),
    url(r'^uteam/(?P<team_id>\w+)/$', base_views.NotMyTeamView.as_view(), name='uteam'),
    url(r'^about/$', 'myproject.views.about',name='about'),
    url(r'^uteam/$', 'myproject.views.my_team_page',name='myteam'),
    url(r'^myteam/$', 'myproject.views.my_team_page',name='myteam'),
	url(r'^league/$', 'myproject.views.league_page',name='league'),
    url(r'^league/(?P<week>\w+)/$', 'myproject.views.league_page',name='league'),
    url(r'^leagueadmin/$', 'myproject.views.leagueadmin',name='leagueadmin'),
    url(r'^leagueadmin/(?P<arg>\w+)/$', 'myproject.views.leagueadmin',name='leagueadmin'),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$', 'myproject.views.logout_user',name='logout_user'),
	url(r'^profile/$', base_views.ProfileView.as_view(),name='ProfileView'),
    url(r'^profile/edit/$', 'myproject.views.profileedit',name='profileedit'),
	url(r'^joinleague/$', 'myproject.views.joinleague',name='joinleague'),
	url(r'^pickup/(?P<posid>\w+)/$', 'myproject.views.pickup',name='pickup'),
	url(r'^list/(?P<posid>\w+)/$', 'myproject.views.list_player',name='list'),
    url(r'^matchup/$', 'myproject.views.matchup_page',name='matchup'),
    url(r'^draft/$', 'myproject.views.draftpage',name='draftpage'),
    url(r'^matchup/$', 'myproject.views.matchup_page',name='matchup'),
    url(r'^matchup/(?P<matchup_id>\w+)/$', 'myproject.views.matchup_page',name='matchup'),
    url(r'^sysadmin/$', 'myproject.views.sysadmin',name='sysadmin'),
    url(r'^sysadmin/(?P<arg>\w+)/(?P<argval>.*?)$', 'myproject.views.sysadmin',name='sysadmin'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^playerpage/$','myproject.top_player_list.views.playerpage'),
    url(r'^playerpage/(?P<arg>\w+)','myproject.top_player_list.views.playerpage'),
    url(r'^leaguelist/(?P<league_id>\w+)','myproject.views.league_list'),
    url(r'^transactions/$', 'myproject.views.transactions_page'),
)
