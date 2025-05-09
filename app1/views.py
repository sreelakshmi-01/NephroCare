from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

def userhome(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()  # Save the submitted question
            return redirect('userhome')
    else:
        form = FAQForm()

    faqs = FAQ.objects.filter(is_approved=True)
    features = Feature.objects.all()

    return render(request, 'userhome.html', {'form': form, 'faqs': faqs, 'features': features})

def adminbase(request):
    return render(request, 'adminbase.html')

def kyk(request):
    return render(request, 'kyk.html')


def feature_list(request):
    # Fetch all features to display in the admin panel
    features = Feature.objects.all()
    return render(request, 'add_feature.html', {'features': features})

def add_feature(request):
    if request.method == "POST":
        form = FeatureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('userhome') 
    else:
        form = FeatureForm()

    # Fetch all features to display in the admin panel
    features = Feature.objects.all()
    return render(request, 'add_feature.html', {'form': form, 'features': features})


def edit_feature(request, id):
    feature = get_object_or_404(Feature, id=id)
    if request.method == 'POST':
        form = FeatureForm(request.POST, request.FILES, instance=feature)
        if form.is_valid():
            form.save()
            return redirect('feature_list')
    else:
        form = FeatureForm(instance=feature)

    return render(request, 'edit_feature.html', {'form': form})


def delete_feature(request, id):
    feature = get_object_or_404(Feature, id=id)
    feature.delete()
    return redirect('feature_list')

def faq(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('userhome')
    else:
        form = FAQForm()

    # Show only approved FAQs to the user
    faqs = FAQ.objects.filter(is_approved=True)
    return render(request, 'userhome.html', {'form': form, 'faqs': faqs})

def admin_faq(request):
    pending_faqs = FAQ.objects.filter(is_approved=False)

    approved_faqs = FAQ.objects.filter(is_approved=True)

    if request.method == "POST":
        # Process the answer and approval for each FAQ
        faq_id = request.POST.get("faq_id")
        answer = request.POST.get("answer")
        faq = get_object_or_404(FAQ, id=faq_id)

        faq.answer = answer
        faq.is_approved = True
        faq.save()

        return redirect('admin_faq')

    return render(request, 'admin_faq.html', {
        'pending_faqs': pending_faqs,
        'approved_faqs': approved_faqs
    })

def delete_faq(request, id):
    faq = get_object_or_404(FAQ, id=id)
    faq.delete()
    return redirect('admin_faq')

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        User.objects.create(name=name, email=email, password=password)

        return redirect("login")

    return render(request, "user_register.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")

def add_dcenter(request):
    centers = DialysisCenter.objects.all()
    if request.method == 'POST':
        form = DialysisCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_dcenter')
    else:
        form = DialysisCenterForm()

    return render(request, 'add_dcenter.html', {'form': form, 'centers': centers})

def edit_dcenter(request, center_id):
    center = get_object_or_404(DialysisCenter, id=center_id)
    if request.method == 'POST':
        form = DialysisCenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            return redirect('add_dcenter')
    else:
        form = DialysisCenterForm(instance=center)

    return render(request, 'edit_dcenter.html', {'form': form, 'center': center})

def delete_dcenter(request, center_id):
    center = get_object_or_404(DialysisCenter, id=center_id)
    center.delete()
    return redirect('add_dcenter')

def dialysis_center(request):
    # Fetch unique districts from the database
    districts = DialysisCenter.objects.values_list('district', flat=True).distinct()

    selected_district = request.GET.get('district')
    if selected_district:
        centers = DialysisCenter.objects.filter(district=selected_district)
    else:
        centers = DialysisCenter.objects.all()

    return render(request, 'dialysis_center.html', {'centers': centers, 'districts': districts})

def gfr(request):
    return render(request, "gfr.html")

def diet(request):
    return render(request, 'diet.html')

def add_hospital(request):
    hosps = Hospital.objects.all()
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_hospitals')
    else:
        form = HospitalForm()

    return render(request, 'add_hospitals.html', {'form': form, 'hosps': hosps})

def edit_hosp(request, hosp_id):
    hosp = get_object_or_404(Hospital, id=hosp_id)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hosp)
        if form.is_valid():
            form.save()
            return redirect('add_hospitals')
    else:
        form = HospitalForm(instance=hosp)

    return render(request, 'edit_hospital.html', {'form': form, 'hosp': hosp})

def delete_hosp(request, hosp_id):
    hosp = get_object_or_404(Hospital, id=hosp_id)
    hosp.delete()
    return redirect('add_hospitals')

def hospital_list(request):
    districts = Hospital.objects.values_list('district', flat=True).distinct()

    selected_district = request.GET.get('district')
    if selected_district:
        hosps = Hospital.objects.filter(district=selected_district)
    else:
        hosps = Hospital.objects.all()

    return render(request, 'book_appointment.html', {'hosps': hosps, 'districts': districts})


def doctor_registration(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    doctor = form.save()

                    User.objects.create(
                        name=doctor.name,
                        email=doctor.email,
                        password=doctor.password,
                        role='doctor'
                    )

                    messages.success(request, "Doctor registered successfully!")
                    return redirect('login')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = DoctorForm()

    hospitals = Hospital.objects.all()
    return render(request, 'doctor_register.html', {'form': form, 'hospitals': hospitals})


def doctor_dashboard(request):
    if 'user_id' not in request.session or request.session.get('user_role') != 'doctor':
        return redirect('login')

    try:
        doctor = Doctor.objects.get(email=request.session.get('email'))
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found!")
        return redirect('login')

    # ✅ Fetch appointments for this doctor
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')

    return render(request, 'doctor_home.html', {
        'doctor': doctor,
        'appointments': appointments
    })
from django.http import JsonResponse

def toggle_doctor_status(request):
    if request.method == "POST" and request.session.get('email'):
        try:
            doctor = Doctor.objects.get(email=request.session.get('email'))
            doctor.status = "No" if doctor.status == "Yes" else "Yes"
            doctor.save()
            return JsonResponse({'status': doctor.status})
        except Doctor.DoesNotExist:
            return JsonResponse({'error': 'Doctor not found'}, status=404)
    return JsonResponse({'error': 'Unauthorized'}, status=401)


def doctor_list(request, hosp_id):
    doctors = Doctor.objects.filter(hospital_id = hosp_id)
    return render(request, 'doctor_list.html', {'doctors': doctors})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['user_role'] = user.role
                request.session['email'] = user.email


                print(f"User role in session: {request.session.get('user_role')}")


                next_url = request.session.get('next')
                if next_url:
                    del request.session['next']
                    return redirect(next_url)

                return redirect(
                    'adminbase' if user.role == "admin" else
                    'doctor_dashboard' if user.role == "doctor" else
                    'userhome'
                )

            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User does not exist")

    return render(request, "login.html")


def book(request, doctor_id):

    # 🔐 Require login
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to book an appointment.")
        request.session['next'] = request.path
        return redirect('login')

    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)

    if user.role != 'user':
        messages.error(request, "Only users can book appointments.")
        return redirect('login')

    doctor = get_object_or_404(Doctor, id=doctor_id)
    hospital = doctor.hospital

    appointments = Appointment.objects.filter(user=user).order_by('-date')
    if request.method == 'POST':
        print("🔔 Form submitted")
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        age = request.POST['age']
        gender = request.POST['gender']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        date = request.POST['date']
        timing = request.POST['timing']

        Appointment.objects.create(
            user=user,
            name=name,
            mobile=mobile,
            email=email,
            age=age,
            gender=gender,
            address=address,
            state=state,
            city=city,
            pincode=pincode,
            hospital=hospital,
            doctor=doctor,
            date=date,
            timing=timing
        )
        messages.success(request, 'Appointment booked successfully!')
        return redirect('book', doctor_id=doctor.id)

    return render(request, 'booking_page.html', {
        'doctor': doctor,
        'hospital': hospital,
        'appointments': appointments,
        'user_id': user_id,
    })


from django.contrib.auth.hashers import make_password  # Optional: for secure password saving
from .models import User, UserProfile


def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)

    appointments = Appointment.objects.filter(user=user).order_by('-date')

    if request.method == "POST":
        # Update User model
        user.name = request.POST.get("name")
        password = request.POST.get("password")
        if password:
            user.password = password  # Optional: hash with make_password(password)
        user.save()

        # Update Profile model
        profile.age = request.POST.get("age")
        profile.phone = request.POST.get("phone")
        profile.state = request.POST.get("state")
        profile.city = request.POST.get("city")
        profile.pincode = request.POST.get("pincode")
        profile.address = request.POST.get("address")
        profile.save()

        messages.success(request, "Profile updated successfully!")

        appointments = Appointment.objects.filter(user=user).order_by('-date')

    return render(request, "profile.html", {
        "user": user,
        "profile": profile,
        "appointments": appointments,
    })
from django.db.models import Q

def admin_appointments(request):
    hospital_id = request.GET.get('hospital')
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')

    appointments = Appointment.objects.all()

    if hospital_id:
        appointments = appointments.filter(hospital__id=hospital_id)
    if doctor_id:
        appointments = appointments.filter(doctor__id=doctor_id)
    if date:
        appointments = appointments.filter(date=date)

    hospitals = Hospital.objects.all()
    doctors = Doctor.objects.all()

    context = {
        'appointments': appointments,
        'hospitals': hospitals,
        'doctors': doctors,
        'selected_hospital': hospital_id,
        'selected_doctor': doctor_id,
        'selected_date': date,
    }

    return render(request, 'admin_appointments.html', context)

def add_stage(request):
    if request.method == 'POST':
        form = StageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_stage')
    else:
        form = StageForm()
    return render(request, 'add_stage.html', {'form': form})

def add_diet_plan(request):
    if request.method == 'POST':
        form = DietPlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_diet_plan')
    else:
        form = DietPlanForm()
    return render(request, 'add_diet_plan.html', {'form': form})

def add_workout_plan(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_workout_plan')
    else:
        form = WorkoutPlanForm()
    return render(request, 'add_workout_plan.html', {'form': form})

def stage_detail(request, stage_id):
    stage = get_object_or_404(Stage, pk=stage_id)
    diet_plans = DietPlan.objects.filter(stage=stage)
    workout_plans = WorkoutPlan.objects.filter(stage=stage)
    return render(request, 'stage_detail.html', {
        'stage': stage,
        'diet_plans': diet_plans,
        'workout_plans': workout_plans
    })

def admin_doctors(request):
    hospital_id = request.GET.get('hospital')
    doctors = Doctor.objects.all()
    hospitals = Hospital.objects.all()

    if hospital_id:
        doctors = doctors.filter(hospital_id=hospital_id)

    context = {
        'doctors': doctors,
        'hospitals': hospitals,
        'selected_hospital': hospital_id,
    }
    return render(request, 'admin_doctors.html', context)


def admin_doctors(request):
    hospital_id = request.GET.get('hospital')
    doctors = Doctor.objects.all()
    hospitals = Hospital.objects.all()

    if hospital_id:
        doctors = doctors.filter(hospital_id=hospital_id)

    return render(request, 'admin_doctors.html', {
        'doctors': doctors,
        'hospitals': hospitals,
        'selected_hospital': hospital_id
    })

def admin_doctor_view(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'admin_doctor_view.html', {'doctor': doctor})

def admin_doctor_edit(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('admin_doctors')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'admin_doctor_edit.html', {'form': form})


def admin_doctor_delete(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect('admin_doctors')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment

@csrf_exempt
def mark_completed(request, appt_id):
    if request.method == "POST":
        try:
            appt = Appointment.objects.get(id=appt_id)
            appt.status = "Completed"
            appt.save()
            return JsonResponse({"success": True})
        except Appointment.DoesNotExist:
            return JsonResponse({"success": False})

def medicine_store(request):
    return render(request, 'medicine.html')
