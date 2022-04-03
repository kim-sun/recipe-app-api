from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # exclude = []  # 排除此 model 中指定之 field 與 fields 相反
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        # 可針對 fields 中指定欄位設定特性 如僅供寫 最小長度 等

    # django rest_framework 內建func
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            # rest_framework know how to handle the Error by code as 400
            raise serializers.ValidationError(msg, code='authentication')

        # override the validation which need a return
        attrs['user'] = user
        return attrs
