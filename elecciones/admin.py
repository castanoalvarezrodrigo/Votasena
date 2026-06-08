from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib import admin

from .models import Candidacy, Profile, Vote


class VotasenaAdminSite(AdminSite):
    site_header = 'Administración Votasena'
    site_title = 'Votasena Admin'
    index_title = 'Panel de administración'

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


admin_site = VotasenaAdminSite(name='votasena_admin')


class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'ficha')
    search_fields = ('user__username', 'ficha')


class CandidacyAdmin(ModelAdmin):
    list_display = ('name', 'role', 'ficha')
    list_filter = ('role', 'ficha')
    search_fields = ('name',)
    fieldsets = (
        ('Datos personales', {
            'fields': ('name', 'role', 'ficha', 'description')
        }),
        ('Propuestas', {
            'fields': ('proposals', 'profile_image'),
            'description': 'Ingresa las propuestas separadas por saltos de línea (Enter) y la foto de perfil del candidato.'
        }),
    )


class VoteAdmin(ModelAdmin):
    list_display = ('voter', 'candidacy', 'role', 'created_at')
    search_fields = ('voter__user__username', 'candidacy__name')
    list_filter = ('role',)
    readonly_fields = ('created_at',)


admin_site.register(Profile, ProfileAdmin)
admin_site.register(Candidacy, CandidacyAdmin)
admin_site.register(Vote, VoteAdmin)
