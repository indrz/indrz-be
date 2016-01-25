from django import forms
from poi_manager.models import Poi, PoiCategory
from mptt.forms import TreeNodeChoiceField


class PoiCategoryForm(forms.ModelForm):
    cat_name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    parent = TreeNodeChoiceField(queryset=PoiCategory.objects.all(), required=False)

    class Meta:
        model = PoiCategory
        fields = ('cat_name', 'parent',)


class PoiForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    floor_num = forms.IntegerField(initial=0, required=False)
    fk_poi_category = TreeNodeChoiceField(queryset=PoiCategory.objects.all())

    class Meta:
        model = Poi
        fields = ('name', 'floor_num', 'fk_poi_category',)
