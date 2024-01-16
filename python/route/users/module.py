from python.handler.users.module import create_user_handler, list_users_handler, \
    get_user_handler, delete_user_handler, login_user_handler


def register_user_routes(app):
    app.add_url_rule("/users", methods=["POST"], view_func=create_user_handler)
    app.add_url_rule("/users", methods=["GET"], view_func=list_users_handler)
    app.add_url_rule("/users/<key>", methods=["GET"], view_func=get_user_handler)
    app.add_url_rule("/users/<key>", methods=["DELETE"], view_func=delete_user_handler)
    app.add_url_rule("/users/login", methods=["POST"], view_func=login_user_handler)
