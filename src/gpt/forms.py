from django import forms
from .models import Memo

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['title', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 20 * 1024 * 1024:  # 20 MB
                raise forms.ValidationError('ファイルサイズは20MB以下にしてください。')
        return file
