from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy

from .models import Car, CarComment
from .forms import CarForm


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


class CarsUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    template_name = "cars/cars_create.html"
    form_class = CarForm

    def get_success_url(self):
        return reverse_lazy("cars:cars_detail", kwargs={"pk": self.object.pk})


class CarsDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy("cars:cars_list")
