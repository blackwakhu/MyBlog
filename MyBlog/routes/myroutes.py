from flask import Blueprint, render_template, redirect, flash, url_for
from MyBlog.extension import mongo
from MyBlog.forms.myforms import Form1
from bson.objectid import ObjectId
from datetime import datetime

blog = Blueprint("blog", __name__)


@blog.route('/')
def home():
    blogger = mongo.db.myFlaskBlog
    blogs = blogger.find()
    return render_template("blogs/home.html", blogs=blogs)


@blog.route('/detail/<blog_id>')
def detail(blog_id):
    blogger = mongo.db.myFlaskBlog
    my_blog = blogger.find_one({"_id": ObjectId(blog_id)})
    view = my_blog["views"] + 1
    blogger.update_one({"_id": ObjectId(blog_id)}, {"$set": {"views": view}})
    myblog = blogger.find_one({"_id": ObjectId(blog_id)})
    print(myblog)
    return render_template("blogs/detail.html", myblog=myblog)


@blog.route('/like/<blog_id>')
def like(blog_id):
    blogger = mongo.db.myFlaskBlog
    my_blog = blogger.find_one({"_id": ObjectId(blog_id)})
    likes = my_blog["like"] + 1
    blogger.update_one({"_id": ObjectId(blog_id)}, {"$set": {"like": likes}})
    return redirect(url_for('blog.home'))


@blog.route('/dislike/<blog_id>')
def dislike(blog_id):
    blogger = mongo.db.myFlaskBlog
    my_blog = blogger.find_one({"_id": ObjectId(blog_id)})
    dislikes = my_blog["dislike"] + 1
    blogger.update_one({"_id": ObjectId(blog_id)}, {"$set": {"dislike": dislikes}})
    return redirect(url_for('blog.home'))


@blog.route('/delete/<blog_id>')
def delete(blog_id):
    blogger = mongo.db.myFlaskBlog
    blogger.delete_one({"_id": ObjectId(blog_id)})
    return redirect("/")


@blog.route('/add', methods=["post", "get"])
def add():
    form = Form1()
    blogger = mongo.db.myFlaskBlog
    if form.validate_on_submit():
        my_dict = {
            "author": form.author.data,
            "title": form.title.data,
            "content": form.content.data,
            "email": form.email.data,
            "date": datetime.utcnow(),
            "views": 0,
            "like": 0,
            "dislike": 0,
            "passwd": form.passwd.data,
            "username": form.username.data,
            "security question": form.security_question.data,
            "answer": form.answer.data,
            "subject": form.subject.data,
        }
        blogger.insert_one(my_dict)
        print(my_dict)
        flash("saved", 201)
        return redirect('/')
    return render_template("blogs/create.html", form=form)


@blog.route('/author')
def author():
    blogger = mongo.db.myFlaskBlog
    blogs = blogger.find()
    authors = list()
    for i in blogs:
        authors.append({"name": i['author'], "username": i["username"], "email": i["email"]})
    return render_template("blogs/author.html", authors=authors)


@blog.route('/author works/<author_name>')
def author_works(author_name):
    blogger = mongo.db.myFlaskBlog
    names = blogger.find()
    data = list()
    subject_matter = list()
    for name in names:
        data.append(
            {
                "_id": name['_id'],
                "author": name['author'],
                "title": name['title'],
                "content": name['content'],
                "subject": name['subject'],
             })
    for i in data:
        if author_name == i['author']:
            subject_matter.append(i)
    return render_template("blogs/author_works.html", subject_matter=subject_matter, author_name=author_name)


@blog.route('/subject works/<subject_title>')
def subject_works(subject_title):
    blogger = mongo.db.myFlaskBlog
    names = blogger.find()
    data = list()
    subject_matter = list()
    for name in names:
        data.append(
            {
                "_id": name['_id'],
                "author": name['author'],
                "title": name['title'],
                "content": name['content'],
                "subject": name['subject'],
             })
    for i in data:
        if subject_title == i['subject']:
            subject_matter.append(i)
    return render_template("blogs/subject_works.html", subject_matter=subject_matter, subject_title=subject_title)


@blog.route('/subject')
def subject():
    blogger = mongo.db.myFlaskBlog
    blogs = blogger.find()
    subjects = list()
    for i in blogs:
        subjects.append(i['subject'])
    subjects = list(set(subjects))
    return render_template("blogs/subject.html", subjects=subjects)


@blog.route('/about')
def about():
    return render_template("about.html")


@blog.errorhandler(404)
def page_not_found(e):
    return e, 404
