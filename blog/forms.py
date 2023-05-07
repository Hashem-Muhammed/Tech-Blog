from django import forms
from .models import Author,Post , Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    class Meta:
        model = Author
        fields = ['first_name' , 'last_name' ,'email','password1','password2']
      
    def clean_email(self):
            email = self.cleaned_data['email']
            if Author.objects.filter(email=email).exists():
                print("ESSS")
                raise forms.ValidationError ("Email Already Exists!")
            return email       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2' 
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'first_name',
                'last_name',
                'email',
                'password',
                
            ),
            Submit('submit', 'Submit', css_class='button white'),
        )
        
class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","content","tag","author","postImage"]
        labels = {
            "title" : "Title",
            "content" : "Content",
            "author" : "Author"
          
        }

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name' , 'last_name' , 'profileImage']    



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        