from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from .models import Memo
from .forms import MemoForm, RentForm
import os
import openai
import base64
from markdown import markdown
import re

base_url = "https://api.openai.iniad.org/api/v1"
api_key = os.getenv('OPENAI_API_KEY')

# アップロードしたファイルをほかのユーザーから見れなくするコード
# configの方にurlがある
def protected_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', path)
    memo = get_object_or_404(Memo, file='uploads/' + path)
    if memo.author != request.user:
        return HttpResponseForbidden("You do not have permission to access this file.")
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        return response


class MemoCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Memo
    form_class = MemoForm
    template_name = 'gpt/article_form.html'

    # ほかのユーザーから編集、削除されないようにしている
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class MemoUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Memo
    form_class = MemoForm
    template_name = 'gpt/article_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')

        return super().dispatch(request, *args, **kwargs)

class MemoDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Memo
    success_url = reverse_lazy('gpt:index')
    template_name = 'gpt/article_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete this.')

        return super().dispatch(request, *args, **kwargs)

class MemoListView(LoginRequiredMixin, generic.ListView):
    model = Memo
    template_name = 'gpt/article_list.html'

    def get_queryset(self):
        return Memo.objects.filter(author=self.request.user)

'''
# これは元のコードです。
# この下のMemoDetailViewが生成系AIを使用して解説をしてるもの
class MemoDetailView(LoginRequiredMixin, generic.DetailView):
    model = Memo
    template_name = 'gpt/article_detail.html'
    context_object_name = 'memo'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to view this.')

        if not obj.explanation and obj.file:
            photo_path = os.path.join(settings.MEDIA_ROOT, obj.file.name)
            photo64_url = encode_image(photo_path)
            client = openai.OpenAI(api_key=api_key, base_url=base_url)
            response = client.chat.completions.create(
                # miniだとあまり性能が良くない
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "次の画像は賃貸契約の見積書です。次の内容を写真から抜き出し、*で数値を囲んでください。例えば、賃料:*50000*みたいな感じです。なお、記載がない場合は0と出力してください。賃料 当月,賃料 翌月,敷金,礼金,仲介手数料,管理費 当月,管理費 翌月,共益費 当月,共益費 翌月,町内会費 当月,町内会費 翌月,駐車料 当月,駐車料 翌月,保険料,鍵交換,インターネット代,消毒代,退去時クリーニング費用,その他,合計金額"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url":f"data:image/jpeg;base64,{photo64_url}"
                                }
                            }
                        ]
                    }
                ],
            )
            # マークダウン形式に対応するために記載
            explanation_markdown = response.choices[0].message.content
            obj.explanation = explanation_markdown
            obj.save()

        return super().dispatch(request, *args, **kwargs)
'''
    
class MemoDetailView(LoginRequiredMixin, generic.DetailView):
    model = Memo
    template_name = 'gpt/article_detail.html'
    context_object_name = 'memo'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to view this.')

        if not obj.explanation and obj.file:
            photo_path = os.path.join(settings.MEDIA_ROOT, obj.file.name)
            photo64_url = encode_image(photo_path)
            client = openai.OpenAI(api_key=api_key, base_url=base_url)
            response = client.chat.completions.create(
                # miniだとあまり性能が良くない
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "次の画像は賃貸契約の見積書です。次の内容を写真から抜き出し、*で数値を囲んでください。例えば、賃料:*50000*みたいな感じです。なお、記載がない場合は0と出力し、次の内容に書いていないものがあった場合は全てその他に足し合わせて入れてください。。賃料 当月,賃料 翌月,敷金,礼金,仲介手数料,管理費 当月,管理費 翌月,共益費 当月,共益費 翌月,町内会費 当月,町内会費 翌月,駐車料 当月,駐車料 翌月,保険料,鍵交換,インターネット代,消毒代,退去時クリーニング費用,その他,合計金額"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url":f"data:image/jpeg;base64,{photo64_url}"
                                }
                            }
                        ]
                    }
                ],
            )

            patterns = {
                "賃料 当月": r"賃料 当月:\*(\d+)\*",
                "賃料 翌月": r"賃料 翌月:\*(\d+)\*",
                "敷金": r"敷金:\*(\d+)\*",
                "礼金": r"礼金:\*(\d+)\*",
                "仲介手数料": r"仲介手数料:\*(\d+)\*",
                "管理費 当月": r"管理費 当月:\*(\d+)\*",
                "管理費 翌月": r"管理費 翌月:\*(\d+)\*",
                "共益費 当月": r"共益費 当月:\*(\d+)\*",
                "共益費 翌月": r"共益費 翌月:\*(\d+)\*",
                "町内会費 当月": r"町内会費 当月:\*(\d+)\*",
                "町内会費 翌月": r"町内会費 翌月:\*(\d+)\*",
                "駐車料 当月": r"駐車料 当月:\*(\d+)\*",
                "駐車料 翌月": r"駐車料 翌月:\*(\d+)\*",
                "保険料": r"保険料:\*(\d+)\*",
                "鍵交換": r"鍵交換:\*(\d+)\*",
                "インターネット代": r"インターネット代:\*(\d+)\*",
                "消毒代": r"消毒代:\*(\d+)\*",
                "退去時クリーニング費用": r"退去時クリーニング費用:\*(\d+)\*",
                "その他": r"その他:\*(\d+)\*",
                "合計金額": r"合計金額:\*(\d+)\*"
            }

            # 各項目を辞書形式で抽出
            result = {}
            response_text = response.choices[0].message.content
            for key, pattern in patterns.items():
                match = re.search(pattern, response_text)
                result[key] = int(match.group(1)) if match else 0


            # マークダウン形式に対応するために記載
            explanation_markdown = result
            obj.explanation = explanation_markdown
            obj.save()

        return super().dispatch(request, *args, **kwargs)

    # 写真の形式を識別
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        memo = self.get_object()
        file_extension = memo.file.name.split('.')[-1].lower()
        context['is_image'] = file_extension in ['png', 'jpg', 'jpeg']
        if memo.explanation:
            context['explanation_html'] = markdown(memo.explanation)
        return context


# このMemoDetailViewが生成系AIが解説していないもの
# トークンを減らさないように、こちらも残してある
'''
class MemoDetailView(LoginRequiredMixin, generic.DetailView):
    model = Memo
    template_name = 'gpt/article_detail.html'
    context_object_name = 'memo'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to view this.')

        return super().dispatch(request, *args, **kwargs)

    # アップロードされたファイルを識別
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        memo = self.get_object()
        file_extension = memo.file.name.split('.')[-1].lower()
        context['is_image'] = file_extension in ['png', 'jpg', 'jpeg']
        return context
'''


# 写真のエンコード
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
