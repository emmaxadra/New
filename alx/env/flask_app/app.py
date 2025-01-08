import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from flask import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'mail' in request.form and 'password' in request.form:
        # Create variables for easy access
        mail = request.form['mail']
        password = request.form['password']
        # Check if account exists using MySQL
     #   conn = get_db_connection()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM user1 WHERE mail = ? AND password = ?', (mail, password,))
        # Fetch one record and return result
        users = cur.fetchone()
        # If account exists in accounts table in out database

        if users:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['mail'] = users[1]

            # Redirect to home page
            return redirect(url_for('/'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/register/',methods=('GET','POST'))
#for new users
def register():
    if request.method ==  'POST':
        name = request.form['name']
        country = request.form['country']
        number = request.form['number']
        mail = request.form['mail']
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO user1 (name,country,number,mail, username,password) VALUES (?,?,?,?,?,?)',
                    (name, country, number, mail,username,password))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('create'))
    return render_template('register.html')

