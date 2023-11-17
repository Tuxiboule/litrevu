from django import forms
from .models import UserFollows, Ticket, Review, UserBlock


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['follow_user']
        widgets = {
                    'follow_user': forms.TextInput(attrs={'placeholder': 'Entrez le nom d\'utilisateur'}),
                    }


class BlockForm(forms.ModelForm):
    class Meta:
        model = UserBlock
        fields = ['block_user']
        widgets = {
                    'block_user': forms.TextInput(attrs={'placeholder': 'Entrez le nom d\'utilisateur'}),
        }


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre', }


class ReviewCreateForm(forms.ModelForm):

    ticket_title = forms.CharField(max_length=255, label='Titre')
    ticket_description = forms.CharField(widget=forms.Textarea, label='Description')
    ticket_image = forms.ImageField(label='Image')

    class Meta:
        model = Review
        fields = ['ticket_title', 'ticket_description', 'ticket_image', 'headline', 'body', 'rating']

        labels = {'headline': 'Titre', 'body': 'Description', 'rating': 'Note'}
