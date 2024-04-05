from django.urls import path
from .views import user_signup, user_login, search_users, send_friend_request, accept_friend_request, reject_friend_request, list_friends, list_pending_friend_requests

urlpatterns = [
    path('signup/', user_signup),
    path('login/', user_login),
    path('search/', search_users),
    path('send-friend-request/', send_friend_request),
    path('accept-friend-request/', accept_friend_request),
    path('reject-friend-request/', reject_friend_request),
    path('list-friends/', list_friends),
    path('list-pending-requests/', list_pending_friend_requests),
]
