from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


# -----------------------------------------------------------
class GetRecommendationsView(APIView):
    def get(self, request):
        return Response({"details": "Recommendation OK"}, status=status.HTTP_200_OK)