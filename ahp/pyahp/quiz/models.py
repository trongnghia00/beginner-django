from django.db import models

# Create your models here.

from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    weight_adjustments = models.JSONField(default=dict)  # Lưu các thay đổi độ ưu tiên tiêu chí

    def __str__(self):
        return self.choice_text