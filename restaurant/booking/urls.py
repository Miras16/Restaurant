import patterns as patterns
from django.urls import path
from .views import *
from .import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from xml.etree.ElementInclude import include
urlpatterns = [
    path('', views.index, name="home"),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('profile/', profile, name='Profile'),
    path('add_post/', views.addpost, name='addpost'),
    path('blog/', blog, name='blog'),
    path('search/', search, name='search'),
    path('<slug:slug>/', blog_detail, name='post_detail'),
    path('comment/<int:id>', views.comment_delete, name='comment'),
    path('delete/<int:id>', views.booking_delete, name='deleteb'),
    path('add_comment/<slug:slug>/', blog_detail, name='add_comment')




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)