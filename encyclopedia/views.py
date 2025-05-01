from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect
import re
from random import choice
from markdown2 import markdown

class SearchForm(forms.Form):
    entry = forms.CharField(label = "Search")

class EditPage(forms.Form):
    content = forms.CharField(label = "Edit Markdown content", widget=forms.Textarea())

class CreatePage(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(label = "Markdown content", widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "form": SearchForm(),
        "entries": util.list_entries(False)
    })

def create(request):
    if request.method == "POST":
        form = CreatePage(request.POST)

        if form.is_valid():
            if form.cleaned_data["title"].lower() in util.list_entries():

                return render(request, "encyclopedia/error.html", {
                    "form": SearchForm(),
                    "error": f"{form.cleaned_data['title']} entry already exists!"
                })
            
            else:
                util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
                return HttpResponseRedirect(reverse("wiki:entry", args=[form.cleaned_data["title"]]))
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": SearchForm(),
        "create": CreatePage()
    })

def edit(request, TITLE):
    if request.method == "POST":
        form = EditPage(request.POST)
        if form.is_valid():
            util.save_entry(TITLE, form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("wiki:entry", args=[TITLE]))
    return render(request, "encyclopedia/edit.html",{
        "form": SearchForm(),
        "title": TITLE.upper(),
        "edit": EditPage(initial={'content': util.get_entry(TITLE)}),
    })

def random(request, TITLE):
    entries = util.list_entries()
    if TITLE.lower() == 'null':
        return HttpResponseRedirect(reverse("wiki:entry", args=[choice(entries)]))
    entries.remove(TITLE.lower())
    return HttpResponseRedirect(reverse("wiki:entry", args=[choice(entries)]))

def entry(request, TITLE):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():

            TITLE = form.cleaned_data["entry"]

            if TITLE.lower() in util.list_entries():

                return HttpResponseRedirect(reverse("wiki:entry", args=[TITLE]))
            
            else:

                pattern = re.compile(rf"{TITLE}", re.IGNORECASE)
                entries = util.list_entries(False)
                entries_modified = []

                for entry in entries:
                    if pattern.search(entry):
                        entries_modified.append(entry)

                return render(request, "encyclopedia/results.html",{
                    "title": TITLE,
                    "entries": entries_modified,
                    "form": SearchForm()
                })
            
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
    if util.get_entry(TITLE) == None:
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm(),
            "error": f"{TITLE} does not exist!"
        })
    return render(request, "encyclopedia/entry.html",{
        "title": TITLE.upper(),
        "content": markdown(util.get_entry(TITLE), extras=["spoiler", "strike"]),
        "form": SearchForm()
    })