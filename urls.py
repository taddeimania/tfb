from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from tfb import views as base_views
from tfb.messages import views as message_views
from tfb.player_card import views as player_card_views
from tfb.top_player_list import views as top_player_list
from tfb.draft import views as draft_views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', base_views.about, name='about'),
	url(r'^home/$', base_views.HomeView.as_view(), name='home'),
	url(r'^players/$', base_views.HomeView.as_view(), name='home'),
	url(r'^blue/$', base_views.BlankView.as_view(), name='blank'),
	url(r'^player/(?P<player_id>\w+)/$', player_card_views.PlayerPageView.as_view(), name='player'),
    url(r'^uteam/(?P<team_id>\w+)/$', base_views.NotMyTeamView.as_view(), name='uteam'),
    url(r'^about/$', base_views.about ,name='about'),
    url(r'^uteam/$', base_views.my_team_page,name='myteam'),
    url(r'^myteam/$', base_views.my_team_page,name='myteam'),
    url(r'^messages/$', message_views.MessageView.as_view(),name='message'),
	url(r'^league/$', base_views.league_page,name='league'),
    url(r'^league/(?P<week>\w+)/$', base_views.league_page,name='league'),
    url(r'^leagueadmin/$', base_views.leagueadmin,name='leagueadmin'),
    url(r'^leagueadmin/(?P<arg>\w+)/$', base_views.leagueadmin,name='leagueadmin'),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$', base_views.logout_user,name='logout_user'),
	url(r'^profile/$', base_views.ProfileView.as_view(),name='ProfileView'),
    url(r'^profile/edit/$', base_views.profileedit,name='profileedit'),
	url(r'^joinleague/$', base_views.joinleague,name='joinleague'),
	url(r'^pickup/(?P<posid>\w+)/$', base_views.pickup,name='pickup'),
	url(r'^list/(?P<posid>\w+)/$', base_views.list_player,name='list'),
    url(r'^matchup/$', base_views.matchup_page,name='matchup'),
    url(r'^draft/$', draft_views.draftpage, name='draftpage'),
    url(r'^drag/$', draft_views.drag_and_drop, name='draftpage'),
    url(r'^matchup/$', base_views.matchup_page,name='matchup'),
    url(r'^matchup/(?P<matchup_id>\w+)/$', base_views.matchup_page,name='matchup'),
    url(r'^sysadmin/$', base_views.sysadmin,name='sysadmin'),
    url(r'^sysadmin/(?P<arg>\w+)/(?P<argval>.*?)$', base_views.sysadmin,name='sysadmin'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^playerpage/$', top_player_list.playerpage),
    url(r'^playernotfound/$', top_player_list.PlayerNotFound.as_view()),
    url(r'^playerpage/(?P<arg>\w+)', top_player_list.playerpage),
    url(r'^playerpage/(?P<arg>\w+)', top_player_list.playerpage),
    url(r'^leaguelist/(?P<league_id>\w+)', base_views.league_list),
    url(r'^transactions/$', base_views.transactions_page),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
