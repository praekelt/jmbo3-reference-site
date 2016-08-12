import json

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from jmbo.models import ModelBase

from mysite.tests.urls import urlpatterns

from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.test import APIClient

from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class ModelBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelBase
        fields = ("title",)


class MockListView(generics.ListAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ModelBaseSerializer

    model = ModelBase

    def get_queryset(self, request):
        queryset = ModelBase.permitted.get_queryset(request.user)
        return queryset

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = ModelBaseSerializer(queryset, many=True)
        return Response(serializer.data)


urlpatterns += [
    url(r"^modelbase-list/$", MockListView.as_view()),
]


class TokenAuthenticationTestCase(TestCase):
    """
    Test that users can be authenticated using
    JWT and view objects.
    """

    urls = "mysite.tests.test_authentication"

    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()


        # create admin user and non-staff user
        self.admin_user = User.objects.create_superuser(
            "admin",
            "admin@test.com",
            "password"
        )
        self.admin_user.save()

        self.non_staff_user = User.objects.create_user(
            "john",
            "john@doe.com",
            "password"
        )
        self.non_staff_user.save()

        # obtain tokens for both users
        data = {
            "username": "admin",
            "password": "password"
        }
        response = self.client.post(reverse("jwt:obtain_token"), data)
        self.admin_user_jwt = response.data["token"]

        data = {
            "username": "john",
            "password": "password"
        }
        response = self.client.post(reverse("jwt:obtain_token"), data)
        self.non_staff_user_jwt = response.data["token"]

        # create published object
        published_object = ModelBase(
            title="Published object",
            state="published"
        )
        published_object.save()
        published_object.sites = Site.objects.all()
        published_object.save()

        # create unpublished object
        unpublished_object = ModelBase(
            title="Unpublished object",
            state="unpublished"
        )
        unpublished_object.save()
        unpublished_object.sites = Site.objects.all()
        unpublished_object.save()

    def test_admin_has_access_to_all(self):
        authorization_header = "JWT {0}".format(self.admin_user_jwt)
        response = self.client.get(
            "/modelbase-list/",
            HTTP_AUTHORIZATION=authorization_header
        )
        items = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(items),
            ModelBase.permitted.get_queryset(self.admin_user).count()
        )

    def test_non_staff_only_accesses_published(self):
        authorization_header = "JWT {0}".format(self.non_staff_user_jwt)
        response = self.client.get(
            "/modelbase-list/",
            HTTP_AUTHORIZATION=authorization_header)
        items = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(items),
            ModelBase.permitted.get_queryset(self.non_staff_user).count()
        )

    def test_unauthenticated_user_has_no_access(self):
        # unauthenticated requests using rest_framework_jwt return a 401
        response = self.client.get("/modelbase-list/")
        self.assertEqual(response.status_code, 401)

        # an unauthenticated user shoulnd't be able to see any items
        items = json.loads(response.content)
        self.failIf(len(items) == 0)