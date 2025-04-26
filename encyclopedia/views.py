from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponse
import re

class SearchForm(forms.Form):
    entry = forms.CharField(label = "Search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "form": SearchForm(),
        "entries": util.list_entries(False)
    })
def entry(request, TITLE):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            TITLE = form.cleaned_data["entry"]
            if TITLE.lower() in util.list_entries():
                return render(request, "encyclopedia/entry.html",{
                    "title": TITLE.upper(),
                    "content": util.get_entry(TITLE),
                    "form": SearchForm()
                })
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