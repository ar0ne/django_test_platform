from django.conf.urls import include, url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
    # ex: /subject/
    url(r'^subject/$', views.SubjectListView.as_view(), name='subject_list'),
    # ex: /subject/2/
    url(r'^subject/(?P<pk>[0-9]+)/$', views.SubjectView.as_view(), name='subject'),
    # ex: /subject/2/test/
    url(r'^subject/(?P<subject_id>[0-9]+)/test/$', views.subject_test_view, name='subject_test'),
    # ex: /subject/2/topic/
    url(r'^subject/(?P<pk>[0-9]+)/topic/$', views.TopicListView.as_view(), name='topic_list'),
    # ex: /subject/2/topic/3/test/
    url(r'^subject/(?P<subject_id>[0-9]+)/topic/(?P<topic_id>[0-9]+)/test/$', views.topic_test_view, name='topic_test'),
    # ex: /subject/2/topic/3/test/act/
    url(r'^subject/(?P<subject_id>[0-9]+)/test/act/$', views.test, name='test'),
    # ex: /subject/2/topic/3/result/
    url(r'^subject/(?P<subject_id>[0-9]+)/result/$', views.result_view, name='result'),

]
