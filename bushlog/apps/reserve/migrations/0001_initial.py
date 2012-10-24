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
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='users', null=True, to=orm['location.Country'])),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('bottom_left_bound', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bottom_left_bound', to=orm['location.Coordinate'])),
            ('top_right_bound', self.gf('django.db.models.fields.related.ForeignKey')(related_name='top_right_bound', to=orm['location.Coordinate'])),
        ))
        db.send_create_signal('reserve', ['Reserve'])

        # Adding M2M table for field species on 'Reserve'
        db.create_table('reserve_reserve_species', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reserve', models.ForeignKey(orm['reserve.reserve'], null=False)),
            ('species', models.ForeignKey(orm['wildlife.species'], null=False))
        ))
        db.create_unique('reserve_reserve_species', ['reserve_id', 'species_id'])


    def backwards(self, orm):
        # Deleting model 'Reserve'
        db.delete_table('reserve_reserve')

        # Removing M2M table for field species on 'Reserve'
        db.delete_table('reserve_reserve_species')


    models = {
        'location.coordinate': {
            'Meta': {'object_name': 'Coordinate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'})
        },
        'location.country': {
            'Meta': {'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'reserve.reserve': {
            'Meta': {'object_name': 'Reserve'},
            'bottom_left_bound': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bottom_left_bound'", 'to': "orm['location.Coordinate']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'to': "orm['location.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'species': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'reserves'", 'symmetrical': 'False', 'to': "orm['wildlife.Species']"}),
            'top_right_bound': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'top_right_bound'", 'to': "orm['location.Coordinate']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'wildlife.species': {
            'Meta': {'object_name': 'Species'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'default_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'female_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'female_info'", 'to': "orm['wildlife.SpeciesInfo']"}),
            'general_info': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'male_info'", 'to': "orm['wildlife.SpeciesInfo']"}),
            'marker': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'similiar_species': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'similiar_species_rel_+'", 'null': 'True', 'to': "orm['wildlife.Species']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'wildlife.speciesinfo': {
            'Meta': {'object_name': 'SpeciesInfo'},
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '1', 'blank': 'True'}),
            'horn_length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '1', 'blank': 'True'}),
            'mass': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['reserve']