from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import RoutingEdge


class RoutingEdgeSerializer(GeoFeatureModelSerializer):
    """
    GeoJSON serializer for a single routing edge.
    """

    class Meta:
        model = RoutingEdge
        geo_field = "geom"
        fields = (
            "id",
            "geom",
            "campus",
            "building",
            "floor_from",
            "floor_to",
            "line_type",
            "is_private",
            "cost",
            "reverse_cost",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        line_type = attrs.get("line_type", getattr(self.instance, "line_type", None))
        floor_from = attrs.get("floor_from", getattr(self.instance, "floor_from", None))
        floor_to = attrs.get("floor_to", getattr(self.instance, "floor_to", None))

        if line_type in (
            RoutingEdge.LINE_TYPE_ELEVATOR,
            RoutingEdge.LINE_TYPE_STAIRS,
        ):
            if floor_from == floor_to:
                raise serializers.ValidationError(
                    "elevator and stairs must connect different floors."
                )

        if line_type in (
            RoutingEdge.LINE_TYPE_ELEVATOR_NO_FLOOR_CHANGE,
            RoutingEdge.LINE_TYPE_STAIRS_NO_FLOOR_CHANGE,
        ):
            if floor_from != floor_to:
                raise serializers.ValidationError(
                    "elevator-no-floor-change and stairs-no-floor-change must not change floors."
                )

        return attrs


class BulkRoutingEdgePayloadSerializer(serializers.Serializer):
    """
    Payload for bulk-save endpoint.
    """

    campus = serializers.PrimaryKeyRelatedField(
        queryset=RoutingEdge._meta.get_field("campus").remote_field.model.objects.all()
    )
    building = serializers.PrimaryKeyRelatedField(
        queryset=RoutingEdge._meta.get_field("building").remote_field.model.objects.all()
    )

    created = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )
    updated = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )
    deleted = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )
