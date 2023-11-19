from django import forms
from .models import UserFollows, Ticket, Review, UserBlock


class SubscriptionForm(forms.ModelForm):
    # Form fo user subscription
    class Meta:
        model = UserFollows
        fields = ['follow_user']
        widgets = {
                    'follow_user': forms.TextInput(attrs={'placeholder': 'Entrez le nom d\'utilisateur'}),
                    }


class BlockForm(forms.ModelForm):
    # For for user block
    class Meta:
        model = UserBlock
        fields = ['block_user']
        widgets = {
                    'block_user': forms.TextInput(attrs={'placeholder': 'Entrez le nom d\'utilisateur'}),
        }


class TicketCreateForm(forms.ModelForm):
    # Form for creation of a ticket
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre', }


class ReviewCreateForm(forms.ModelForm):
    # For for creation of a review
    ticket_title = forms.CharField(max_length=255, label='Titre')
    ticket_description = forms.CharField(widget=forms.Textarea, label='Description')
    ticket_image = forms.ImageField(label='Image')

    RATING_CHOICES = [
        (0, "- 0"),
        (1, "- 1"),
        (2, "- 2"),
        (3, "- 3"),
        (4, "- 4"),
        (5, "- 5"),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['ticket_title', 'ticket_description', 'ticket_image', 'headline', 'body', 'rating']

        labels = {'headline': 'Titre', 'body': 'Description', 'rating': 'Note'}
