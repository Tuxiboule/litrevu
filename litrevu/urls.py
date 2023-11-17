from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
        name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
        name='password_change_done'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('flow/', login_required(reviews.views.flow), name='flow'),

    # Vues et URLs pour les tickets
    path('create-ticket/', reviews.views.TicketCreate.as_view(), name='create-ticket'),
    path('create-review/', reviews.views.ReviewCreate.as_view(), name='create-review'),
    path('delete_item/<int:item_id>/', reviews.views.delete_item, name='delete_item'),

    path('user_posts', reviews.views.user_posts, name='user_posts'),
    path('subscriptions/', reviews.views.subscription_view, name='subscriptions'),
    path('unfollow/<int:follow_id>/', reviews.views.unfollow, name='unfollow'),
    path('ticket-update/<int:ticket_id>/', reviews.views.ticket_update, name='ticket_update'),
    path('review-update/<int:review_id>/', reviews.views.review_update, name='review_update'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)