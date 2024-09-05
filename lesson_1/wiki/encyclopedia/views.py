from django.shortcuts import render, redirect
from django.http import Http404
from . import util
from markdown2 import markdown
from random import choice

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title) #obtain the content or none
    #In case we dont have it
    if not content:
        raise Http404("Not a valid title")
    #convert markdown into html
    content = markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })


def search(request):
    query = request.GET.get('q', '').strip().lower() #get the query
    entries = util.list_entries() #all the possible entries

    #dictioanry with the name in lowercase for comparision and the real name
    entry_dict = {entry.lower(): entry for entry in entries}

    # Comprobar coincidencia exacta
    if query in entry_dict:
        return redirect("wiki", title=entry_dict[query])

    # Looking for all substrings
    matching_entries = [entry for entry in entries if query in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": matching_entries
    })


def create(request):
    # Take two arguments
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        #The title is empty
        if not title:
            return render(request, "encyclopedia/create.html", {
                "error": "Title cannot be empty."
            })
        # Check the title
        if title in util.list_entries():
            return render(request, "encyclopedia/create.html", {
                "error": "An entry with that title already exists."
            })
        # Keep it in disc if it does not exist
        util.save_entry(title, content)
        return redirect("wiki", title=title)

    return render(request, "encyclopedia/create.html")


def edit(request, title):
    if request.method == "POST":
        content = request.POST['content']
        # Save the updated entry
        util.save_entry(title, content)
        # Redirect to the updated entry page
        return redirect("wiki", title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/edit.html", {
                "error": "The requested page was not found."
            })

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def rand(request):
    entries = util.list_entries()
    return redirect("wiki", title=choice(entries)) #select one of them
