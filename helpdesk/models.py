# coding: utf-8
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from regions.models import Region, Contact
from datetime import date


class Project(models.Model):

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name_short

    class Meta:
        verbose_name = u'проект'
        verbose_name_plural = u'проекты'

    name = models.CharField(verbose_name=u'проект', max_length=128)
    name_short = models.CharField(verbose_name=u'проект кратко', max_length=20)
    common_email = models.EmailField(verbose_name=u'общий e-mail', null=True, blank=True)


class Contract(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name_short

    class Meta:
        verbose_name = u'договор'
        verbose_name_plural = u'договоры'

    name_short = models.CharField(verbose_name=u'краткое имя', max_length=128)
    name = models.CharField(verbose_name=u'имя', max_length=128)
    project = models.ForeignKey(Project, verbose_name=u'связанный проект')
    contract_subject = models.CharField(verbose_name=u'предмет договора', max_length=128)
    contract_id = models.CharField(verbose_name=u'номер договора', max_length=32)
    contract_date = models.DateField(verbose_name=u'дата заключения')
    contract_expires = models.DateField(verbose_name=u'действует до', null=True, blank=True)
    annex_id = models.CharField(verbose_name=u'номер доп. соглашения', max_length=32, null=True, blank=True)
    annex_date = models.DateField(verbose_name=u'дата заключения доп. соглашения', null=True, blank=True)
    comment = models.TextField(verbose_name=u'комментарий', blank=True)


class Status(models.Model):

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'статус'
        verbose_name_plural = u'статусы'

    name = models.CharField(verbose_name=u'статус', max_length=20)


class Priority(models.Model):

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'приоритет'
        verbose_name_plural = u'приоритеты'

    name = models.CharField(verbose_name=u'приоритет', max_length=20)


class Component(models.Model):

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'компонент'
        verbose_name_plural = u'компоненты'

    name = models.CharField(verbose_name=u'компонент', max_length=20)
    project = models.ForeignKey(Project, verbose_name=u'проект', default=4)


class Source(models.Model):

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'источник'
        verbose_name_plural = u'источники'

    name = models.CharField(verbose_name=u'источник', max_length=20)


class ServiceType(models.Model):

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'тип запроса'
        verbose_name_plural = u'типы запросов'

    name = models.CharField(verbose_name=u'тип запроса', max_length=50)
    name_short = models.CharField(verbose_name=u'тип запроса кратко', max_length=20)
    name_full = models.CharField(verbose_name=u'тип услуги по договору', max_length=150)
    project = models.ForeignKey(Project, verbose_name=u'проект', default=4)


class Issue(models.Model):

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.issue_id

    class Meta:
        verbose_name = u'запрос'
        verbose_name_plural = u'запросы'
        ordering = ['-created']

    issue_id = models.CharField(verbose_name=u'номер запроса', max_length=30)
    external_id = models.CharField(verbose_name=u'входящий номер', max_length=50, blank=True)
    subject = models.CharField(verbose_name=u'тема', max_length=255)
    opened = models.DateField(verbose_name=u'дата открытия', null=True)
    created = models.DateTimeField(verbose_name=u'создан', auto_now_add=True)
    changed = models.DateTimeField(verbose_name=u'изменен', auto_now=True)
    priority = models.ForeignKey(Priority, verbose_name=u'приоритет', default=3)
    status = models.ForeignKey(Status, verbose_name=u'статус', default=1)
    project = models.ForeignKey(Project, verbose_name=u'проект', default=4)
    component = models.ForeignKey(Component, verbose_name=u'компонент', null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, verbose_name=u'тип запроса', default=1)
    source = models.ForeignKey(Source, verbose_name=u'источник', null=True, blank=True)
    control = models.DateField(verbose_name=u'дата контроля')
    creator = models.ForeignKey(User, related_name='issues_created', verbose_name=u'автор')
    assignee = models.ForeignKey(User, related_name='issues_assigned', verbose_name=u'ответственный')
    region = models.ForeignKey(Region, verbose_name=u'регион')
    formed = models.BooleanField(verbose_name=u'оформлен', default=False
                                 , help_text=u'Оформлено для отчета')
    contact = models.ForeignKey(Contact, verbose_name=u'контакт', blank=True, null=True)
    description = models.TextField(verbose_name=u'описание', blank=True
                                   , help_text=u'Данная информация не идет в отчет')
    report_description = models.TextField(verbose_name=u'описание для отчета', blank=True
                                          , help_text=u'Краткое описание запрошенной услуги')
    report_solution = models.TextField(verbose_name=u'решение для отчета', blank=True
                                       , help_text=u'Краткое описание содержания оказанной услуги')
    legacy_id = models.IntegerField(verbose_name='mySQL ID', null=True, blank=True)
    contracts = models.ManyToManyField(Contract, verbose_name=u'договор', blank=True)

    @property
    def expired(self):
        return self.control < date.today()

    @property
    def expires(self):
        return self.control >= date.today() and (self.control - date.today()).days <= 1

    @property
    def expires_tomorrow(self):
        return (self.control - date.today()).days == 1

    @property
    def expires_today(self):
        return self.control == date.today()

    @property
    def get_url(self):
        return settings.BASE_URL + reverse('helpdesk:issue', args=[self.id])


class Comment(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.comment_text[:20]

    class Meta:
        verbose_name = u'комментарий'
        verbose_name_plural = u'комментарии'

    comment_text = models.TextField(verbose_name=u'текст комментария')
    author = models.ForeignKey(User, verbose_name=u'автор')
    issue = models.ForeignKey(Issue, verbose_name=u'запрос')
    created = models.DateTimeField(verbose_name=u'создан', auto_now_add=True)
    legacy_id = models.IntegerField(verbose_name='MySQL ID', null=True, blank=True)