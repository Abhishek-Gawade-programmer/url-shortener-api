from django.conf import settings
from django.db import models


def b36encode(num):
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    charsLen = len(chars)
    s = ""
    while num:
        s = chars[num % charsLen] + s
        num //= charsLen

    return s.zfill(6)


class URL(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="urls", on_delete=models.CASCADE
    )
    url = models.URLField()
    code = models.CharField(max_length=6, blank=True)
    clicks = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    def click(self):
        self.clicks = models.F("clicks") + 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
            self.code = b36encode(self.id)
            self.save()
        else:
            super().save(*args, **kwargs)
