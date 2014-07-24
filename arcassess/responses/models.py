import django
from django.db import models

class User(models.Model):
    id = models.CharField(max_length=8, primary_key=True)


class ArcAssess(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    creation_date = models.DateField()
    creator = models.ForeignKey(django.contrib.auth.models.User)

    def stats(self):
        result = dict()
        responses = self.response_set.all()
        result['count'] = responses.count()
        result['average'] = responses.aggregate(models.Avg('score'))
        result['words'] = responses.values('word').annotate(models.Count("id")).order_by()
        return result

    def __unicode__(self):
        return u"{}: {} {}".format(self.id, self.creator.id,
                                   self.creation_date)


class Response(models.Model):
    request = models.ForeignKey(ArcAssess)
    responder = models.ForeignKey(User)
    score = models.IntegerField()
    word = models.CharField(max_length=32)

    def __unicode__(self):
        return u"{}: {} {} {} {}".format(self.id, self.request.id,
                                         self.responder.id,
                                         self.score, self.word)
