from django.contrib import admin
from django.urls import path

import web.views

urlpatterns = [
    path('authorize', web.views.authorize, name="authorize"),
    path('oauth2callback', web.views.callback, name="callback"),
    path('revoke', web.views.revoke, name="revoke"),
    path('clear', web.views.clear, name="clear"),
    path('content', web.views.content, name="content")
]
