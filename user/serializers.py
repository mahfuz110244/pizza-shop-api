from rest_framework import serializers
from .models import Customer
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    # email = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=14)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        username = data.get('username', None)
        password = data.get('password', None)

        # # As mentioned above, an email is required. Raise an exception if an
        # # email is not provided.
        # if username is None:
        #     raise serializers.ValidationError(
        #         'An Username is required to log in.'
        #     )
        #
        # # As mentioned above, a password is required. Raise an exception if a
        # # password is not provided.
        # if password is None:
        #     raise serializers.ValidationError(
        #         'A password is required to log in.'
        #     )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=username, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )



        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'username': user.username
        }


class CustomerLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'username']
        # fields = '__all__'
        # exclude = ['password', 'otp', 'email']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'username', 'address', 'latitude', 'longitude']


class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'username']
