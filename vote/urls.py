from django.urls import path

from . import views


app_name = 'vote'
urlpatterns = [
    path('index/', views.active, name='active'),
    path('completed/', views.completed, name='completed'),
    path('send/', views.SendView.as_view(), name='send'),
    path('plot/<int:vote_id>/', views.plot_pic, name='plot_pic'),
    path('<int:vote_id>/', views.detail, name='detail'),
    path('<int:vote_id>/vote/', views.vote, name='vote'),
]
