from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH
from .validators import max_value_current_year, validate_username


class User(AbstractUser):
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=(validate_username,)
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Role(models.TextChoices):
        'Роль',
        USER = 'user', ('Пользователь'),
        MODERATOR = 'moderator', ('Модератор'),
        ADMIN = 'admin', ('Администратор')

    role = models.CharField(
        max_length=len(max(max(Role.choices, key=len))),
        choices=Role.choices,
        default=Role.USER,
    )

    @property
    def is_admin(self):
        return (
            self.role == self.Role.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_user(self):
        return self.role == self.Role.USER


class CategoryGenre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальный человеко-понятный идентификатор'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryGenre):

    class Meta:
        verbose_name = 'Категория'


class Genre(CategoryGenre):

    class Meta:
        verbose_name = 'Жанр'


class Title(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[max_value_current_year]
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenres',
        verbose_name='Жанр',
        related_name='genre'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='category'
    )

    def __str__(self):
        return self.name


class TitleGenres(models.Model):
    title = models.ForeignKey(Title, null=True, on_delete=models.SET_NULL)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)


class UserAddObject(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return (
            f'{self.author.username}: {self.text[:25]}'
        )


class Review(UserAddObject):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Оценка ниже 1 невозможна'
            ),
            MaxValueValidator(
                10,
                message='Оценка выше 10 невозможна'
            )
        ],
        verbose_name='Оценка'
    )

    class Meta(UserAddObject.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(UserAddObject):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(UserAddObject.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
