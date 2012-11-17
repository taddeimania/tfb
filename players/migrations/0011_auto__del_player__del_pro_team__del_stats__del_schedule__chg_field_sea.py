# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Player'
        db.delete_table('players_player')

        # Deleting model 'Pro_Team'
        db.delete_table('players_pro_team')

        # Deleting model 'Stats'
        db.delete_table('players_stats')

        # Deleting model 'Schedule'
        db.delete_table('players_schedule')


        # Changing field 'SeasonRanking.player'
        db.alter_column('players_seasonranking', 'player_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tecmo_player.Player']))

        # Changing field 'Roster.player'
        db.alter_column('players_roster', 'player_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tecmo_player.Player']))

        # Changing field 'Transaction.player'
        db.alter_column('players_transaction', 'player_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tecmo_player.Player']))

    def backwards(self, orm):
        # Adding model 'Player'
        db.create_table('players_player', (
            ('picture', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('player_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('pos', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('pro_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Pro_Team'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('players', ['Player'])

        # Adding model 'Pro_Team'
        db.create_table('players_pro_team', (
            ('loss', self.gf('django.db.models.fields.IntegerField')()),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key='true')),
            ('wins', self.gf('django.db.models.fields.IntegerField')()),
            ('long', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('tie', self.gf('django.db.models.fields.IntegerField')()),
            ('bye', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('players', ['Pro_Team'])

        # Adding model 'Stats'
        db.create_table('players_stats', (
            ('prtd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rustd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'])),
            ('guid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('xpm', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pc', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pa', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fanpts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rec', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('health', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('week', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('fgm', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recyds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pastd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tm2', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('krtd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rectd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('intcp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rusyds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pasyds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rusat', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('players', ['Stats'])

        # Adding model 'Schedule'
        db.create_table('players_schedule', (
            ('week', self.gf('django.db.models.fields.IntegerField')()),
            ('awayscore', self.gf('django.db.models.fields.IntegerField')()),
            ('away', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('homescore', self.gf('django.db.models.fields.IntegerField')()),
            ('home', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('players', ['Schedule'])


        # Changing field 'SeasonRanking.player'
        db.alter_column('players_seasonranking', 'player_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player']))

        # Changing field 'Roster.player'
        db.alter_column('players_roster', 'player_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player']))

        # Changing field 'Transaction.player'
        db.alter_column('players_transaction', 'player_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player']))

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
        'players.roster': {
            'Meta': {'object_name': 'Roster'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tecmo_player.Player']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Team']"}),
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
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tecmo_player.Player']"}),
            'ranking': ('django.db.models.fields.IntegerField', [], {})
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
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tecmo_player.Player']"}),
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
        },
        'tecmo_player.player': {
            'Meta': {'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'player_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'pro_team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tecmo_player.Pro_Team']"})
        },
        'tecmo_player.pro_team': {
            'Meta': {'object_name': 'Pro_Team'},
            'bye': ('django.db.models.fields.IntegerField', [], {}),
            'long': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'loss': ('django.db.models.fields.IntegerField', [], {}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': "'true'"}),
            'tie': ('django.db.models.fields.IntegerField', [], {}),
            'wins': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['players']