from flask import Flask,render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  DataRequired

app = Flask(__name__)


class Config(object):
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root_mysql@127.0.0.1:3306/author_book'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = 'djdjdjdjoijsojoi'


app.config.from_object(Config)
# app.app_context().push()  # uncomment when not use app
# 推送应用上下文环境 RuntimeError: Working outside of application,https://www.jianshu.com/p/b12290ba46c7
db = SQLAlchemy(app)


class Author(db.Model):
	__tablename__ = "test_author"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	books = db.relationship("Book", backref='author')

class Book(db.Model):
	__tablename__ = "test_book"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	author_id = db.Column(db.Integer, db.ForeignKey('test_author.id'))


class AuthorBookForm(FlaskForm):
	author_name = StringField(label='author',validators=[DataRequired("required")])
	book_name = StringField(label='book',validators=[DataRequired("required")])
	submit = SubmitField(label='submit')


@app.route("/", methods=['GET','POST'])
def index():
	form = AuthorBookForm()
	if form.validate_on_submit():
		author_name = form.author_name.data
		book_name = form.book_name.data
		author = Author(name=author_name)
		db.session.add(author)
		db.session.commit()
		# book = Book(name=book_name, author_id = author.id)
		book = Book(name=book_name, author=author)  # alternative way
		db.session.add(book)
		db.session.commit()
	author_li = Author.query.all()
	return render_template('author_book.html',authors=author_li, form=form)


@app.route("/delete_book", methods=['POST'])
def delete_book():
	req_dict = request.get_json()
	book_id = req_dict.get('book_id')
	book = Book.query.get(book_id)
	db.session.delete(book)
	db.session.commit()
	# return redirect(url_for("index"))
	return jsonify(code=0, message='OK')


if __name__ == '__main__':
	# init test data
	# db.drop_all()
	# db.create_all()
	# au1 = Author(name='刘慈欣')
	# au2 = Author(name='吴承恩')
	# au3 = Author(name='曹雪芹')
	# db.session.add_all(([au1,au2,au3]))
	# db.session.commit()
	# bk1 = Book(name='三体1',author_id=au1.id)
	# bk2 = Book(name='三体2',author_id=au1.id)
	# bk3 = Book(name='三体3',author_id=au1.id)
	# db.session.add_all(([bk1,bk2,bk3]))
	# db.session.commit()
	app.run(debug=True)
