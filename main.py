from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    id = request.query_string
    if request.method == 'GET':
        if not id:
            return render_template('blog.html', blogs=blogs)
        else:
            b = int(request.args.get('b'))
            blog = Blog.query.get(b)
            return render_template('singleposting.html', blog=blog)

@app.route('/newpost')
def newpost():
    return render_template('newposting.html')

@app.route('/newpost', methods=['POST'])
def add_post():
    title = request.form['title']
    body = request.form['body']

    if not title and not body:
        return render_template('newposting.html', 
                                title_error='Please enter a title', 
                                body_error='Please enter your blog')

    elif not title:
        return render_template('newposting.html', 
                                title_error='Please enter a title', body=body)
    
    elif not body:
        return render_template('newposting.html', title=title, 
                                body_error='Please enter your blog')
        
    else:
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()

        blog = Blog.query.get(new_post.id)
        return render_template('singleposting.html', blog=blog)
        
@app.route("/")
def index():
    return redirect("/blog")
    
if __name__ == '__main__':
    app.run() 
