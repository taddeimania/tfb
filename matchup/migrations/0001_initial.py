# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Matchup'
        db.create_table('matchup_matchup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('week', self.gf('django.db.models.fields.IntegerField')()),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(related_name='league', to=orm['players.League'])),
            ('team_one', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_one', to=orm['players.Team'])),
            ('team_one_points', self.gf('django.db.models.fields.IntegerField')()),
            ('team_two', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_two', to=orm['players.Team'])),
            ('team_two_points', self.gf('django.db.models.fields.IntegerField')()),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winner', null=True, to=orm['players.Team'])),
        ))
        db.send_create_signal('matchup', ['Matchup'])


    def backwards(self, orm):
        # Deleting model 'Matchup'
        db.delete_table('matchup_matchup')


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
        'matchup.matchup': {
            'Meta': {'object_name': 'Matchup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'league'", 'to': "orm['players.League']"}),
            'team_one': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_one'", 'to': "orm['players.Team']"}),
            'team_one_points': ('django.db.models.fields.IntegerField', [], {}),
            'team_two': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_two'", 'to': "orm['players.Team']"}),
            'team_two_points': ('django.db.models.fields.IntegerField', [], {}),
            'week': ('django.db.models.fields.IntegerField', [], {}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner'", 'null': 'True', 'to': "orm['players.Team']"})
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
        'players.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'userpic': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['matchup']