from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'classroom', 'subject', 'teacher', 'weekday', 'time']
        read_only_fields = ['id']

    def validate(self, attrs):
        # Mövcud instance varsa (PATCH/PUT üçün)
        if self.instance:
            # Mövcud obyektin özünü yoxlamaq istəmirik
            qs = Schedule.objects.exclude(pk=self.instance.pk)
        else:
            qs = Schedule.objects.all()

        classroom = attrs.get('classroom', getattr(self.instance, 'classroom', None))
        weekday = attrs.get('weekday', getattr(self.instance, 'weekday', None))
        time = attrs.get('time', getattr(self.instance, 'time', None))

        if qs.filter(classroom=classroom, weekday=weekday, time=time).exists():
            raise serializers.ValidationError({
                'non_field_errors': ['Bu sinifdə bu gün və vaxt üçün artıq dərs mövcuddur.']
            })

        return attrs
