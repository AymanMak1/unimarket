from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Category, Goods, Carousel
from haystack.generic_views import SearchView
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


def index(request):
    context = {}
    context["slides"] = Carousel.objects.all()
    context["categories"] = Category.objects.filter(is_published=True)
    paginator = Paginator(Category.objects.filter(is_published=True), 9)
    context["recommend"] = Goods.objects.filter(is_recommend=True, is_active=True)
    context["top"] = Goods.objects.filter(is_published=True, is_active=True).order_by(
        "-id"
    )
    context["site_title"] = _("main")
    return render(request, "shop/index.html", context)


def my_items(request):
    context = {}
    context["my_items"] = Goods.objects.filter(
        is_published=True, author=request.user
    ).order_by("-id")
    context["categories"] = Category.objects.filter(is_published=True)
    return render(request, "shop/my_items.html", context)


def categories(request):
    context = {}
    paginator = Paginator(Category.objects.filter(is_published=True), 9)
    page = request.GET.get("page")
    context["categories"] = paginator.get_page(page)
    if "last_product" in request.session:
        try:
            context["last_product"] = Goods.objects.get(
                id=request.session["last_product"]
            )
        except:
            pass
    context["site_title"] = _("categories")
    return render(request, "shop/categories.html", context)


def cat(request, category):
    context = {}
    paginator = Paginator(
        Goods.objects.filter(
            category=category, is_published=True, is_active=True
        ).order_by("-id"),
        9,
    )
    page = request.GET.get("page")
    context["products"] = paginator.get_page(page)
    context["categories"] = Category.objects.filter(is_published=True)
    if "last_product" in request.session:
        try:
            context["last_product"] = Goods.objects.get(
                id=request.session["last_product"]
            )
        except:
            pass
    context["site_title"] = Category.objects.get(id=category).title
    return render(request, "shop/category.html", context)


def product(request, title):
    if request.method == "GET":
        try:
            if "toggle" in request.GET:
                p = Goods.objects.get(id=int(title))
                p.is_active = int(request.GET["toggle"])
                p.save()
            elif "delete" in request.GET:
                Goods.objects.get(id=int(title)).delete()
                context = {}
                context["my_items"] = Goods.objects.filter(
                    is_published=True, author=request.user
                ).order_by("-id")
                context["categories"] = Category.objects.filter(is_published=True)
                return render(request, "shop/my_items.html", context)
        except:
            pass
    request.session["last_product"] = title
    context = {}
    product = Goods.objects.get(id=int(title))
    context["categories"] = Category.objects.filter(is_published=True)
    if "last_product" in request.session:
        try:
            context["last_product"] = Goods.objects.get(
                id=request.session["last_product"]
            )
        except:
            pass
    context["product"] = product
    context["site_title"] = title
    context["is_author"] = request.user == product.author
    context["is_active"] = product.is_active
    return render(request, "shop/product.html", context)


def create_post(request):
    if request.method == "POST":
        data = request.POST
        cat = Category.objects.get(id=int(data["category"]))
        Goods.objects.create(
            title=data["title"],
            category=cat,
            price=float(data["cost"]),
            image=request.FILES["image"],
            text=data["description"],
            author=request.user,
        )
        return redirect(f"/categories/{cat.id}/")

    context = {}
    context["categories"] = Category.objects.filter(is_published=True)
    if "last_product" in request.session:
        try:

            context["last_product"] = Goods.objects.get(
                id=request.session["last_product"]
            )
        except:
            pass
    context["site_title"] = _("make_order")
    return render(request, "shop/order.html", context)


class MySearchView(SearchView):
    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.filter(is_published=True)
        if "last_product" in self.request.session:
            try:
                context["last_product"] = Goods.objects.get(
                    id=self.request.session["last_product"]
                )
            except:
                pass
        context["site_title"] = "{} | {}".format(_("search"), self.queryset.query)
        return context


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
