from django.contrib import admin
from .models import UserFollows, Ticket, Review
from authentication.models import User

admin.site.register(UserFollows)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(User)
