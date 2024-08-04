from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class UserReviewDetail(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)




    # def get_queryset(self):
    #     username=self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')  # Get the primary key from the URL
        try:
            watchlist = WatchList.objects.get(pk=pk)  # Retrieve the WatchList object
        except WatchList.DoesNotExist:
            raise ValidationError("The watchlist item does not exist.")

        review_user = self.request.user  # Get the user making the request

        # Check if the user has already reviewed this watchlist item
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watchlist item.")

        # Update the average rating
        rating = serializer.validated_data['rating']
        if watchlist.number_rating == 0:
            watchlist.avg_rating = rating
        else:
            watchlist.avg_rating = (watchlist.avg_rating * watchlist.number_rating + rating) / (watchlist.number_rating + 1)

        watchlist.number_rating += 1
        watchlist.save()  # Save the watchlist changes

        # Save the review with the associated watchlist and user
        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['review_user__username', 'active']
    filter_backends = [filters.SearchFilter]
    search_fields = ['active']



    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    def get(self,request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True, context = {'request':request})
        return Response(serializer.data)

    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error)

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'msg':'This data doesnot exist'},status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform,context = {'request':request})
        return Response(serializer.data)

    def put(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'msg':'This data doesnot exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'msg':'This data doesnot exist'}, status=status.HTTP_404_NOT_FOUND)
        platform.delete()
        return Response({'msg':'The User deleted from db successfully'}, status=status.HTTP_204_NO_CONTENT)






class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        watchlist = WatchList.objects.all()  # Corrected to use WatchList model
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchListDetailAV(APIView):  # Renamed to be consistent with WatchList model
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)  # Corrected to use WatchList model
        except WatchList.DoesNotExist:
            return Response({'error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)  # Corrected to use WatchList model
        except WatchList.DoesNotExist:
            return Response({'error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)  # Corrected to use WatchList model
        except WatchList.DoesNotExist:
            return Response({'error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)

        watchlist.delete()
        return Response({'msg': 'Item Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)



class MovieList(generics.ListAPIView):
    serializer_class = WatchListSerializer
    queryset = WatchList.objects.all()
    # filter_backends = [filters.SearchFilter]
    filter_backends = [filters.OrderingFilter]
    search_fields = ['avg_rating']
    # search_fields = ['^title', 'platform__name']


# class MovieList(generics.ListAPIView):
#     serializer_class = WatchListSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['title', 'platform_name']
#
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return Review.objects.filter(watchlist=pk)
#
#

# class MovieList(generics.ListAPIView):
#     serializer_class =WatchListSerializer
#     queryset = Review.objects.all()
#     # permission_classes = [IsAuthenticated]
#     # throttle_classes = [UserRateThrottle,AnonRateThrottle]
#     # filter_backends = [DjangoFilterBackend]
#     # filterset_fields = ['review_user__username', 'active']
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['title','platform_name']
#
#
#
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return Review.objects.filter(watchlist=pk)




# class ReviewCreate(generics.CreateAPIView):
#     serializer_class = ReviewSerializer
#
#     def get_queryset(self):
#         return Review.objects.all()
#
#     def perform_create(self, serializer):
#         pk = self.kwargs.get('pk')  # Get the primary key from the URL
#         watchlist = WatchList.objects.get(pk=pk)  # Retrieve the WatchList object
#         review_user = self.request.user  # Get the user making the request
#
#         # Check if the user has already reviewed this watchlist item
#         review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
#         if review_queryset.exists():
#             raise ValidationError("You have already reviewed this watchlist item.")
#         if watchlist.number_rating == 0:
#             watchlist.avg_rating  = serializer.validated_data['rating']
#         else:
#             watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
#
#         watchlist.number_rating = watchlist.number_rating + 1
#         WatchList.save()
#         # Save the review with the associated watchlist and user
#         serializer.save(watchlist=watchlist, review_user=review_user)






# class ReviewCreate(generics.CreateAPIView):
#     serializer_class = ReviewSerializer
#
#     def perform_create(self,serializer):
#         pk = self.kwargs.get('pk')
#         watchlist = WatchList.objects.get(pk=pk)
#         serializer.save(watchlist=watchlist)
#
#
#
#
#
# class ReviewList(generics.ListAPIView):
#     # queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         Review.objects.filter(watchlist=pk)
#
# class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#
#


# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#





# from watchlist_app.models import Movie
# from watchlist_app.api.serializers import WatchListSerializer
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
#
# class WatchListAV(APIView):
#     def get(self, request):
#         movies = Movie.objects.all()
#         serializer = WatchListSerializer(movies, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class MovieDetailAV(APIView):
#
#     def get(self, request, pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         movie.delete()
#         return Response({'msg': 'Item Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
#
#
#
#





























# from watchlist_app.models import Movie
# from watchlist_app.api.serializers import MovieSerializer
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
# from rest_framework.views import APIView
#
# class MovieListAV(APIView):
#     def geet(self,request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#
#     def post(self,request):
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
#
#
# class MovieDetailAV(APIView):
#
#     def get(self,request,pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#
#
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#
#     def put(self,request):
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request):
#         movie.delete()
#         return Response({'msg': 'Item Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#









# @api_view(['GET', 'POST'])  # This decorator is used to define the requests that should be accepted by the view
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#
    # elif request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     try:
    #     movie = Movie.objects.get(pk=pk)
    # except Movie.DoesNotExist:
    #     return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    #
    # if request.method == 'GET':
    #     serializer = MovieSerializer(movie)
    #     return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
#     elif request.method == 'DELETE':
        # movie.delete()
        # return Response({'msg': 'Item Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
