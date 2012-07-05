# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pro_Team'
        db.create_table('players_pro_team', (
            ('short', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key='true')),
            ('long', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('bye', self.gf('django.db.models.fields.IntegerField')()),
            ('wins', self.gf('django.db.models.fields.IntegerField')()),
            ('loss', self.gf('django.db.models.fields.IntegerField')()),
            ('tie', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('players', ['Pro_Team'])

        # Adding model 'Player'
        db.create_table('players_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('player_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('pro_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Pro_Team'])),
            ('picture', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('players', ['Player'])

        # Adding model 'Schedule'
        db.create_table('players_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('away', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('awayscore', self.gf('django.db.models.fields.IntegerField')()),
            ('home', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('homescore', self.gf('django.db.models.fields.IntegerField')()),
            ('week', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('players', ['Schedule'])

        # Adding model 'Stats'
        db.create_table('players_stats', (
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'])),
            ('week', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('pa', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pc', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pastd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('intcp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pasyds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rec', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recyds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rectd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('krtd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('prtd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rusat', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rusyds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rustd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('xpm', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fgm', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tm2', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('health', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('fanpts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('guid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal('players', ['Stats'])

        # Adding model 'League'
        db.create_table('players_league', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('lslogan', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('maxteam', self.gf('django.db.models.fields.IntegerField')()),
            ('active', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('invite_code', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
        ))
        db.send_create_signal('players', ['League'])

        # Adding model 'UserProfile'
        db.create_table('players_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('userpic', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('players', ['UserProfile'])

        # Adding model 'Team'
        db.create_table('players_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.UserProfile'])),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.League'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('win', self.gf('django.db.models.fields.IntegerField')()),
            ('loss', self.gf('django.db.models.fields.IntegerField')()),
            ('slogan', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('total_points', self.gf('django.db.models.fields.IntegerField')()),
            ('total_points_against', self.gf('django.db.models.fields.IntegerField')()),
            ('iscommish', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
        ))
        db.send_create_signal('players', ['Team'])

        # Adding model 'Roster'
        db.create_table('players_roster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('week', self.gf('django.db.models.fields.IntegerField')()),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Team'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'])),
        ))
        db.send_create_signal('players', ['Roster'])

        # Adding model 'Curweek'
        db.create_table('players_curweek', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('curweek', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('players', ['Curweek'])

        # Adding model 'Transaction'
        db.create_table('players_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Team'])),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.League'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.UserProfile'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'])),
        ))
        db.send_create_signal('players', ['Transaction'])

        # Adding model 'Matchup'
        db.create_table('players_matchup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('week', self.gf('django.db.models.fields.IntegerField')()),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.League'])),
            ('team_one', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_one', to=orm['players.Team'])),
            ('team_one_points', self.gf('django.db.models.fields.IntegerField')()),
            ('team_two', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_two', to=orm['players.Team'])),
            ('team_two_points', self.gf('django.db.models.fields.IntegerField')()),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winner', null=True, to=orm['players.Team'])),
        ))
        db.send_create_signal('players', ['Matchup'])

        # Adding model 'Season'
        db.create_table('players_season', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('players', ['Season'])

        # Adding model 'Trophy'
        db.create_table('players_trophy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('players', ['Trophy'])

        # Adding model 'TrophyAssignment'
        db.create_table('players_trophyassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.UserProfile'])),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Season'])),
            ('trophy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Trophy'])),
        ))
        db.send_create_signal('players', ['TrophyAssignment'])

        # Adding model 'SeasonRanking'
        db.create_table('players_seasonranking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ranking', self.gf('django.db.models.fields.IntegerField')()),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'])),
        ))
        db.send_create_signal('players', ['SeasonRanking'])


    def backwards(self, orm):
        # Deleting model 'Pro_Team'
        db.delete_table('players_pro_team')

        # Deleting model 'Player'
        db.delete_table('players_player')

        # Deleting model 'Schedule'
        db.delete_table('players_schedule')

        # Deleting model 'Stats'
        db.delete_table('players_stats')

        # Deleting model 'League'
        db.delete_table('players_league')

        # Deleting model 'UserProfile'
        db.delete_table('players_userprofile')

        # Deleting model 'Team'
        db.delete_table('players_team')

        # Deleting model 'Roster'
        db.delete_table('players_roster')

        # Deleting model 'Curweek'
        db.delete_table('players_curweek')

        # Deleting model 'Transaction'
        db.delete_table('players_transaction')

        # Deleting model 'Matchup'
        db.delete_table('players_matchup')

        # Deleting model 'Season'
        db.delete_table('players_season')

        # Deleting model 'Trophy'
        db.delete_table('players_trophy')

        # Deleting model 'TrophyAssignment'
        db.delete_table('players_trophyassignment')

        # Deleting model 'SeasonRanking'
        db.delete_table('players_seasonranking')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'players.curweek': {
            'Meta': {'object_name': 'Curweek'},
            'curweek': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'players.league': {
            'Meta': {'object_name': 'League'},
            'active': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'lslogan': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'maxteam': ('django.db.models.fields.IntegerField', [], {})
        },
        'players.matchup': {
            'Meta': {'object_name': 'Matchup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.League']"}),
            'team_one': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_one'", 'to': "orm['players.Team']"}),
            'team_one_points': ('django.db.models.fields.IntegerField', [], {}),
            'team_two': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_two'", 'to': "orm['players.Team']"}),
            'team_two_points': ('django.db.models.fields.IntegerField', [], {}),
            'week': ('django.db.models.fields.IntegerField', [], {}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner'", 'null': 'True', 'to': "orm['players.Team']"})
        },
        'players.player': {
            'Meta': {'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'player_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'pro_team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Pro_Team']"})
        },
        'players.pro_team': {
            'Meta': {'object_name': 'Pro_Team'},
            'bye': ('django.db.models.fields.IntegerField', [], {}),
            'long': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'loss': ('django.db.models.fields.IntegerField', [], {}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': "'true'"}),
            'tie': ('django.db.models.fields.IntegerField', [], {}),
            'wins': ('django.db.models.fields.IntegerField', [], {})
        },
        'players.roster': {
            'Meta': {'object_name': 'Roster'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Team']"}),
            'week': ('django.db.models.fields.IntegerField', [], {})
        },
        'players.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'away': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'awayscore': ('django.db.models.fields.IntegerField', [], {}),
            'home': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'homescore': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'week': ('django.db.models.fields.IntegerField', [], {})
        },
        'players.season': {
            'Meta': {'object_name': 'Season'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'players.seasonranking': {
            'Meta': {'ordering': "['ranking']", 'object_name': 'SeasonRanking'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']"}),
            'ranking': ('django.db.models.fields.IntegerField', [], {})
        },
        'players.stats': {
            'Meta': {'object_name': 'Stats'},
            'fanpts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fgm': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'guid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'health': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'intcp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'krtd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pa': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pastd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pasyds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pc': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']"}),
            'prtd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rec': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rectd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recyds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rusat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rustd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rusyds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tm2': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'week': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'xpm': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'players.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iscommish': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.League']"}),
            'loss': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.UserProfile']"}),
            'slogan': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_points': ('django.db.models.fields.IntegerField', [], {}),
            'total_points_against': ('django.db.models.fields.IntegerField', [], {}),
            'win': ('django.db.models.fields.IntegerField', [], {})
        },
        'players.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.League']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.UserProfile']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Team']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'players.trophy': {
            'Meta': {'object_name': 'Trophy'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'players.trophyassignment': {
            'Meta': {'object_name': 'TrophyAssignment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.UserProfile']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Season']"}),
            'trophy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Trophy']"})
        },
        'players.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'userpic': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['players']