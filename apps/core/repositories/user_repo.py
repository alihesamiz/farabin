from apps.core.models import User
from constants.typing import UserType


class UserRepository:
    @staticmethod
    def get_user_by_phone_number(phone_number: str) -> UserType:
        try:
            return User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise 
        
    @staticmethod
    def get_user_by_id(user_id: int) -> UserType:
        return User.objects.filter(pk=user_id)
