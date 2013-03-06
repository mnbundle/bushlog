# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SightingImage.caption'
        db.delete_column('sighting_sightingimage', 'caption')


        # Changing field 'SightingImage.sighting'
        db.alter_column('sighting_sightingimage', 'sighting_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['sighting.Sighting']))

    def backwards(self, orm):
        # Adding field 'SightingImage.caption'
        db.add_column('sighting_sightingimage', 'caption',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2013, 3, 6, 0, 0), max_length=50),
                      keep_default=False)


        # Changing field 'SightingImage.sighting'
        db.alter_column('sighting_sightingimage', 'sighting_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sighting.Sighting']))

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
        'sighting.sighting': {
            'Meta': {'ordering': "['-date_of_sighting']", 'object_name': 'Sighting'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_sighting': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'estimated_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Coordinate']"}),
            'reserve': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sightings'", 'to': "orm['reserve.Reserve']"}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sightings'", 'to': "orm['wildlife.Species']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sightings'", 'to': "orm['auth.User']"}),
            'with_kill': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'with_young': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'sighting.sightingimage': {
            'Meta': {'object_name': 'SightingImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'sighting': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'to': "orm['sighting.Sighting']"})
        },
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

    complete_apps = ['sighting']