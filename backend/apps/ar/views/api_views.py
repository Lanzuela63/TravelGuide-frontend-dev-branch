from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from math import radians, sin, cos, sqrt, atan2

from apps.ar.models import ARScene
from apps.ar.serializers import ARSceneSerializer


# -------------------------
# Utility
# -------------------------
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points in kilometers."""
    R = 6371  # Earth radius in km
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = (
        sin(dLat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# -------------------------
# AR Scene Endpoints
# -------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def list_ar_scenes(request):
    scenes = ARScene.objects.all()
    serializer = ARSceneSerializer(scenes, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def nearby_ar_scenes(request):
    """
    Finds AR scenes within a given radius from a user's location.
    Expects 'lat' and 'lon' as query parameters.
    """
    try:
        user_lat = float(request.query_params.get("lat"))
        user_lon = float(request.query_params.get("lon"))
    except (TypeError, ValueError):
        return Response(
            {"error": "Invalid or missing 'lat' and 'lon' parameters."}, status=400
        )

    radius_km = 10
    nearby_scenes = []

    for scene in ARScene.objects.all():
        if scene.latitude is not None and scene.longitude is not None:
            distance = haversine_distance(
                user_lat, user_lon, scene.latitude, scene.longitude
            )
            if distance <= radius_km:
                nearby_scenes.append(scene)

    serializer = ARSceneSerializer(
        nearby_scenes, many=True, context={"request": request}
    )
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def test_ar_api(request):
    """
    Simple mock AR API endpoint to verify mobile connection.
    """
    data = [
        {
            "id": 1,
            "name": "Test AR Scene",
            "description": "Mock AR scene for testing connectivity.",
            "latitude": 13.12345,
            "longitude": 123.12345,
            "marker_image": None,
            "model_url": None,
            "objects": [
                {
                    "id": 101,
                    "name": "Test Object",
                    "model_url": "https://example.com/test-model.glb",
                    "rotation_deg": "0,0,0",
                    "scale": 1.0,
                    "info": "Sample AR object for testing",
                    "image": None,
                    "offset_x": 0,
                    "offset_y": 0,
                    "offset_z": 0,
                    "description": "Mock 3D object",
                }
            ],
        }
    ]
    return Response(data)
