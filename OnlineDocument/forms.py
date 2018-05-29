import logging

from django import forms
from OnlineDocument import tasks
from OnlineDocument.models import Document, Category, Tag

logger = logging.getLogger("django")


def get_available_choices():
    choices = ()
    for choice in Category.objects.all():
        choices = choices + ((choice.name, choice.name),)
    return choices


class UploadForm(forms.Form):
    title = forms.CharField(
        label="标题",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入文章标题，不超过50个字'
        }),
    )

    original_file = forms.FileField(
        label="文件",
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx',
            'class': 'file-loading'
        }),
    )

    category = forms.ChoiceField(
        label="分类",
        choices=get_available_choices(),
        widget=forms.RadioSelect(attrs={
            'class': 'radio-inline'
        }),
    )

    tags = forms.CharField(
        label="标签",
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入标签，用" "分割'
        }),
    )

    def save(self, user):
        clean_data = self.cleaned_data
        title = clean_data['title']
        original_file = clean_data['original_file']
        tags = clean_data['tags'].split(' ')
        category = clean_data['category']
        document = Document.objects.create(
            author=user,
            title=title,
            original_file=original_file,
            category=Category.objects.get(name=category)
        )
        for tag in tags:
            try:
                tag_object = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                logger.info(tag + " Does not exist, create tag object now.")
                tag_object = Tag.objects.create(name=tag)
            finally:
                document.tags.add(tag_object)
        document.save()
        task = tasks.convert_file.apply_async(args=[document.pk], countdown=5)
        logger.info(task.task_id)
