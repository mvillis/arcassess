# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'responses_user', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True)),
        ))
        db.send_create_signal(u'responses', ['User'])

        # Adding model 'SurveyTemplate'
        db.create_table(u'responses_surveytemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('word_flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'responses', ['SurveyTemplate'])

        # Adding M2M table for field users on 'SurveyTemplate'
        m2m_table_name = db.shorten_name(u'responses_surveytemplate_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('surveytemplate', models.ForeignKey(orm[u'responses.surveytemplate'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['surveytemplate_id', 'user_id'])

        # Adding model 'Assess'
        db.create_table(u'responses_assess', (
            ('id', self.gf('django.db.models.fields.CharField')(default='GaXgh27g', max_length=8, primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responses.SurveyTemplate'])),
        ))
        db.send_create_signal(u'responses', ['Assess'])

        # Adding model 'Response'
        db.create_table(u'responses_response', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responses.Assess'])),
            ('responder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responses.User'])),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'responses', ['Response'])

        # Adding model 'Question'
        db.create_table(u'responses_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responses.SurveyTemplate'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'responses', ['Question'])

        # Adding model 'Rating'
        db.create_table(u'responses_rating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responses.Response'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'responses', ['Rating'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'responses_user')

        # Deleting model 'SurveyTemplate'
        db.delete_table(u'responses_surveytemplate')

        # Removing M2M table for field users on 'SurveyTemplate'
        db.delete_table(db.shorten_name(u'responses_surveytemplate_users'))

        # Deleting model 'Assess'
        db.delete_table(u'responses_assess')

        # Deleting model 'Response'
        db.delete_table(u'responses_response')

        # Deleting model 'Question'
        db.delete_table(u'responses_question')

        # Deleting model 'Rating'
        db.delete_table(u'responses_rating')


    models = {
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'responses.assess': {
            'Meta': {'object_name': 'Assess'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'GaXgh27g'", 'max_length': '8', 'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['responses.SurveyTemplate']"})
        },
        u'responses.question': {
            'Meta': {'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['responses.SurveyTemplate']"})
        },
        u'responses.rating': {
            'Meta': {'object_name': 'Rating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['responses.Response']"}),
            'score': ('django.db.models.fields.IntegerField', [], {})
        },
        u'responses.response': {
            'Meta': {'object_name': 'Response'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['responses.Assess']"}),
            'responder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['responses.User']"}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'responses.surveytemplate': {
            'Meta': {'object_name': 'SurveyTemplate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'word_flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'responses.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'})
        }
    }

    complete_apps = ['responses']