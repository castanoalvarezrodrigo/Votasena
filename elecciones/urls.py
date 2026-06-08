from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('vote/', views.vote_view, name='vote'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/aprendices/', views.admin_aprendices, name='admin_aprendices'),
    path('admin-panel/aprendices/nuevo/', views.admin_aprendiz_create, name='admin_aprendiz_create'),
    path('admin-panel/aprendices/<int:profile_id>/editar/', views.admin_aprendiz_edit, name='admin_aprendiz_edit'),
    path('admin-panel/aprendices/<int:profile_id>/eliminar/', views.admin_aprendiz_delete, name='admin_aprendiz_delete'),
    path('admin-panel/candidatos/', views.admin_candidacies, name='admin_candidacies'),
    path('admin-panel/candidatos/nuevo/', views.admin_candidacy_create, name='admin_candidacy_create'),
    path('admin-panel/candidatos/<int:candidacy_id>/editar/', views.admin_candidacy_edit, name='admin_candidacy_edit'),
    path('admin-panel/candidatos/<int:candidacy_id>/eliminar/', views.admin_candidacy_delete, name='admin_candidacy_delete'),
    path('admin-panel/votos/', views.admin_votes, name='admin_votes'),
    path('admin-panel/votos/export/', views.admin_votes_export, name='admin_votes_export'),
]