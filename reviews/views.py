from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView
from .models import Ticket, Review, UserFollows, UserBlock
from .forms import SubscriptionForm, TicketCreateForm, ReviewCreateForm, BlockForm
from django.urls import reverse_lazy
from authentication.models import User

from operator import attrgetter


@login_required
def flow(request):
    """_summary_
    Flow view, askin for user and followed_user posts
    """
    user = request.user
    print(type(request))
    items = prepare_flow(user)
    return render(request, 'reviews/flow.html', {'items': items})


def prepare_flow(user):
    """_summary_
    Returns a list of all own/followed posts from an user
    Args:
        user (Ojbect.user): connected user
    Returns:
        sorted_items (list(Review, Ticket)) : contains all sorted reviews/tickets from a user, from users they follow, excluding blocked users
    """
    reviews_list = []
    tickets_list = []
    posters = [user]

    follows = list(UserFollows.objects.filter(user=user))
    blocked = list(UserBlock.objects.filter(user=user))

    # browse all followers for a user
    for follow in follows:
        posters.append(follow.follow_user)

    # all posts for all followers
    for poster in posters:
        poster_reviews = Review.objects.filter(user=poster)
        poster_tickets = Ticket.objects.filter(user=poster)

        reviews_list += poster_reviews
        tickets_list += poster_tickets

    items = tickets_list + reviews_list

    # responses to user tickets
    for review in Review.objects.all():
        if review.ticket.user == user and review.user != user:
            items.append(review)

    for item in items:
        # blocked user removing
        if any(blocked_user.block_user == item.user for blocked_user in blocked):
            items.remove(item)

        # set 'Review' or 'Ticket' attribute on items
        item.item_type = 'Review' if isinstance(item, Review) else 'Ticket'

        if item.item_type == 'Review':
            item.rating = item.rating_to_stars(item.rating)

    sorted_items = sorted(items, key=attrgetter("time_created"), reverse=True)
    return sorted_items


@login_required
def subscription_view(request):
    """_summary_
    View for follow/block management
    """
    user = request.user
    subscriptions = UserFollows.objects.filter(user=user)
    followers = UserFollows.objects.filter(follow_user=user)
    blocked = UserBlock.objects.filter(user=user)
    form_block = BlockForm(request.POST or None)
    form_sub = SubscriptionForm(request.POST or None)

    # all followed users
    for object in User.objects.all():
        if form_sub['follow_user'].value() == object.username:
            choice = object

    # all blocked users
    for object in User.objects.all():
        if form_block['block_user'].value() == object.username:
            block_choice = object

    # follow add
    try:
        if request.method == 'POST' and form_sub['follow_user'].value() == choice.username:
            followee = choice
            if not UserFollows.objects.filter(user=user, follow_user=followee).exists():
                UserFollows.objects.create(user=user, follow_user=followee)
    except Exception as e:
        print(e)

    # block add
    try:
        if request.method == 'POST' and form_block['block_user'].value() == block_choice.username:
            blockee = block_choice

            if not UserBlock.objects.filter(user=user, block_user=blockee).exists():
                UserBlock.objects.create(user=user, block_user=blockee)
    except Exception as e:
        print(e)

    return render(request, 'reviews/subscriptions.html',
                  {'subscriptions': subscriptions, 'followers': followers, 'blocked': blocked,
                   'form_sub': form_sub, 'form_block': form_block})


@login_required
def user_posts(request):
    """_summary_
    View to delete/edit posts of connected user
    """
    user = request.user
    user_tickets = list(Ticket.objects.filter(user=user))
    user_reviews = list(Review.objects.filter(user=user))
    items = user_tickets + user_reviews

    # set 'Review' or 'Ticket' attribute on items
    for item in items:
        item.item_type = 'Review' if isinstance(item, Review) else 'Ticket'
        if item.item_type == 'Review':
            item.rating = item.rating_to_stars(item.rating)

    sorted_items = sorted(items, key=attrgetter("time_created"), reverse=True)
    context = {'items': sorted_items}

    return render(request, 'reviews/user_posts.html', context)


@login_required
def unfollow(request, follow_id):
    """_summary_
    View for unfollow a user followed by connected user
    """
    user_follow = UserFollows.objects.get(id=follow_id)

    if user_follow.user == request.user:
        user_follow.unfollow()

    return redirect('subscriptions')


@login_required
def unblock(request, block_id):
    """_summary_
    View for unblock a user followed by connected user
    """
    user_block = UserBlock.objects.get(id=block_id)

    if user_block.user == request.user:
        user_block.unblock()

    return redirect('subscriptions')


@login_required
def delete_item(request, item_id):
    """_summary_
    View to delete a review/ticket
    """
    try:
        item = Ticket.objects.get(id=item_id)
    except Ticket.DoesNotExist:
        try:
            item = Review.objects.get(id=item_id)
        except Review.DoesNotExist:
            print("Pas d'item correspondant")
            return redirect('user_posts')

    # Check if user is allowed to delete the post
    if item.user == request.user:
        item.delete()
        return redirect('user_posts')
    else:
        return redirect('user_posts')


@login_required
def ticket_update(request, ticket_id):
    """_summary_
    View for updating a connected user ticket
    """
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        form = TicketCreateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('user_posts')
    else:
        form = TicketCreateForm(instance=ticket)

    return render(request, 'reviews/ticket_update.html', {'form': form, 'ticket': ticket})


@login_required
def review_update(request, review_id):
    """_summary_
    View for updating a connected user review
    """
    review = Review.objects.get(id=review_id)

    # Pre-fill form with existing ticket informations
    ticket_data = {
        'ticket_title': review.ticket.title,
        'ticket_description': review.ticket.description,
        'ticket_image': review.ticket.image,
    }

    if request.method == 'POST':
        form = ReviewCreateForm(request.POST, instance=review, initial=ticket_data)
        # save form only if it is valid
        if form.is_valid():
            form.save()
            return redirect('user_posts')
    else:
        form = ReviewCreateForm(instance=review, initial=ticket_data)

    return render(request, 'reviews/review_update.html', {'form': form, 'review': review})


@login_required
def ticket_answer(request, ticket_id):
    """_summary_
    View for answering to an existing ticket in a user flow
    """
    ticket = Ticket.objects.get(id=ticket_id)

    # check if ticket already have been answered
    try:
        review = Review.objects.get(ticket=ticket)
        messages.success(request, f'Il y déjà une critique pour le ticket : {ticket.title}.')
        return redirect('flow')
    except Review.DoesNotExist:
        pass
    # Pre-fill form with existing ticket informations
    ticket_data = {
        'ticket_title': ticket.title,
        'ticket_description': ticket.description,
        'ticket_image': ticket.image,
    }

    if request.method == 'POST':
        form = ReviewCreateForm(request.POST, initial=ticket_data)
        # save form only if it is valid
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            form.save()
            return redirect('flow')
    else:
        form = ReviewCreateForm(initial=ticket_data)

    return render(request, 'reviews/review_form.html', {'form': form, 'ticket': ticket})


class TicketCreate(CreateView, LoginRequiredMixin):
    """_summary_
    Class-based view for creating a ticket
    """
    model = Ticket
    template_name = 'reviews/ticket_form.html'
    form_class = TicketCreateForm
    success_url = reverse_lazy('flow')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewCreate(LoginRequiredMixin, CreateView):
    """ _summary_
    Class-based view for creating a review.
    """
    model = Review
    form_class = ReviewCreateForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        # get ReviewCreateForm informations
        ticket_title = form.cleaned_data['ticket_title']
        ticket_description = form.cleaned_data['ticket_description']
        ticket_image = form.cleaned_data['ticket_image']
        headline = form.cleaned_data['headline']
        body = form.cleaned_data['body']
        rating = form.cleaned_data['rating']

        # Create a new ticket
        ticket = Ticket.objects.create(
            title=ticket_title,
            description=ticket_description,
            image=ticket_image,
            user=self.request.user
        )

        # Create a review associated with ticket
        review = Review.objects.create(
            headline=headline,
            body=body,
            rating=rating,
            ticket=ticket,
            user=self.request.user
        )
        form.cleaned_data['review'] = review

        return redirect('flow')
