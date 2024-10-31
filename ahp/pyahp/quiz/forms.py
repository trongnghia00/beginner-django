from django import forms
from .models import Question, Choice

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        questions = Question.objects.all()
        for question in questions:
            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.question_text,
                choices=choices,
                widget=forms.RadioSelect
            )