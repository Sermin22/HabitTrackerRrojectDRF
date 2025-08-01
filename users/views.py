from rest_framework.generics import CreateAPIView
from users.models import CustomUser
from users.serilizers import CustomUserSerializer


class CustomUserCreateAPIView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    # permission_classes = [AllowAny]  # если в settings.py настройка IsAuthenticated

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
