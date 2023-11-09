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
    path('tickets/', reviews.views.TicketList.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', reviews.views.TicketDetail.as_view(), name='ticket-detail'),
    path('create-ticket/', reviews.views.TicketCreate.as_view(), name='create-ticket'),
    path('user_posts', reviews.views.user_posts, name='user_posts'),
    # Vues et URLs pour les critiques
    path('reviews/', reviews.views.ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', reviews.views.ReviewDetail.as_view(), name='review-detail'),
    path('create-review/', reviews.views.ReviewCreate.as_view(), name='create-review'),

    # Vue pour les abonnements
    path('subscriptions/', reviews.views.subscription_view, name='subscriptions'),
    path('unfollow/<int:follow_id>/', reviews.views.unfollow, name='unfollow'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)