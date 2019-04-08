from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
import pics.views as views
app_name  = 'pics'
urlpatterns = [
    url(r'^$',views.index,name='home'),
    path('login',views.login_function,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout_view,name='logout'),
    path('add_album',views.CreateAlbum.as_view(),name="add_album"),
    path('delete_album/<int:pk>',views.DeleteAlbum.as_view(),name='delete_album'),
    path('update_album/<int:pk>',views.UpdateAlbum.as_view(),name='update_album'),
    path('all_albums',views.ListView.as_view(),name='all_albums'),
    path('<int:pk>',views.AlbumDetail.as_view(),name="detail"),
    path('add_photos/<int:album_id>', views.CreateAlbumPhotos.as_view(), name="add_album_photos"),
    path('delete_photo/<int:pk>', views.DeleteAlbumPhotos.as_view(), name='delete_album_photos'),
    path('update_photo/<int:pk>', views.UpdateAlbumPhotos.as_view(), name='update_album_photos'),
    path('<int:album_id>/all_albums_photos', views.ListViewPhotos.as_view(), name='all_albums_photos'),
    path('photos/<int:pk>', views.AlbumDetailPhotos.as_view(), name="detail_photos"),
]