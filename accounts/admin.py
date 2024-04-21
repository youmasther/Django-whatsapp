from django.contrib import admin
from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import *
# # Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('__str__' ,'prenom', 'nom', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields= ('email', 'prenom', 'nom',)
    ordering = ('date_joined',) 
    readonly_fields = ('id','date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations Personnels ', {'fields': ('prenom','nom', 'image')}),
        ('Permissions', {'fields': ('is_active','is_admin', 'is_staff', 'is_superuser')}),
    )
    # ordering = 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'prenom', 'nom',),
        }),
    )
    

admin.site.register(User, UserAdmin)
admin.site.register(Messages)