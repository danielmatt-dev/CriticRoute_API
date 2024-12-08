from rest_framework import serializers


class ProyectoSerializer(serializers.Serializer):

    titulo = serializers.CharField(
        min_length=10,
        max_length=50,
        error_messages={
            'min_length': 'El título debe tener al menos 10 caracteres',
            'max_length': 'El título no puede tener más de 50 caracteres',
            'required': 'El título es obligatorio',
        }
    )

    descripcion = serializers.CharField(
        min_length=0,
        max_length=255,
        allow_blank=True,
        error_messages={
            'max_length': 'La descripción no puede tener más de 255 caracteres',
            'required': 'La descripción es obligatoria',
        }
    )

    file_bytes = serializers.CharField(
        min_length=0,
        error_messages={
            'min_length': 'El file no debe estar vacío',
            'required': 'El file es obligatorio',
        }
    )
