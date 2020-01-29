from django.apps import AppConfig
from .models import Person
import hashlib
from datetime import date

def mieszanie(text,len=0):
    if len > 0:
        zmieszane = hashlib.md5(str.encode(text)).hexdigest()[-len:]
    else:
        zmieszane = hashlib.md5(str.encode(text)).hexdigest()
    return zmieszane

def anonimisation(*args):
    x = 0
    today = datetime.now().date()
    if not args:
        osoby = Person.objects.filter(
                anonymization_date<=today,
                anonymized=False)
        for osoba in osoby:
            x += 1
            print('Wszyscy (' + str(x) +'): '+osoba.name)
            print('#Nazwisko: ' + mieszanie(osoba.name))
            print('#PESEL: ' + mieszanie(osoba.pesel,11))
            osoba.name = mieszanie(osoba.name)
            osoba.pesel = mieszanie(osoba.pesel,11)
            osoba.save()
    else:
        for arg in args:
            if Person.objects.filter(id=arg,anonymized=False):
                x += 1
                osoba = Person.objects.get(id=arg,anonymized=False)
                osoba.name = mieszanie(osoba.name)
                osoba.pesel = mieszanie(osoba.pesel,11)
                osoba.save()
                print('Hashuję dane osoby z listy('+ str(x) +'): '+osoba.name)
                print('#Nazwisko: ' + mieszanie(osoba.name))
                print('#PESEL: ' + mieszanie(osoba.pesel,11))

def add_person(ilosc:int):
    message = "Dodaję " + str(ilosc) + " osób"
    print(message)
    nazwiska = {["M",1,"Antoni","Nowak"],
            ["M",2,"Jakub","Kowalski"],
            ["M",3,"Jan","Wiśniewski"]
            }

def main(*args):
    anonimisation(args)

if __name__ == '__main__':
    main()
