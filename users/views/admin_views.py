from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from calendar import month_name
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from categories.models import Category
from orders.models import Order


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
def admin_dashboard(request):
    today = timezone.now().date()
    current_year = today.year

    # Get monthly revenue for current year
    monthly_revenue = (
        Order.objects.filter(created__year=current_year, status="completed")
        .annotate(month=ExtractMonth("created"))
        .values("month")
        .annotate(revenue=Sum("total_amount"))
        .order_by("month")
    )

    # Create revenue data for all months (including 0 for months with no revenue)
    revenue_by_month = [0] * 12
    for item in monthly_revenue:
        revenue_by_month[item["month"] - 1] = float(item["revenue"] or 0)

    # Get month names
    month_names = list(month_name)[1:]  # Skip empty string at index 0

    context = {
        "pending_orders": Order.objects.filter(status="pending").count(),
        "cancelled_orders": Order.objects.filter(status="cancelled").count(),
        "processing_orders": Order.objects.filter(status="processing").count(),
        "today_income": Order.objects.filter(
            created__date=today, status="completed"
        ).aggregate(Sum("total_amount"))["total_amount__sum"]
        or 0.00,
        "recent_orders": Order.objects.order_by("-created")[:10],
        "month_names": month_names,
        "monthly_revenue": revenue_by_month,
    }

    return render(request, "users/admin/index.html", context)


@login_required
def admin_orders(request):
    # Get filter parameters
    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")

    # Base queryset
    orders = Order.objects.select_related(
        "user", "shipping_address", "billing_address"
    ).all()

    # Apply filters
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query)
            | Q(user__email__icontains=search_query)
            | Q(address__street_address__icontains=search_query)
        )

    if status_filter and status_filter != "all":
        orders = orders.filter(status=status_filter)

    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get("page", 1)
    orders_page = paginator.get_page(page_number)

    context = {
        "orders": orders_page,
        "search_query": search_query,
        "status_filter": status_filter,
        "status_choices": Order.StatusChoices.choices,
    }

    return render(request, "users/admin/orders/index.html", context)


@login_required
@user_passes_test(is_admin)
def admin_order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related(
            "shipping_address", "billing_address", "user"
        ).prefetch_related("items", "items__product"),
        id=order_id,
    )

    context = {
        "order": order,
    }
    return render(request, "users/admin/orders/detail.html", context)


def admin_order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "users/admin/orders/edit.html", {"order": order})


@user_passes_test(is_admin)
def admin_categories(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "users/admin/categories/index.html", context)


@user_passes_test(is_admin)
def admin_category_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        status = request.POST.get("status")
        image = request.FILES.get("image")

        category = Category.objects.create(
            name=name, status=status, image=image
        )
        messages.success(request, "Category added successfully!")
        return redirect("users:admin_categories")

    return render(request, "users/admin/categories/add.html")


@user_passes_test(is_admin)
def admin_category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.name = request.POST.get("name")
        category.status = request.POST.get("status")

        if "image" in request.FILES:
            category.image = request.FILES["image"]

        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect("users:admin_categories")

    context = {"category": category}
    return render(request, "users/admin/categories/edit.html", context)
