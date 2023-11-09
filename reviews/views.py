from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Ticket, Review, UserFollows
from .forms import SubscriptionForm, TicketCreateForm
from django.urls import reverse_lazy


@login_required
def flow(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request, 'reviews/flow.html', {'tickets': tickets, 'reviews': reviews})


@login_required
def subscription_view(request):
    user = request.user

    # Utilisateurs suivis par l'utilisateur actif
    subscriptions = UserFollows.objects.filter(user=user)

    # Utilisateurs qui suivent l'utilisateur actif
    followers = UserFollows.objects.filter(follow_user=user)

    form = SubscriptionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        followee = form.cleaned_data['follow_user']
        if not UserFollows.objects.filter(user=user, follow_user=followee).exists():
            UserFollows.objects.create(user=user, follow_user=followee)

    return render(request, 'reviews/subscriptions.html', {'subscriptions': subscriptions, 'followers': followers, 'form': form})


def user_posts(request):
    user = request.user
    user_tickets = Ticket.objects.filter(user=user)
    user_reviews = Review.objects.filter(user=user)

    context = {'user': user, 'user_tickets': user_tickets, 'user_reviews' : user_reviews}    
    return render(request, 'reviews/user_posts.html', context)


@login_required
def unfollow(request, follow_id):

    user_follow = UserFollows.objects.get(id=follow_id)

    if user_follow.user == request.user:
        user_follow.unfollow()

    return redirect('subscriptions')


# Liste de tous les tickets
class TicketList(ListView):
    model = Ticket
    template_name = 'reviews/ticket_list.html'
    context_object_name = 'tickets'


# Détail d'un ticket
class TicketDetail(DetailView):
    model = Ticket
    template_name = 'reviews/ticket_detail.html'
    context_object_name = 'ticket'


# Création d'un ticket (nécessite une authentification)
class TicketCreate(CreateView, LoginRequiredMixin):
    model = Ticket
    template_name = 'reviews/ticket_form.html'
    form_class = TicketCreateForm
    success_url = reverse_lazy('flow')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Liste de toutes les critiques
class ReviewList(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'


# Détail d'une critique
class ReviewDetail(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'
    context_object_name = 'review'


# Création d'une critique (nécessite une authentification)
class ReviewCreate(CreateView, LoginRequiredMixin):
    model = Review
    template_name = 'reviews/review_form.html'
    fields = ['book_title', 'book_desc', 'book_image', 'rating', 'ticket']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
