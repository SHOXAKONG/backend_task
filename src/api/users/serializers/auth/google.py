from django.conf import settings
from rest_framework import serializers
from google.oauth2 import id_token as google_id_token
from google.auth.transport.requests import Request
import requests as http

class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=False, write_only=True)
    access_token = serializers.CharField(required=False, write_only=True)

    def validate(self, attrs):
        id_tok = attrs.get("id_token")
        acc_tok = attrs.get("access_token")

        if bool(id_tok) == bool(acc_tok):
            raise serializers.ValidationError(
                "Provide exactly one of: id_token or access_token."
            )

        if id_tok:
            try:
                claims = google_id_token.verify_oauth2_token(
                    id_tok, Request(), settings.GOOGLE_CLIENT_ID
                )
            except Exception as e:
                raise serializers.ValidationError(
                    {"id_token": "Invalid Google id_token", "detail": str(e)}
                )
        else:
            r = http.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {acc_tok}"},
                timeout=10,
            )
            if r.status_code != 200:
                raise serializers.ValidationError(
                    {"access_token": "Invalid access_token", "google_error": r.json()}
                )
            claims = r.json()

        email = claims.get("email")
        if not email:
            raise serializers.ValidationError("Google response has no email.")

        attrs["claims"] = claims
        return attrs
