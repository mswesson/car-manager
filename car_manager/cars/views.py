from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

from .models import Car, CarComment
from .forms import CarForm, CommentCarForm

# Car


class CarsListView(ListView):
    model = Car
    template_name = "cars/cars_list.html"
    paginate_by = 9


class CarsCreateView(LoginRequiredMixin, CreateView):
    model = Car
    template_name = "cars/cars_create.html"
    form_class = CarForm

    def get_success_url(self):
        return reverse_lazy("cars:cars_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CarsDetailView(LoginRequiredMixin, DetailView):
    model = Car
    template_name = "cars/cars_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = self.object.comments.all()

        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        return context


class CarsUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    template_name = "cars/cars_update.html"
    form_class = CarForm

    def get_success_url(self):
        return reverse_lazy("cars:cars_detail", kwargs={"pk": self.object.pk})


class CarsDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy("cars:cars_list")


# CarComment


class CarCommentCreateView(CreateView):
    model = CarComment
    template_name = "cars/comments_cars_create.html"
    form_class = CommentCarForm
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse_lazy(
            "cars:cars_detail", kwargs={"pk": self.object.car.pk}
        )

    def form_valid(self, form):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        car = Car.objects.filter(pk=pk).first()
        form.instance.author = self.request.user
        form.instance.car = car
        return super().form_valid(form)


class CarCommentDeleteView(LoginRequiredMixin, DeleteView):
    model = CarComment

    def get_success_url(self):
        return reverse_lazy(
            "cars:cars_detail", kwargs={"pk": self.object.car.pk}
        )

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        raise Http404()

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        object = self.get_object()
        if request.user != object.author:
            raise PermissionDenied()
        return super().post(request, *args, **kwargs)


class CarCommentsUpdateView(LoginRequiredMixin, UpdateView):
    model = CarComment
    form_class = CommentCarForm

    def get_success_url(self):
        return reverse_lazy(
            "cars:cars_detail", kwargs={"pk": self.object.car.pk}
        )

    def form_valid(self, form):
        object = self.get_object()
        car = object.car
        form.instance.author = self.request.user
        form.instance.car = car
        return super().form_valid(form)
