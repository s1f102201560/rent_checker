from django import forms
from .models import Memo

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['title', 'file']

    # ファイルサイズが20MB以下の場合に投稿できるようにしてる
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 20 * 1024 * 1024:  # 20 MB
                raise forms.ValidationError('ファイルサイズは20MB以下にしてください。')
        return file

class RentForm(forms.Form):
    CHOICES = [
        ("rent_current", "賃料 当月"),
        ("rent_next", "賃料 翌月"),
        ("deposit", "敷金"),
        ("key_money", "礼金"),
        ("agency_fee", "仲介手数料"),
        ("management_current", "管理費 当月"),
        ("management_next", "管理費 翌月"),
        ("common_current", "共益費 当月"),
        ("common_next", "共益費 翌月"),
        ("neighborhood_current", "町内会費 当月"),
        ("neighborhood_next", "町内会費 翌月"),
        ("parking_current", "駐車料 当月"),
        ("parking_next", "駐車料 翌月"),
        ("insurance", "保険料"),
        ("key_exchange", "鍵交換"),
        ("internet", "インターネット代"),
        ("disinfection", "消毒代"),
        ("cleaning_fee", "退去時クリーニング費用"),
        ("other", "その他"),
    ]

    options = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CHOICES,
        label="選択項目",
    )