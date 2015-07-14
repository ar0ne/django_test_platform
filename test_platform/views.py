from django.shortcuts import render
from django.views import generic
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
            subject_id = self.kwargs['pk']
        )

def subject_test(request, subject_id):
    return render(request, 'test_platform/subject/test.html')

def topic_test(request, subject_id, topic_id):
    return render(request, 'test_platform/topic/test.html')