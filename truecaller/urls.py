from django.urls import path

from truecaller.views import (LoginView, LogoutView, ContactListView, ProfileListView, 
RegisterView, UserlistView,SpamMarkedView,SearchName,SearchPhoneNumber)

urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('register', RegisterView.as_view()),
    path('user', UserlistView.as_view()),
    path('user/<int:pk>', UserlistView.as_view()),
    path('contact', ContactListView.as_view()),
    path('profile', ProfileListView.as_view()),
    # queries

    path('spam_marked', SpamMarkedView.as_view()),
    path('search_by_name', SearchName.as_view()),
    path('search_by_phone_number', SearchPhoneNumber.as_view()),
    

]