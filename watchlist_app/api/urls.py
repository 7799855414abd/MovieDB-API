# # urls.py
from django.urls import path
from watchlist_app.api.views import MovieList, UserReviewDetail, ReviewCreate, ReviewList, ReviewDetail, StreamPlatformAV, StreamPlatformDetailAV, WatchListAV, WatchListDetailAV

urlpatterns = [
    path('movie_list/', WatchListAV.as_view(), name='watchlist-list'),
    path('movie_list/<int:pk>/', WatchListDetailAV.as_view(), name='watchlist-detail'),
    path('stream/', StreamPlatformAV.as_view(), name='streamplatform-list'),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-list-create'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('reviews/', UserReviewDetail.as_view(), name='review-detail'),
    path('ml/', MovieList.as_view(), name='movie-list'),
]







# from django.urls import path
# from watchlist_app.api.views import ReviewList, ReviewDetail, StreamPlatformAV, StreamPlatformDetailAV, WatchListAV, WatchListDetailAV, ReviewList
#
# urlpatterns = [
#     path('list/', WatchListAV.as_view(), name='watchlist-list'),
#     path('list/<int:pk>/', WatchListDetailAV.as_view(), name='watchlist-detail'),
#     path('stream/', StreamPlatformAV.as_view(), name='streamplatform-list'),
#     path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
#     # path('review/', ReviewList.as_view(), name ='review-list'),
#     # path('review/<int:pk>/', ReviewDetail.as_view(), name ='review-detail'),
#     path('stream/<int:pk>/review/', ReviewList.as_view(), name ='review-list'),
#     path('stream/review/<int:pk>/', ReviewDetail.as_view(), name ='review-detail')
#
# ]
#








# from django.urls import path
# # from watchlist_app.api.views import movie_list, movie_details
# from watchlist_app.api.views import StreamPlatformDetailAV, StreamPlatformAV,WatchListAV, WatchListDetailAV
#
#
# urlpatterns = [
#     path('list/', WatchListAV.as_view(), name='movie_list'),
#     path('list/<int:pk>/',WatchListDetailAV.as_view(), name='movie_detail'),
#     path('stream/', StreamPlatformAV.as_view(), name='stream_list'),
#     path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream_detail'),
# ]
#


# urlpatterns = [
#     path('list/', movie_list, name='movie_list'),
#     path('list/<int:pk>/', movie_details, name='movie_detail'),
# ]
