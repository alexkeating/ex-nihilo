from app.auth import auth
from app.auth.views import RegisterAPI, LoginAPI, LogoutAPI


auth.add_url_rule('/auth/register/', view_func=RegisterAPI.as_view('register'))
auth.add_url_rule('/auth/login/', view_func=LoginAPI.as_view('login'))
auth.add_url_rule('/auth/logout/', view_func=LogoutAPI.as_view('logout'))

