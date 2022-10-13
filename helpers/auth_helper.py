import jwt,uuid
from rest_framework.response import Response
from rest_framework import status
from wolfpack.settings import JwtConstants
from helpers.api_helper import api_response, API_Messages
from helpers.enum_helper import ResponseType
from accounts.models import TokenBlackList, User

def login_required():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                token = request.headers['Authorization'].split(" ")[-1]
                TokenBlackList.objects.get(token=token)
                return Response(api_response(ResponseType.FAILED, API_Messages.SESSION_EXPIRED), status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                try:
                    payload = jwt.decode(token,
                        JwtConstants.SECRET_KEY,
                        algorithms=JwtConstants.JWT_ALGORITHM,
                    )
                    request.user = User.objects.get(id=uuid.UUID(payload["id"]))
                    return func(request, *args, **kwargs)
                except Exception as exp:
                    return Response(api_response(ResponseType.FAILED, API_Messages.SESSION_EXPIRED), status=status.HTTP_401_UNAUTHORIZED)
        return wrapper
    return decorator