from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Rotas públicas
    path('', views.home, name='home'),  # Página inicial
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('finalizar-periodo/', views.finalizar_periodo, name='finalizar_periodo'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.edit_profile, name='edit_profile'),
    path('meus_periodos/', views.meus_periodos, name='meus_periodos'),
    path('alterar-senha/', views.change_password, name='change_password'),

    # Rotas protegidas
    path('dashboard/', views.dashboard, name='dashboard'),
    path('adicionar/', views.adicionar_materia, name='adicionar_materia'),
    path('editar/<int:pk>/', views.editar_materia, name='editar_materia'),
    path('remover/<int:pk>/', views.remover_materia, name='remover_materia'),
    path('restaurar/<int:pk>/', views.restaurar_materia, name='restaurar_materia'),  # Nova rota
    path('lixeira/', views.lixeira, name='lixeira'),  # Nova rota para a página de lixeira
    path('materia/<int:pk>/anotacoes/', views.ver_anotacoes, name='ver_anotacoes'),
    path('materia/<int:id>/adicionar_faltas/', views.adicionar_faltas, name='adicionar_faltas'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)