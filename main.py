import plotly
import plotly.graph_objs as go
import json

from flask import render_template, flash, request, redirect, session
from ORM import *
from WTForms import *

app.secret_key = 'development key'


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/edit_users', methods = ['GET', 'POST'])
def edit_users():

    form = UsersForm()
    select_result = Groups.query.filter_by().all()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required')
            return render_template('users.html', data=select_result, form=form)
        else:
            group_code = session['group_edit_pk_data']
            group = Groups.query.filter_by(code=group_code).first()
            group.code = form.code.data
            db.session.commit()
            return render_template("users.html", data=select_result, form=form)

    return render_template("users.html", data=select_result, form=form)


@app.route('/users', methods=['GET', 'POST'])
def users():

    form = UsersForm()
    select_result = Groups.query.filter_by().all()

    if request.method == 'POST':

        selected_code = request.form.get('del')
        if selected_code is not None:
            selected_row = Groups.query.filter_by(code=selected_code).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            return render_template('users.html', data=select_result, form=form)

        selected_code = request.form.get('edit')
        if selected_code is not None:
            selected_row = Groups.query.filter_by(code=selected_code).first()
            session['group_edit_pk_data'] = selected_code
            return render_template("edit_users.html", row=selected_row, form=form)

        print(form.validate())
        if not form.validate():
            flash('All fields are required.')
            return render_template('users.html', data=select_result, form=form)
        else:
            group = Groups(form.code.data)
            db.session.add(group)
            db.session.commit()
            select_result.append(group)

    return render_template('users.html', data=select_result, form=form)


@app.route('/edit_sites', methods=['GET', 'POST'])
def edit_sites():

    form = SitesForm()
    select_result = Subjects.query.filter_by().all()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('edit_sites.html')
        else:
            subject_name = session['subject_edit_pk_data']
            subject = Subjects.query.filter_by(name=subject_name).first()
            subject.name = form.name.data
            db.session.commit()
            return render_template("sites.html", data=select_result, form=form)

    return render_template("sites.html", data=select_result, form=form)


@app.route('/sites', methods=['GET', 'POST'])
def sites():

    form = SitesForm()
    select_result = Subjects.query.filter_by().all()

    if request.method == 'POST':

        selected_name = request.form.get('del')
        if selected_name is not None:
            selected_row = Subjects.query.filter_by(name=selected_name).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            return render_template('sites.html', data=select_result, form=form)

        selected_name = request.form.get('edit')
        if selected_name is not None:
            selected_row = Subjects.query.filter_by(name=selected_name).first()
            session['subject_edit_pk_data'] = selected_name
            return render_template("edit_sites.html", row=selected_row, form=form)

        print(form.validate())
        if not form.validate():
            flash('All fields are required.')
            return render_template('sites.html', data=select_result, form=form)
        else:
            subject = Subjects(form.name.data)
            db.session.add(subject)
            db.session.commit()
            select_result.append(subject)

    return render_template('sites.html', data=select_result, form=form)


@app.route('/edit_styles', methods=['GET', 'POST'])
def edit_styles():

    form = StylesForm()
    select_result = Students.query.filter_by().all()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required')
            return render_template('styles.html', data=select_result, form=form)
        else:
            selected_pk_data_list = session['student_edit_pk_data'].split("█")
            selected_group_code = selected_pk_data_list[0]
            selected_spooky_book = selected_pk_data_list[1]
            print(selected_group_code, selected_spooky_book)
            student = Students.query.filter_by(study_book=selected_spooky_book, group_code=selected_group_code).first()
            student.first_name = form.first_name.data
            student.last_name = form.last_name.data
            student.study_book = form.study_book.data
            student.group_code = form.group_code.data
            db.session.commit()
            return render_template("styles.html", data=select_result, form=form)

    return render_template("styles.html", data=select_result, form=form)


@app.route('/styles', methods=['GET', 'POST'])
def styles():

    form = StylesForm()
    select_result = Students.query.filter_by().all()

    if request.method == 'POST':

        selected_pk_data = request.form.get('del')
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data.split("█")
            selected_group_code = selected_pk_data[0]
            selected_spooky_book = selected_pk_data[1]
            print(selected_spooky_book, selected_group_code)
            selected_row = Students.query.filter_by(study_book=selected_spooky_book, group_code=selected_group_code).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            return render_template('styles.html', data=select_result, form=form)

        selected_pk_data = request.form.get('edit')
        if selected_pk_data is not None:
            selected_pk_data_list = selected_pk_data.split("█")
            selected_group_code = selected_pk_data_list[0]
            selected_spooky_book = selected_pk_data_list[1]
            selected_row = Students.query.filter_by(study_book=selected_spooky_book, group_code=selected_group_code).first()
            session['student_edit_pk_data'] = selected_pk_data
            return render_template("edit_styles.html", row=selected_row, form=form)

        print(form.validate())
        if not form.validate():
            flash('All fields are required.')
            return render_template('styles.html', data=select_result, form=form)
        else:
            student = Students(form.first_name.data, form.last_name.data, form.study_book.data, form.group_code.data)
            db.session.add(student)
            db.session.commit()
            select_result.append(student)

    return render_template('styles.html', data=select_result, form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    last_char = None
    if request.method == 'POST':

        last_char = request.form.get('last_char')
        if len(last_char) > 1:
            return redirect('/dashboard')

    select_result_raw = Groups.query.filter_by().all()
    if last_char is not None and last_char != "":
        select_result = [select_result_row.code for select_result_row in select_result_raw
                         if select_result_row.code[-1] == last_char]
    else:
        select_result = [select_result_row.code for select_result_row in select_result_raw]

    codes_starts_result = list(map(lambda s: s[:2], select_result))
    codes = list(set(codes_starts_result))
    counting_stars = [0] * len(codes)

    for no_more_counting_dollars in codes_starts_result:
        counting_stars[codes.index(no_more_counting_dollars[:2])] += 1

    bar, pie = go.Bar(x=codes, y=counting_stars, marker=dict(color='rgb(122, 122, 122)')), go.Pie(labels=codes, values=counting_stars)

    data1, data2 = [bar], [pie]
    ids = ["1", "2"]

    graphJSON1 = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html',
                           graphJSON1=graphJSON1, graphJSON2=graphJSON2, ids=ids)


if __name__ == '__main__':
    app.run(debug=True)