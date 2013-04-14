# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Species.inverted_default_image'
        db.add_column(u'wildlife_species', 'inverted_default_image',
                      self.gf('django.db.models.fields.files.ImageField')(default=' ', max_length=250),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Species.inverted_default_image'
        db.delete_column(u'wildlife_species', 'inverted_default_image')


    models = {
        u'wildlife.species': {
            'Meta': {'ordering': "['common_name']", 'object_name': 'Species'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'default_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'female_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'female_info'", 'to': u"orm['wildlife.SpeciesInfo']"}),
            'general_info': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inverted_default_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'male_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'male_info'", 'to': u"orm['wildlife.SpeciesInfo']"}),
            'marker': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'similiar_species': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'similiar_species_rel_+'", 'null': 'True', 'to': u"orm['wildlife.Species']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'wildlife.speciesinfo': {
            'Meta': {'object_name': 'SpeciesInfo'},
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '1', 'blank': 'True'}),
            'horn_length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '1', 'blank': 'True'}),
            'mass': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['wildlife']