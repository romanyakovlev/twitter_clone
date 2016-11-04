from django import forms
from twitter_app.models import UserProfile

class UserProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('image',)
