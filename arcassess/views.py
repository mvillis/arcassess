from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http import request
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from responses.forms import SurveyResponseForm, ErrorBox
from responses.models import User, Assess, Response, Question, Rating
from arcassess import utils, responses


def admin(request):
    if request.method == 'POST':
        return reverse_lazy('assess_create')
    return render(request, 'admin.html')


def submit(request, survey_id):
    userid = responses.get_or_create_userid(request)
    user, created = User.objects.get_or_create(id=userid)
    survey = get_object_or_404(Assess, pk=survey_id)
    questions = Question.objects.filter(template_id=survey.template.id)
    thanks = ""
    if request.method == 'POST':
        form = SurveyResponseForm(request.POST, error_class=ErrorBox)
        response_id = request.POST.get('id', None)
        if form.is_valid():
            srf = form.cleaned_data
            # TODO check that id is unique!
            response = Response(id=response_id, request=survey, word=srf['word'], responder=user)
            response.save()
            response_id = response.id
            form_data = []
            for question in questions:
                try:
                    previous = Rating.objects.get(response=response, question=question.question)
                    previous.score = form.data[str(question.id)]
                    previous.save()
                    form_data.append([question.id, question.question, previous.score])
                except Rating.DoesNotExist:
                    rating = Rating(response=response, question=question.question, score=form.data[str(question.id)])
                    rating.save()
                    form_data.append([question.id, question.question, rating.score])
            data = {'response': response, 'questions': form_data}
            form = SurveyResponseForm(data=data)
            thanks = "Thank you for submitting your answers. You can " \
                     "amend them now or later if you need to"
        else:
            # data = {'response': {'word': ''}, 'questions': form_data}
            form = SurveyResponseForm(data=data)
    else:
        form_data = []

        try:
            previous = Response.objects.get(request=survey_id, responder=user)
            ratings = Rating.objects.filter(response=previous)
            for rating in ratings:
                question = Question.objects.get(template=survey.template, question=rating.question)
                form_data.append([question.id, question.question, rating.score])
            response_id = previous.id
        except Response.DoesNotExist:
            previous = None
            response_id = None
            for question in survey.template.question_set.all():
                form_data.append([question.id, question.question, None])
        data = {'response': previous, 'questions': form_data}
        form = SurveyResponseForm(data=data)
    return render(request, 'form.html', {'form': form, 'thanks': thanks, 'response_id': response_id})


def result(request, survey_id):
    survey = get_object_or_404(Assess, pk=survey_id)
    if request.user == survey.creator:
        arcassess = Assess.objects.get(pk=survey_id)
        results = arcassess.response_set.all()
        return render(request, 'results.html', {'id': survey_id, 'stats': survey.stats(), 'results': results})
    else:
        raise PermissionDenied


def home(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect("/admin/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {'form': form, })


def questions(request):
    if request.method == 'POST':
        form_id = utils.random_string(8)
        # TODO check that id is unique!
        survey = Assess(creation_date=datetime.now(), creator=request.user, id=form_id)
        survey.save()
        return HttpResponseRedirect('/admin/%s' % form_id)
    return render(request, 'questions.html')


class QuestionList(ListView):
    model = Question
    context_object_name = 'object_list'
    # queryset = Question.objects.filter(archassess)
    template_name = 'questions.html'


class QuestionCreate(CreateView):
    model = Question
    fields = ['template', 'question']
    template_name = 'question_form.html'
    success_url = reverse_lazy('question_list')


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['question']
    template_name = 'question_form.html'
    success_url = reverse_lazy('question_list')


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('question_list')


class AssessCreate(CreateView):
    model = Assess
    fields = ['template']
    template_name = 'assess_form.html'
    success_url = reverse_lazy('result')

    def form_valid(self, form):
        assess = form.save(commit=False)
        assess.creator = self.request.user
        assess.save()
        return HttpResponseRedirect(reverse_lazy('result', kwargs={'survey_id': assess.id}))
        # return HttpResponseRedirect('/admin/%s' % form_id)


class AssessDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('admin')


class AssessList(ListView):
    model = Question
    context_object_name = 'object_list'
    template_name = 'admin.html'

    def get_queryset(self):
        return Assess.objects.filter(creator=self.request.user).order_by('-creation_date')


