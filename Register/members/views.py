from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404

from django.urls import reverse

from queueing.models import QueueTicket
from registrator.models import Section, SubService, AssignedService
from .models import CustomUser, OperatorProfile
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        # Agar foydalanuvchi login bo‘lgan bo‘lsa, uni dashboard sahifasiga yo‘naltiramiz
        if request.user.is_authenticated:
            return redirect(reverse('service-dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('service-dashboard')


CustomUser = get_user_model()


@login_required
def staff_add(request):
    if request.method == "POST":
        # 🔎 Foydalanuvchidan kelgan ma'lumotlarni olish
        second = request.POST.get("second_name", "").strip()
        first = request.POST.get("first_name", "").strip()
        third = request.POST.get("third_name", "").strip()
        full_name = f"{second} {first} {third}".strip()

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        print(password, confirm_password)

        gender = request.POST.get("gender")
        department = request.POST.get("department_name")
        staff_position = request.POST.get("staff_position")
        user_role = request.POST.get("user_role")

        # 🧾 Debug printlar
        print("🚀 Yangi foydalanuvchi qo‘shish jarayoni boshlandi:")
        print(f"👤 Full name: {full_name}")
        print(f"🔑 Username: {username}")
        print(f"📌 Gender: {gender}")
        print(f"🏢 Bo‘lim: {department}")
        print(f"📎 Lavozim: {staff_position}")
        print(f"🧾 Role: {user_role}")
        print(f"✅ Parol mosligi: {password == confirm_password}")

        # ✅ Formani tekshirish
        if not all([second, first, username, password, confirm_password, gender, department, staff_position, user_role]):
            print("❌ Xatolik: Barcha majburiy maydonlar to‘ldirilmagan!")
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to‘ldiring!")
            return redirect("staff-add")

        if password != confirm_password:
            print("❌ Xatolik: Parollar mos emas!")
            messages.error(request, "Parollar bir-biriga mos emas!")
            return redirect("staff-add")

        if CustomUser.objects.filter(username=username).exists():
            print("❌ Xatolik: Username allaqachon mavjud!")
            messages.error(request, "Ushbu username allaqachon band!")
            return redirect("staff-add")

        # ✅ Rollarni ajratish
        is_superuser = user_role == "admin"
        is_staff = is_superuser
        is_operator = user_role == "operator"
        is_leader = user_role == "leader"

        print(f"🛡 is_superuser: {is_superuser}, is_staff: {is_staff}, is_operator: {is_operator}, is_leader: {is_leader}")

        # ✅ Foydalanuvchini yaratish
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            full_name=full_name,
            first_name_native=first,
            second_name=second,
            third_name=third,
            gender=gender,
            department_name=department,
            staff_position=staff_position,
            is_superuser=is_superuser,
            is_staff=is_staff
        )

        # ✅ Qo‘shimcha flaglar (agar mavjud bo‘lsa)
        if hasattr(user, 'is_operator'):
            user.is_operator = is_operator
        if hasattr(user, 'is_leader'):
            user.is_leader = is_leader
        user.save()

        print("✅ Foydalanuvchi muvaffaqiyatli yaratildi:", user)

        messages.success(request, "✅ Hodim muvaffaqiyatli qo‘shildi.")
        return redirect("staff-add")

    # Hodimlar ro‘yxatini chiqarish
    users = CustomUser.objects.all().order_by('-id')
    return render(request, "members/staff_add.html", {"users": users})


def check_username(request):
    username = request.GET.get("username")
    is_available = not CustomUser.objects.filter(username=username).exists()
    return JsonResponse({"available": is_available})


# views.py
def get_operator_level_icon(level):
    return {
        "VIP": ("👑", "VIP"),
        "Usta": ("🔥", "Usta"),
        "Yaxshi": ("🌟", "Yaxshi"),
        "Oddiy": ("⭐", "Oddiy"),
        "Boshlovchi": ("🟢", "Boshlovchi")
    }.get(level, ("🟢", "Boshlovchi"))

class StaffListView(ListView):
    model = CustomUser
    template_name = 'members/staff_list.html'
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = CustomUser.objects.all().order_by('full_name')
        if query:
            qs = qs.filter(full_name__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        operator_profiles = OperatorProfile.objects.in_bulk(field_name='operator')

        stats = {}
        for user in context['users']:
            profile = operator_profiles.get(user.id)
            level = profile.level if profile else "Boshlovchi"
            icon, level_text = get_operator_level_icon(level)
            today_count = QueueTicket.objects.filter(served_by=user, ended_at__date=today, status='done').count()
            total_count = QueueTicket.objects.filter(served_by=user, status='done').count()

            stats[user.id] = {
                'level': level_text,
                'icon': icon,
                'today_count': today_count,
                'total_count': total_count,
                'is_superuser': user.is_superuser,
                'is_leader': getattr(user, 'is_leader', False),
                'is_operator': getattr(user, 'is_operator', False),
            }

        context['stats'] = stats
        return context


class ResetPasswordView(View):
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.password = make_password("namdpi451")
        user.save()
        messages.success(request, f"{user.full_name} uchun parol yangilandi: namdpi451")
        return redirect(reverse('staff-list'))


class DeleteStaffView(View):
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        messages.success(request, f"{user.full_name} o‘chirildi.")
        return redirect(reverse('staff-list'))


class AssignServiceView(View):
    def get(self, request):
        user_id = request.GET.get("user_id")
        selected_user = CustomUser.objects.filter(id=user_id).first() if user_id else None
        sections = Section.objects.all()
        users = CustomUser.objects.all()
        assignments = AssignedService.objects.filter(user=selected_user) if selected_user else []

        if selected_user:
            assigned_ids = assignments.values_list("service_id", flat=True)
            available_subservices = SubService.objects.exclude(id__in=assigned_ids)
        else:
            available_subservices = SubService.objects.none()

        context = {
            "selected_user": selected_user,
            "users": users,
            "sections": sections,
            "assignments": assignments,
            "available_subservices": available_subservices
        }
        return render(request, "members/assign_services.html", context)

    def post(self, request):
        user_id = request.POST.get("user")
        subservices = request.POST.getlist("subservices")

        user = get_object_or_404(CustomUser, id=user_id)

        added = 0
        for ss_id in subservices:
            service = get_object_or_404(SubService, id=ss_id)
            if not AssignedService.objects.filter(user=user, service=service).exists():
                AssignedService.objects.create(user=user, service=service)
                added += 1

        if added:
            messages.success(request, f"{added} ta xizmat biriktirildi.")

        return redirect(f"{request.path}?user_id={user.id}")


class BulkAssignSubServicesView(View):
    def post(self, request):
        user_id = request.POST.get('user')
        subservice_ids = request.POST.getlist('subservices')
        user = get_object_or_404(CustomUser, id=user_id)

        for sid in subservice_ids:
            service = get_object_or_404(SubService, id=sid)
            AssignedService.objects.get_or_create(user=user, service=service)

        messages.success(request, "Xizmatlar muvaffaqiyatli biriktirildi.")
        return redirect(f"{reverse('assign-services')}?user_id={user.id}")


class UnassignServiceView(View):
    def post(self, request, pk):
        assignment = get_object_or_404(AssignedService, id=pk)
        user_id = request.POST.get("user")
        assignment.delete()
        messages.success(request, "Xizmat muvaffaqiyatli olib tashlandi.")
        return redirect(f"/staff/assign/?user_id={user_id}")
