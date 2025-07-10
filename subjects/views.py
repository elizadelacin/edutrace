from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Subject
from .serializers import SubjectSerializer
from .permissions import IsAdminOrReadOnly

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
