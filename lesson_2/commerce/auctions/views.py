from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *


def index(request):
    listings = Listing.objects.filter(is_active=True) #only the active auctions appear
    return render(request, "auctions/index.html", {
        "listings": listings
        })


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category_id = request.POST["category"]
        new_category_name = request.POST["new_category"]

        # New or existing
        if category_id:
            category = get_object_or_404(Category, id=category_id)
        elif new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            if created:
                messages.success(request, f"New category '{new_category_name}' created.")

        # Crear el listing
        listing = Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_price=starting_bid,
            image_url=image_url,
            category=category,
            owner=request.user
        )

        messages.success(request, "Listing created successfully!")
        return redirect("index")

    # Si no es un POST, obtener todas las categorías
    categories = Category.objects.all()
    return render(request, "auctions/create_listing.html", {"categories": categories})


@login_required
def watchlist(request):
    user_watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_watchlist
    })


@login_required
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    is_owner = request.user == listing.owner
    user_watchlist = request.user.watchlist.all()

    # Handle adding or removing from watchlist
    if "add_to_watchlist" in request.POST:
        if listing in user_watchlist:
            request.user.watchlist.remove(listing)
            messages.success(request, "Removed from watchlist.")
        else:
            request.user.watchlist.add(listing)
            messages.success(request, "Added to watchlist.")
        return redirect("listing_detail", listing_id=listing.id)

    # Handle bidding
    if "place_bid" in request.POST:
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Bid amount is required.")
        else:
            try:
                amount = float(amount)
            except ValueError:
                messages.error(request, "Invalid bid amount.")
                return redirect("listing_detail", listing_id=listing.id)

            if amount < listing.starting_bid:
                messages.error(request, "Bid must be at least the starting bid.")
            elif listing.bids.exists() and amount <= listing.bids.latest("created_at").amount:
                messages.error(request, "Bid must be greater than the current highest bid.")
            else:
                Bid.objects.create(listing=listing, user=request.user, amount=amount)
                listing.current_price = amount
                listing.save()
                messages.success(request, "Bid placed successfully.")
            return redirect("listing_detail", listing_id=listing.id)

    # Handle closing the auction
    if "close_auction" in request.POST and is_owner:
        if listing.bids.exists():
            listing.is_active = False
            listing.save()
            messages.success(request, "Auction closed.")
        else:
            messages.error(request, "Cannot close auction with no bids.")
        return redirect("listing_detail", listing_id=listing.id)

    # Add comment
    if "add_comment" in request.POST:
        comment_text = request.POST["comment"]
        if not comment_text:
            messages.error(request, "Comment cannot be empty.")
        else:
            Comment.objects.create(listing=listing, user=request.user, text=comment_text)
            messages.success(request, "Comment added.")
        return redirect("listing_detail", listing_id=listing.id)

    # Check if the user has won the auction
    highest_bid = listing.bids.order_by("-amount").first()
    user_won = highest_bid and highest_bid.user == request.user

    context = {
        "listing": listing,
        "user_won": user_won,
        "highest_bid": highest_bid,
        "comments": listing.comments.all(),
    }

    return render(request, "auctions/listing_detail.html", context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
