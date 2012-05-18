# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Region'
        db.create_table('estatebase_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['Region'])

        # Adding model 'Locality'
        db.create_table('estatebase_locality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Region'], null=True, blank=True)),
        ))
        db.send_create_signal('estatebase', ['Locality'])

        # Adding model 'Microdistrict'
        db.create_table('estatebase_microdistrict', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('locality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Locality'])),
        ))
        db.send_create_signal('estatebase', ['Microdistrict'])

        # Adding model 'Street'
        db.create_table('estatebase_street', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('locality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Locality'])),
        ))
        db.send_create_signal('estatebase', ['Street'])

        # Adding model 'EstateTypeCategory'
        db.create_table('estatebase_estatetypecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['EstateTypeCategory'])

        # Adding model 'EstateType'
        db.create_table('estatebase_estatetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('estate_type_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.EstateTypeCategory'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('estatebase', ['EstateType'])

        # Adding model 'Estate'
        db.create_table('estatebase_estate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estate_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.EstateType'], null=True, blank=True)),
        ))
        db.send_create_signal('estatebase', ['Estate'])


    def backwards(self, orm):
        
        # Deleting model 'Region'
        db.delete_table('estatebase_region')

        # Deleting model 'Locality'
        db.delete_table('estatebase_locality')

        # Deleting model 'Microdistrict'
        db.delete_table('estatebase_microdistrict')

        # Deleting model 'Street'
        db.delete_table('estatebase_street')

        # Deleting model 'EstateTypeCategory'
        db.delete_table('estatebase_estatetypecategory')

        # Deleting model 'EstateType'
        db.delete_table('estatebase_estatetype')

        # Deleting model 'Estate'
        db.delete_table('estatebase_estate')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'estatebase.estate': {
            'Meta': {'object_name': 'Estate'},
            'estate_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'estatebase.estatetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'EstateType'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'estate_type_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateTypeCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'estatebase.estatetypecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'EstateTypeCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
        },
        'estatebase.locality': {
            'Meta': {'ordering': "['name']", 'object_name': 'Locality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'null': 'True', 'blank': 'True'})
        },
        'estatebase.microdistrict': {
            'Meta': {'ordering': "['name']", 'object_name': 'Microdistrict'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.street': {
            'Meta': {'ordering': "['name']", 'object_name': 'Street'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['estatebase']