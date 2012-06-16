from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from messages import views as message_views
from tfb import views as base_views
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
    url(r'^about/$', 'tfb.views.about',name='about'),
    url(r'^uteam/$', 'tfb.views.my_team_page',name='myteam'),
    url(r'^myteam/$', 'tfb.views.my_team_page',name='myteam'),
    url(r'^messages/$', message_views.MessageView.as_view(),name='message'),
	url(r'^league/$', 'tfb.views.league_page',name='league'),
    url(r'^league/(?P<week>\w+)/$', 'tfb.views.league_page',name='league'),
    url(r'^leagueadmin/$', 'tfb.views.leagueadmin',name='leagueadmin'),
    url(r'^leagueadmin/(?P<arg>\w+)/$', 'tfb.views.leagueadmin',name='leagueadmin'),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$', 'tfb.views.logout_user',name='logout_user'),
	url(r'^profile/$', base_views.ProfileView.as_view(),name='ProfileView'),
    url(r'^profile/edit/$', 'tfb.views.profileedit',name='profileedit'),
	url(r'^joinleague/$', 'tfb.views.joinleague',name='joinleague'),
	url(r'^pickup/(?P<posid>\w+)/$', 'tfb.views.pickup',name='pickup'),
	url(r'^list/(?P<posid>\w+)/$', 'tfb.views.list_player',name='list'),
    url(r'^matchup/$', 'tfb.views.matchup_page',name='matchup'),
    url(r'^draft/$', 'tfb.draft.views.draftpage',name='draftpage'),
    url(r'^matchup/$', 'tfb.views.matchup_page',name='matchup'),
    url(r'^matchup/(?P<matchup_id>\w+)/$', 'tfb.views.matchup_page',name='matchup'),
    url(r'^sysadmin/$', '.views.sysadmin',name='sysadmin'),
    url(r'^sysadmin/(?P<arg>\w+)/(?P<argval>.*?)$', 'tfb.views.sysadmin',name='sysadmin'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^playerpage/$', 'tfb.top_player_list.views.playerpage'),
    url(r'^playernotfound/$', top_player_list.PlayerNotFound.as_view()),
    url(r'^playerpage/(?P<arg>\w+)', 'tfb.top_player_list.views.playerpage'),
    url(r'^playerpage/(?P<arg>\w+)', 'tfb.top_player_list.views.playerpage'),
    url(r'^leaguelist/(?P<league_id>\w+)', 'tfb.views.league_list'),
    url(r'^transactions/$', 'tfb.views.transactions_page'),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
