from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class AgentForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',
                  'username',
                  'first_name',
                  'last_name'
                  )
