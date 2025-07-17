from apps.core.models import User


class UserRepository:
    @staticmethod
    def get_user_by_phone_number(phone_number: str):
        return User.objects.get(phone_number=phone_number)

    @staticmethod
    def get_user_by_id(user_id: int):
        return User.objects.filter(pk=user_id)
