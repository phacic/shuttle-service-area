from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from company.utils import ActiveStatus, ActiveManager


class Provider(models.Model):
    STATUS_CHOICES = ActiveStatus.to_list()

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = PhoneNumberField(region='IN')
    language = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)
    # could be used to soft-delete a provider
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default=ActiveStatus.ACTIVE.value)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def remove(self, force=False):
        """
        either permanent delete or soft-delete
        :param force: True to permanently delete
        :return:
        """
        if not force:
            self.status = ActiveStatus.INACTIVE.value
            self.save()
        else:
            self.delete()


# class ServiceArea(models.Model):
#