from django.contrib import admin
from .models import CustomUser, NivelAcceso, Registro, Address, Phone

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'dni', 'numero_legajo', 'nivel_acceso')
    search_fields = ('username', 'email', 'dni')
    list_filter = ('nivel_acceso',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(NivelAcceso)
admin.site.register(Registro)
admin.site.register(Address)
admin.site.register(Phone)
