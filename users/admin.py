# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Usuario, Profesor, Estudiante


class UsuariosAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'is_staff',
        'first_name',
        'last_name',
        'telefono',
        'direccion'

    )
    list_filter = (
        'username',
        'email',
        'first_name',
        'last_name',
        'telefono',
        'direccion'

    )
    fieldsets = UserAdmin.fieldsets


class EstudianteAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'is_staff',
        'first_name',
        'last_name',
        'telefono',
        'direccion',
        'codigo_de_estudiante'

    )
    list_filter = (
        'username',
        'email',
        'first_name',
        'last_name',
        'telefono',
        'direccion',
        'codigo_de_estudiante'

    )


class ProfesorAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'is_staff',
        'first_name',
        'last_name',
        'facultad',
        'telefono',
        'direccion',
        'facultad'

    )
    list_filter = (
        'facultad',

    )
# Register your models here.


admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Usuario, UsuariosAdmin)

