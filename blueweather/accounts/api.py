from django.http.request import HttpRequest

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

from django.db.utils import IntegrityError

from django.core.exceptions import ValidationError

from blueweather.api.decorators import api
from blueweather.api.exceptions import NotFoundError, ValidateError


@api(name="login", methods=['POST'], allow_get_params=False)
def login_view(request: HttpRequest, username: str, password: str):
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return {
            'username': user.get_username(),
            'name': user.get_full_name()
        }
    raise NotFoundError(400, "Invalid username or password")


@api(name="logout")
def logout_view(request: HttpRequest):
    logout(request)


@api(methods=['POST'], allow_get_params=False)
def password_change(request: HttpRequest, password: str, new_password: str):
    user = authenticate(
        request,
        username=request.user.get_username(),
        password=password
    )
    if user:
        # Validate the password
        try:
            if password == new_password:
                raise ValidationError([
                    "New password cannot the same as the old password"
                ])
            validate_password(new_password, user)
        except ValidationError as error:
            raise ValidateError(
                error.messages,
                detail="Password Validation Error"
            )

        user.set_password(new_password)
        user.save()
        return {"detail": "Password successfully changed"}
    raise NotFoundError(400, "Invalid Password")


@api(methods=['POST'], allow_get_params=False)
def register(request: HttpRequest, username: str, password: str, name: str):
    first_name, last_name = name.strip().split(' ', maxsplit=1)

    try:
        try:
            validate_password(password)
        except ValidationError as error:
            raise ValidateError(
                {'password': error.messages}
            )
        user: User = User.objects.create_user(
            username=username,
            first_name=first_name.strip(),
            last_name=last_name.strip()
        )
        user.set_password(password)
    except IntegrityError as error:
        message, value = error.args[0].split(':', maxsplit=1)
        message: str = message.strip()
        value: str = value.strip()
        if message.startswith("UNIQUE"):
            message = "already taken"
        raise ValidateError({
            value.split('.')[-1]: message
        })
