from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Ticket, Review, UserFollows
from .forms import SubscriptionForm, TicketCreateForm, ReviewCreateForm
from django.urls import reverse_lazy
from authentication.models import User

from operator import attrgetter



@login_required
def flow(request):
    user = request.user
    items = prepare_flow(user)
    return render(request, 'reviews/flow.html', {'items': items})


def prepare_flow(user):
    reviews_list = []
    tickets_list = []
    posters = [user]

    follows = list(UserFollows.objects.filter(user=user))
    for follow in follows:
        posters.append(follow.follow_user)

    # add all ticket/review in dedicated lists
    for poster in posters:
        poster_reviews = Review.objects.filter(user=poster)
        poster_tickets = Ticket.objects.filter(user=poster)
        reviews_list += poster_reviews
        tickets_list += poster_tickets

    items = tickets_list + reviews_list
    for item in items:
        item.item_type = 'Review' if isinstance(item, Review) else 'Ticket'
    sorted_items = sorted(items, key=attrgetter("time_created"), reverse=True)

    return sorted_items

@login_required
def subscription_view(request):
    user = request.user

    # Utilisateurs suivis par l'utilisateur actif
    subscriptions = UserFollows.objects.filter(user=user)

    # Utilisateurs qui suivent l'utilisateur actif
    followers = UserFollows.objects.filter(follow_user=user)

    form = SubscriptionForm(request.POST or None)

    for object in User.objects.all():
        if form['follow_user'].value() == object.username:
            choice = object

    try:
        if request.method == 'POST' and form['follow_user'].value() == choice.username:
            followee = choice
            if not UserFollows.objects.filter(user=user, follow_user=followee).exists():
                UserFollows.objects.create(user=user, follow_user=followee)

    except Exception as e:
        print(e)

    return render(request, 'reviews/subscriptions.html', {'subscriptions': subscriptions, 'followers': followers, 'form': form})


@login_required
def user_posts(request):
    user = request.user
    user_tickets = list(Ticket.objects.filter(user=user))
    user_reviews = list(Review.objects.filter(user=user))
    items = user_tickets + user_reviews
    
    for item in items:
        item.item_type = 'Review' if isinstance(item, Review) else 'Ticket'
    sorted_items = sorted(items, key=attrgetter("time_created"), reverse=True)
    context = {'items': sorted_items}
    return render(request, 'reviews/user_posts.html', context)


@login_required
def unfollow(request, follow_id):

    user_follow = UserFollows.objects.get(id=follow_id)

    if user_follow.user == request.user:
        user_follow.unfollow()

    return redirect('subscriptions')

@login_required
def delete_item(request, item_id):

    print("Début de delete item", item_id)

    try:
        item = Ticket.objects.get(id=item_id)
    except Ticket.DoesNotExist:
        try:
            item = Review.objects.get(id=item_id)
        except Review.DoesNotExist:
            print("Pas d'item correspondant")
            return redirect('user_posts')

    # Vérifier si l'utilisateur a le droit de supprimer l'objet
    if item.user == request.user:
        item.delete()
        # Rediriger vers la page appropriée après la suppression
        return redirect('user_posts')
    else:
        return redirect('user_posts')
    

def ticket_update(request, ticket_id):

    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        form = TicketCreateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('user_posts')
    else:
        form = TicketCreateForm(instance=ticket)

    return render(request, 'reviews/ticket_update.html', {'form': form, 'ticket': ticket})


def review_update(request, review_id):
    review = Review.objects.get(id=review_id)

    # Préremplir les informations du ticket dans le formulaire
    ticket_data = {
        'ticket_title': review.ticket.title,
        'ticket_description': review.ticket.description,
        'ticket_image': review.ticket.image,
        # Ajoutez d'autres champs du ticket au besoin
    }
    print(request.method)
    if request.method == 'POST':
        form = ReviewCreateForm(request.POST, instance=review, initial=ticket_data)
        if form.is_valid():
            form.save()
            return redirect('user_posts')
    else:
        form = ReviewCreateForm(instance=review, initial=ticket_data)

    return render(request, 'reviews/review_update.html', {'form': form, 'review': review})




# Création d'un ticket (nécessite une authentification)
class TicketCreate(CreateView, LoginRequiredMixin):
    model = Ticket
    template_name = 'reviews/ticket_form.html'
    form_class = TicketCreateForm
    success_url = reverse_lazy('flow')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Création d'une critique (nécessite une authentification)
class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        # Récupérer les données du formulaire ReviewCreateForm
        ticket_title = form.cleaned_data['ticket_title']
        ticket_description = form.cleaned_data['ticket_description']
        ticket_image = form.cleaned_data['ticket_image']
        headline = form.cleaned_data['headline']
        body = form.cleaned_data['body']
        rating = form.cleaned_data['rating']

        # Créer un nouvel objet Ticket
        ticket = Ticket.objects.create(
            title=ticket_title,
            description=ticket_description,
            image=ticket_image,
            user=self.request.user
        )

        # Créer un nouvel objet Review lié au Ticket
        review = Review.objects.create(
            headline=headline,
            body=body,
            rating=rating,
            ticket=ticket,
            user=self.request.user
        )
        form.cleaned_data['review'] = review
        # Rediriger l'utilisateur vers une autre page (vous pouvez personnaliser cela)
        return super().form_valid(form)
    
    def get_success_url(self):
        # Spécifiez l'URL vers laquelle rediriger l'utilisateur après la création réussie
        return reverse_lazy('flow')