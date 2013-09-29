# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'project_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('alias', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'project', ['Project'])

        # Adding model 'Membership'
        db.create_table(u'project_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teams', to=orm['project.Project'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teams', to=orm['account.User'])),
            ('date_joined', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'project', ['Membership'])

        # Adding model 'SpentTime'
        db.create_table(u'project_spenttime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='spent_time', to=orm['account.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='spent_time', to=orm['project.Project'])),
            ('task', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('finished_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('eta', self.gf('django.db.models.fields.DateTimeField')()),
            ('spent_time', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'project', ['SpentTime'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'project_project')

        # Deleting model 'Membership'
        db.delete_table(u'project_membership')

        # Deleting model 'SpentTime'
        db.delete_table(u'project_spenttime')


    models = {
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jid': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'project.membership': {
            'Meta': {'object_name': 'Membership'},
            'date_joined': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': u"orm['project.Project']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': u"orm['account.User']"})
        },
        u'project.project': {
            'Meta': {'object_name': 'Project'},
            'alias': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'team': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['account.User']", 'through': u"orm['project.Membership']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'project.spenttime': {
            'Meta': {'object_name': 'SpentTime'},
            'eta': ('django.db.models.fields.DateTimeField', [], {}),
            'finished_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spent_time'", 'to': u"orm['project.Project']"}),
            'spent_time': ('django.db.models.fields.FloatField', [], {}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spent_time'", 'to': u"orm['account.User']"})
        }
    }

    complete_apps = ['project']