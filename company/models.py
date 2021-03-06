from django.contrib.gis.db import models
from phonenumber_field.modelfields import PhoneNumberField

from company.utils import ActiveStatus

STATUS_CHOICES = ActiveStatus.to_list()


class ActiveManager(models.Manager):
    """
    return only active objects (objects with status A)
    """

    def get_queryset(self):
        return super().get_queryset().filter(status=ActiveStatus.ACTIVE.value)


class CompanyBaseModel(models.Model):
    status = models.CharField(max_length=5, choices=STATUS_CHOICES,
                              default=ActiveStatus.ACTIVE.value)
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

    class Meta:
        abstract = True


class Provider(CompanyBaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = PhoneNumberField(region='IN')
    language = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ServiceArea(CompanyBaseModel):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='service_areas')
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    poly = models.PolygonField()
