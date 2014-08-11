import time
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelformset_factory
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, render_to_response
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from responses.forms import ErrorBox, RatingForm, ResponseForm
from responses.models import User, Assess, Response, Question, Rating, SurveyTemplate
from arcassess import utils, responses


def admin(request):
    if request.method == 'POST':
        return reverse_lazy('assess_create')
    return render(request, 'admin.html')


def submit(request, survey_id):

    userid = responses.get_or_create_userid(request)
    user, created = User.objects.get_or_create(id=userid)
    survey = get_object_or_404(Assess, pk=survey_id)
    thanks = ""
    response_id = None

    if request.method == 'GET':
        try:
            response = Response.objects.get(responder=user, request=survey)
            RatingFormSet = modelformset_factory(Rating, form=RatingForm, max_num=1)
            ratings_formset = RatingFormSet(queryset=Rating.objects.filter(response=response))
            response_form = ResponseForm(instance=response)
            response_id = response.id
        except Response.DoesNotExist:
            initial_ratings = []
            questions = Question.objects.filter(template_id=survey.template.id)
            for question in questions:
                initial_ratings.append({'question': question.question, 'score': None})
            RatingFormSet = modelformset_factory(Rating, form=RatingForm, extra=len(questions))
            ratings_formset = RatingFormSet(initial=initial_ratings, queryset=Rating.objects.none())
            response_form = ResponseForm()
            response_id = None

        return render(request, 'form.html', {'rating_forms': ratings_formset,
                                             'response_form': response_form,
                                             'thanks': None,
                                             'response_id': response_id})

    if request.method == 'POST':
        RatingFormSet = modelformset_factory(Rating, form=RatingForm)
        ratings_formset = RatingFormSet(request.POST, error_class=ErrorBox)
        response_form = ResponseForm(request.POST, error_class=ErrorBox)
        response_id = request.POST.get('id', None)
        ratings = []
        if ratings_formset.is_valid() and response_form.is_valid():
            response = Response(request=survey, responder=user, word=response_form.clean_word(), id=response_id)
            response.save()
            response_id = response.id
            for rating in ratings_formset:
                if rating.cleaned_data['id']:
                    new_rating = Rating(
                        response=response,
                        question=rating.cleaned_data['question'],
                        score=rating.cleaned_data['score'],
                        id=rating.cleaned_data['id'].id
                    )
                else:
                    new_rating = Rating(
                        response=response,
                        question=rating.cleaned_data['question'],
                        score=rating.cleaned_data['score'],
                        id=None
                    )
                new_rating = new_rating.save()
                ratings.append(new_rating)
            RatingFormSet = modelformset_factory(Rating, form=RatingForm, max_num=1)
            ratings_formset = RatingFormSet(queryset=Rating.objects.filter(response=response))
            response_form = ResponseForm(instance=response)
            thanks = "Thank you for submitting your answers. You can " \
                     "amend them now or later if you need to."

        return render(request, 'form.html',
                  {'rating_forms': ratings_formset, 'response_form': response_form, 'thanks': thanks,
                   'response_id': response_id})


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


def chart(request):
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            }
    }
    return render_to_response('piechart.html', data)


class QuestionList(ListView):
    model = Question
    context_object_name = 'object_list'
    template_name = 'questions.html'

    def get_queryset(self):
        return Question.objects.filter(template=self.kwargs['template_id'])


class QuestionCreate(CreateView):
    model = Question
    fields = ['template', 'question']
    template_name = 'question_form.html'

    def get_initial(self):
        return {'template': self.kwargs['template_id']}

    def get_success_url(self):
        return reverse_lazy('question_list', kwargs={'template_id': self.kwargs['template_id']})


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['question']
    template_name = 'question_form.html'

    def get_success_url(self):
        return reverse_lazy('question_list', kwargs={'template_id': self.kwargs['template_id']})


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('question_list')
    template_name = 'question_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('question_list', kwargs={'template_id': self.kwargs['template_id']})


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


class AssessDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('admin')


class AssessList(ListView):
    model = Question
    context_object_name = 'object_list'
    template_name = 'admin.html'

    def get_queryset(self):
        return Assess.objects.filter(creator=self.request.user).order_by('-creation_date')


class SurveyTemplateCreate(CreateView):
    model = SurveyTemplate
    fields = ['name', 'word_flag']
    template_name = 'surveytemplate_form.html'
    success_url = reverse_lazy('template_list')
