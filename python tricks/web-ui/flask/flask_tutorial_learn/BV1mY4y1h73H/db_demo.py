from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


class Config(object):
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root_mysql@127.0.0.1:3306/db_python'
	SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)
app.app_context().push()  # 推送应用上下文环境 RuntimeError: Working outside of application,https://www.jianshu.com/p/b12290ba46c7
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = "test_users"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	email = db.Column(db.String(128), unique=True)
	password = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey("test_roles.id"))

class Role(db.Model):
	__tablename__ = 'test_roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	users = db.relationship('User',backref='role')


# @app.route("/")
# def index():
# 	return "index page"


if __name__ == '__main__':
	# app.run(debug=True)

	# db operation
	db.drop_all()  # setup only
	db.create_all()

	roles1 = Role(name='admin')
	db.session.add(roles1)
	db.session.commit()

	roles2 = Role(name='stuff')
	db.session.add(roles2)
	db.session.commit()

	us1 = User(name='a',email='a@123.com', password='a', role_id = roles1.id)
	us2 = User(name='b',email='b@123.com', password='b', role_id = roles2.id)
	us3 = User(name='c',email='c@123.com', password='c', role_id = roles2.id)
	us4 = User(name='d',email='d@123.com', password='d', role_id = roles1.id)

	db.session.add_all([us1,us2,us3, us4])
	db.session.commit()
