from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address, Phone, NivelAcceso
from .forms import CustomUserForm

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    can_delete = True

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1
    can_delete = True

class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    model = CustomUser
    list_display = ('username', 'email', 'dni', 'numero_legajo', 'nivel_acceso')
    list_filter = ('nivel_acceso',)
    search_fields = ('username', 'email', 'dni', 'numero_legajo')
    ordering = ('username',)
    
    # Inline forms
    inlines = [AddressInline, PhoneInline]
    
    # Fieldsets to customize the layout
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('dni', 'numero_legajo', 'nivel_acceso')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'nivel_acceso'),
        }),
    )

class NivelAccesoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel', 'descripcion')
    search_fields = ('nombre',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(NivelAcceso, NivelAccesoAdmin)
