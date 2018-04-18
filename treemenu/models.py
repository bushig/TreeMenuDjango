from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=100)
    root_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, related_name='childs', null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name