# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pro_Team'
        db.create_table('tecmo_player_pro_team', (
            ('short', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key='true')),
            ('long', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('bye', self.gf('django.db.models.fields.IntegerField')()),
            ('wins', self.gf('django.db.models.fields.IntegerField')()),
            ('loss', self.gf('django.db.models.fields.IntegerField')()),
            ('tie', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('tecmo_player', ['Pro_Team'])

        # Adding model 'Player'
        db.create_table('tecmo_player_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('player_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('pro_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tecmo_player.Pro_Team'])),
            ('picture', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('tecmo_player', ['Player'])

        # Adding model 'Schedule'
        db.create_table('tecmo_player_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('away', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('awayscore', self.gf('django.db.models.fields.IntegerField')()),
            ('home', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('homescore', self.gf('django.db.models.fields.IntegerField')()),
            ('week', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('tecmo_player', ['Schedule'])

        # Adding model 'Stats'
        db.create_table('tecmo_player_stats', (
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tecmo_player.Player'])),
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
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('fanpts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('guid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal('tecmo_player', ['Stats'])


    def backwards(self, orm):
        # Deleting model 'Pro_Team'
        db.delete_table('tecmo_player_pro_team')

        # Deleting model 'Player'
        db.delete_table('tecmo_player_player')

        # Deleting model 'Schedule'
        db.delete_table('tecmo_player_schedule')

        # Deleting model 'Stats'
        db.delete_table('tecmo_player_stats')


    models = {
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
        },
        'tecmo_player.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'away': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'awayscore': ('django.db.models.fields.IntegerField', [], {}),
            'home': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'homescore': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'week': ('django.db.models.fields.IntegerField', [], {})
        },
        'tecmo_player.stats': {
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
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tecmo_player.Player']"}),
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
        }
    }

    complete_apps = ['tecmo_player']