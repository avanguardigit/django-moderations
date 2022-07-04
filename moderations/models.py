from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _("States")

    def __str__(self):
        return self.name

class Case(models.Model):
    target_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_case_object',on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target_object = GenericForeignKey('target_content_type', 'target_object_id')

    state = models.ForeignKey("State", default=1 ,on_delete=models.RESTRICT)
    judgement = models.ForeignKey("Judgement", on_delete=models.RESTRICT, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        unique_together = ('target_content_type', 'target_object_id',)

    def __str__(self):
        return f"{self.target_object}"

    @property
    def count_reports(self):
        return self.report_set.count()

class Motivation(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _("Motivations")

    def __str__(self):
        return self.name

class Report(models.Model):
    signaler = models.ForeignKey(User, related_name="signaler", null=True, blank=True, on_delete=models.SET_NULL)
    motivation = models.ForeignKey("Motivation", on_delete=models.RESTRICT)
    target_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_report_object', on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target_object = GenericForeignKey('target_content_type', 'target_object_id')
    case = models.ForeignKey("Case", on_delete=models.RESTRICT, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"{self.signaler} {self.motivation}"

    def save(self, *args, **kwargs):
        #if self._state.adding:
        #
        target_content_type = self.target_content_type
        target_object_id = self.target_object_id
        qs = Case.objects.filter(target_content_type=target_content_type, target_object_id=target_object_id)
        if not qs.exists():
            case = Case.objects.create(target_content_type=target_content_type, target_object_id=target_object_id)
            case.save()
        else:
            case = qs[0]
        self.case = case
        return super().save(*args, **kwargs)


class Judgement(models.Model):
    moderator = models.ForeignKey(User, related_name="moderator", null=True, blank=True, on_delete=models.RESTRICT)
    reported = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    moderator_note = models.TextField(max_length=1000, null=True, blank=True)
    ACTIONS = (
        ('NoAction', 'NoAction'),
        ('Mute', 'Mute'),
        ('Ban', 'Ban'),
    )
    action = models.CharField(choices=ACTIONS, max_length=20)
    end_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"#{self.pk} {self.case} - {self.action} BY {self.moderator}"

    @property
    def case(self):
        return self.case_set.all()[0]