# Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.contrib.auth.models import Group
from rest_framework import viewsets
from users.serializers import UserSerializer, GroupSerializer
from users.models import User


from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
    from rest_framework.permissions import IsAuthenticated

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
    from rest_framework.permissions import IsAuthenticated

    queryset = Group.objects.all()
    serializer_class = GroupSerializer



