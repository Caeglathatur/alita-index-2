from django.db import models


class Message(models.Model):
    message = models.TextField(
        verbose_name='message',
        max_length=1000,
    )
    subject = models.ForeignKey(
        'Subject',
        verbose_name='subject',
        on_delete=models.SET_NULL,
        null=True,
    )
    sent = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.message


class Subject(models.Model):

    class Meta:
        ordering = ['order']

    name = models.CharField(
        max_length=150,
    )
    order = models.IntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
