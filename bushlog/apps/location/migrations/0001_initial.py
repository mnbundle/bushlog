# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Polygon'
        db.create_table(u'location_polygon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'location', ['Polygon'])

        # Adding model 'Coordinate'
        db.create_table(u'location_coordinate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
            ('polygon', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='coordinates', null=True, to=orm['location.Polygon'])),
        ))
        db.send_create_signal(u'location', ['Coordinate'])

        # Adding model 'Country'
        db.create_table(u'location_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'location', ['Country'])


    def backwards(self, orm):
        # Deleting model 'Polygon'
        db.delete_table(u'location_polygon')

        # Deleting model 'Coordinate'
        db.delete_table(u'location_coordinate')

        # Deleting model 'Country'
        db.delete_table(u'location_country')


    models = {
        u'location.coordinate': {
            'Meta': {'object_name': 'Coordinate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'polygon': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'coordinates'", 'null': 'True', 'to': u"orm['location.Polygon']"})
        },
        u'location.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'location.polygon': {
            'Meta': {'object_name': 'Polygon'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['location']