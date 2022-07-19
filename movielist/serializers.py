from rest_framework import serializers
from movielist.models import Movie, Person
from showtime.models import Cinema

class MovieSerializer(serializers.ModelSerializer):
    actors = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Person.objects.all())
    director = serializers.SlugRelatedField(slug_field='name', queryset=Person.objects.all())

    class Meta:
        model = Movie
        fields = ("id", "title", "year", "description", "director", "actors")


class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="movies-detail")

    class Meta:
        model = Cinema
        fields = ("name", "city", "movies")
