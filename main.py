# -*- coding: utf8 -*-
from flask import Flask, render_template, redirect, request, abort, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.users import User
from data.problems import Problem
from data.contests import Contest
from data.solutions import Solution
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms import FileField
from wtforms.fields.html5 import EmailField, DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
import os


def update_solutions():
    session = db_session.create_session()
    solutions = session.query(Solution).filter(Solution.status == 'Running...')
    for i in solutions:
        try:
            res = open('test' + str(i.id) + '.txt').read()
            i.status = res
            os.system('del ' + os.getcwd() + '\\test' + str(i.id) + '.txt')
        except:
            continue
    session.commit()


class RegisterForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class AddProblemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    time_limit = IntegerField('Time limit', validators=[DataRequired()])
    file_in = StringField('File in', validators=[DataRequired()])
    file_out = StringField('File out', validators=[DataRequired()])
    task_file = FileField('Task file', validators=[FileRequired()])
    tests_file = FileField('Tests file', validators=[FileRequired(),
                                                     FileAllowed(['txt'], '.txt only!')])
    answers_file = FileField('Answers file', validators=[FileRequired(),
                                                         FileAllowed(['txt'], '.txt only!')])
    submit = SubmitField('Add problem')


class ProblemForm(FlaskForm):
    solution_file = FileField('Solution file', validators=[FileRequired(),
                                                           FileAllowed(['cpp'], '.cpp only!')])
    submit = SubmitField('Send solution')


class AddContestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateTimeLocalField('Start date', validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    finish_date = DateTimeLocalField('Finish date', validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    problems = StringField('Problems id', validators=[DataRequired()])
    submit = SubmitField('Add contest')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'IJUDGE_KEY'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
def index():
    update_solutions()
    session = db_session.create_session()
    now = datetime.datetime.now()
    contests = session.query(Contest).filter(Contest.start_date <= now, Contest.finish_date > now)
    no_one = False
    if contests.first():
        no_one = True
    contests_bef = []
    contests_after = []
    if current_user.is_authenticated and current_user.id == 1:
        contests_bef = session.query(Contest).filter(Contest.finish_date < now)
        contests_after = session.query(Contest).filter(Contest.start_date >= now)
        if contests_bef.first():
            no_one = True
        if contests_after.first():
            no_one = True
    return render_template('index.html', title='Ijudge', contests=contests, no_one=no_one,
                           contests_after=contests_after, contests_bef=contests_bef)


@app.route('/register', methods=['GET', 'POST'])
def register():
    update_solutions()
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register',
                                               form=form,
                                               message="Passwords do not match")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register',
                                           form=form,
                                           message="This user already exists")
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.hashed_password = generate_password_hash(form.password.data)
        session.add(user)
        session.commit()
        if current_user.is_authenticated:
            logout_user()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    update_solutions()
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Login',
                               message="Incorrect login or password",
                               form=form)
    return render_template('login.html', title='Login', form=form)


@app.route('/add_problem', methods=['GET', 'POST'])
@login_required
def add_problem():
    update_solutions()
    if current_user.id != 1:
        abort(404)
    form = AddProblemForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        prob = Problem()
        prob.name = form.name.data
        prob.time_limit = form.time_limit.data
        prob.file_in = form.file_in.data
        prob.file_out = form.file_out.data
        idnow = len(session.query(Problem).all()) + 1
        path = os.getcwd()
        path += '\\problems\\' + str(idnow) + '\\'
        ###############################
        name = form.task_file.data.filename
        ras = name[name.index('.'):]
        if not os.path.exists(path):
            os.makedirs(path)
        form.task_file.data.save(path + 'task_file' + ras)
        prob.task_file = path + 'task_file' + ras
        ###############################
        name = form.tests_file.data.filename
        ras = name[name.index('.'):]
        if not os.path.exists(path):
            os.makedirs(path)
        form.tests_file.data.save(path + 'tests_file' + ras)
        prob.tests_file = path + 'tests_file' + ras
        ###############################
        name = form.answers_file.data.filename
        ras = name[name.index('.'):]
        if not os.path.exists(path):
            os.makedirs(path)
        form.answers_file.data.save(path + 'answers_file' + ras)
        prob.answers_file = path + 'answers_file' + ras
        ###############################
        session.add(prob)
        session.commit()
        return redirect('/')
    return render_template('add_problem.html', title='Add problem', form=form)


@app.route('/add_contest', methods=['GET', 'POST'])
@login_required
def add_contest():
    update_solutions()
    if current_user.id != 1:
        abort(404)
    form = AddContestForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        problems = session.query(Problem).all()
        contest = Contest()
        contest.name = form.name.data
        contest.start_date = form.start_date.data
        contest.finish_date = form.finish_date.data
        pr = form.problems.data
        try:
            mass = list(map(int, pr.split(', ')))
        except Exception:
            return render_template('add_contest.html', title='Add contest', form=form,
                                   problems=problems, message='Problems id does not respect')
        for i in mass:
            prob = session.query(Problem).filter(Problem.id == i).first()
            if not prob:
                return render_template('add_contest.html', title='Add contest', form=form,
                                       problems=problems, message='Some of problems do not exist')
            contest.problems.append(prob)
        if form.start_date.data > form.finish_date.data:
            return render_template('add_contest.html', title='Add contest', form=form,
                                   problems=problems, message='Start date can not be later than finish')
        if form.start_date.data < datetime.datetime.now():
            return render_template('add_contest.html', title='Add contest', form=form,
                                   problems=problems, message='Start date can not be earlier than today')
        contest.start_date = form.start_date.data
        contest.finish_date = form.finish_date.data
        session.add(contest)
        session.commit()
        return redirect('/')
    session = db_session.create_session()
    problems = session.query(Problem).all()
    return render_template('add_contest.html', title='Add contest', form=form, problems=problems)


@app.route('/contest/<int:contest_id>')
@login_required
def get_contest(contest_id):
    update_solutions()
    session = db_session.create_session()
    contest = session.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        abort(404)
    if current_user.id != 1:
        now = datetime.datetime.now()
        if contest.start_date > now or contest.finish_date < now:
            abort(404)
    problems = contest.problems
    solutions = session.query(Solution).filter(Solution.user_id == current_user.id)
    problems_new = []
    for i in problems:
        now = [i, False]
        sol = solutions.filter(Solution.problem_id == i.id, Solution.status == "OK").first()
        if sol:
            now[1] = True
        problems_new.append(now)
    return render_template('contest.html', title="Contest", problems=problems_new,
                           contest=contest)


@app.route('/delete/contest/<int:contest_id>')
@login_required
def delete_contest(contest_id):
    update_solutions()
    session = db_session.create_session()
    contest = session.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        abort(404)
    if current_user.id != 1:
        abort(404)
    session.delete(contest)
    session.commit()
    return redirect('/')


@app.route('/contest/<int:contest_id>/problem/<int:problem_id>', methods=['GET', 'POST'])
@login_required
def problem_in_contest(contest_id, problem_id):
    update_solutions()
    session = db_session.create_session()
    contest = session.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        abort(404)
    problem = session.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        abort(404)
    if problem not in contest.problems:
        abort(404)
    form = ProblemForm()
    if form.validate_on_submit():
        solution = Solution()
        solution.user_id = current_user.id
        solution.status = "Running..."
        solution.problem_id = problem_id
        solution.time = datetime.datetime.now()
        path = os.getcwd() + '\\solutions'
        if not os.path.exists(path):
            os.makedirs(path)
        solution.solution_file = path + '\\solution' + str(solution.id) + '.cpp'
        session.add(solution)
        session.commit()
        form.solution_file.data.save(path + '\\solution' + str(solution.id) + '.cpp')
        params = str(solution.id) + ' ' + str(problem_id) + ' ' + problem.file_in + ' '
        params += problem.file_out + ' ' + str(problem.time_limit)
        cmd = 'start /b python ' + os.getcwd() + '\\testing.py ' + params
        os.system(cmd)
        return redirect('/contest/' + str(contest_id) + '/problem/' + str(problem_id))
    solutions = session.query(Solution).filter(Solution.user_id == current_user.id,
                                               Solution.problem_id == problem_id).all()
    solutions_sorted = sorted(solutions, key=lambda x: x.time, reverse=True)
    return render_template('problem_in_contest.html', title='Problem', form=form,
                           solutions=solutions_sorted, problem=problem, contest_id=contest_id)


@app.route('/download/problem/<int:problem_id>')
@login_required
def download_problem(problem_id):
    update_solutions()
    session = db_session.create_session()
    problem = session.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        abort(404)
    if current_user.id != 1:
        now = datetime.datetime.now()
        contests = session.query(Contest).filter(Contest.start_date <= now,
                                                 Contest.finish_date > now).all()
        ok = False
        for i in contests:
            if problem in i.problems:
                ok = True
                break
        if not ok:
            abort(404)
    point = problem.task_file[::-1].index('.')
    directory = os.getcwd() + '\\problems\\' + str(problem_id)
    file = 'task_file' + problem.task_file[len(problem.task_file) - point - 1:]
    return send_file(directory + '\\' + file, as_attachment=True)


@app.route('/download/solution/<int:solution_id>')
@login_required
def download_solution(solution_id):
    update_solutions()
    session = db_session.create_session()
    solution = session.query(Solution).filter(Solution.id == solution_id).first()
    if not solution:
        abort(404)
    if current_user.id != 1 and solution.user_id != current_user.id:
        abort(404)
    directory = os.getcwd() + '\\solutions'
    file = 'solution' + str(solution.id) + '.cpp'
    return send_file(directory + '\\' + file, as_attachment=True)


def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/ijudge_db")
    main()