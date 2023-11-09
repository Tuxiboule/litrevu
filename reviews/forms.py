from django import forms
from .models import UserFollows, Ticket


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['follow_user']


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre',}