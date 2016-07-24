from django.contrib import admin
from django import forms

from jmbo.admin import ModelBaseAdmin

from mysite.models import Car, Manufacturer


class CarAdmin(admin.ModelAdmin):
    pass


class ManufacturerAdminForm(forms.ModelForm):
    foo = forms.CharField(required=False)

    class Meta:
        model = Manufacturer
        fields = ("title", "year")

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title.lower() == "bmw":
            raise forms.ValidationError(
                    "Pick a better car"
            )
        return title

    def clean(self):
        cd = self.cleaned_data
        if cd.get('title', '') == 'jeep' and cd.get('year', 0) == 2016:
            raise forms.ValidationError('Ryan says no!')
        return cd


class ManufacturerAdmin(admin.ModelAdmin):
    form = ManufacturerAdminForm


admin.site.register(Car, CarAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
