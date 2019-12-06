from flask import request, jsonify, Blueprint
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from datetime import datetime

from core.models import User, Blog

core_module = Blueprint('core_module', __name__)


def success_response(data):
    response = {
        'status': True,
        'status_code': 200,
        'data': data,
        'error': None
    }
    return response


def failure_response(status_code, error):
    response = {
        'status': False,
        'status_code': status_code,
        'data': None,
        'error': error
    }
    return response


@core_module.route('/user/login/', methods=['POST'])
def user_login(create_new=False):
    data = request.get_json()
    if create_new is True:
        username = data.get('username')
        password = data.get('password')
        user_group = data.get('user_group')
        if user_group not in ['admin', 'staff']:
            user_group = 'staff'
        user = User.add_user(username, password, user_group)
        response = success_response({'user_created': True, '_id': user.id})
        return jsonify(response)
    else:
        username = data.get('username')
        password = data.get('password')

        user = User.objects(name=username).first()
        if user is None:
            response = failure_response(400, 'username not found')
            return jsonify(response)
        else:
            if check_password_hash(user.password, password) is True:
                login_user(user)
                response = success_response({'login': 'success', 'name': user.name, '_id': user.id})
                return jsonify(response)


@core_module.route('/user/logout/')
def logout():
    logout_user()
    response = success_response({'logged_out': True})
    return jsonify(response)


class BlogView(MethodView):
    decorators = [login_required]

    def __init__(self):
        self.user_is_admin = User.check_admin_rights()

    def get(self, blog_id=None):
        limit = request.args.get('limit', 0)
        if blog_id is None:
            blogs = []
            for blog in Blog.objects.order_by('created_date')[int(limit)]:
                obj = {
                    'id': blog.id,
                    'name': blog.name,
                    'createdAt': blog.created_date.timestamp()
                }
                blogs.append(obj)
        else:
            blog = Blog.objects(_id=blog_id).first()
            if blog is None:
                response = failure_response(404, 'Blog does not exist')
            else:
                obj = {
                    'name': blog.name,
                    'content': blog.content,
                    'createdAt': blog.created_date
                }
                response = success_response({'blog': obj})
            return jsonify(response)

    def post(self):
        data = request.get_json()
        if self.user_is_admin is False:
            response = failure_response(401, 'Unauthenticated requests')
            return jsonify(response)
        name = data.get('name')
        content = data.get('content')
        if name or content is None:
            response = failure_response(400, 'Missing required fields')
            return jsonify(response)
        elif name.isalpha() is False or content.isalpha() is False:
            response = failure_response(400, 'Non string values are not accepted')
            return jsonify(response)
        blog = Blog(name=name, content=content, posted_user=current_user)
        blog.save()
        response = success_response({'blog_id': blog.id})
        return jsonify(response)

    def put(self, blog_id):
        if self.user_is_admin is False:
            response = failure_response(401, 'Unauthenticated requests')
            return jsonify(response)
        data = request.get_json()
        name = data.get('name')
        content = data.get('content')
        blog = Blog.objects(_id=blog_id).first()
        if blog is None:
            response = failure_response(400, 'Invalid requests')
            return jsonify(response)
        blog.name = name
        blog.content = content
        blog.updated_date = datetime.now()
        blog.save()

    def delete(self, blog_id):
        if self.user_is_admin is False:
            response = failure_response(401, 'Unauthenticated requests')
            return jsonify(response)
        blog = Blog.objects(_id=blog_id).first()
        if blog is not None:
            blog.delete()
        response = success_response({'deleted': True})
        return jsonify(response)
