from django.contrib.auth.models import AbstractUser
from django.db import models

#model for user
class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name="watchlisted_by", blank=True)

#model for categories
class Category(models.Model):
    name = models.CharField(max_length=100)
    listings = models.ManyToManyField("Listing", related_name="listing_category", blank=True)

    def __str__(self):
        return self.name

#model for listing
class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(blank=True, null=True) #optional
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True) #optional
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

#model for bids
class Bid(models.Model):
    listing = models.ForeignKey(Listing, related_name="bids", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

#model for comments
class Comment(models.Model):
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"
