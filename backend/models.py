from django.db import models


class LinkPrecedenceTypes(models.TextChoices):
    PRIMARY = "primary", "primary"
    SECONDARY = "secondary", "secondary"


class Contact(models.Model):
    phoneNumber = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedId = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    linkPrecedence = models.CharField(max_length=10, null=True, choices=LinkPrecedenceTypes.choices)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True)
