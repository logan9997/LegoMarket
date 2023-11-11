from django.db import models
from config import ModelsConfig

class Item(models.Model):
    item_id = models.CharField(
        max_length=ModelsConfig.Length.ITEM_ID,
        primary_key=True
    )
    item_name = models.CharField(
        max_length=ModelsConfig.Length.ITEM_NAME
    )
    item_type = models.CharField(
        max_length=ModelsConfig.Length.ITEM_TYPE,
        choices=(ModelsConfig.Choice.ITEM_TYPE)
    )
    year_released = models.IntegerField()
    image_path = models.CharField(
        max_length=ModelsConfig.Length.IMAGE_PATH,
        null=True,
        blank=True
    )


class Price(models.Model):
    record_id = models.AutoField(
        primary_key=True
    )
    item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE
    )
    date = models.DateField()
    price_new = models.DecimalField(
        max_digits=ModelsConfig.Decimal.MAX_DIGITS, 
        decimal_places=ModelsConfig.Decimal.DECIMAL_PLACE
    )
    price_used = models.DecimalField(
        max_digits=ModelsConfig.Decimal.MAX_DIGITS, 
        decimal_places=ModelsConfig.Decimal.DECIMAL_PLACE
    )
    qty_used = models.IntegerField()
    qty_new = models.IntegerField()

    class Meta:
        unique_together = ('item', 'date')


class User(models.Model):
    user_id = models.AutoField(
        primary_key=True
    )
    username = models.CharField(
        max_length=ModelsConfig.Length.USERNAME
    )
    password = models.CharField(
        max_length=ModelsConfig.Length.PASSWORD
    )