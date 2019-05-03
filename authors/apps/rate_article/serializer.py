from rest_framework import serializers
from .models import Rate


class RateSerializer(serializers.ModelSerializer):
    """Serializer to rate articles"""

    def validate_rating(self, rating):
        if rating < 1 or rating > 5:
            raise serializers.ValidationError("rating should include numbers 1 to 5")
        return rating

    class Meta:

        model = Rate

        fields = ('rating', 'user')
