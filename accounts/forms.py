from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm

class UserCreationForm(BaseCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].label = 'Display Name'