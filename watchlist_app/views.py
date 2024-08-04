# from django.shortcuts import render, get_object_or_404
# from watchlist_app.models import Movie
# from django.http import JsonResponse
# # python -m venv menv
# # menv\Scripts\activate
#
# # Create your views here.
# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {
#         'movies': list(movies.values())
#     }
#     return JsonResponse(data)
#
# def movie_details(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     data = {
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active,
#         # add other fields as needed
#     }
#     return JsonResponse(data)
#
#
#
#
#
#
#
# # from django.shortcuts import render
# # from watchlist_app.models import Movie
# # from django.http import JsonResponse
# #
# # # Create your views here.
# # def movie_list(request):
# #     movies = Movie.objects.all()
# #     print(movies.values())
# #     data ={
# #         'movies':list(movies.values())
# #     }
# #
# #     return JsonResponse(data) #here we convert teh dictionary into the json format
# #
# # def movie_detail(request,pk):
# #     movie =  Movie.objects.get(pk=pk)
# #     return JsonResponse(movie.values())
