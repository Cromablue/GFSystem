from django.urls import path
from . import views

urlpatterns = [
    # Rotas públicas
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('finalizar-periodo/', views.finalizar_periodo, name='finalizar_periodo'),

    # Rotas protegidas
    path('dashboard/', views.dashboard, name='dashboard'),
    path('adicionar/', views.adicionar_materia, name='adicionar_materia'),
    path('editar/<int:pk>/', views.editar_materia, name='editar_materia'),
    path('remover/<int:pk>/', views.remover_materia, name='remover_materia'),
    path('materia/<int:id>/adicionar_faltas/', views.adicionar_faltas, name='adicionar_faltas'),
]
