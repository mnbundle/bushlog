# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Reserve'
        db.create_table(u'reserve_reserve', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('border', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reserves', to=orm['location.Polygon'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'reserve', ['Reserve'])

        # Adding M2M table for field species on 'Reserve'
        db.create_table(u'reserve_reserve_species', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reserve', models.ForeignKey(orm[u'reserve.reserve'], null=False)),
            ('species', models.ForeignKey(orm[u'wildlife.species'], null=False))
        ))
        db.create_unique(u'reserve_reserve_species', ['reserve_id', 'species_id'])

        # Adding M2M table for field country on 'Reserve'
        db.create_table(u'reserve_reserve_country', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reserve', models.ForeignKey(orm[u'reserve.reserve'], null=False)),
            ('country', models.ForeignKey(orm[u'location.country'], null=False))
        ))
        db.create_unique(u'reserve_reserve_country', ['reserve_id', 'country_id'])


    def backwards(self, orm):
        # Deleting model 'Reserve'
        db.delete_table(u'reserve_reserve')

        # Removing M2M table for field species on 'Reserve'
        db.delete_table('reserve_reserve_species')

        # Removing M2M table for field country on 'Reserve'
        db.delete_table('reserve_reserve_country')


    models = {
        u'location.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'location.polygon': {
            'Meta': {'object_name': 'Polygon'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'reserve.reserve': {
            'Meta': {'ordering': "['name']", 'object_name': 'Reserve'},
            'border': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reserves'", 'to': u"orm['location.Polygon']"}),
            'country': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'reserves'", 'symmetrical': 'False', 'to': u"orm['location.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'species': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'reserves'", 'symmetrical': 'False', 'to': u"orm['wildlife.Species']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'wildlife.species': {
            'Meta': {'ordering': "['common_name']", 'object_name': 'Species'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'default_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'female_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'female_info'", 'to': u"orm['wildlife.SpeciesInfo']"}),
            'general_info': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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

    complete_apps = ['reserve']