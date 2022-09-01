from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import trendbi.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", trendbi.views.index, name="index"),
    path("db/", trendbi.views.db, name="db"),
    path("admin/", admin.site.urls),
]
