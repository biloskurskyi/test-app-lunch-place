from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.common_views import LunchVotingBaseView
from core.models import Lunch, LunchReport, LunchVoting, User

from .serializers import LunchReportSerializer, LunchSerializer
from .time.day import get_current_day_kiev, hour_in_kiev


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
        user = request.user
        if user.user_type == 0:
            return self.get_user_menu(request)
        elif user.user_type == 1:
            return self.get_for_restaurant(request)
        else:
            return Response({"error": "Invalid user type"}, status=400)

    def get_user_menu(self, request):
        menu = Lunch.objects.filter(day=get_current_day_kiev())
        serializer = LunchSerializer(menu, many=True)
        if not menu.exists():
            return Response({"message": "No menu for today"}, status=200)

        if request.user.user_type == 0:
            return Response(serializer.data, status=200)

        return Response({"message": "This user does not have this permission"}, status=403)

    def get_for_restaurant(self, request):
        user = request.user
        menu = Lunch.objects.filter(user=user.id)
        serializer = LunchSerializer(menu, many=True)
        if not menu.exists():
            return Response({"message": "Menu does not exist"}, status=200)

        if request.user.user_type == 1:
            return Response(serializer.data, status=200)

        return Response({"message": "This user does not have this permission"}, status=403)


class MenuItemView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        if user.user_type == 0:
            return self.get_for_user(request, pk)
        elif user.user_type == 1:
            return self.get_for_restaurant(request, pk)
        else:
            return Response({"error": "Invalid user type"}, status=400)

    def get_for_user(self, request, pk):
        user = request.user
        menu_item = Lunch.objects.filter(id=pk).first()
        if not menu_item or user.user_type != 0:
            return Response({"error": "This item does not exist"}, status=404)

        serializer = LunchSerializer(menu_item, many=False)
        return Response(serializer.data)

    def get_for_restaurant(self, request, pk):
        user = request.user
        menu_item = Lunch.objects.filter(id=pk, user=user.id).first()
        if not menu_item or user.user_type != 1:
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


class LunchVotingView(LunchVotingBaseView):

    def post(self, request, pk):
        user, date = self.get_user_and_date(request)
        lunch = self.get_lunch(pk)

        if not lunch:
            return Response({"error": "Lunch item does not exist"}, status=404)

        permission_error = self.check_user_permission(user)
        if permission_error:
            return Response(*permission_error)

        existing_vote = LunchVoting.objects.filter(user=user, date=date).first()
        if existing_vote:
            return Response({"error": "You have already voted for lunch today"}, status=400)

        time_error = self.check_time_limit()
        if time_error:
            return Response(*time_error)

        vote = LunchVoting(user=user, lunch=lunch, date=date)
        vote.save()

        report, created = LunchReport.objects.get_or_create(lunch=lunch, date=date)
        report.count += 1
        report.save()

        return Response({"message": "Vote cast successfully"})

    def put(self, request, pk):
        user, date = self.get_user_and_date(request)
        lunch_voting = LunchVoting.objects.filter(user=user, date=date).first()

        if not lunch_voting:
            return Response({"error": "Lunch item does not exist"}, status=404)

        permission_error = self.check_user_permission(user)
        if permission_error:
            return Response(*permission_error)

        new_lunch = self.get_lunch(pk)
        if not new_lunch:
            return Response({"error": "This lunch item does not exist"}, status=404)

        time_error = self.check_time_limit()
        if time_error:
            return Response(*time_error)

        old_lunch = lunch_voting.lunch
        lunch_voting.lunch = new_lunch
        lunch_voting.save()

        old_report = LunchReport.objects.get(lunch=old_lunch, date=date)
        old_report.count -= 1
        old_report.save()

        new_report, created = LunchReport.objects.get_or_create(lunch=new_lunch, date=date)
        new_report.count += 1
        new_report.save()

        return Response({"message": "Vote updated successfully"})


class RemoveVotingView(LunchVotingBaseView):
    def delete(self, request):
        user, date = self.get_user_and_date(request)
        lunch_voting = LunchVoting.objects.filter(user=user, date=date).first()

        if not lunch_voting:
            return Response({"error": "Lunch item does not exist"}, status=404)

        permission_error = self.check_user_permission(user)
        if permission_error:
            return Response(*permission_error)

        time_error = self.check_time_limit()
        if time_error:
            return Response(*time_error)

        try:
            lunch_voting.delete()
            old_report = LunchReport.objects.get(lunch=lunch_voting.lunch, date=date)
            old_report.count -= 1
            old_report.save()
            return Response({'message': 'Delete successful!'}, status=204)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class VotingResultsView(APIView):
    def get(self, request):
        user = request.user
        if user.user_type != 1:
            return Response({"error": "You do not have permission to access this resource"}, status=403)

        menu = Lunch.objects.filter(user=user.id, day=get_current_day_kiev())
        if not menu.exists():
            return Response({"message": "No menu for today"}, status=404)

        reports = LunchReport.objects.filter(lunch__in=menu, date=timezone.now().date())
        serializer = LunchReportSerializer(reports, many=True)
        return Response(serializer.data, status=200)
