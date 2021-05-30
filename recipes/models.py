from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Url')
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    ingredients = models.TextField(blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    main_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    favorites = models.BooleanField(default=False)
    cooked = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0, verbose_name='Views')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-id']


class PostImage(models.Model):
    image_path = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name = 'Images gallery'
        verbose_name_plural = 'Additional images'