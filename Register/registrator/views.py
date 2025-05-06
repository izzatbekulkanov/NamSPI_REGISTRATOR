from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.http import JsonResponse
from django.template.loader import render_to_string

from members.models import DailyWorkWindow, OperatorProfile
from .models import Section, SubService, AssignedService
from .forms import SectionForm, SubServiceForm, AssignedServiceForm
from queueing.models import QueueTicket


@login_required
def dashboard(request):
    today = now().date()

    # Bugungi oyna holatini olish
    try:
        work_window = DailyWorkWindow.objects.get(operator=request.user, date=today)
        has_window = True
        window_number = work_window.window_number
        is_leader = work_window.is_leader
    except DailyWorkWindow.DoesNotExist:
        has_window = False
        window_number = None
        is_leader = False

    # Bugungi va umumiy xizmatlar soni
    today_count = QueueTicket.objects.filter(
        served_by=request.user,
        status='done',
        ended_at__date=today
    ).count()

    total_count = QueueTicket.objects.filter(
        served_by=request.user,
        status='done'
    ).count()

    # Operator darajasi
    profile, _ = OperatorProfile.objects.get_or_create(operator=request.user)
    level = profile.level or "Boshlovchi"

    level_icons = {
        "Boshlovchi": "🟢",
        "Oddiy": "⭐",
        "Yaxshi": "🌟",
        "Usta": "🔥",
        "VIP": "👑"
    }
    level_icon = level_icons.get(level, "🟢")

    return render(request, 'services/dashboard.html', {
        'has_window': has_window,
        'window_number': window_number,
        'is_leader': is_leader,
        'today_count': today_count,
        'total_count': total_count,
        'level': level,
        'level_icon': level_icon,
        'today': today,  # agar boshqa joyda ham kerak bo‘lsa
    })


@require_POST
@login_required
def set_daily_window(request):
    today = now().date()
    is_leader = request.POST.get("is_leader") == "yes"  # "yes" bo‘lsa True

    if is_leader:
        window_number = None  # Rahbarga oyna raqami kerak emas
    else:
        window_number = request.POST.get("window_number")
        if not window_number:
            messages.error(request, "Oyna raqami kiritilishi shart.")
            return redirect("service-dashboard")

    DailyWorkWindow.objects.update_or_create(
        operator=request.user,
        date=today,
        defaults={
            "window_number": int(window_number) if window_number else None,
            "is_leader": is_leader
        }
    )
    return redirect("service-dashboard")


def service_dashboard(request):
    sections = Section.objects.all()
    subservices = SubService.objects.select_related('section')
    assignments = AssignedService.objects.select_related('user', 'service')

    active_tab = request.session.pop("active_tab", "section")

    if request.method == "POST":
        active_tab = request.POST.get("active_tab", "section")
        request.session["active_tab"] = active_tab

        if 'section_submit' in request.POST:
            form = SectionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Bo‘lim muvaffaqiyatli saqlandi.")
                return redirect("service-dashboard")

        elif 'subservice_submit' in request.POST:
            form = SubServiceForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Xizmat muvaffaqiyatli qo‘shildi.")
                return redirect("service-dashboard")

    context = {
        'sections': sections,
        'subservices': subservices,
        'section_form': SectionForm(),
        'subservice_form': SubServiceForm(),
        'assigned_form': AssignedServiceForm(),
        'active_tab': active_tab,
    }
    return render(request, 'services/services.html', context)


def delete_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section.delete()
        messages.success(request, "Bo‘lim o‘chirildi.")
        return redirect(f"{request.META.get('HTTP_REFERER', '/')}?tab=section")
    return redirect('service-dashboard')


def delete_subservice(request, pk):
    subservice = get_object_or_404(SubService, pk=pk)
    if request.method == 'POST':
        subservice.delete()
        messages.success(request, "Xizmat o‘chirildi.")
        return redirect(f"{request.META.get('HTTP_REFERER', '/')}?tab=subservice")
    return redirect('service-dashboard')


def delete_assignment(request, pk):
    assignment = get_object_or_404(AssignedService, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, "Biriktirish o‘chirildi.")
        return redirect(f"{request.META.get('HTTP_REFERER', '/')}?tab=assign")
    return redirect('service-dashboard')


@login_required
def operator_queue_view(request):
    assigned_services = AssignedService.objects.filter(user=request.user).values_list('service_id', flat=True)
    assigned_services = list(assigned_services)

    waiting_tickets = QueueTicket.objects.filter(service_id__in=assigned_services, status="waiting").order_by(
        'created_at')
    serving_ticket = QueueTicket.objects.filter(service_id__in=assigned_services, status="serving",
                                                served_by=request.user).first()
    done_tickets = QueueTicket.objects.filter(service_id__in=assigned_services, status="done",
                                              served_by=request.user).order_by('-ended_at')[:20]

    for d in done_tickets:
        if d.started_at and d.ended_at:
            delta = d.ended_at - d.started_at
            total_seconds = int(delta.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            d.duration_display = f"{minutes} daq {seconds} son"
        else:
            d.duration_display = "-"

    return render(request, 'services/operator_queue.html', {
        'waiting_tickets': waiting_tickets,
        'serving_ticket': serving_ticket,
        'done_tickets': done_tickets,
    })


@login_required
def ajax_waiting_tickets(request):
    assigned = AssignedService.objects.filter(user=request.user).values_list('service_id', flat=True)
    waiting_tickets = QueueTicket.objects.filter(service_id__in=assigned, status='waiting').order_by('created_at')
    html = render_to_string('services/_waiting_tickets.html', {'waiting_tickets': waiting_tickets}, request=request)
    return JsonResponse({'html': html})


@login_required
def ajax_serving_ticket(request):
    assigned = AssignedService.objects.filter(user=request.user).values_list('service_id', flat=True)
    serving_ticket = QueueTicket.objects.filter(service_id__in=assigned, status='serving',
                                                served_by=request.user).first()
    html = render_to_string('services/_serving_ticket.html', {'serving_ticket': serving_ticket}, request=request)
    return JsonResponse({'html': html})


@login_required
def ajax_done_tickets(request):
    assigned_services = AssignedService.objects.filter(user=request.user).values_list('service_id', flat=True)

    done_tickets = QueueTicket.objects.filter(
        service_id__in=assigned_services,
        status="done",
        served_by=request.user
    ).order_by('-ended_at')[:20]

    for ticket in done_tickets:
        if ticket.started_at and ticket.ended_at:
            delta = ticket.ended_at - ticket.started_at
            seconds = int(delta.total_seconds())
            m, s = divmod(seconds, 60)
            ticket.duration_display = f"{m} daq {s} son"
        else:
            ticket.duration_display = "-"

    html = render_to_string("services/_done_tickets.html", {
        "done_tickets": done_tickets
    }, request=request)

    return JsonResponse({"html": html})


@require_POST
@login_required
def serve_ticket(request, ticket_id):
    ticket = get_object_or_404(QueueTicket, id=ticket_id)
    assigned_services = AssignedService.objects.filter(user=request.user).values_list('service_id', flat=True)

    print(f"🆔 Operator: {request.user.username} | Ticket ID: {ticket_id} | Status: {ticket.status}")

    if ticket.service_id in assigned_services and ticket.status == "waiting":
        print(f"✅ {ticket.ticket_number} xizmat navbatda — qabul qilishga ruxsat bor.")

        # Avval yakunlanmagan xizmat bormi?
        existing_serving = QueueTicket.objects.filter(
            service_id__in=assigned_services,
            status="serving",
            served_by=request.user
        ).first()

        if existing_serving:
            print(f"⚠️ Avvalgi xizmat yakunlanmagan: {existing_serving.ticket_number}")
            messages.error(request, f"❗️ Avval {existing_serving.ticket_number} raqamli xizmatni yakunlang.")
            return redirect('operator-queue')

        # Operatorning bugungi oyna raqamini aniqlash
        today = now().date()
        try:
            work_window = DailyWorkWindow.objects.get(operator=request.user, date=today)
            operator_window = work_window.window_number
            print(f"🪟 Operatorning bugungi oyna raqami: {operator_window}")
        except DailyWorkWindow.DoesNotExist:
            operator_window = None
            print("⚠️ Oyna raqami topilmadi")

        # Yangi xizmatni boshlash
        ticket.status = "serving"
        ticket.started_at = now()
        ticket.served_by = request.user
        ticket.window_number = operator_window
        ticket.save()

        print(f"🚀 Xizmat boshlandi: {ticket.ticket_number} | Operator: {request.user.get_full_name()} | Vaqt: {ticket.started_at.strftime('%H:%M:%S')}")

        messages.success(request, f"{ticket.ticket_number} - xizmat qabul qilindi.")

    else:
        print(f"❌ Ruxsat yo'q yoki ticket allaqachon qabul qilingan: {ticket.ticket_number}")

    return redirect('operator-queue')


def update_operator_profile(user, is_completed=True):
    profile, _ = OperatorProfile.objects.get_or_create(operator=user)
    if is_completed:
        profile.add_served()


@require_POST
@login_required
def complete_ticket(request, ticket_id):
    ticket = get_object_or_404(QueueTicket, id=ticket_id, served_by=request.user, status="serving")
    ticket.status = "done"
    ticket.result = "completed"
    ticket.ended_at = timezone.now()
    ticket.save()

    # Faqat bajarilgan bo‘lsa xizmat sonini oshiramiz
    update_operator_profile(request.user, is_completed=True)

    messages.success(request, f"✅ {ticket.ticket_number} - xizmat bajarildi!")
    return redirect('operator-queue')


@require_POST
@login_required
def cancel_ticket(request, ticket_id):
    ticket = get_object_or_404(QueueTicket, id=ticket_id, served_by=request.user, status="serving")
    ticket.status = "done"
    ticket.result = "rejected"
    ticket.ended_at = timezone.now()
    ticket.save()

    # Rad etilgan bo‘lsa son oshmaydi
    update_operator_profile(request.user, is_completed=False)

    messages.error(request, f"❌ {ticket.ticket_number} - xizmat rad etildi.")
    return redirect('operator-queue')
