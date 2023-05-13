import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from hw_28_app.models import Ad, Categories
from user.models import User, Location


@method_decorator(csrf_exempt, name="dispatch")
class LocationListView(ListView):
    queryset = Location.objects.order_by("name")

    def get(self, request, *args, **kwargs):
        all_location = Location.objects.all()
        return JsonResponse([loc.serialize() for loc in all_location], safe=False)


class LocationDetailView(DetailView):
    model = Location

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())


@method_decorator(csrf_exempt, name="dispatch")
class LocationCreateView(CreateView):
    model = Location
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_location = Location.objects.create(**data)
        return JsonResponse(new_location.serialize())


@method_decorator(csrf_exempt, name="dispatch")
class LocationUpdateView(UpdateView):
    model = Location
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        if 'name' in data:
            self.object.name = data.get('name')
        if 'lat' in data:
            self.object.lat = data.get('lat')
        if 'lng' in data:
            self.object.lng = data.get('lng')

        self.object.save()


        return JsonResponse(self.object.serialize())


@method_decorator(csrf_exempt, name="dispatch")
class LocationDeleteView(DeleteView):
    model = Location
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, *kwargs)

        return JsonResponse({'status': 'ok'})