from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.conf import settings
from arcassess.responses.models import SurveyTemplate

from arcassess.views import home, admin, submit, register, result, QuestionList, QuestionCreate, QuestionUpdate, QuestionDelete, AssessCreate, AssessList

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^about$', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^admin/(?P<survey_id>[0-9a-zA-Z]{8})/$', login_required(result), name='result'),
    url(r'^admin/questions/$', login_required(QuestionList.as_view()), name="question_list"),
    url(r'^admin/questions/add', login_required(QuestionCreate.as_view()), name='question_add'),
    url(r'question/(?P<pk>[0-9]+)/$', QuestionUpdate.as_view(), name='question_update'),
    url(r'question/(?P<pk>[0-9]+)/delete/$', QuestionDelete.as_view(), name='question_delete'),
    url(r'templates/$', ListView.as_view(model=SurveyTemplate, template_name='surveytemplate_list.html'), name='template_list'),
    url(r'^admin/$', login_required(AssessList.as_view()), name='admin'),
    url(r'^admin/create/$', login_required(AssessCreate.as_view()), name='assess_create'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/register/$', register, name='register'),
    url(r'^([0-9a-zA-Z]{8})$', submit),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
