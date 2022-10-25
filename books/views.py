from django.views.generic.edit import CreateView
from django.forms import ModelForm
from books.models import Book
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class UserLoginView(LoginView):
    template_name = "login.html"
    success_url = "/"

class UserSignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = "/login"

class BooksForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author']
    

class CreateBookView(LoginRequiredMixin, CreateView):
    form_class = BooksForm
    template_name = "create_book.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class ListBooksView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "home.html"
    context_object_name = "books"

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

# home page view
class HomePageView(ListView):
    model = Book
    template_name = "homePage.html"
    context_object_name = "book"
    login_url = "/login/"
