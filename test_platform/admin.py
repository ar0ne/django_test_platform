from django.contrib import admin
from django import forms
from django.forms.models import BaseInlineFormSet

from .models import Question, Answer, Subject, Topic


class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):
    def clean(self):
        """Check that at least one service has been entered."""
        super(AtLeastOneRequiredInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('At least one item required.')

class AnswerInline(admin.TabularInline):
    model = Answer
    formset = AtLeastOneRequiredInlineFormSet

class QuestionAdmin(admin.ModelAdmin):
    """
    Sounds like django have issue with foreign keys
    https://github.com/PetrDlouhy/django-related-admin
    more here:
    http://stackoverflow.com/questions/163823/can-list-display-in-a-django-modeladmin-display-attributes-of-foreignkey-field
    """
    list_display = ('question_text', 'subject', 'topic', 'explanation' )
    inlines = [AnswerInline]
    list_filter = ['subject', 'topic']

class TopicInline(admin.TabularInline):
    extra = 1
    model = Topic

class SubjectAdmin(admin.ModelAdmin):
    inlines = [TopicInline]

class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_name', 'subject')
    list_filter = ['subject']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Question, QuestionAdmin)