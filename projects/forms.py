from django.forms import ModelForm
from django import forms
from django import forms
from .models import *
from django.core.validators import RegexValidator
class ProjectFormAdd(ModelForm):
    tages = forms.CharField(max_length=100, required=False)
    img_regex = RegexValidator(regex=r'(.*/)*.+\.(png|jpg|gif|bmp|jpeg|PNG|JPG|GIF|BMP)$',
                                 message="Image must b e jpg or png or jpeg only .")
    image = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True,
                                                           "accept":"image/gif, image/jpeg, image/png"}),
                                     required=True, validators=[img_regex])
    class Meta:
        model = Projects
        fields = ['title', 'details',
                  'categorie', 'totalTarget',
                  'startCampaign', 'endcampaign',
                  'user',]


class ProjectFormAddImage(ModelForm):
    class Meta:
        model = ImageProject
        fields = ['project', 'image']
class ProjectFormTag(ModelForm):
    class Meta:
        model = ProjectTage
        fields = ['tage']


class SupllierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ['quanty',]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

class SearchForm(forms.Form):
    mode = forms.ChoiceField(required=True,choices=(('1',"Tage"),('2',"title")))
    search = forms.CharField(required=True)
class ReportForm(forms.Form):
    content = forms.CharField(required=True)
#=======================================

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = ImageProject
        fields = ['image']