from django.forms import ModelForm, Form
from django import forms
from .models import Lead, Agent, Category
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()


class LeadForm(ModelForm):
    class Meta:
        model = Lead
        fields = ('first_name',
                  'last_name',
                  'age',
                  'agent',
                  'description',
                  'phone_number',
                  'email')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}


class AssignAgentForm(Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        # we use pop cause django form does not expect request. so we actually do need to remove it.
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class LeadCategoryUpdateForm(ModelForm):
    class Meta:
        model = Lead
        fields = ('category',)


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
