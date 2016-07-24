from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from rest_framework import routers, serializers, viewsets
import rest_framework_extras
from jmbo.admin import ModelBaseAdmin, ModelBaseAdminForm
from jmbo import api as jmbo_api
from post import api as post_api

from mysite.admin import ManufacturerAdminForm
from mysite.views import CarViewSet, ManufacturerViewSet


router = routers.DefaultRouter()

# Instruct DRFE to discover models. Illustrates form override.
rest_framework_extras.discover(router, override=[
        ("mysite-manufacturer", dict(form=ManufacturerAdminForm)),
        #("mysite-post", dict(admin=ModelBaseAdmin, admin_site=admin.site)),
    ]
)

# Register DRFE routers
rest_framework_extras.register(router)

# Register jmbo suite routers
jmbo_api.register(router)
post_api.register(router)

# Register this app's viewsets
router.register(r"cars", CarViewSet)
router.register(r"manufacturers", ManufacturerViewSet)

admin.autodiscover()

urlpatterns = [
    url(r"^api/(?P<version>(v1))/", include(router.urls)),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^jmbo/", include("jmbo.urls")),
    url(r"^comments/", include("django_comments.urls")),
    url(r"^post/", include("post.urls")),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]

if settings.DEBUG:
    urlpatterns += [
        url(r"^media/(?P<path>.*)$", "django.views.static.serve",
        {"document_root": settings.MEDIA_ROOT, "show_indexes": True}),
    ]
