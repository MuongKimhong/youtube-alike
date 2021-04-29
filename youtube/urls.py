from django.urls import path

from youtube.views import *

urlpatterns = [
    path('create-account/', CreateAccount.as_view()),
    path('api/user/token/', CustomTokenObtainPairView.as_view()),
    path('<int:id>/upload-video/', UploadVideo.as_view()),
    path('<int:user_id>/get-all-user-videos/', AllUserVideos.as_view()),
    path('<int:video_id>/video/', VideoDetail.as_view()),
    path('random-videos/', GetRandomVideos.as_view()),
    path('random-videos-based-on-users/<int:user_id>/', GetRandomVideosBaseOnUserViewed.as_view()),
    path('add-user-viewed-video/<int:user_id>/', AddUserViewedVideo.as_view()),
    path('add-user-viewed-videos/<int:user_id>/<int:video_id>/', AddUserViewedVideos.as_view()),
    path('view-count/<int:video_id>/', VideoViewCount.as_view()),
    path('get-related-videos/<int:video_id>/', GetRelatedVideos.as_view()),
    path('check-user-liked-or-disliked/<int:video_id>/<int:user_id>/', CheckIfUserLikedOrDislikedVideo.as_view()),
    path('like-video/<int:video_id>/<int:user_id>/', LikeVideo.as_view()),
    path('dislike-video/<int:video_id>/<int:user_id>/', DislikeVideo.as_view()),
    path('get-comments-authenticated/<int:video_id>/<int:user_id>/', GetVideoCommentsForAuthenticated.as_view()),
    path('get-comments-unauthenticated/<int:video_id>/', GetVideoCommentsForUnauthenticated.as_view()),
    path('send-comment/<int:video_id>/<int:user_id>/', SendVideoComment.as_view()),
    path('like-comment/<int:comment_id>/<int:user_id>/', LikeComment.as_view()),
    path('delete-video/<int:video_id>/<int:user_id>/', DeleteVideo.as_view()),
    path('delete-comment/<int:comment_id>/<int:user_id>/', DeleteComment.as_view()),
    path('edit-comment/<int:comment_id>/<int:user_id>/', EditComment.as_view()),
    path('search-autocomplete/', SearchAutoCompleteEngine.as_view()),
    path('get-search-results/', GetSearchResult.as_view()) ,
    path('get-notifications/<int:user_id>/', GetNotification.as_view()),
]