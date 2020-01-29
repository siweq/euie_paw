from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from .forms import LoginForm
from .models import Card, Person

# strona główna
@login_required
def dashboard(request):
    return render(request,
            'dashboard.html',
            {'section': 'dashboard'})

# widok z wykorzystaniem widoku generycznego Django
# Widoki osoby 
class PersonListView(LoginRequiredMixin,generic.ListView):
    model = Person
    login_url = '/login/'
    paginate_by = 10 
    context_object_name = 'person_list'
    template_name = 'person/list.html'
    ordering = ['-created']
    context = {'section': 'persons'}

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        context['section'] = 'persons'
        return context

class PersonDetailView(LoginRequiredMixin,generic.DetailView):
    model = Person
    login_url = '/login/'
    context_object_name = 'person'
    template_name = 'person/detail.html'

# Widoki KARTY
class CardListView(LoginRequiredMixin,generic.ListView):
    model = Card
    login_url = '/login/'
    paginate_by = 10 
    context_object_name = 'card_list2'
    template_name = 'card/list2.html'
    ordering = ['-created']
    queryset = Card.objects.all()

    def get_queryset(self, **kwargs):
        queryset = super(CardListView, self).get_queryset(**kwargs)
        return queryset

    #@login_required - zastąpione wbudowaną obsługą w klasie
    # LoginRequiredMixin i login_url
    def get_context_data(self, **kwargs):
        context = super(CardListView, self).get_context_data(**kwargs)
        context['section'] = 'cards'
        return context

class CardDetailView(LoginRequiredMixin,generic.DetailView):
    model = Card
    login_url = '/login/'
    context_object_name = 'card'
    template_name = 'card/detail.html'
    
    def card_detail_view(request, id):
        card = get_object_or_404(Card, pk=id)
        return render(request, 'card/detail.html',
                context={'card': card,
                    'section': 'card_detail'})

# Login - zastąpiony przez wbudowane we framework
'''
def user_login(request):
    success_msg = 'Sukces!. Zalogowano!'
    error_msg = 'Błąd logowania :('
    if request.method =='POST':
        # utwórz instancję formularza logowania
        form = LoginForm(request.POST)
        # weryfikacja poprawności wypełnienia formularza (pól)
        if form.is_valid():
            # oczyszczenie danych wejściowych
            cd = form.cleaned_data 
            # użycie danych z formularza do uwierzytelnenia
            user = authenticate(username=cd['username'],
                    password=cd['password'])
            # weryfikacja czy baza zwróciła rekord user (jest w bazie)
            if user is not None:
                if user.is_active:
                    # dla aktywnego user metod login tworzy sesję
                    login(request, user)
                    return HttpResponse(success_msg)
                else:
                    return HttpResponse('Konto jest zablokowane.')
            else:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    # jeżeli get, lub inna metoda, utówrz pusty formularz
    else:
        form = LoginForm()
    #return HttpResponse(error_msg)
    return render(request, 'administracja/login.html', {'form': form})
'''
