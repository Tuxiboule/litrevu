from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    # Form for signup user
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)
