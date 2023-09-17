from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache

#Модель Author содержит объекты всех авторов
#Имеет поля: рейтинг пользователя и связь один-к-одному с моделью User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user}"

#Метод обновляет рейтинг текущего автора
    def update_rating(self):
        post_rating_sum = \
            Post.objects.filter(author=self).aggregate(Sum('post_rating'))['post_rating__sum'] * 3
        comments_by_author_rating = \
            Comment.objects.filter(user=self.user).aggregate(Sum('comment_rating'))['comment_rating__sum']
        post_comment_rating = \
            Comment.objects.filter(post__author__user=self.user).aggregate(Sum('comment_rating'))['comment_rating__sum']

        total_rating = post_rating_sum + comments_by_author_rating + post_comment_rating
        self.user_rating = total_rating
        self.save()

#Модель Категории новостей/статей содержит поле название категорий
class Category(models.Model):
    name_of_category = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name="categories")

    def __str__(self):
        return f"{self.name_of_category}"


#Модель Post содержит в себе статьи и новости, которые создают пользователи
class Post(models.Model):
    article = 'AR'
    news = 'NW'
    type_to_choice = [
        (article, 'Статья'),
        (news, 'Новости')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=type_to_choice, default='article')
    time_of_creation = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField(default='none')
    post_rating = models.FloatField(default=0.0)

#Методы like() и dislike() увеличивают/уменьшают рейтинг на единицу
    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

#Метод preview() возвращает начало статьи
    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return str(self.title + ' | ' + self.preview())

    # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с новостями
    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

#Модель для связи «один ко многим» с моделью Post и «один ко многим» с моделью Category
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

#Модель Comment хранит комментарии, которые можно оставлять под статьями и новостями
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default='Default comment')
    comment_creation_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

