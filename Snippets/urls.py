"""Snippets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from MainApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_page, name='home'),
    #path('accounts/login/', views.index_page, name='home'),
    #path('snippets/add', views.add_snippet_page, name='add_snippet'),
    path('snippets/add', views.add_snippet_page, name='add_snippet'),
    path('comment/add', views.comment_add, name='add_comment'),
    path('comment/view_all', views.comments_view_all, name='view_comments'),
    path('comment/delete/<int:id>', views.comment_delete, name='comment_delete'),
    path('snippets/list', views.snippets_page, name='list_snippet'),
    path('snippets/list_my', views.snippets_page_my, name='list_snippet_my'),
    path('snippets/list_privat', views.snippets_page_privat, name='list_snippet_privat'),
    path('snippets/view_one_snippet/<int:id>', views.snippet_view, name='view_one_snippet'),
    path('snippets/test_page', views.test_page, name='test'),
    path('snippets/delete/<int:id>', views.snippet_delete, name='delete'),
    path('snippets/edit/<int:id>', views.snippet_edit, name='edit_snippet'),
    path('auth/login', views.login_page, name='login'),
    path('auth/add_user', views.create_user, name='add_user'),
    path('auth/logout', views.logout_page, name='logout'),
    path('tarifs/add', views.add_new_tarif , name='add_tarif'),
    path('tarifs/view_all', views.tarif_page , name='view_tarif'),
    path('account/view_account/<int:id>', views.account_view , name='view_account'),
    path('users/view_users', views.users_view_all, name='users_view_all'),
    path('account/account_add_cred', views.account_add_cred, name='add_cred'),
    path('account/account_add_deb', views.account_add_deb, name='add_deb'),
    path('account/view_one_account/<int:id>', views.view_one_account, name='view_one_account'),
    path('account/account_delete/<int:id>', views.account_delete, name='account_delete'),
    path('account/account_view_personal', views.account_view_personal, name='account_personal'),
    path('account/add_elektro', views.add_elektro_page, name='add_elektro'),
    path('account/view_elektro_all', views.elektro_view_all, name='elektro_view_all'),
    path('account/elektro_delete/<int:id>', views.elektro_delete, name='elektro_delete'),
    path('account/add_total_payment', views.add_total_account, name='add_total_payment'),
    path('account/ballance_view', views.ballance_view, name='ballance_view'),
    path('account/account_edit/<int:id>', views.account_edit, name='account_edit'),
    path('account/account_create', views.account_add, name='account_create'),

    path('admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)

