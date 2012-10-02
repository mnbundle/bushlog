# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Reserve'
        db.create_table('reserve_reserve', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('bottom_left_bound', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bottom_left_bound', to=orm['location.Coordinate'])),
            ('top_right_bound', self.gf('django.db.models.fields.related.ForeignKey')(related_name='top_right_bound', to=orm['location.Coordinate'])),
        ))
        db.send_create_signal('reserve', ['Reserve'])


    def backwards(self, orm):
        # Deleting model 'Reserve'
        db.delete_table('reserve_reserve')


    models = {
        'location.coordinate': {
            'Meta': {'object_name': 'Coordinate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'})
        },
        'reserve.reserve': {
            'Meta': {'object_name': 'Reserve'},
            'bottom_left_bound': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bottom_left_bound'", 'to': "orm['location.Coordinate']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'top_right_bound': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'top_right_bound'", 'to': "orm['location.Coordinate']"})
        }
    }

    complete_apps = ['reserve']