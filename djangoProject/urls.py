"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from posts.views import PostView, post_list, post_detail, PostMixinListView, PostDetailView, OwnerDetailView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
<<<<<<< HEAD
    path('api/posts/', PostView.as_view(), name='post-list'),
    path('api/', include('posts.urls')),
=======
    #path('api/posts/', PostView.as_view(), name='post-list'),
    path('api/posts/', PostMixinListView.as_view(), name='post-list'),
    #path('api/posts/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/<int:pk>', OwnerDetailView.as_view(), name='owner-detail'),
>>>>>>> f67c301fbfc3e90900e56d03f654736db4312fdf
    # path('api/post-list', post_list, name='post-list'),
    #path('api/posts/<int:pk>', PostView.as_view(), name='post-detail')
]
