from django.contrib.auth import get_user_model
from django.db import models


class PasskeyCredential(models.Model):
    """Passkey credential public portion stored in the database"""

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="credentials"
    )
    credential_id = models.BinaryField(null=False, blank=False)
    credential_public_key = models.BinaryField(null=False, blank=False)
    current_sign_count = models.IntegerField()

    def __str__(self) -> str:
        return f"<Credential for {self.user}>"
