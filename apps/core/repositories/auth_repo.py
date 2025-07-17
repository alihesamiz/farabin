from apps.core.models import OTP


class AuthRepository:
    @staticmethod
    def get_user_otp(phone_number: str, otp_code: str):
        return (
            OTP.objects.select_related("user")
            .filter(user__phone_number=phone_number, otp_code=otp_code)
            .last()
        )
