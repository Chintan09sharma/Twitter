"""codeasylums URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# django/rest_framework imports
from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter
from django.contrib import admin

# project level imports
from accounts.users import views as users_views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Twitter API')

# intialize DefaultRouter
router = SimpleRouter()
# register accounts app urls with router
router.register(r'accounts', users_views.UserViewSet, basename='accounts')

# urlpatterns
urlpatterns = [
    path('api/', include((router.urls, 'api'), namespace='api')),
    re_path(r'docs/swagger/', schema_view)
]

