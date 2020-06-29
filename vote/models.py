from django.db import models


class Character(models.Model):
    last_name = models.CharField('Фамилия', max_length=30)
    first_name = models.CharField('Имя', max_length=15)
    middle_name = models.CharField('Отчество', max_length=15)
    photo = models.ImageField('Фото', upload_to='upload')
    age = models.IntegerField('Возраст')
    short_biography = models.TextField('Краткая биография')
    vote_count = models.IntegerField('Количество голосов', default=0)

    class Meta:
        ordering = ['-vote_count']

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Vote(models.Model):
    name = models.CharField('Название', max_length=200)
    date_start = models.DateField('Дата начала')
    date_end = models.DateField('Дата окончания')
    max_count_vote = models.IntegerField('Максимальное количество голосов', blank=True, null=True)
    character = models.ManyToManyField(Character, verbose_name='Персонаж', blank=True, null=True)

    def __str__(self):
        return self.name
