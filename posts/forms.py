from django import forms
from .models import Post, CustomUser, Comment
from .validators import validate_symbols
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):

    class Meta: # 메타 클래스는 PostForm이라는 클래스를 만들 때 적용할 여러 옵션을 넣어주는 클래스다. 라고 생각하면 된다.
        model = Post
        #fields = '__all__' # 모든 필드가 적용됨
        fields = ['title', 'content']
        
        # 필드이름을 키로하고 적용할 위젯을 값으로 하는 사전형 변수, 직접 접근할 때 사용하면 됨.
        widgets = {'title' : forms.TextInput(attrs={'class':'title',
                                                     'placeholder': '제목을 입력하세요'}),
                    'content' : forms.Textarea(attrs={'class': 'content',
                                                      'placeholder' : '내용을 입력하세요'})
                   }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        
        if '*' in title:
            raise ValidationError("*는 포함될 수 없습니다.")
        
        return title

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'nickname', 'password1', 'password2')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':2, 'placeholder':'댓글을 입력하세요', 'style':'width:100%; resize:none;'})
        }
