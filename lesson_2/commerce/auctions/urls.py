from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), #display of the listings
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing_detail, name="listing_detail"), #To see a specific listing
    path("create", views.create_listing, name="create_listing"), #Create a listing
    path("watchlist", views.watchlist, name="watchlist"), #The user watchlist
]
