from celery import task
from .models import Person, Card

@task
def anonimisation(*args):
    """
    Funkcja anonimizująca dane osobowe
    po osiągnięciu okresu retencji
    """
    #if len(args) == 0:
    if not args:
        osoby = Person.objects.filter(anonymized=False)
        for osoba in osoby:
            x += 1
            print('Wszyscy ('+x+'): 'osoba.name)
    else:
        for arg in args:
            if Person.objects.filter(id=arg,anonymized=False):
                x += 1
                print('Z listy('+x+'): 'osoba.name)
    



