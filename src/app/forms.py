from django import forms
from app.models import Image

class ImageForm(forms.ModelForm):
    MAX_FILE_SIZE_MB = 20  # 最大ファイルサイズ (MB)

    class Meta:
        model = Image
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            max_file_size = self.MAX_FILE_SIZE_MB * 1024 * 1024  # MB をバイトに変換
            if file.size > max_file_size:
                raise forms.ValidationError(
                    f'ファイルサイズは {self.MAX_FILE_SIZE_MB}MB 以下にしてください。'
                )
        return file
