# coding: utf-8
from django.forms import Form, ModelForm, Textarea, ModelChoiceField, HiddenInput, \
    DateTimeField, DateField, ValidationError, EmailField, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.contrib.auth.models import User
from helpdesk.models import Issue, Comment, Priority, Project, Status, ServiceType, Component, Source, Contract
from regions.models import Region
from django.utils.translation import ugettext as _


class UserForm(ModelForm):
    email = EmailField(error_messages={'invalid': _('Your email address is incorrect')},
                       required=False,
                       label=u'E-mail')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserLabel(object):
    def label_from_instance(self, obj):
        return obj.last_name + ' ' + obj.first_name


class UserModelChoiceField(UserLabel, ModelChoiceField):
    pass


class UserModelMultipleChoiceField(UserLabel, ModelMultipleChoiceField):
    pass


class RegionModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s)" % (obj.name, obj.region_id)


class IssuePeriodForm(Form):
    start = DateTimeField(required=False, label=u'Начальная дата')
    end = DateTimeField(required=False, label=u'Конечная дата')

    def clean(self):
        cleaned_data = super(IssuePeriodForm, self).clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start is None and end is None:
            raise ValidationError(
                _('Both fields cannot be empty'),
                code='both_empty',
            )
        return cleaned_data


class IssueForm(ModelForm):
    assignee = UserModelChoiceField(queryset=User.objects.filter(is_active=True),
                                    label=u'Ответственный',
                                    empty_label=None)
    region = RegionModelChoiceField(queryset=Region.objects.order_by('name_short'),
                                    label=u'Инициатор')

    class Meta:
        model = Issue
        fields = ('external_id', 'subject', 'priority', 'status', 'project', 'component', 'service_type', 'source',
                  'control', 'assignee', 'region', 'formed', 'contact', 'description',
                  'report_description', 'report_solution', 'contracts')
        widgets = {
            'description': Textarea(attrs={'rows': 3}),
            'report_description': Textarea(attrs={'rows': 3}),
            'report_solution': Textarea(attrs={'rows': 3}),
            'contact': HiddenInput,
            'contracts': CheckboxSelectMultiple()
        }

    def clean(self):
        cleaned_data = super(IssueForm, self).clean()
        status = cleaned_data.get('status')
        if status.id == 4:
            formed = cleaned_data.get('formed')
            contracts = cleaned_data.get('contracts')
            if not formed:
                raise ValidationError(
                    _('Issue must be formed to be closed'),
                    code='close_not_formed',
                )
            if not contracts:
                raise ValidationError(
                    _('Contracts must be set for issue to be closed'),
                    code='close_contracts_not_set',
                )
        return cleaned_data


class DescriptionForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('description', )
        widgets = {'description': Textarea(attrs={'rows': 3})}


class ReportForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('report_description', 'report_solution', 'contracts', 'formed')
        widgets = {'report_description': Textarea(attrs={'rows': 3}),
                   'report_solution': Textarea(attrs={'rows': 3}),
                   'contracts': CheckboxSelectMultiple()}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)


class ControlForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('control',)


class FilterForm(Form):
    region = ModelMultipleChoiceField(queryset=Region.objects.order_by('name_short'),
                                      label=u'Регион', required=False)
    project = ModelMultipleChoiceField(queryset=Project.objects.all(),
                                       label=u'Проект', required=False)
    source = ModelMultipleChoiceField(queryset=Source.objects.all(),
                                      label=u'Источник', required=False)
    priority = ModelMultipleChoiceField(queryset=Priority.objects.all(),
                                        label=u'Приоритет', required=False)
    status = ModelMultipleChoiceField(queryset=Status.objects.all(),
                                      label=u'Статус', required=False)
    service_type = ModelMultipleChoiceField(queryset=ServiceType.objects.all(),
                                            label=u'Тип', required=False)
    component = ModelMultipleChoiceField(queryset=Component.objects.all(),
                                         label=u'Компонент', required=False)
    creator = UserModelMultipleChoiceField(queryset=User.objects.filter(is_active=True),
                                           label=u'Автор', required=False)
    assignee = UserModelMultipleChoiceField(queryset=User.objects.filter(is_active=True),
                                            label=u'Ответственный', required=False)
    contracts = ModelMultipleChoiceField(queryset=Contract.objects.all(),
                                         label=u'Договор', required=False, widget=CheckboxSelectMultiple)

    created_start = DateField(required=False, label=u'Начальная дата создания')
    created_end = DateField(required=False, label=u'Конечная дата создания')

    control_start = DateField(required=False, label=u'Начальная дата контроля')
    control_end = DateField(required=False, label=u'Конечная дата контроля')