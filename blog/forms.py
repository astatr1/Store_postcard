from django import forms


class EmailPostForm(forms.Form):
    """Форма для отправки E-Mail из поста, через кнопку поделиться"""
    name = forms.CharField(max_length=25, label="Имя")
    email = forms.EmailField(label="Отправитель")
    to = forms.EmailField(label="Кому")
    comments = forms.CharField(required=False, widget=forms.Textarea,
                               label="Комментарий")