from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books') #me permite acceder a los libros del author, con comando author.books__all
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)