from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name= "minilibrary"),
    path('recomendar/<int:book_id>', views.add_review, name= "recommend_book"),
    path('hello', views.Hello.as_view(), name="hello_cbv"),
    path('welcome/', views.WelcomeView.as_view(), name="welcome"),
    path('books/', views.BookListView.as_view(), name="book_list")
]
