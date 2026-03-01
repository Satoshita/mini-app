from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


class LoginForm(FlaskForm):
    email = StringField(
        'メールアドレス',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'パスワード',
        validators=[DataRequired()]
    )

    submit = SubmitField('ログイン')


class RegisterForm(FlaskForm):
    name = StringField(
        '名前',
        validators=[DataRequired()]
    )

    email = StringField(
        'メールアドレス',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'パスワード',
        validators=[DataRequired(), Length(min=6)]
    )

    submit = SubmitField('登録')


class PersonForm(FlaskForm):
    name = StringField(
        '名前',
        validators=[DataRequired()]
    )

    age = IntegerField(
        '年齢',
        validators=[DataRequired(), NumberRange(min=0)]
    )

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    submit = SubmitField('登録')


class EditForm(FlaskForm):
    name = StringField(
        '名前',
        validators=[DataRequired()]
    )

    age = IntegerField(
        '年齢',
        validators=[DataRequired(), NumberRange(max=120)]
    )

    email = StringField(
        'メールアドレス',
        validators=[DataRequired(), Email()]
    )

    submit = SubmitField('更新')