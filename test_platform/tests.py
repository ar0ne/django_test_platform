from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Question, Answer, Subject, Topic


def create_subject(subject_name="Test=Subject", description=""):
    return Subject.objects.create(subject_name=subject_name,description=description)

def create_topic(subject, topic_name="Test Topic", description=""):
    return Topic.objects.create(topic_name=topic_name, subject=subject, description=description)

def create_question(subject, topic=None, question_text="Test Question", explanation=""):
    return Question.objects.create(question_text=question_text, topic=topic, subject=subject, explanation=explanation)

def create_answer(question, is_right, answer_text="Test Answer"):
    return Answer.objects.create(answer_text=answer_text, question=question, is_right=is_right)

class QuestionTest(TestCase):
    def test_question_have_at_least_one_right_answer_1(self):
        """
        One question must have at least one right answer
        """
        subject = create_subject()
        question = create_question(subject=subject)
        for status in [True, False, True]:
            create_answer(question=question, is_right=status)
        self.assertEqual(len(question.answer_set.filter(is_right=True)) > 0, True)

    def test_question_have_at_least_one_right_answer_2(self):
        """
        One question must have at least one right answer
        """
        subject = create_subject()
        question = create_question(subject=subject)
        for status in [True, True, True]:
            create_answer(question=question, is_right=status)
        self.assertEqual(len(question.answer_set.filter(is_right=True)) > 0, True)

    def test_question_have_at_least_one_right_answer_3(self):
        """
        One question must have at least one right answer
        """
        subject = create_subject()
        question = create_question(subject=subject)
        for status in [False, False, True]:
            create_answer(question=question, is_right=status)
        self.assertEqual(len(question.answer_set.filter(is_right=True)) > 0, True)

    def test_question_have_at_least_one_right_answer_4(self):
        """
        One question must have at least one right answer
        """
        subject = create_subject()
        question = create_question(subject=subject)
        for status in [False, False, False]:
            create_answer(question=question, is_right=status)
        self.assertEqual(len(question.answer_set.filter(is_right=True)) > 0, False)

    def test_topic_from_other_subject(self):
        """
        Topic can't be not from question.subject
        """
        subject_for_topic = create_subject()
        subject_for_question = create_subject()
        topic = create_topic(subject=subject_for_topic)
        try:
            question = create_question(subject=subject_for_question, topic=topic)
        except:
            pass
        else:
            self.assertEqual(question.topic.subject_id == question.subject.id, True,
                "Question can't be from different subjects")

class TopicTest(TestCase):
    def test_topic_from_other_subject(self):
        """
        Topic can't be from subject which don't have his questions
        """
        subject_for_topic = create_subject()
        topic = create_topic(subject=subject_for_topic)
        subject_for_question = create_subject()
        try:
            question = create_question(topic=topic, subject=subject_for_question)
        except:
            pass
        else:
            self.assertEqual(topic.subject.id == question.topic.subject.id, True,
                "Topic can't have different subject and questions from other")

    def test_questions_from_different_subjects(self):
        """
        Two question from one topic can't be from different subjects
        """
        main_subject = create_subject()
        topic = create_topic(subject=main_subject)
        try:
            question_1 = create_question(subject=main_subject, topic=topic)
            question_2 = create_question(subject=create_subject(), topic=topic)
        except:
            pass
        else:
            self.assertEqual(len(topic.question_set.filter(subject=main_subject)) == len(topic.question_set.all()), True,
                "All question must to be from one subject")

class SubjectListViewTest(TestCase):
    def test_index_view_with_no_subjects(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('test_platform:subject_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No subjects are available.')
        self.assertQuerysetEqual(response.context['subject_list'], [])

    def test_index_view_with_subject(self):
        """
        View must to show available subjects.
        """
        sub_1 = create_subject(subject_name="Subject 1")
        sub_2 = create_subject(subject_name="Subject 2")
        response = self.client.get(reverse('test_platform:subject_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, sub_1.subject_name, status_code=200)
        self.assertContains(response, sub_2.subject_name, status_code=200)

class SubjectDetailViewTest(TestCase):
    def test_subject_without_questions_and_topics(self):
        """
        View mustn't have 'Subject Test' button and any topics
        """
        sub = create_subject()
        response = self.client.get(reverse('test_platform:subject', args=(sub.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No topics are available.')
        self.assertNotContains(response, 'Subject Test')

    def test_subject_without_questions_but_with_topic(self):
        """
        View must not have 'Subject Test' button, but contain topics
        """
        sub = create_subject()
        topic = create_topic(subject=sub, topic_name='Test Topic')
        response = self.client.get(reverse('test_platform:subject', args=(sub.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'No topics are available.')
        self.assertContains(response, 'Test Topic')
        self.assertNotContains(response, 'Subject Test')