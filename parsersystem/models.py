from django.db import models

# ORM модель таблицы resources
class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    resource_name = models.CharField(null=True, blank=True, max_length=100)
    resource_url = models.CharField(null=True, blank=True, max_length=100)
    top_tag = models.CharField(null=True, blank=True, max_length=100)
    bottom_tag = models.CharField(null=True, blank=True, max_length=100)
    title_cut = models.CharField(null=True, blank=True, max_length=100)
    date_cut = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.resource_name

# ORM модель таблицы items
class Items(models.Model):
    id = models.AutoField(primary_key=True)
    res_id = models.DecimalField(max_digits=5, decimal_places=0)
    link = models.CharField(null=True, blank=True, max_length=100)
    title = models.CharField(null=True, blank=True, max_length=100)
    content = models.TextField(null=True, blank=True, max_length=1000)
    nd_date = models.CharField(null=True, blank=True, max_length=100)
    s_date = models.CharField(null=True, blank=True, max_length=100)
    not_date = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.title

