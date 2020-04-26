from django.contrib import admin
from django.urls import path

import web.views

urlpatterns = [
    path('authorize', web.views.authorize),
    path('oauth2callback', web.views.callback, "callback"),
    path('revoke', web.views.revoke),
    path('clear', web.views.clear),
    path('content', web.views.content, "content")
]
