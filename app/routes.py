from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import logout_user, login_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, apm, elasticapm
from app.forms import LoginForm, ContactForm, CommentForm, SearchForm
from app.models import User, Post, Comment, Tag, blog_tag
from app.helpers import send_email
from app import cache
import flask_featureflags as feature



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        if feature.is_active_feature('apm_feature'):
            elasticapm.set_user_context(user_id=current_user.id,username=current_user.username,email=current_user.email)
    else:
        if feature.is_active_feature('apm_feature'):
            elasticapm.set_user_context(username='Anonymous')
    g.search_form = SearchForm()


@feature.is_active_feature('search_feature')
@app.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                            app.config['POSTS_PER_PAGE'])
    next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
        if total > page * app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=('Search'), posts=posts,
                        next_url=next_url, prev_url=prev_url)

@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def index():
    latest_post = Post.query.order_by(Post.timestamp.desc()).first()
    contactform = ContactForm()
    #emailsubscribeform = EmailSubscribeForm()
    if contactform.validate_on_submit():
        text_body = "{} said {}".format(contactform.contactemail.data, contactform.comment.data)
        send_email('New Contact!', contactform.contactemail.data, app.config['ADMINS'], text_body, text_body)
        flash('Thanks for reaching out!')
        #subscribe_commentor(contactform.contactemail.data, client)
        return redirect(url_for('index'))
    # if emailsubscribeform.validate_on_submit():
    #     #subscribe_user(emailsubscribeform.email.data, client)
    #     return redirect(url_for('index'))
    return render_template('index.html', title='Home', contactform=contactform, latest_post=latest_post)



@app.route('/blog')
@cache.cached(timeout=50)
def blog():
    all_tags = Tag.query.order_by(Tag.count.desc()).all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    page_first = url_for('blog', page=1)
    page_last = url_for('blog', page=posts.pages)
    next_url = url_for('blog', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('blog', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("blog.html", title='Blog', posts=posts.items,
                          next_url=next_url, prev_url=prev_url, tags=all_tags, page_first=page_first, page_last=page_last)


@app.route('/posts/<int:id>', methods=['GET','POST'])
@cache.cached(timeout=50)
def display(id):
    all_tags = Tag.query.order_by(Tag.count.desc()).all()
    data = Post.query.filter_by(id=id).first_or_404()
    try:
        comments = Comment.query.filter_by(post_id=id)
        tags = data.tags
        comment_count = 0
        for c in comments:
            comment_count += 1
    except:
        pass
    commentform = CommentForm()
    if commentform.validate_on_submit():
        comment = Comment(name=commentform.name.data, email=commentform.email.data, comment=commentform.comment.data, review=data)
        db.session.add(comment)
        db.session.commit()
        flash('Comment updated!')
        #subscribe_commentor(commentform.email.data, client)
        return redirect('/posts/{}'.format(id))
    return render_template('posts.html', data=data, commentform=commentform, comment_count = int(comment_count), comments=comments, tags=tags, all_tags=all_tags)

@app.route('/categories/<string:name>', methods=['GET'])
@cache.cached(timeout=50)
def posts_by_tag(name):
    all_tags = Tag.query.order_by(Tag.count.desc()).all()
    category = Tag.query.filter_by(name=name).first()
    flash('Showing all posts tagged with {}'.format(category.name))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.tags.contains(category)).order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    page_first = url_for('blog', page=1)
    page_last = url_for('blog', page=posts.pages)
    next_url = url_for('blog', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('blog', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("categories.html", title='Categories', posts=posts.items,
                          next_url=next_url, prev_url=prev_url, tags=all_tags, page_first=page_first, page_last=page_last, request=request)



@app.route('/blog_editor', methods=['GET', 'POST'])
def blog_editor():
    if request.method == 'POST':
        tag_string = request.form.get('tagdata')
        tags = tag_string.split(",")
        new_data = Post(body=request.form.get('editordata'), author=current_user, description=request.form.get('descriptiondata'), title=request.form.get('titledata'))
        for tag in tags:
            post_tag = add_tags(tag)
            new_data.tags.append(post_tag)
        db.session.add(new_data)
        all_tags = Tag.query.all()
        for tag in all_tags:
            count = len(tag.posts)
            tag.count = count
            db.session.add(tag)
        db.session.commit()
    return render_template('blog_editor.html', title='Blog Editor')

def add_tags(tag):
    existing_tag = Tag.query.filter(Tag.name == tag.lower()).one_or_none()
    if existing_tag is not None:
        return existing_tag
    else:
       new_tag = Tag()
       new_tag.name = tag.lower()
       return new_tag

@app.route('/login', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user is None or not user.check_password(loginform.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=loginform.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', loginform=loginform)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def add_tags(tag):
    existing_tag = Tag.query.filter(Tag.name == tag.lower()).one_or_none()
    if existing_tag is not None:
        return existing_tag
    else:
       new_tag = Tag()
       new_tag.name = tag.lower()
       clean_whitespace = str(new_tag.name).replace(' ','')
       new_tag.name = clean_whitespace
       return new_tag

