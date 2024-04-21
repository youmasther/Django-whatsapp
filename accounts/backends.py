from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CaseInsensitiveModelBackend(ModelBackend):
	"""The `CaseInsensitiveModelBackend` class in Python provides a custom authentication method that
	allows case-insensitive username authentication."""
	def authenticate(self, request, username=None, password=None, **kwargs):
        """
		The function `authenticate` in Python is used to authenticate a user based on the provided username
        and password.
        
        :param request: The `request` parameter typically represents the HTTP request that is being made to
        the server. It contains information such as headers, method, body, and other details related to the
        request being made by the client to the server. In the context of the `authenticate` method you
        provided, the `request
        :param username: The `username` parameter in the `authenticate` method is used to specify the
        username of the user trying to authenticate. It can be provided as an argument or as a keyword
        argument in the method call. If not provided as an argument, the method will attempt to extract it
        from the `USERNAME_FIELD
        :param password: The `password` parameter in the `authenticate` method is used to store the
        password provided by the user for authentication. It is typically used to validate the user's
        identity by checking if the password matches the one stored in the database for the corresponding
        user account
        :return: The code is returning the user object if the provided username and password are valid and
        the user can be authenticated.
        """
		
        UserModel = get_user_model()
		if username is None:
			username = kwargs.get(UserModel.USERNAME_FIELD)

		try:
			case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
			user = UserModel._default_manager.get(**{case_insensitive_username_field:username})
		except UserModel.DoesNotExist:
			UserModel().set_password(password)
		else:
			if user.check_password(password) and self.user_can_authenticate(user):
				return user
		