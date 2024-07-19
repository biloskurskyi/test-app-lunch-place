from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Lunch
from menu.time.day import get_current_day_kiev, hour_in_kiev


class LunchVotingBaseView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user_and_date(self, request):
        user = request.user
        date = timezone.now().date()
        return user, date

    def get_lunch(self, pk):
        return Lunch.objects.filter(id=pk, day=get_current_day_kiev()).first()

    def check_user_permission(self, user):
        if user.user_type != 0:
            return {"error": "You have not permission for voting."}, 403
        return None

    def check_time_limit(self):
        if hour_in_kiev >= 17:
            return {"error": "time for voting is closed for today. Be faster tomorrow:)"}, 200
        return None
