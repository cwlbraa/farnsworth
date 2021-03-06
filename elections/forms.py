'''
Project: Farnsworth

Author: Karandeep Singh Nagra
'''

from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory

from elections.models import Petition, PetitionComment, \
    Poll, PollSettings, PollQuestion, PollChoice, \
    PollAnswer, PollRanks

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ("title", "description", "end_date")

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        super(PetitionForm, self).__init__(*args, **kwargs)

    def save(self):
        petition = super(PetitionForm, self).save(commit=False)
        petition.owner = self.profile
        petition.save()

class PetitionCommentForm(forms.ModelForm):
    class Meta:
        model = PetitionComment
        fields = ("body",)

    def __init__(self, *args, **kwargs):
        self.petition = kwargs.pop('petition')
        self.profile = kwargs.pop('profile')
        super(PetitionCommentForm, self).__init__(*args, **kwargs)

    def save(self):
        comment = super(PetitionCommentForm, self).save(commit=False)
        comment.user = self.profile
        comment.petition = self.petition
        comment.save()
        comment.petition.number_of_comments += 1
        comment.petition.save()

class PetitionSignatureForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        self.petition = kwargs.pop('petition')
        super(PetitionSignatureForm, self).save(*args, **kwargs)

    def save(self):
        if self.profile in self.petition.signatures.all():
            self.petition.signatures.remove(self.profile)
        else:
            self.petition.signatures.add(self.profile)
        self.petition.save()
        return self.petition

class PollForm(form.ModelForm):
    class Meta:
        model = Poll
        fields = (
            "title",
            "description",
            "close_date",
            "anonymity_allowed",
            "alumni_allowed",
            )

    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        if 'election' in kwargs:
            self.election = True
            self.fields.pop('anonymity_allowed')
            self.fields.pop('alumni_allowed')
        else:
            self.election = False
        self.profile = kwargs.pop('profile')

    def save(self):
        poll = super(PollForm, self).save(commit=False)
        if self.election:
            poll.election = True
            poll.anonymity_allowed = True
        poll.save()

class PollQuestionForm(models.Model):
    choices = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="One line per option.",
        )

    class Meta:
        model = PollQuestion
        fields = ("body", "question_type", "range_upper_limit", "write_ins_allowed")

    def __init__(self, *args, **kwargs):
        super(PollQuestionForm, self).__init__(*args, **kwargs)
        self.fields['ranger_upper_limit'].required = False
        self.fields['write_ins_allowed'].required = False

    def is_valid(self):
        if not super(PollQuestionForm, self).is_valid():
            return False
        if self.cleaned_data['question_type'] != PollQuestion.TEXT:
            if not self.cleaned_data['choice_text']:
                self._errors['choices'] = self.error_class(
                    [u"No choices entered.  Choices are required for a {0} type question.".format(
                        dict(self.fields['question_type'].choices)[self.cleaned_data['question_type']
                        )
                    )
                return False
            if not self.cleaned_data['choice_text'].endswith('\n'):
                self.cleaned_data['choice_text'] += '\n'
            if self.cleaned_data['choice_text'].count('\n') < 2:
                self._errors['choices'] = self.error_class(
                    [u"Only one choice entered. Maybe this should be a yes/no question?"]
                    )
                return False
        if self.cleaned_data['question_type'] == PollQuestion.RANGE:
            if not self.cleaned_data['range_upper_limit']:
                self._errors['range_upper_limit'] = self.error_class(
                    [u"No upper limit entered.  An upper limit is required for range type questions."]
                    )
                return False
            if self.cleaned_data['range_upper_limit'] < 1:
                self._errors['range_upper_limit'] = self.error_class(
                    [u"Upper limit is less than 1.  It must be at least 1."]
                    )
                return False
        return True

    def save(self):
        question = super(PollQuestionForm, self).save(commit=False)
        if self.cleaned_data['question_type'] in [PollQuestion.CHOICE,
          PollQuestion.RANK, PollQuestion.CHECKBOXES]:
            for choice_string in self.cleaned_data['choices'].split('\n'):
                choice = Choice(question=question, body=choice_string)
                choice.save()
        return question

class BasePollQuestionFormSet(BaseModelFormSet):
    def save(self, poll):
        questions = super(BasePollQuestionFormSet, self).save(commit=False):
        for question in questions:
            question.poll = poll
            question.save()
        return questions

PollQuestionFormSet = modelformset_factory(
    PollQuestion, form=PollQuestionForm,
    formset=BasePollQuestionFormSet,
    can_delete=True, extra=1, max_num=50,
    )

class QuestionAnswerForm(forms.Form):
    """ Form for a user to answer a question. """
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        self.question = kwargs.pop('question')
        super(QuestionAnswerForm, self).__init__(*args, **kwargs)
        if self.question.question_type == PollQuestion.CHOICE:
            self.fields['answer'] = forms.ModelChoiceField(
                    queryset=PollChoice.objects.filter(question=self.question),
                    widget=forms.widgets.RadioSelect,
                    required=self.question.required,
                    )
        elif self.question.question_type == PollQuestion.CHECKBOXES:
            self.fields['answer'] = forms.ModelMultipleChoiceField(
                    queryset=PollChoice.objects.filter(question=self.question),
                    widget=forms.widgets.CheckboxSelectMultiple,
                    required=self.question.required,
                    )
        elif self.question.question_type == PollQuestion.TEXT:
            self.fields['answer'] = forms.CharField(
                    widget=forms.Textarea,
                    required=self.question.required,
                    )
        elif self.question.question_type == PollQuestion.RANK:
            for c in PollChoice.objects.filter(question=self.question):
                self.fields['rank_{0}'.format(c.pk)] = forms.IntegerField(required=False)
                self.fields['rank_{0}'.format(c.pk)].label = c.name
        elif self.question.question_type == PollQuestion.RANGE:
            for c in PollChoice.objects.filter(question=self.question):
                self.fields['range_{0}'.format(c.pk)] = forms.ChoiceField(
                    choices = ((s, str(s)) for s in range(0, self.question.range_upper_limit)),
                    required=self.question.required,
                    )

    def save(self):
        if self.question.question_type == PollQuestion.CHOICE:
            for c in self.question.poll_choice_set.all():
                if self.profile.user in c.voters.all():
                    c.voters.remove(self.profile.user)
                    c.save()
            poll_choice = self.cleaned_data['answer']
            poll_choice.voters.add(self.profile.user)
            poll_choice.save()
        elif self.question.question_type == PollQuestion.CHECKBOXES:
            for c in self.question.poll_choice_set.all():
                if self.profile.user in c.voters.all():
                    c.voters.remove(self.profile.user)
                    c.save()
            for poll_choice in self.cleaned_data['answer']:
                poll_choice.voters.add(self.profile.user)
                poll_choice.save()
        elif self.question.question_type == PollQuestion.TEXT:
          and self.cleaned_data['answer']:
            poll_answer = PollAnswer(
                question=self.question,
                body=self.cleaned_data['answer'],
                owner=self.profile.user,
                )
            poll_answer.save()
        elif self.question.question_type == PollQuestion.RANK:
            choice_rankings = [(c, self.cleaned_data['rank_{}'.format(c.pk)]) for c in self.question.poll_choice_set.all()]
            choice_rankings = PollRanks.normalize_ranking(choice_rankings)
            poll_ranks = PollRanks(
                question=self.question,
                rankings=PollRanks.create_ranking(choice_rankings),
                owner=self.profile.user,
                )
            poll_ranks.save()
        elif self.question.question_type == PollQuestion.RANGE:
            choice_rankings = [(c, self.cleaned_data['rank_{}'.format(c.pk)]) for c in self.question.poll_choice_set.all()]
            poll_ranks = PollRanks(
                question=self.question,
                rankings=PollRanks.create_ranking(choice_rankings),
                owner=self.profile.user,
                )
            poll_ranks.save()
