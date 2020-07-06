from django.db import models
import datetime


class Character(models.Model):
    last_name = models.CharField('Фамилия', max_length=30)
    first_name = models.CharField('Имя', max_length=15)
    middle_name = models.CharField('Отчество', max_length=15)
    photo = models.ImageField('Фото', upload_to='upload')
    date_of_birth = models.DateField('Дата рождения')
    short_biography = models.TextField('Краткая биография')
    vote_count = models.IntegerField('Количество голосов', default=0)

    def age(self):   # определение возраста персонажа по дате рождения
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month | \
                (today.month == self.date_of_birth.month & today.day < self.date_of_birth.day):
            age -= 1
        return age

    class Meta:
        ordering = ['-vote_count']
        verbose_name = u'Персонаж'
        verbose_name_plural = u'Персонажи'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Vote(models.Model):
    name = models.CharField('Название', max_length=200)
    date_start = models.DateField('Дата начала')
    date_end = models.DateField('Дата окончания')
    max_count_vote = models.IntegerField('Максимальное количество голосов', blank=True, null=True)
    character = models.ManyToManyField(Character, verbose_name='Персонаж', blank=True, null=True)

    class Meta:
        verbose_name = u'Голосование'
        verbose_name_plural = u'Голосования'

    def __str__(self):
        return self.name
