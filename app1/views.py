from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

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

                return redirect('adminbase' if user.role == "admin" else 'userhome')
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