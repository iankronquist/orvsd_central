from flask.ext.wtf import (Form, TextField, PasswordField, BooleanField,
                           SelectField, SelectMultipleField, Required, Email)


class LoginForm(Form):
    name = TextField('name', [Required()])
    password = PasswordField('password', [Required()])


class AddUser(Form):
    user = TextField('user', [Required()])
    password = PasswordField('password', [Required()])
    confirm_pass = PasswordField('confirm_pass', [Required()])
    email = TextField('username', [Required(), Email()])
    role = SelectField('role', choices=[('viewonly', 'View Only'),
                                        ('helpdesk', 'Helpdesk'),
                                        ('admin', 'Admin')])


class InstallCourse(Form):
    defaults = [('None', '---')]
    site = SelectMultipleField('Site', choices=defaults)
    course = SelectMultipleField('Course', choices=defaults)
    filter = SelectField('Filter', choices=defaults)
