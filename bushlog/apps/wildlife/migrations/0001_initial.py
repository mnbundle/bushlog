# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SpeciesInfo'
        db.create_table(u'wildlife_speciesinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('height', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=1, blank=True)),
            ('length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=1, blank=True)),
            ('mass', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=1, blank=True)),
            ('horn_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=1, blank=True)),
        ))
        db.send_create_signal(u'wildlife', ['SpeciesInfo'])

        # Adding model 'Species'
        db.create_table(u'wildlife_species', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('scientific_name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('marker', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('default_image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('general_info', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('female_info', self.gf('django.db.models.fields.related.ForeignKey')(related_name='female_info', to=orm['wildlife.SpeciesInfo'])),
            ('male_info', self.gf('django.db.models.fields.related.ForeignKey')(related_name='male_info', to=orm['wildlife.SpeciesInfo'])),
        ))
        db.send_create_signal(u'wildlife', ['Species'])

        # Adding M2M table for field similiar_species on 'Species'
        db.create_table(u'wildlife_species_similiar_species', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_species', models.ForeignKey(orm[u'wildlife.species'], null=False)),
            ('to_species', models.ForeignKey(orm[u'wildlife.species'], null=False))
        ))
        db.create_unique(u'wildlife_species_similiar_species', ['from_species_id', 'to_species_id'])


    def backwards(self, orm):
        # Deleting model 'SpeciesInfo'
        db.delete_table(u'wildlife_speciesinfo')

        # Deleting model 'Species'
        db.delete_table(u'wildlife_species')

        # Removing M2M table for field similiar_species on 'Species'
        db.delete_table('wildlife_species_similiar_species')


    models = {
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

    complete_apps = ['wildlife']