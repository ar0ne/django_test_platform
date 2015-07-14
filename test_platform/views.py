from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from .models import *

# landing page?
def index(request):
    return render(request, 'test_platform/index.html')

class SubjectListView(generic.ListView):
    template_name = "test_platform/subject/list.html"
    context_object_name = "subject_list"

    def get_queryset(self):
        return Subject.objects.all()

class SubjectView(generic.DetailView):
    template_name = "test_platform/subject/detail.html"
    model = Subject

class TopicListView(generic.ListView):
    template_name = "test_platform/topic/list.html"
    model = Topic
    context_object_name = "topic_list"

    def get_queryset(self):
        return Topic.objects.filter(
            subject_id=self.kwargs['pk'],
        )

def subject_test_view(request, subject_id):

    all_question_of_subject = Question.objects.filter(
        subject_id=subject_id,
    )

    if all_question_of_subject.count() < 20:
        return render(request, "test_platform/subject/detail.html", {
            'subject': Subject.objects.get(pk=subject_id),
            'error_message': "Sorry, but database doesn't have enought question for this subject!"
        })

    random_questions = all_question_of_subject.order_by('?')[:20]

    return render(request, 'test_platform/topic/test.html', {
        'questions': random_questions,
        'subject_id': subject_id,
    })

def topic_test_view(request, subject_id, topic_id):

    all_question_of_subject_and_topic = Question.objects.filter(
        subject_id=subject_id,
        topic_id=topic_id,
    )

    if all_question_of_subject_and_topic.count() <= 0:
        return render(request, 'test_platform/topic/list.html', {
            'error_message': "Sorry, but database doesn't have enought questions for this topics",
            'topic_list': Topic.objects.filter(
                subject_id=subject_id,
            )
        })

    """ not more than 20 questions """
    if all_question_of_subject_and_topic.count() > 20:
        all_question_of_subject_and_topic = all_question_of_subject_and_topic.order_by('?')[:20]

    return render(request, 'test_platform/topic/test.html', {
        'questions': all_question_of_subject_and_topic,
        'subject_id': subject_id,
    })

def test(request, subject_id):
    count = 0
    for post_q in request.POST:
        if post_q.split("_")[0] != 'questionId':
            continue
        else:
            try:
                question = Question.objects.get(pk=post_q.split("_")[1])
            except(KeyError, Question.DoesNotExist):
                return render(request, 'test_platform/subject',{
                    'error_message': "Not allowed answer in test!",
                    'subject_id': subject_id
                })
            else:
                for answer in question.answer_set.filter(is_right=True):
                    if answer.id == int(request.POST[post_q]):
                        count += 1

    result = "Your score is %s / %s" % (count, (len(request.POST) - 1))

 #   return HttpResponseRedirect(reverse("test_platform:result", args=(subject_id,)))
    return render_to_response('test_platform/topic/result.html', {
        'result': result,
    })

def result_view(request, subject_id,result):
    return render(request, 'test_platform/topic/result.html', {
        'subject_id': subject_id,
        'result': result,
    })
