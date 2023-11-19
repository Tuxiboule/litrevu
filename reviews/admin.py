from django.contrib import admin
from .models import UserFollows, Ticket, Review, UserBlock
from authentication.models import User

# Add model here to retreive them in admin interface
admin.site.register(UserFollows)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(UserBlock)
