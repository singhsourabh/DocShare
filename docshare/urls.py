from django.contrib import admin
from django.urls import path
from userauth import views as auth_views
from document import views as doc_share_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.Login.as_view(), name='login'),
    path('logout/', auth_views.Logout.as_view(), name='logout'),
    path('register/', auth_views.RegisterUser.as_view(), name='register'),
    path('doc-list/', doc_share_views.DocumentList.as_view(), name='doclist'),
    path('doc-delete/<pk>/', doc_share_views.DeleteDocument.as_view(), name='docdelete'),
    path('doc-upload/', doc_share_views.DoucumentUpload.as_view(), name='upload'),
    path('doc-share/', doc_share_views.DocumentShare.as_view(), name='share'),
    path('doc-share-list/', doc_share_views.ShareList.as_view(), name='share-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
