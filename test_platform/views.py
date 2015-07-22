from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import *


def index(request):
    return render(request, 'test_platform/index.html')

class SubjectListView(generic.ListView):
    template_name = "test_platform/subject/list.html"
    context_object_name = "subject_list"

    def get_context_data(self, **kwargs):
        context = super(SubjectListView, self).get_context_data(**kwargs)
        context['title'] = 'Test platform | Subjects'
        return context

    def get_queryset(self):
        return Subject.objects.all()

class SubjectDetailView(generic.DetailView):
    template_name = "test_platform/subject/detail.html"
    model = Subject
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super(SubjectDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Test platform | Subject detail'
        return context


def subject_test_view(request, subject_id):

    all_question_of_subject = Question.objects.filter(
        subject_id=subject_id,
    )

    if all_question_of_subject.count() < 20:
        return render(request, "test_platform/subject/detail.html", {
            'subject': Subject.objects.get(pk=subject_id),
            'error_message': "Sorry, but database doesn't have enough question for this subject!",
            'title': "Test platform | Subject detail"
        })

    random_questions = all_question_of_subject.order_by('?')[:20]

    return render(request, 'test_platform/subject/test.html', {
        'questions': random_questions,
        'subject': Subject.objects.get(pk=subject_id),
        'title': "Test"
    })

def topic_test_view(request, subject_id, topic_id):

    all_question_of_subject_and_topic = Question.objects.filter(
        subject_id=subject_id,
        topic_id=topic_id,
    )

    if all_question_of_subject_and_topic.count() <= 0:
        return render(request, 'test_platform/subject/detail.html', {
            'error_message': "Sorry, but database doesn't have enough questions for this topic",
            'subject': Subject.objects.get(pk=subject_id),
            'title': "Test platform | Subject",
        })

    """ not more than 20 questions """
    if all_question_of_subject_and_topic.count() > 20:
        all_question_of_subject_and_topic = all_question_of_subject_and_topic.order_by('?')[:20]

    return render(request, 'test_platform/subject/test.html', {
        'questions': all_question_of_subject_and_topic,
        'subject': Subject.objects.get(pk=subject_id),
        'title': "Test platform | Topic test"
    })

def test(request, subject_id):

    if not request.POST:
        return redirect('/subject', subject_id=subject_id )

    # ex: { question_id: answer_id }
    # One question - one answer
    user_post_data = [{question_id.split('_')[1]: request.POST[question_id]} for question_id in request.POST if question_id.split('_')[0] == 'questionId']

    result = {
        'questions': [],
        'wrong_answers': [],
        'right_answers': []
    }

    for user_question_and_answer in user_post_data:
        for user_question_id, user_answer_id in user_question_and_answer.items():
            try:
                question = Question.objects.get(pk=user_question_id)
            except(KeyError, Question.DoesNotExist):
                return render(request, 'test_platform/subject/detail.html', {
                    'error_message': "Not allowed question in test!",
                    'subject': Subject.objects.get(pk=subject_id),
                    'title': 'Test platform | Subjects',
                })

            try:
                answer = question.answer_set.filter(is_right=True).first()
            except:
                return render(request, 'test_platform/subject/detail.html', {
                    'error_message': "Couldn't find answer or more then one answer for question!",
                    'subject': Subject.objects.get(pk=subject_id),
                    'title': 'Test platform | Subjects',
                })

            if answer.id == int(user_answer_id):
                result['right_answers'].append(answer.id)
            else:
                result['wrong_answers'].append(Answer.objects.get(pk=user_answer_id).id)
                pass

            result['questions'].append(question.id)

    result_str = "Your score is %s of %s" % (len(result['right_answers']), (len(result['questions'])))

    request.session['test_data'] = {
        'result_str': result_str,
        'result': result,
        'title': "Test platform | Test",
    }

    return HttpResponseRedirect(reverse('test_platform:result', args=(subject_id,)))


def result(request, subject_id):

    post_data = request.session.get('test_data')

    if not post_data:
        return render(request, 'test_platform/subject/detail.html', {
            'error_message': "Some problems with input data!",
            'subject': Subject.objects.get(pk=subject_id),
            'title': 'Test platform | Subjects',
        })

    del request.session['test_data']
    request.session.modified = True

    results = {
        'questions':   [Question.objects.get(pk=q_id) for q_id in post_data['result']['questions']],
        'right_answers': [Answer.objects.get(pk=a_id) for a_id in post_data['result']['right_answers']],
        'wrong_answers': [Answer.objects.get(pk=a_id) for a_id in post_data['result']['wrong_answers']],
    }

    return render(request, 'test_platform/subject/result.html', {
        'result_str': post_data['result_str'],
        'result': results,
        'title': post_data['title'],
        'subject': Subject.objects.get(pk=subject_id),
    })


