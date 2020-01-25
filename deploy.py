from flask import *
from flask_sqlalchemy import *
from flask_login import login_required, logout_user, current_user, login_user, UserMixin, current_user
from datetime import datetime
from werkzeug.security import *
from sqlalchemy import *
from passlib.hash import sha256_crypt
from pytz import timezone
from flask_login import LoginManager

format = "%d-%m-%Y"
now_utc = datetime.now(timezone('UTC'))

''' 
Got an idea t    def __init__(self, username, password):
        self.username = username
        self.password = password
o make a website to share whats going on woth everyone on their day and admin can delete all posts but the user can only delete his posts
'''

app = Flask(__name__, static_folder='./static') 
app.secret_key = "Amitp@ndey123121"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
login_manager = LoginManager()
login_manager.init_app(app)
db=SQLAlchemy(app)

class blogposts(db.Model):
    __tablename__="Post"
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    content=db.Column(db.Text, nullable=False)
    author=db.Column(db.String, nullable=False, default="N/A")
    date=db.Column(db.String, nullable=False, default=now_utc.strftime(format))

    def __repr__(self):
        return "Blog Post " + str(self.id)


class login(db.Model, UserMixin):
    __tablename__="Login"
    id=db.Column(db.Integer, primary_key=True)
    firstname=db.Column(db.String, nullable=True)
    lastname=db.Column(db.String, nullable=True)
    password=db.Column(db.String, nullable=True)
    username=db.Column(db.String, nullable=False)
    gender=db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)



'''
#code when i start to wok on login and signup

class login(db.Model):
    username=db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False)
    name=db.Column(db.String, nullable=False)

    def __repr__(self):
        return "Login " + str(self.id)
'''

#INDEX
@app.route('/')
@login_required
def index():
    return redirect(url_for('login1'))

#POST REATION AND DISPLAY
@app.route('/posts', methods=["GET", "POST"])
@login_required
def posts():

    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = blogposts(title=post_title, content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_post = blogposts.query.all()
        return render_template('posts.html', posts=all_post) 

@app.route('/posts/new', methods=["GET", "POST"])
@login_required
def new_post():

    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = blogposts(title=post_title, content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_post = blogposts.query.all()
        return render_template('new_post.html', posts=all_post)

'''
#POST DELETING
@app.route("/posts/delete/<int:id>")
def delete_post(id):
    post = blogposts.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")

'''
'''#POST EDITING
@app.route('/posts/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    post = blogposts.query.get(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("edit.html", post=post)
        '''

#Register Part

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        first = request.form["first"]
        last = request.form["last"]
        username = request.form["username"]
        gender = request.form["gen"]
        password = request.form["pass1"]
        confirm = request.form["pass2"]
        existing_user = login.query.filter_by(username=username).first()
        if existing_user is None:
            if password == confirm:
                user=login(firstname=first, lastname=last, password=password, username=username, gender=gender)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('login1'))

            return render_template("register.html")
    return render_template("register.html")


@app.route("/login",methods=['GET','POST'])
def login1():
    if current_user.is_authenticated:
        return redirect(url_for('posts'))
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        pass_check = str(login.query.filter_by(username=username).first().password)
        user = login.query.filter_by(username=username).first()
        if user:
            if pass_check == password:
                login_user(user)
                next = request.args.get('next')
                return redirect(next or url_for('index'))
        flash('Invalid username/password combination')
        return redirect(url_for('login1')) 
    return render_template("login.html")     

@app.route("/logout")
@login_required
def logout_page():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('login1'))

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return login.query.get(user_id)
    return None    

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('login1'))
'''
@app.route("/home/<string:name>/post/<int:id>")
def hell(name ,id):
    return "Hello ,"+ name +", Your post id is : "+str(id)

@app.route('/only_get',methods=["POST"])

def get_only():
    return "You ccan only get this page"
'''

if __name__ == "__main__":
    app.run(debug=True)
