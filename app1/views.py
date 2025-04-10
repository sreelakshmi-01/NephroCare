from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

# User home view
def userhome(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()  # Save the submitted question
            return redirect('userhome')  # Redirect to avoid resubmission on refresh
    else:
        form = FAQForm()

    # Get the approved FAQs to display on the page
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

# Add feature view (for admin to add a new feature)
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


# Edit feature view (for admin to edit a feature)
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


# Delete feature view (for admin to delete a feature)
def delete_feature(request, id):
    feature = get_object_or_404(Feature, id=id)
    feature.delete()
    return redirect('feature_list')

def faq(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('userhome')  # Redirect after successful submission
    else:
        form = FAQForm()

    # Show only approved FAQs to the user
    faqs = FAQ.objects.filter(is_approved=True)
    return render(request, 'userhome.html', {'form': form, 'faqs': faqs})

# View for Admin to Approve & Answer Questions
def admin_faq(request):
    # Get pending FAQs (not approved)
    pending_faqs = FAQ.objects.filter(is_approved=False)

    # Get approved FAQs
    approved_faqs = FAQ.objects.filter(is_approved=True)

    if request.method == "POST":
        # Process the answer and approval for each FAQ
        faq_id = request.POST.get("faq_id")
        answer = request.POST.get("answer")
        faq = get_object_or_404(FAQ, id=faq_id)

        # Update the FAQ with the provided answer and approve it
        faq.answer = answer
        faq.is_approved = True
        faq.save()

        return redirect('admin_faq')  # Redirect to refresh the page after form submission

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

        # Create and save user to the database
        User.objects.create(name=name, email=email, password=password)

        return redirect("login")

    return render(request, "user_register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.password == password:  # No hashing for now
                request.session['user_id'] = user.id  # Store user session
                request.session['user_role'] = user.role  # Store role for redirection
                request.session['email'] = user.email  # Store email for fetching doctor data

                # Debugging
                print(f"User role in session: {request.session.get('user_role')}")

                return redirect(
                    'adminbase' if user.role == "admin" else 'doctor_dashboard' if user.role == "doctor" else 'userhome')

            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User does not exist")

    return render(request, "login.html")

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
            return redirect('add_dcenter')  # Redirect back to main page
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

    # Apply filter if a district is selected
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
    # Fetch unique districts from the database
    districts = Hospital.objects.values_list('district', flat=True).distinct()

    # Apply filter if a district is selected
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

                    # Create user entry in the User table
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
            print(form.errors)  # Debugging: Print form errors in console
            messages.error(request, "Invalid form data.")
    else:
        form = DoctorForm()

    hospitals = Hospital.objects.all()
    return render(request, 'doctor_register.html', {'form': form, 'hospitals': hospitals})


def doctor_dashboard(request):
    if 'user_id' not in request.session or request.session.get('user_role') != 'doctor':
        return redirect('login')  # Redirect if not logged in or wrong role

    try:
        doctor = Doctor.objects.get(email=request.session.get('email'))
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found!")
        return redirect('login')

    return render(request, 'doctor_home.html', {'doctor': doctor})

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
from django.shortcuts import render, get_object_or_404, redirect
from .models import Hospital, Doctor, Appointment
from django.contrib import messages

def book(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    hospital = doctor.hospital

    if request.method == 'POST':
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
        return redirect('book')

    return render(request, 'booking_page.html', {
        'doctor': doctor,
        'hospital': hospital,
    })
