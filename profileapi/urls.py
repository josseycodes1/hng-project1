from django.urls import path
from .views import ProfileView
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('me', ProfileView.as_view(), name='profile'),
    path('docs/', include_docs_urls(title='Profile API')),
]