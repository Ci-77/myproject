
from . import views
from django.urls import include, path
from myapp.modules.login.urls import urls as login_urls
from myapp.modules.article.urls import urls as article_urls

urlpatterns = [
    path('login_module/',include(login_urls)),
    path('article_module/',include(article_urls))
]