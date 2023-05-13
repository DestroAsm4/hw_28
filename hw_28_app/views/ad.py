import json

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from hw_28_app.models import Ad, Categories
from user.models import User

TOTAL_ON_PAGE = 10

@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    queryset = Ad.objects.order_by("-price")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        ad_on_page = paginator.get_page(page_number)

        return JsonResponse({
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'items': [ad.serialize() for ad in ad_on_page]
        }, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if 'author' in data:

            data['author'] = get_object_or_404(User, pk=data.get('author'))

        if 'category' in data:

            data['category'] = get_object_or_404(Categories, pk=data.get('category'))

        new_ad = Ad.objects.create(**data)
        return JsonResponse(new_ad.serialize())


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        if 'name' in data:
            self.object.name = data.get('name')
        if 'author' in data:
            author = get_object_or_404(User, pk=data.get('author'))
            self.object.author = author
        if 'price' in data:
            self.object.price = data.get('price')
        if 'is_published' in data:


            self.object.is_published = data.get('is_published')
        if 'category' in data:
            category = get_object_or_404(Categories, pk=data.get('category'))
            self.object.category = category

        self.object.save()



        return JsonResponse(self.object.serialize())


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, *kwargs)

        return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name="dispatch")
class AdUploadImageView(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get('image')
        self.object.save()



        return JsonResponse(self.object.serialize())