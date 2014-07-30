from django import forms
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.http import request
from arcassess.responses.models import Response, Assess, Rating
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re


class ErrorBox(ErrorList):
    def __unicode__(self):
        return mark_safe(self.as_box())

    def as_box(self):
        if not self: return u''
        return u'<div class="error box">%s</div>' % self.as_lines()

    def as_lines(self):
        return "<br/>".join(e for e in self)


class SurveyResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['word']

    word = forms.CharField(label='Word', max_length=32)

    def clean_score(self):
        score = self.cleaned_data['score']
        if int(score) < 1:
            raise forms.ValidationError('temperature %d is too low' % score)
        if int(score) > 10:
            raise forms.ValidationError('temperature %d is too high' % score)
        return score

    def clean_word(self):
        word = self.cleaned_data['word']
        matches = re.findall(r'[^A-Za-z0-9\'-]', word)
        if matches:
            error = '"{word}" contains invalid characters ' \
                    '{matches}'.format(word=escape(word), matches=list({str(x) for x in matches}))
            raise forms.ValidationError(error)
        return word

    def get_score_for_question(self, question):
        try:
            return Rating.objects.get(question=question.question).score
        except Rating.DoesNotExist:
            return None


