from django.db import models
from django.core.validators import validate_comma_separated_integer_list


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, related_name='childs', null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name



class Menu(models.Model):
    name = models.CharField(max_length=100)
    root_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    foreign_keys = models.CharField(blank=True, null=True, max_length=120, validators=(validate_comma_separated_integer_list,))
    def __str__(self):
        return self.name

    def get_all_children(self, curr_item=None):
        r = []
        r.append(curr_item.id)
        for c in MenuItem.objects.filter(parent=curr_item):
            _r = self.get_all_children(curr_item=c)
            if 0 < len(_r):
                r.extend(_r)
        return r

    def save(self, *args, **kwargs):

        self.foreign_keys = self.get_all_children(self.root_item)
        print(self.foreign_keys)
        super().save(*args, **kwargs)
