from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Subject
from .serializers import SubjectSerializer
from .permissions import IsAdminOrReadOnly

class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return Subject.objects.all()

        elif user.role == 'TEACHER':
            return Subject.objects.filter(teacher=user)

        elif user.role == 'PARENT':
            children = user.children.all()
            classrooms = [child.classroom for child in children]
            return Subject.objects.filter(teacher__classroom__in=classrooms).distinct()

        return Subject.objects.none()
