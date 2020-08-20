from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("items/<int:itemID>", views.items, name="items"),
    path("new", views.new, name="new"),
    path("watch", views.watch, name="watch"),
    path("category", views.categories, name="categories"),
    path("category/<str:categoryName>", views.category, name="category"),
    path("accounts/login/", views.loginRequired)
]
