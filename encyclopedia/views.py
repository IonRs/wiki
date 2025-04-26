from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect
import re
from random import choice

class SearchForm(forms.Form):
    entry = forms.CharField(label = "Search")
class CreatePage(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(label = "Markdown content", widget=forms.Textarea(attrs={
            'placeholder': 'Enter your content'
        })
)
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
                    "form": SearchForm()
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

def entry(request, TITLE):
    if TITLE == "random":
        return HttpResponseRedirect(reverse("wiki:entry", args=[choice(util.list_entries())]))
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
                #entries = [entry for entry in util.list_entries() if TITLE.lower() in entry]
                return render(request, "encyclopedia/results.html",{
                    "title": TITLE,
                    "entries": entries_modified,
                    "form": SearchForm()
                })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
    return render(request, "encyclopedia/entry.html",{
        "title": TITLE.upper(),
        "content": util.get_entry(TITLE),
        "form": SearchForm()
    })