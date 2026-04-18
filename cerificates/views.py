from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Certificate
import uuid


# ─── HOME ──────────────────────────────────────────────────────────────────────
def home(request):
    certificates = Certificate.objects.filter(status='valid')[:6]
    return render(request, 'certificates/index.html', {'certificates': certificates})


# ─── SEARCH ────────────────────────────────────────────────────────────────────
def search(request):
    query   = request.GET.get('q', '').strip()
    results = []
    error   = None

    if query:
        # Try UUID match first
        try:
            uid = uuid.UUID(query)
            results = Certificate.objects.filter(certificate_id=uid)
        except ValueError:
            # Fall back to name / course search
            results = Certificate.objects.filter(
                Q(student_name__icontains=query) |
                Q(course_title__icontains=query)
            )

        if not results.exists():
            error = f'No certificates found for "{query}".'

    return render(request, 'certificates/search_results.html', {
        'query':   query,
        'results': results,
        'error':   error,
    })


# ─── VERIFY ────────────────────────────────────────────────────────────────────
def verify(request, certificate_id=None):
    cert  = None
    error = None

    if request.method == 'POST':
        raw = request.POST.get('certificate_id', '').strip()
        try:
            uid  = uuid.UUID(raw)
            cert = Certificate.objects.get(certificate_id=uid)
        except (ValueError, Certificate.DoesNotExist):
            error = 'Certificate not found. Please check the ID and try again.'

    elif certificate_id:
        try:
            cert = Certificate.objects.get(certificate_id=certificate_id)
        except Certificate.DoesNotExist:
            error = 'Certificate not found.'

    return render(request, 'certificates/verify.html', {
        'cert':  cert,
        'error': error,
    })


# ─── CERTIFICATE DETAIL ────────────────────────────────────────────────────────
def certificate_detail(request, certificate_id):
    cert = get_object_or_404(Certificate, certificate_id=certificate_id)
    return render(request, 'certificates/certificate_detail.html', {'cert': cert})


# ─── AUTH: SIGNUP ──────────────────────────────────────────────────────────────
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f'Welcome, {username}! Account created.')
            return redirect('home')

    return render(request, 'certificates/signup.html')


# ─── AUTH: LOGIN ───────────────────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'certificates/login.html')


# ─── AUTH: LOGOUT ──────────────────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    return redirect('home')


# ─── PROFILE ──────────────────────────────────────────────────────────────────
@login_required
def profile_view(request):
    return render(request, 'certificates/profile.html', {'user': request.user})