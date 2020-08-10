# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 16:30:50 2020

@author: Yury
"""


from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    re_path(r'bloggers/$', views.BloggerListView.as_view(), name='bloggers'),
    # re_path(r'posts/(?P<pk>/d+)$',
    # views.PostDetailView.as_view(), 'post-detail'),
    re_path(r'posts/(?P<pk>\d+)$',
            views.post_with_comment_form, name='post-detail'),
    re_path(r'bloggers/(?P<pk>\d+)$',
            views.BloggerDetailView.as_view(), name='blogger-detail'),
    re_path(r'^bloggers/(?P<pk>\d+)/update/$',
            views.BloggerUpdate.as_view(), name='blogger-update'),
    re_path(r'^bloggers/(?P<pk>\d+)/delete/$',
            views.BloggerDelete.as_view(), name='blogger-delete'),
    re_path(r'^posts/create/$',
            views.PostCreate.as_view(), name='post-create'),
    re_path(r'^posts/(?P<pk>\d+)/update/$',
            views.PostUpdate.as_view(), name='post-update'),
    re_path(r'^posts/(?P<pk>\d+)/delete/$',
            views.PostDelete.as_view(), name='post-delete'),
    ]
