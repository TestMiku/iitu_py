from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from main import views

urlpatterns = [
    path("OneSignalSDKWorker.js", views.OneSignalSDKWorker, name="OneSignalSDKWorker"),
    
    path("", RedirectView.as_view(url=reverse_lazy("chapters")), name="home"),

    path("chapters/search", views.SearchChaptersListView.as_view(), name="search1"),
    path("chapters", views.ChaptersTemplateView.as_view(), name="chapters"),
    path(
        "groups/<int:pk>/chapters",
        views.ChaptersTemplateView.as_view(),
        name="chapters_with_parent",
    ),
    path(
        "groups/create",
        views.ChapterGroupCreateView.as_view(),
        name="create_chapter_group",
    ),
    path('profile_view', views.profile_view, name='profile_view'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/send_notifications_to_email/0', views.send_notifications_to_email_1, name='send_notifications_to_email_1'),
    path('profile/send_notifications_to_email/1', views.send_notifications_to_email_0, name='send_notifications_to_email_0'),

    # path('profile/<str:email>', views.profile, name='profile'),
]
