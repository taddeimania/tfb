# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Matchup'
        db.delete_table('players_matchup')


    def backwards(self, orm):
        # Adding model 'Matchup'
        db.create_table('players_matchup', (
            ('week', self.gf('django.db.models.fields.IntegerField')()),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.League'])),
            ('team_two_points', self.gf('django.db.models.fields.IntegerField')()),
            ('team_one', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_one', to=orm['players.Team'])),
            ('team_two', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_two', to=orm['players.Team'])),
            ('team_one_points', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winner', null=True, to=orm['players.Team'])),
        ))
        db.send_create_signal('players', ['Matchup'])


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
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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
            'image': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
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
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'userpic': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['players']