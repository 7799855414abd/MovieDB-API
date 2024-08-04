# from django.contrib import admin
# from watchlist_app.models import WatchList, StreamPlatform
# # Register your models here.
#
#
# class WatchListAdmin(admin.ModelAdmin):
#   list_display = ('pk','title','storyline','active','created')
#
# class StreamPlatformAdmin(admin.ModelAdmin):
#   list_display = ('pk','name','about','website')
#
#
# admin.site.register(WatchList, WatchListAdmin)
# admin.site.register(StreamPlatform, StreamPlatformAdmin)


from django.contrib import admin
from watchlist_app.models import WatchList, StreamPlatform, Review

class WatchListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'storyline', 'active', 'created')

class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'about', 'website')

admin.site.register(WatchList, WatchListAdmin)
admin.site.register(StreamPlatform, StreamPlatformAdmin)
admin.site.register(Review)
