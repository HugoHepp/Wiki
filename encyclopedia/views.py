from django.shortcuts import render
from django.shortcuts import render
from django import forms
from django.shortcuts import redirect
from django.contrib import messages
import os
import random
import markdown2


from . import util

# Form for sid navbar
class Searchform(forms.Form):
    search = forms.CharField(label="Search")

# Form for add entry
class Addform(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())

# Form for edit entry
class Editform(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())


# Home page
def index(request):

	if request.method == 'POST':

		# Get query from search sidenav and redirect user to the page or the list that can correspond 	
		form = Searchform(request.POST)
		# check whether it's valid:
		if form.is_valid():
			data = form.cleaned_data["search"]
			print(data)
			if data.capitalize() in util.list_entries():
				# return the entry page 
				return redirect("/"+data)
			else:
				# return the list of entry that can correspond  
				return render(request, "encyclopedia/search.html", {"form" : Searchform(), "entries": util.list_entries(), "searchterm": data })   
	else:
		# Return Home page if request is GET 
	    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), "form" : Searchform()})


def greet(request, name):

	# Get the entry page if it exist
	if name.capitalize() in util.list_entries():	

		# return the entry page with markdown 
		entry = markdown2.markdown(util.get_entry(name))
		return render(request, "encyclopedia/quote.html", {"quote": entry, "name": name, "form" : Searchform()})

	# Return apology if not 
	else :

		return redirect("/apology/")


def apology(request):

	# return apology page
	return render(request, "encyclopedia/apology.html",{"form" : Searchform()})

def ranarticle(request):


	# Return a random entry 
	rand = str(random.choice(os.listdir("C:\\Users\\Hugo\\Desktop\\wiki\\entries")))
	randfin = rand[:-3]
	ranurl = "/" + randfin
	return redirect(ranurl)
       


def add(request):

    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = Addform(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Get the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # If it already exist, return error
      
            if title.capitalize() in util.list_entries():
            	return render( request, "encyclopedia/add.html", {'alert_flag': True,  "addform": Addform(), "form" : Searchform()})

            # If it doesn't exist yet, save the entry
            else:
            	util.save_entry(title.capitalize(), content)
            	return redirect("/"+title)
        else:

        	messages.error(request, "Error")
    else:
    	# If GET Method , return add page
    	return render(request, "encyclopedia/add.html", {
        "addform": Addform(), "form" : Searchform()
    })


def edit(request):

	if request.method == "POST":

		form = Editform(request.POST)

		if form.is_valid():

			# Get the edited content, save it and return to the entry page
			content = form.cleaned_data["content"]
			title = form.cleaned_data["title"]
			util.save_entry(title.capitalize(), content)
			url = "/" + title
			print(url)
			return redirect(url)  	

	else:

		# If GET Method, Get the entry from the previous page and prefill form to edit
		previouspage = request.META.get('HTTP_REFERER')
		indexofkey = previouspage.rindex("/")
		prev = previouspage[indexofkey+1:]
		articletoedit = util.get_entry(prev)
		editform = Editform()
		editform.fields["title"].initial = prev

		editform.fields["content"].initial = articletoedit

		# Return form in edit page
		return render(request, "encyclopedia/edit.html", {
       "form" : Searchform(), "editform" : editform})

	# Return to the entry after edit 
	previouspage = request.META.get('HTTP_REFERER')
	return redirect("/")




