from django.contrib import admin
from .models import Reader,Room,Role,Person,PersonRoles,Card

# Register your models here
#admin.site.register(Reader)
@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('id','room','direction','desc','type','created','updated')
    list_filter = ('direction','room','type')
    search_fields = ('id','desc')
    prepopulated_fields = {'desc': ('id',)}
    ordering = ('room','id','desc')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id','name','location','kind','created','updated')
    list_filter = ['kind']
    search_fields = ['location']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id','name','desc','admin','created','updated')
    list_filter = ['admin']
    ordering = ['name']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id','name','pesel','hire_date','active','fire_date','anonymized']
    list_filter = ('active','anonymized')
    ordering = ('active','name')

@admin.register(PersonRoles)
class PersonRolesAdmin(admin.ModelAdmin):
    ordering = ['id']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    model = Card
    list_display = ('id','type','active','status','valid_date')
    list_filter = ('status','type','active','supplier')
    search_fields = ('id','person','supplier')
    ordering = ['id']

    def admin_change_url(obj):
        if not obj:
            return ''
        app_label = obj._meta.app_label
        model_name = obj._mea.model.__name__.lower()
        return reverse('admin:{}_{}_change'.format(app_label,model_name), 
                args=(obj.pk,))

