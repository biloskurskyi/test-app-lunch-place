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
        menu = Lunch.objects.filter(day=3)
        serializer = LunchSerializer(menu, many=True)
        if not menu.exists():
            return Response({"message": "No menu for today"}, status=200)

        if request.user.user_type == 0:
            return Response(serializer.data, status=200)

        return Response({"message": "This user has not this permission"}, status=403)


class MenuItemView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        menu_item = Lunch.objects.filter(id=pk).first()
        if not menu_item or user.user_type != 0:
            return Response({"error": "This item does not exist"}, status=404)

        serializer = LunchSerializer(menu_item, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        request.data['user'] = user.id
        menu_item = Lunch.objects.filter(id=pk, user_id=user.id).first()
        if not menu_item:
            return Response({"error": "This item does not exist"}, status=404)

        menu = request.data.get('menu', menu_item.menu)
        day = request.data.get('day', menu_item.day)
        serializer = LunchSerializer(menu_item, data={'menu': menu, 'day': day},
                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = request.user
        menu_item = Lunch.objects.filter(id=pk, user_id=user.id).first()
        if not menu_item:
            return Response({"error": "Post not found"}, status=404)

        try:
            menu_item.delete()
            return Response({
                'message': 'Delete successful!'
            }, status=204)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
