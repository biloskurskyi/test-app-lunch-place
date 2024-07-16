from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Lunch, User

from .serializers import LunchSerializer


# Create your views here.

class MenuView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = LunchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid() and request.user.user_type == 1:
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"message": "This user has not this permission"}, status=400)

    def get(self, request):
        # user = request.user
        menu = Lunch.objects.filter(day=1)
        serializer = LunchSerializer(menu, many=True)
        if not menu.exists():
            return Response({"message": "No menu for today"}, status=200)

        if request.user.user_type == 0:
            return Response(serializer.data, status=200)

        return Response({"message": "This user has not this permission"}, status=403)
