from django.urls import path
from miniblog import views
from rest_framework import renderers
from miniblog.views import MiniBlogViewSet, UserViewSet, api_root

mb_list = MiniBlogViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

mb_detail = MiniBlogViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

mb_highlight = MiniBlogViewSet.as_view({
    'get': 'highlight'
}, 
renderer_classes=[renderers.StaticHTMLRenderer]
)

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns1 = [
    path('', views.api_root),
    path('blogs/<int:pk>/highlight/',  mb_list,     name='miniblog-highlight'),
    path('blogs/',                     mb_detail,   name="miniblog-list"),
    path('blogs/<int:pk>/',            mb_highlight,name="miniblog-detail"),
    path('users/',                     user_list,   name="users-list"),
    path('users/<int:pk>/',            user_detail, name="users-list"),

]


from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns1)


"""
urlpatterns = [
    path('blogs/', views.miniblog_list_csrf),
    path('blogs2/', views.list_decorator),
    path('blogs3/', views.MiniBlogListAPIView.as_view()),
    path('blogs4/', views.MiniBlogListMixins.as_view()),

    path('blog/<int:pk>/', views.miniblog_detail_csrf),
    path('blog2/<int:pk>/', views.detail_decorator),
    path('blog3/<int:pk>/', views.MiniBlogDetailAPIView.as_view()),
    path('blog4/<int:pk>/', views.MiniBlogDetailMixins.as_view()),
]
-----------------------------------
    path('', views.api_root),
    path('snippets/',
        views.SnippetList.as_view(),
        name='snippet-list'),
    path('snippets/<int:pk>/',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    path('snippets/<int:pk>/highlight/',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    path('users/',
        views.UserList.as_view(),
        name='user-list'),
    path('users/<int:pk>/',
        views.UserDetail.as_view(),
        name='user-detail')
"""