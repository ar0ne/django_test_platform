from django.db import models

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return self.subject_name

class Topic(models.Model):
    topic_name = models.CharField(max_length=100, default='Other')
    subject = models.ForeignKey(Subject)
    description = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return self.topic_name

class Question(models.Model):
    question_text = models.CharField(max_length=1000)
    explanation = models.CharField(max_length=300, default='', blank=True)
    topic = models.ForeignKey(Topic, blank=True, null=True)
    subject = models.ForeignKey(Subject)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    answer_text = models.CharField(max_length=300)
    question = models.ForeignKey(Question)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text





