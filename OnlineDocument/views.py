from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Count, Sum
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, ListView, DetailView
from haystack.query import SearchQuerySet

from OnlineDocument.forms import UploadForm
from OnlineDocument.models import Document, Category, RateDetail, Favorite, History
from OnlineDocument.decorator import check_login, check_request
from users.models import Profile
import logging
import os
import json

logger = logging.getLogger('django')


# Create your views here.


def index(request):
    nickname = ''
    avatar = ''
    if request.user.is_authenticated:
        nickname = Profile.objects.get(user=request.user).nickname
        avatar = Profile.objects.get(user=request.user).avatar
    context = {
        'test': 'Checkout is working now!',
        'welcome': 'Hello World.',
        'nickname': nickname,
        'avatar': avatar,
    }
    logger.info('index rendered.')
    return render(request, 'index.html', context)


def upload_success(request):
    return render(request, 'upload_success.html')


class UploadView(FormView):
    template_name = 'upload.html'
    form_class = UploadForm
    success_url = '/upload/success/'

    def form_valid(self, form):
        logger.info("valid form.")
        form.save(self.request.user)
        return super(UploadView, self).form_valid(form)

    def form_invalid(self, form):
        logger.info("invalid form.")
        return super(UploadView, self).form_invalid(form)


class IndexDocumentListView(ListView):
    template_name = 'index.html'

    def get_queryset(self, **kwargs):
        new_document_list = Document.objects.all().order_by(F('views') + (F('like') / (F('dislike') + 1)))[:100:-1]
        paginator = Paginator(new_document_list, 10)
        page = self.request.GET.get('page')
        try:
            new_document_list = paginator.page(page)
        except PageNotAnInteger:
            new_document_list = paginator.page(1)
        except EmptyPage:
            new_document_list = paginator.page(paginator.num_pages)
        return new_document_list


class EducationListView(ListView):
    template_name = 'education.html'

    def get_queryset(self, **kwargs):
        object_list = Document.objects.filter(category=Category.objects.get(name='教育')) \
                          .order_by(F('views') + (F('like') / (F('dislike') + 1)))[::-1]
        paginator = Paginator(object_list, 20)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        return object_list


class ProfessionalListView(ListView):
    template_name = 'professional.html'

    def get_queryset(self, **kwargs):
        object_list = Document.objects.filter(category=Category.objects.get(name='专业')) \
                          .order_by(F('views') + (F('like') / (F('dislike') + 1)))[::-1]
        paginator = Paginator(object_list, 20)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        return object_list


class FunctionalListView(ListView):
    template_name = 'functional.html'

    def get_queryset(self, **kwargs):
        object_list = Document.objects.filter(category=Category.objects.get(name='实用')) \
                          .order_by(F('views') + (F('like') / (F('dislike') + 1)))[::-1]
        paginator = Paginator(object_list, 20)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        return object_list


class ExamListView(ListView):
    template_name = 'exam.html'

    def get_queryset(self, **kwargs):
        object_list = Document.objects.filter(category=Category.objects.get(name='考试')) \
                          .order_by(F('views') + (F('like') / (F('dislike') + 1)))[::-1]
        paginator = Paginator(object_list, 20)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        return object_list


class LifeListView(ListView):
    template_name = 'life.html'

    def get_queryset(self, **kwargs):
        object_list = Document.objects.filter(category=Category.objects.get(name='生活')) \
                          .order_by(F('views') + (F('like') / (F('dislike') + 1)))[::-1]
        paginator = Paginator(object_list, 20)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        return object_list


class DocumentDetailView(DetailView):
    template_name = 'document_detail.html'

    def get_object(self, **kwargs):
        doc_id = self.kwargs.get('id')
        try:
            doc = Document.objects.get(pk=doc_id)
            doc.views += 1
            doc.save()
            doc.pdf_file = os.path.split(doc.pdf_file.path)[1]
            try:
                history = History.objects.get(user=self.request.user)
            except History.DoesNotExist:
                history = History(user=self.request.user)
                history.save()
            if doc not in history.document.all():
                history.document.add(doc)
        except Document.DoesNotExist:
            raise Http404("查看的文档不存在")
        return doc


@check_login
@check_request('id', 'direct')
def likes_change(request):
    data = {}
    data['status'] = 200
    data['message'] = 'ok'
    data['nums'] = 0
    id = request.GET.get('id')
    user = request.user
    direct = 1 if request.GET.get('direct') == '1' else -1
    try:
        doc = Document.objects.get(pk=id)
    except Exception as e:
        data['status'] = 403
        data['message'] = 'no such document'

    try:
        detail = RateDetail.objects.get(document=doc, user=user)
    except Exception as e:
        detail = RateDetail(document=doc, user=user, is_rated=False)
    liked = 1 if detail.is_rated else -1

    if liked == direct:
        data['status'] = 403
        data['message'] = 'Invalid operation'
    else:
        doc.like += direct
        if doc.like < 0:
            doc.like = 0
        doc.save()
        data['nums'] = doc.like
        detail.is_rated = direct == 1
        detail.save()
    return HttpResponse(json.dumps(data), content_type="application/json")


@check_login
@check_request('id', 'direct')
def dislikes_change(request):
    data = {}
    data['status'] = 200
    data['message'] = 'ok'
    data['nums'] = 0
    id = request.GET.get('id')
    user = request.user
    direct = 1 if request.GET.get('direct') == '1' else -1
    try:
        doc = Document.objects.get(pk=id)
    except Exception as e:
        data['status'] = 403
        data['message'] = 'no such document'
        return HttpResponse(json.dumps(data), content_type="application/json")

    try:
        detail = RateDetail.objects.get(document=doc, user=user)
    except Exception as e:
        detail = RateDetail(document=doc, user=user, is_rated=False)
    liked = 1 if detail.is_rated else -1

    if liked == direct:
        data['status'] = 403
        data['message'] = 'Invalid operation'
    else:
        doc.dislike += direct
        if doc.dislike < 0:
            doc.dislike = 0
        doc.save()
        data['nums'] = doc.like
        detail.is_rated = direct == 1
        detail.save()
    return HttpResponse(json.dumps(data), content_type="application/json")


@check_login
@check_request('id')
def check_rate_status(request):
    data = {}
    data['status'] = 200
    data['message'] = 'ok'
    data['rate'] = 0
    id = request.GET.get('id')
    user = request.user
    try:
        doc = Document.objects.get(pk=id)
    except Exception as e:
        data['status'] = 403
        data['message'] = 'no such document'
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
        detail = RateDetail.objects.get(document=doc, user=user)
    except Exception as e:
        detail = RateDetail(document=doc, user=user, is_rated=False)
    data['rate'] = 1 if detail.is_rated else 0
    return HttpResponse(json.dumps(data), content_type="application/json")


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')


class FavoriteListView(ListView):
    template_name = 'favorite.html'

    def get_queryset(self, **kwargs):
        object_list = []
        try:
            favorite = Favorite.objects.get(user=self.request.user)
            object_list = favorite.document.all()[::-1]
        except Favorite.DoesNotExist:
            new_favorite = Favorite(user=self.request.user)
            new_favorite.save()
            object_list = new_favorite
        try:
            paginator = Paginator(object_list, 20)
            page = self.request.GET.get('page')
            try:
                object_list = paginator.page(page)
            except PageNotAnInteger:
                object_list = paginator.page(1)
            except EmptyPage:
                object_list = paginator.page(paginator.num_pages)
        except Exception as e:
            object_list = []
        return object_list


class HistoryListView(ListView):
    template_name = 'history.html'

    def get_queryset(self, **kwargs):
        object_list = []
        try:
            history = History.objects.get(user=self.request.user)
            object_list = history.document.all()[::-1]
        except History.DoesNotExist:
            new_history = History(user=self.request.user)
            new_history.save()
            object_list = new_history
        try:
            paginator = Paginator(object_list, 20)
            page = self.request.GET.get('page')
            try:
                object_list = paginator.page(page)
            except PageNotAnInteger:
                object_list = paginator.page(1)
            except EmptyPage:
                object_list = paginator.page(paginator.num_pages)
        except Exception as e:
            object_list = []
        return object_list


@check_login
@check_request('id')
def add_to_favorite(request):
    data = {}
    data['status'] = 200
    data['message'] = 'ok'
    id = request.GET.get('id')
    user = request.user
    try:
        favorite = Favorite.objects.get(user=user)
        favorite.document.add(Document.objects.get(pk=id))
        favorite.save()
    except Exception as e:
        data['status'] = 403
        data['message'] = 'no such document'
    return HttpResponse(json.dumps(data), content_type="application/json")


@check_login
@check_request('id')
def check_favorite_status(request):
    data = {}
    data['status'] = 200
    data['message'] = 'ok'
    data['favorite'] = 0
    id = request.GET.get('id')
    user = request.user
    try:
        document = Document.objects.get(pk=id)
        favorite = Favorite.objects.get(user=user)
        data['favorite'] = 1 if document in favorite.document.all() else 0
    except Favorite.DoesNotExist:
        favorite = Favorite(user=user)
        favorite.save()
    except Document.DoesNotExist:
        data['status'] = 403
        data['message'] = 'no such document'
    return HttpResponse(json.dumps(data), content_type="application/json")


@check_login
@check_request('id')
def delete_document(request):
    data = {}
    data['status'] = 200
    data['message'] = 'ok'
    id = request.GET.get('id')
    try:
        document = Document.objects.get(pk=id)
        document.delete()
    except Document.DoesNotExist:
        data['status'] = 403
        data['message'] = 'no such document'
    return render(request,'remove_success.html')


class UserDocumentListView(ListView):
    template_name = 'user_document_list.html'

    def get_queryset(self, **kwargs):
        object_list = []
        try:
            object_list = Document.objects.filter(author=self.request.user) \
                          .order_by(F('views') + (F('like') / (F('dislike') + 1)))[::-1]
            paginator = Paginator(object_list, 20)
            page = self.request.GET.get('page')
            try:
                object_list = paginator.page(page)
            except PageNotAnInteger:
                object_list = paginator.page(1)
            except EmptyPage:
                object_list = paginator.page(paginator.num_pages)
        except Document.DoesNotExist:
            object_list = []
        return object_list


def my(request):
    document_count = Document.objects.all().values('author').filter(author=request.user).annotate(count=Count('author')).values('count')[0]
    document_count = document_count['count']
    document_views = Document.objects.values('views').filter(author=request.user).aggregate(Sum('views'))['views__sum']

    context = {
        'document_count': document_count,
        'document_views': document_views,
    }
    return render(request,'my.html',context)
