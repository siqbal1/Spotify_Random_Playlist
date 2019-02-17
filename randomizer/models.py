from random import randint
from django.db import models
from django.db.models import Count

# Create your models here.
class TrackManager(models.Manager):
    def random(self, n):
        """
        Returns a sublist of n random track
        """
        count = self.aggregate(ids=Count('id'))['ids']
        random_track_list = []
        all_tracks = self.all()
        for x in range(n):
            random_index = randint(0, count - 1)

            random_track_list.append(all_tracks[random_index].id)

        return random_track_list

    def drop_table(self):
        cursor = connection.cursor()
        table_name = self.model._meta.db_table
        sql = "DROP TABLE %s;" % (table_name, )
        cursor.execute(sql)

# class Music_Genre(models.Model):
#     name = models.CharField(max_length=200, primary_key=True)
#
#     def __str__(self):
#         ret_str = "Genre: " + self.name

class Track(models.Model):
    id = models.CharField(max_length=200,
                        unique=True,
                        primary_key=True)


    objects = TrackManager()


    def __str__(self):
        ret_str = "Track id: " + str(self.id)

        return ret_str
