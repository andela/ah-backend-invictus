from rest_framework.serializers import ValidationError


class ValidateArticleCreation:

    def validate_title(self, title):
        if len(title) < 3:
            raise ValidationError("Title should be atleast 10 characters")
