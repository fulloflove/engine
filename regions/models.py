# coding: utf-8
from django.db import models

# Cuate your models here.


class District(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Федеральные округа'

    name = models.CharField(verbose_name=u'Округ', max_length=128)
    name_short = models.CharField(verbose_name=u'Округ кратко', max_length=128, default='')


class Region(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Регионы'

    region_id = models.IntegerField(verbose_name=u'Номер региона')
    name = models.CharField(verbose_name=u'Регион', max_length=200)
    name_short = models.CharField(verbose_name=u'Регион кратко', max_length=50, blank=True)
    gu = models.TextField(verbose_name=u'ГУ кратко', max_length=200)
    gu_full = models.TextField(verbose_name=u'ГУ полное', max_length=200, blank=True)
    region_count = models.IntegerField(verbose_name=u'Счетчик записей')
    project_name = models.CharField(verbose_name=u'Региональный проект', max_length=100, blank=True)
    gu_dp = models.TextField(verbose_name=u'Дат. падеж кратко', default='', max_length=100, blank=True)
    gu_rp = models.TextField(verbose_name=u'Род. падеж полное', default='', max_length=200, blank=True)
    address_gu = models.TextField(verbose_name=u'Адрес ГУ', max_length=200, blank=True)
    phone_code = models.TextField(verbose_name=u'Телефонный код', max_length=20, blank=True)
    time_zone = models.IntegerField(verbose_name=u'Временная зона', blank=True)
    is_head = models.BooleanField(verbose_name=u'Столица округа', default=False)
    district = models.ForeignKey(District, verbose_name=u'Округ', default=1, null=True)


class Contact(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Контакты'

    name = models.CharField(verbose_name=u'Ф.И.О.', max_length=128)
    phone = models.CharField(verbose_name=u'Телефон', max_length=128, null=True, blank=True)
    email = models.CharField(verbose_name='E-mail', max_length=128, null=True, blank=True)
    job = models.CharField(verbose_name=u'Должность', max_length=200, null=True, blank=True)
    region = models.ForeignKey(Region, verbose_name=u'Регион')
    legacy_id = models.IntegerField(verbose_name='MySQL ID', null=True, blank=True)

    @property
    def emails_as_list(self):
        return self.email.replace(';',' ').replace(',',' ').split()

