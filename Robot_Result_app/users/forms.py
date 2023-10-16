from django_registration.forms import RegistrationFormUniqueEmail, RegistrationFormCaseInsensitive, RegistrationForm
from users.models import User


class UserForm(RegistrationFormUniqueEmail,RegistrationFormCaseInsensitive):

    class Meta(RegistrationForm.Meta):
        model = User
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            "password1",
            "password2",
            "first_name",
            "last_name",
        ]