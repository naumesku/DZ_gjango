from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from product.forms import ProductForm, VersionForm, ModeratorForm
from product.models import Product, Version, Category
from product.services import get_cached_category


class ProductListView(ListView):
    model = Product

class CategoryListView(ListView):
    model = Category
    def get_queryset(self):
        return get_cached_category()

def contacts(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Контакты'
    }
    return render(request, 'product/contacts.html', context)


class ProductDetailView(DetailView):
    model = Product
    form_class = ProductForm

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user_own = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm, ModeratorForm
    permission_required = 'product.change_product'

    def get_success_url(self):
        return reverse('product:product_update', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        if not self.request.user.has_perm('product.set_published'):
            return ModeratorForm
        return ProductForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user == self.object.user_own or self.request.user.is_superuser:
            VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
            if self.request.method == 'POST':
                formset = VersionFormset(self.request.POST, instance=self.object)
                # context_data['version'] = get_object_or_404(Version, pk=self.kwargs.get('pk'))
            else:
                formset = VersionFormset(instance=self.object)

            context_data['formset'] = formset
        return context_data


    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)