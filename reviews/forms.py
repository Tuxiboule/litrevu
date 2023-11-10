from django import forms
from .models import UserFollows, Ticket


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['follow_user']
        widgets = {
                    'follow_user': forms.TextInput(attrs={'placeholder': 'Entrez le nom d\'utilisateur'}),
                    }


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre',}