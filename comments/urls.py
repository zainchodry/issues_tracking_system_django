from django.urls import path
from .views import (
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    CommentReactionView,
)

app_name = 'comments'

urlpatterns = [
    path('issue/<int:issue_pk>/add/', CommentCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', CommentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', CommentDeleteView.as_view(), name='delete'),
    path('<int:pk>/react/', CommentReactionView.as_view(), name='react'),
]
