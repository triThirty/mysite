from django.conf.urls import include, url
from views import *
from django.contrib import admin
from dollars import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^time/(\d{1,2})/$',hello)
    url(r'^$',views.homepage),
    url(r'^chatroom/',views.chatroom),
]
