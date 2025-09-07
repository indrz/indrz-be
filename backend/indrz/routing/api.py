
from routing.routing_node_networklines import generate_routing_network
from django.contrib import messages

from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def run_node_network(request):
    try:
        route_generated = generate_routing_network()
        if route_generated.get('status') == 'success':
            messages.success(request, "Script executed successfully")
            return Response({"message": "Script started successfully"}, status=status.HTTP_200_OK)
        else:
            messages.error(request, f"Error generating the routing network")
            return Response({"message": "Script failed to start"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except APIException as e:
        messages.error(request, f"Error executing script: {str(e)}")
        return Response({"error": f"Error executing script: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
