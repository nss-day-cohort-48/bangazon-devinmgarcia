from django.db import models

class CustomerProductLike(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="likes")
    class Meta:
        unique_together = ('customer', "product")