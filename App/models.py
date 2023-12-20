from django.db import models
from config import ModelsConfig
from django.db.models import F, ExpressionWrapper, Case, When, Value

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


class Portfolio(models.Model):
    entry_id = models.AutoField(
        primary_key=True
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    bought_for = models.DecimalField(
        max_digits=ModelsConfig.Decimal.MAX_DIGITS, 
        decimal_places=ModelsConfig.Decimal.DECIMAL_PLACE
    )
    date_acquired = models.DateField()
    notes = models.CharField(
        max_length=ModelsConfig.Length.NOTES
    )