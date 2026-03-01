from flask import Blueprint, render_template, flash, redirect, request, url_for
from .models import Person
from . import db
from .forms import EditForm, PersonForm
from flask_login import login_required, current_user

main= Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PersonForm()

    if form.validate_on_submit():
        person = Person(
            name=form.name.data,
            age=form.age.data,
            email=form.email.data,
            user_id=current_user.id
        )

        db.session.add(person)
        db.session.commit()

        flash('登録しました。', 'success')
        return redirect(url_for('main.index'))

    persons = Person.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'index.html',
        form=form,
        people=persons
    )


@main.route('/over20')
def over20():
    people = Person.query.filter(Person.age >= 20).all()

    return render_template(
        'over20.html',
        people=people
    )


@main.route('/under20')
def under20():
    people = Person.query.filter(Person.age < 20).all()

    return render_template(
        'under20.html',
        people=people
    )


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    person = Person.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    form = EditForm(obj=person)

    if form.validate_on_submit():
        person.name = form.name.data
        person.age = form.age.data
        person.email = form.email.data
        db.session.commit()
        flash('更新しました。')
        return redirect(url_for('main.index'))


    return render_template(
        'edit.html',
        person=person,
        form=form
    )


@main.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    person = Person.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('main.index'))


#　バリデーションを関数化
def validate_age(age):
    try:
        age = int(age)
    except ValueError:
        return False, '年齢は数字で入力してください。'

    if age < 0 or age > 100:
        return False, '100までの正数で入力してください。。'

    return True, age
