from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum

from orders.models import Order


@login_required
def admin_dashboard(request):
    today = timezone.now().date()

    context = {
        "pending_orders": Order.objects.filter(status="pending").count(),
        "cancelled_orders": Order.objects.filter(status="cancelled").count(),
        "processing_orders": Order.objects.filter(status="processing").count(),
        "today_income": Order.objects.filter(
            created__date=today, status="completed"
        ).aggregate(Sum("total_amount"))["total_amount__sum"]
        or 0.00,
        "recent_orders": Order.objects.order_by("-created")[:10],
    }

    return render(request, "users/admin/index.html", context)
