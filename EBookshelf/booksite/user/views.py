from django.contrib.auth import login

from django.shortcuts import redirect, render

from django.urls import reverse
from django.http import HttpResponseRedirect

from user.forms import CustomUserCreationForm
from .forms import FormBookForm
from .models import BookForm


def dashboard(request):

    return render(request, "user/dashboard.html")


def register(request):

    if request.method == "GET":

        return render(

            request, "user/register.html",

            {"form": CustomUserCreationForm}

        )

    elif request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect(reverse("dashboard"))

        else:

            return register('GET')



def bookaddform(request):
    if request.method == "GET":
        all_books = BookForm.objects.all()
        return render(request, 'user/bookform.html', {"form": FormBookForm, 'all_books':all_books})

    elif request.method == "POST":
        form = FormBookForm(request.POST)
        form.save()
        return redirect('bookform')
        
def delete_book(request, id):
    book = BookForm.objects.get(id=id)
    book.delete()
    return redirect('bookform')