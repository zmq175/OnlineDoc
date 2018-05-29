from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexDocumentListView.as_view(), name='index'),
    path('education/', views.EducationListView.as_view(), name='education'),
    path('professional/', views.ProfessionalListView.as_view(), name='professional'),
    path('functional/', views.FunctionalListView.as_view(), name='functional'),
    path('exam/', views.ExamListView.as_view(), name='exam'),
    path('life/', views.LifeListView.as_view(), name='life'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('doc/<int:id>', views.DocumentDetailView.as_view(), name='document_detail'),
    path('likes_change/', views.likes_change, name='likes_change'),
    path('dislikes_change/', views.dislikes_change, name='dislike_change'),
    path('check_rate_status/', views.check_rate_status, name='check_rate_status'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('favorite/', views.FavoriteListView.as_view(), name='favorite'),
    path('history', views.HistoryListView.as_view(), name='history'),
    path('add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('check_favorite_status/', views.check_favorite_status, name='check_favorite_status'),
    path('delete_document/', views.delete_document, name='delete_document'),
    path('my/', views.my, name='my'),
    path('my/document/', views.UserDocumentListView.as_view(), name='user_document'),
]