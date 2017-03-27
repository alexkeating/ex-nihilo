from app import restful_api
from app.user.views import User

restful_api.add_resource(User, '/user/<string:todo_id>/', '/user/')