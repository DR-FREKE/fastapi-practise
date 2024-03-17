from typing import Annotated
from fastapi import Request, Depends
from middlewares.auth_middleware import auth
from Error.customerror import NotAuthorizedError



async def authorize_admin(user: auth = auth, req: Request = None):
    """
    Middleware function to authorize admin access.

    Args:
        user (dict): User information.
        req (Request, optional): Request object. Defaults to None.

    Raises:
        NotAuthorizedError: If the user is not authorized as an admin.

    Returns:
        dict: User information if authorized.
    """
    if user.get('role') != "admin":
        raise NotAuthorizedError("UnAuthorized Request")
    else:
        return user
    
admin_dependency = Annotated[dict, Depends(authorize_admin)]