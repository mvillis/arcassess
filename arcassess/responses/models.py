import django
from django.db import models
from django.http import request
from arcassess import utils


class User(models.Model):
    id = models.CharField(max_length=8, primary_key=True)


class SurveyTemplate(models.Model):
    name = models.CharField(max_length=128)
    word_flag = models.BooleanField(default=True)
    users = models.ManyToManyField(django.contrib.auth.models.User)

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def __unicode__(self):
        return u"{}: {}".format(self.id, self.name)


class Assess(models.Model):
    id = models.CharField(max_length=8, primary_key=True, default=utils.random_string(8))
    creation_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(django.contrib.auth.models.User)
    template = models.ForeignKey(SurveyTemplate)

    def stats(self):
        result = dict()
        responses = self.response_set.all()
        result['average'] = responses.aggregate(models.Avg('rating__score'))
        result['count'] = responses.count()
        result['words'] = responses.values('word').annotate(models.Count("id")).order_by()
        return result

    def __unicode__(self):
        return u"{}: {} {}".format(self.template.name, self.creation_date.isoformat(), self.id)


class Response(models.Model):
    request = models.ForeignKey(Assess)
    responder = models.ForeignKey(User)
    word = models.CharField(max_length=32)

    def stats(self):
        result = dict()
        ratings = self.rating_set.all()
        result['average'] = ratings.aggregate(models.Avg('score'))
        result['values'] = ratings.values('score')
        return result

    def __unicode__(self):
        return u"{}: {} {} {} {}".format(self.id, self.request.id,
                                         self.responder.id,
                                         self.word)


class Question(models.Model):
    template = models.ForeignKey(SurveyTemplate)
    question = models.CharField(max_length=256)

    def __unicode__(self):
        return u"{}: {}".format(self.id, self.question)


class Rating(models.Model):
    response = models.ForeignKey(Response)
    question = models.CharField(max_length=256)
    score = models.IntegerField()