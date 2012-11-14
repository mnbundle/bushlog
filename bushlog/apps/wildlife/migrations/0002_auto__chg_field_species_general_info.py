# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Species.general_info'
        db.alter_column('wildlife_species', 'general_info', self.gf('django.db.models.fields.CharField')(max_length=250))

    def backwards(self, orm):

        # Changing field 'Species.general_info'
        db.alter_column('wildlife_species', 'general_info', self.gf('django.db.models.fields.TextField')())

    models = {
        'wildlife.species': {
            'Meta': {'object_name': 'Species'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'default_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'female_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'female_info'", 'to': "orm['wildlife.SpeciesInfo']"}),
            'general_info': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
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

    complete_apps = ['wildlife']