import datetime

from django.db import models


class Table(models.Model):
    name = models.CharField(max_length=1024, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Row(models.Model):
    table = models.ForeignKey(Table, on_delete=models.RESTRICT)
    name = models.CharField(max_length=1024)
    properties = models.JSONField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True)
    deleted_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.table} - {self.name}"


class Cell(models.Model):
    row = models.ForeignKey(
        Row,
        on_delete=models.RESTRICT,
        related_name="cells",
        related_query_name="cell",
    )
    date = models.DateField(null=True, blank=True)
    field = models.CharField(max_length=512)

    class Type(models.TextChoices):
        NUMBER = "number"
        STRING = "string"

    type = models.CharField(max_length=512, choices=Type.choices)
    value = models.TextField()

    def __str__(self) -> str:
        return f"{self.row} - {self.field}: {self.type} = {self.value}"

    class Meta:
        unique_together = ["row", "date", "field", "type"]
        ordering = ["row", "date", "field"]
