from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo
import secrets
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SECRET_KEY']='9677dd2480e303794412b5be0961124d'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)


class Faculty(db.Model):
	f_id=db.Column(db.Integer,primary_key=True)
	f_name=db.Column(db.String(50),nullable=False)

class Student(db.Model):
	s_id=db.Column(db.Integer,primary_key=True)
	s_name=db.Column(db.String(50),nullable=False)
	s_branch=db.Column(db.String(10),nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)


class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('New Course')

@app.route("/newcourse", methods=['GET', 'POST'])
def newcourse():
    form = CourseForm()
    if form.validate_on_submit():
        c1 = Course(name=form.name.data, content=form.content.data)
        db.session.add(c1)
        db.session.commit()
        flash('Course has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('newcourse.html', title='New Course',form=form)





faculties=[
	{'id':'6286','name':'Dr. Murali Mohan'},
	{'id':'1111','name':'N Rajesh'},
	{'id':'2222','name':'Banerjee'}
]

students_klu=[
	{'id':'31755','name':'V Srinivas'},
	{'id':'30656','name':'K Jithu'},
	{'id':'31240','name':'P Gyan Sai'},
	{'id':'31440','name':'R Sai Kiran'}
]

@app.route("/")
@app.route("/home")
def home():
	courses = Course.query.all()
	return render_template('home.html', courses=courses)
	return render_template('home.html',title="HOME")

@app.route("/cse")
def cse():
	return render_template('cse.html',title="CSE",faculty=faculties,students=students_klu)

@app.route("/ece")
def ece():
	return render_template('ece.html',title="ECE")

@app.route("/faculty")
def faculty():
	fall=Faculty.query.all()
	return render_template('faculty.html',title="FACULTY",faculties=fall)

@app.route("/students")
def students():
	sall=Student.query.all()
	return render_template('students.html',title="STUDENTS",students=sall)

if __name__ == '__main__':
	app.run(debug=True)


