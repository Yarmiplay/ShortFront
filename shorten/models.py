from django.db import models

# A single table with the short key and destination link
class Links(models.Model):
    key = models.CharField(max_length=7, primary_key=True)
    dest = models.URLField()
    hit_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Key: {self.key}, Destination: {self.dest}"
    
    # Function to increase counter by 1
    def increment_hit_count(self):
        self.hit_count += 1
        self.save()