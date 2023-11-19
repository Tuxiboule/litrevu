from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    # Model for ticket
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    # Model for review (include a ticker)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def rating_to_stars(self, rating):
        """_summary_
        Convert int rating to a star view
        Args:
            rating (int): rating of the review
        Returns:
            list(str): list of b/w stars to be displayed
        """
        rating = int(rating)
        total_stars = 5
        black_stars = rating
        white_stars = total_stars - black_stars
        star_view = '⭐' * black_stars + '☆' * white_stars
        return star_view


class UserFollows(models.Model):
    # Model for following an user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_follows')
    follow_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    def unfollow(self):
        """_summary_
        Delete follow object
        """
        self.delete()


class UserBlock(models.Model):
    # Model for blocking a user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_blocks')
    block_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocked_by')

    def unblock(self):
        """_summary_
        Delete block object
        """
        self.delete()
