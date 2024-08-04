# serializers.py
from rest_framework import serializers
from watchlist_app.models import StreamPlatform, WatchList,Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Review
        exclude=['watchlist']
        # fields='__all__'



class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True,read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'






















# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
#     watchlist = WatchListSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = StreamPlatform
#         fields = '__all__'
#
#









# from rest_framework import serializers
# from watchlist_app.models import StreamPlatform, WatchList
#
# class WatchListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WatchList
#         fields = "__all__"
#
#     def create(self, validated_data):
#         return WatchList.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.storyline = validated_data.get('storyline', instance.storyline)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
#     # watchlist = serializers.HyperlinkedIdentityField(
#     #     many=True,
#     #     read_only=True,
#     #     view_name='stream_list'  # Replace with your actual view name for WatchList detail
#     # )
#     watchlist = WatchListSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = StreamPlatform
#         fields = '__all__'
#
#     def create(self, validated_data):
#         return StreamPlatform.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.about = validated_data.get('about', instance.about)
#         instance.website = validated_data.get('website', instance.website)
#         instance.save()
#         return instance
#













# from rest_framework import serializers
# from watchlist_app.models import WatchList
# from rest_framework import serializers
# from watchlist_app.models import StreamPlatform
#
#
#
# class WatchListSerializer(serializers.ModelSerializer):
#     # len_name = serializers.SerializerMethodField()
#     # Here we are creating the new fields by using the SerializerMethod
#     class Meta:
#         model = WatchList
#         fields = "__all__"
#
#     # def get_len_name(self,object):
#     #     length = len(object.name)
#     #     return length
#
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
#
# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    # watchlist = WatchListSerializer(many=True, read_only=True)
#     # watchlist = serializers.StringRelatedField(many=True)
#     watchlist =  serializers.HyperlinkedRelatedField(
#         many=True,
#         read_only=True,
#         view_name='movie_detail'
#     )
#     class Meta:
#         model = StreamPlatform
#         fields = '__all__'
#
#     def create(self, validated_data):
#         return StreamPlatform.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.about = validated_data.get('description', instance.about)
#         instance.website = validated_data.get('active', instance.website)
#         instance.save()
#         return instance
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
# # id = serializers.IntegerField(read_only=True) # This fieldpermitted for only the read comabination
# # name = serializers.CharField(max_length=100, validators=[name_length])
# # description = serializers.CharField()
# # active = serializers.BooleanField()
#
#     # Field level validatiion
#     # def validate_name(self,value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("name is Too short")
#     #     else:
#     #         return value
#
#     # def validate(self, data):
#     #     if data['name'] == data['description']:
#     #         raise serializers.ValidationError("Title and Description should be different")
#     #     else:
#     #         return data
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
#
#
#
#
#
#
#
#     # def validate_name(self, value):
#     #     if not value:
#     #         raise serializers.ValidationError("Name cannot be empty.")
#     #     return value
#     #
#     # def validate_description(self, value):
#     #     if not value:
#     #         raise serializers.ValidationError("Description cannot be empty.")
#     #     return value
