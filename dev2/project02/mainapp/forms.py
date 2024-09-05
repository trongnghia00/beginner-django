from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

from django.forms import ModelForm
from .models import Thought

class ThoughtForm(ModelForm):
    class Meta:
        model = Thought
        fields = ['title', 'content']
        labels = {
            'title': 'Tiêu đề',
            'content': 'Nội dung',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề', 
            }),
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập nội dung', 
            }),
        }

class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        label='Tên đăng nhập',
        help_text='Bắt buộc. Tối đa 150 ký tự.',
        max_length=150,
        min_length=4,
        error_messages={
            'required': 'Vui lòng nhập tên đăng nhập.',
            'unique': 'Tên đăng nhập này đã được sử dụng.',
            'max_length': 'Tên đăng nhập không được dài quá 100 ký tự.',
            'min_length': 'Tên đăng nhập phải có ít nhất 4 ký tự.',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập tên đăng nhập'
        })
    )

    email = forms.EmailField(
        label="Địa chỉ Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập Email'
        }),
        error_messages={
            'invalid': 'Vui lòng nhập một địa chỉ email hợp lệ.',
        }
    )

    password1 = forms.CharField(
        label='Mật khẩu',
        help_text="""<ul>
        <li>Mật khẩu không thể tương tự với thông tin cá nhân của bạn</li>
        <li>Mật khẩu phải có ít nhất 8 ký tự</li>
        <li>Mật khẩu không thể quá phổ thông</li>
        <li>Mật khẩu không thể hoàn toàn là số</li>
        </ul>""",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Vui lòng nhập mật khẩu.',
        }
    )

    password2 = forms.CharField(
        label='Xác nhận mật khẩu',
        help_text='Nhập lại chính xác như trên. Dùng để xác nhận.',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Vui lòng xác nhận mật khẩu.',
            'password_mismatch': 'Mật khẩu không khớp.',
        }
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

class UpdateUserForm(forms.ModelForm):
    password = None # Không cập nhật password
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập nội dung', 
            }),
        }
        help_texts = {
            'username': '',
        }