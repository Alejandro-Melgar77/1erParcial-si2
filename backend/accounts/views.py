# accounts/views.py

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import base64
import io
from PIL import Image

from .models import (
    User,
    Unit,
    CommonArea,
    Reservation,
    Expense,
    Vehicle,
    Visitor,
    FaceRecord,
    SecurityEvent,
)
from .serializers import (
    UserSerializer,
    UnitSerializer,
    CommonAreaSerializer,
    ReservationSerializer,
    ExpenseSerializer,
    VehicleSerializer,
    VisitorSerializer,
    FaceRecordSerializer,
    SecurityEventSerializer,
    RegisterSerializer,
)

User = get_user_model()

# ------------------------
# Registro de usuario
# ------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)

        # Devolvemos los datos del usuario recién creado
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)

# ------------------------
# Listar usuarios (solo admin)
# ------------------------
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# ------------------------
# Actualizar rol de usuario (solo admin)
# ------------------------
class UpdateUserRoleView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# ------------------------
# Login con tokens + datos de usuario
# ------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Agregamos la info del usuario logueado
        data['user'] = UserSerializer(self.user).data
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ------------------------
# CRUD para modelos
# ------------------------

# CRUD User
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# CRUD Unit
class UnitListView(generics.ListCreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

class UnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

# CRUD CommonArea
class CommonAreaListView(generics.ListCreateAPIView):
    queryset = CommonArea.objects.all()
    serializer_class = CommonAreaSerializer
    permission_classes = [IsAuthenticated]

class CommonAreaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommonArea.objects.all()
    serializer_class = CommonAreaSerializer
    permission_classes = [IsAuthenticated]

# CRUD Reservation
class ReservationListView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

# CRUD Expense
class ExpenseListView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

# CRUD Vehicle
class VehicleListView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

# CRUD Visitor
class VisitorListView(generics.ListCreateAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [IsAuthenticated]

class VisitorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [IsAuthenticated]

# CRUD FaceRecord
class FaceRecordListView(generics.ListCreateAPIView):
    queryset = FaceRecord.objects.all()
    serializer_class = FaceRecordSerializer
    permission_classes = [IsAuthenticated]

class FaceRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FaceRecord.objects.all()
    serializer_class = FaceRecordSerializer
    permission_classes = [IsAuthenticated]

# CRUD SecurityEvent
class SecurityEventListView(generics.ListCreateAPIView):
    queryset = SecurityEvent.objects.all()
    serializer_class = SecurityEventSerializer
    permission_classes = [IsAuthenticated]

class SecurityEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SecurityEvent.objects.all()
    serializer_class = SecurityEventSerializer
    permission_classes = [IsAuthenticated]

# ------------------------
# Reconocimiento facial
# ------------------------

from .face_recognition_utils import save_face_encoding, recognize_face


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_face(request):
    """
    Vista para registrar el rostro de un usuario.
    Espera recibir una imagen en base64.
    """
    user = request.user
    image_data = request.data.get('image')  # Imagen en base64

    if not image_data:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Decodificar imagen base64
    try:
        img_binary = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_binary))
        img_path = f'/tmp/{user.id}_face.jpg'  # temporal
        img.save(img_path)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    success = save_face_encoding(user, img_path)
    if success:
        return Response({'message': 'Face registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'No face detected in image'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recognize_face_view(request):
    """
    Vista para reconocer un rostro enviado desde la cámara.
    """
    image_data = request.data.get('image')  # Imagen en base64

    if not image_data:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Decodificar imagen base64
    try:
        img_binary = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_binary))
        img_path = f'/tmp/unknown_face.jpg'  # temporal
        img.save(img_path)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    user = recognize_face(img_path)
    if user:
        return Response({'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Unknown face'}, status=status.HTTP_404_NOT_FOUND)