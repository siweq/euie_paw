from django.db import models
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.urls import reverse
import administracja.tools as tools

# Prywatne menadzery modeli
'''
Przykadowe wywołania: 
Card.activeCards.all() - zwraca wszystkie aktywne karty
Card.activeCards.filter(type='HID') - tylko aktywne typu HID
'''
#class ActiveManager(models.Manager):
#    def get_queryset(self):
#        return super(ActiveManager,self).get_queryset()\
#                                        .filter(active=True)

# Modela bazy danych dla ORM
class Room(models.Model):
    KIND = (
            ('Office','Pomieszczenie biurowe'),
            ('Factory','Pomieszczenie produkcyjne'),
            ('Warehouse','Pomieszczenie magazynowe'),
            ('Other','Inne pomieszczenia')
    )
    name = models.CharField(max_length=30,
            verbose_name="Nazwa")
    location = models.CharField(max_length=50,
            verbose_name="Lokalizacja")
    kind = models.CharField(max_length=10,
            choices = KIND,
            verbose_name="Rodzaj pomieszczenia")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=u'Pomieszczenie'
        verbose_name_plural=u'Pomieszczenia'

    def __str__(self):
        return str(self.name+', '+self.location)

class Reader(models.Model):
    RFID_STD = (
            ('HID','HID 13.56MHz 4kb'),
            ('Mifare','Mifare 13.56MHz 1kb'),
            ('Unique','Unique 125kHZ 1kb')
    )
    DIRECTION = (
            ('OUT','OUT'),
            ('IN','IN')
    )
    id = models.CharField(max_length=10,
            primary_key=True,
            unique=True)
    direction = models.CharField(max_length=3,
            choices = DIRECTION,
            verbose_name="Kierunek")
    room = models.ForeignKey(Room,
            on_delete=models.CASCADE,
            related_name='room_readers',
            verbose_name="Pomieszczenie")
    desc = models.CharField(max_length=250,
            verbose_name="Opis")
    type = models.CharField(max_length=10,
            choices = RFID_STD,
            default = 'HID',
            verbose_name="Typ")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=u"Czytnik"
        verbose_name_plural=u"Czytniki"

    def __str__(self):
        return self.desc

class Role(models.Model):
    name = models.CharField(max_length=10,
            verbose_name="Rola")
    desc = models.CharField(max_length=50,
            verbose_name="Opis")
    admin = models.BooleanField(default=False,
            verbose_name="Rola administracyjna")
    persons = models.ManyToManyField(
            to='Person',
            through='PersonRoles',
            related_name='used_roles',
            blank=True,
            verbose_name="Osoba")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=u"Rola"
        verbose_name_plural=u"Role"

    def __str__(self):
        return self.name

class Person(models.Model):
    name =  models.CharField(max_length=100,
            verbose_name='Imię i nazwisko')
    pesel = models.CharField(max_length=11,
            verbose_name='PESEL',
            help_text='Podaj poprawny PESEL')
    hire_date = models.DateField(default=datetime.now,
            verbose_name='Data zatrudnienia')
    fire_date = models.DateField(blank=True,
            null=True,
            verbose_name='Data zwolnienia',
            help_text='Data zwolnienia nie może być wcześniejsza niż data zatrudnienia')
    active  = models.BooleanField(default=False,
            verbose_name='Aktywna')
    anonymized = models.BooleanField(default=False,
            verbose_name='Zanomizowana') 
    hash_date = models.DateField(blank=True,
            null=True,
            verbose_name='Data anonimizacji')
    retention = models.IntegerField(default=5,
            null=False,
            verbose_name='Okres retencji RODO',
            help_text='Standardowy okres retencji wynosi 5 lat + dni do końca roku kalendarzowego')
    created = models.DateTimeField(auto_now_add=True,
            verbose_name='Data dodania rekordu')
    updated = models.DateTimeField(auto_now=True,
            verbose_name='Data aktualizacji rekordu')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Osoba'
        verbose_name_plural = u'Osoby'

    def get_absolute_url(self):
        return reverse('person_detail', kwargs={'pk': self.pk})
    
    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label,
            self._meta.model_name),
            args=[self.id])

    def add_admin_url(self):
        return reverse('admin:%s_%s_add' % (self._meta.app_label,
            self._meta.model_name))

    def get_retention_date(self):
        if self.hash_date:
            retention_date = self.hash_date
        elif self.fire_date and self.active is not True:
            retention_date = date(self.fire_date.year+self.retention,12,31)
        else:
            retention_date = None
        return retention_date

    def assigned_cards(self):
        karty = Card.objects.filter(status=1,person=self.id)
        return karty

    def assigned_active_cards(self):
        karty = Card.objects.filter(status=1,person=self.id,active=True)
        return karty

    def save(self, *args, **kwargs):
        hash_date = Person.get_retention_date(self)
        if hash_date <= datetime.now().date():
            self.hash_date = hash_date
            self.name = tools.mieszanie(self.name)
            self.pesel = tools.mieszanie(self.pesel,11) 
            self.anonymized = True
        super(Person,self).save(*args, **kwargs)

class PersonRoles(models.Model):
    person = models.ForeignKey(Person, 
            on_delete=models.DO_NOTHING,
            verbose_name="Osoba")
    role = models.ForeignKey(Role, 
            on_delete=models.DO_NOTHING,
            verbose_name="Rola")

    class Meta:
        verbose_name_plural=u"Role Osób"
        verbose_name=u"Rola Osoby"

    def __str__(self):
        return "{} {}".format(self.role_id, self.person_id)

class Card(models.Model):
    RFID_STD = (
        ('HID','HID'),
        ('Mifare','Mifare'),
        ('Unique','Unique')
    )
    CARD_STATUS = (
        ('0','Available'),
        ('1','Assigned'),
        ('2','Disabled'),
    )
    id = models.CharField(max_length=48,
        primary_key=True,
        unique=True,
        verbose_name='Nr karty')
    type = models.CharField(max_length=10,
        choices = RFID_STD,
        verbose_name='typ')
    supplier = models.CharField(max_length=100,
        verbose_name='dostawca')
    status = models.CharField(
        max_length=1,
        choices=CARD_STATUS,
        default='0',
        verbose_name='Status',
        help_text='Status karty')
    person = models.ForeignKey('Person',
            on_delete=models.SET_NULL, 
            null=True,
            blank=True,
            verbose_name='Użytkownik') 
    valid_date = models.DateField(blank=True,
            null=True,
            verbose_name='data ważności')
    active = models.BooleanField(default=True,
            verbose_name='aktywna')
    created = models.DateTimeField(auto_now_add=True,
            verbose_name='data dodania')
    updated = models.DateTimeField(auto_now=True,
            verbose_name='data modyfikacji')
    
    class Meta:
        verbose_name = u'Karta'
        verbose_name_plural = u'Karty'

    def __str__(self):
        return str(self.id+' ('+self.type+')')

    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'pk': self.pk})
            
    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label,                     self._meta.model_name),
            args=[self.id])

    def add_admin_url(self):
        return reverse('admin:%s_%s_add' % (self._meta.app_label,                     self._meta.model_name))

    # zasłonięcie generycznej metody save
    def save(self, *args, **kwargs):
        if self.person:
            self.status = '1'
        if self.active == False:
            self.status = '2'
        if not self.valid_date:
            self.valid_date = (self.created+timedelta(days=3650)).date()
        super(Card,self).save(*args, **kwargs)

    def PrintAllCards(self):
         att = (self.id,
                self.type,
                self.supplier,
                self.valid_date,
                self.active)
         return att
    
    #activeCards = ActiveManager()
    #objects = models.Manager()

