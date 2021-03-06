"""tobystombola URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from tombola import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomePage, name="home_page"),
    path("tombolas/new", views.NewTombola, name="new_tombola"),
    path("tombolas/<int:game_id>/", views.ViewTombola, name="view_tombola"),
    path(
        "tombolas/<int:game_id>/inprogress/",
        views.TombolaInProgress,
        name="tombola_in_progress",
    ),
    path(
        "tombolas/<int:game_id>/finished/",
        views.TombolaFinished,
        name="tombola_finished",
    ),
    path("tombolas/<int:game_id>/buy/", views.BuyTicket, name="buy_ticket"),
    path("tombolas/", views.HomePage),
    path(
        "api/tombolas/<int:game_id>/buy/",
        views.ApiBuyTicket,
        name="api_buy_ticket",
    ),
]
