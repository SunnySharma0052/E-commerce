from django.shortcuts import render, redirect
from .models import User, DeletedAccount
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from random import randint


# Create your views here.

# View to render the homepage with the accounts navbar
def accounts_navbar_view(request):
    return render(request, 'home.html')








# Signup view for new users
def signup_view(request):
    if request.method == 'POST':
        # Collect form data
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('emailid')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Server-side validations
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/signup.html')

        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, 'Phone number must be exactly 10 digits')
            return render(request, 'accounts/signup.html')

        if len(firstname) > 50 or len(lastname) > 50:
            messages.error(request, 'First Name and Last Name should not exceed 50 characters.')
            return render(request, 'accounts/signup.html')

        if len(address) > 80:
            messages.error(request, 'Address should not exceed 80 characters.')
            return render(request, 'accounts/signup.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'accounts/signup.html')

        # Check if email or phone already exists
        if User.objects.filter(email_id=email).exists():
            messages.error(request, 'Email is already registered')
            return render(request, 'accounts/signup.html')

        if User.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number is already registered')
            return render(request, 'accounts/signup.html')

        # Create new user
        new_user = User(
            first_name=firstname,
            last_name=lastname,
            email_id=email,
            phone=phone,
            address=address,
            password=make_password(password)
        )
        new_user.save()

        messages.success(request, 'Signup Successful! Please Log-in')
        return render(request, 'accounts/login.html')

    # If GET request, render the signup form
    return render(request, 'accounts/signup.html')














# Login view for user authentication
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('emailid', '')
        password = request.POST.get('password', '')

        user = User.objects.filter(email_id=email).first()

        if user is None:
            messages.error(request, "❌ Incorrect Email ID & Password")
            return redirect('login')

        # Check password
        if not check_password(password, user.password):
            messages.error(request, "❌ Incorrect Password")
            return redirect('login')

        # Handle deletion scenario
        if hasattr(user, 'deletion_info'):
            deletion = user.deletion_info
            if deletion.is_expired():
                user.delete()
                deletion.delete()
                messages.error(request, "❌ Your account was permanently deleted after 30 days.")
                return redirect('signup')
            else:
                deletion.delete()
                user.is_active = True
                user.save()
                messages.success(request, "✅ Your account has been recovered.")

        # ✅ Authentication success - Save custom session
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        request.session['phone'] = user.phone
        request.session['email_id'] = user.email_id
        request.session['is_authenticated'] = True

        return redirect('home')

    return render(request, 'accounts/login.html')







# Logout view
def logout_view(request):
    if request.session.get('is_authenticated'):
        request.session.flush()  # Clears all session data
        messages.success(request, "✅ You have been successfully logged out!")  # Logout success message
    return redirect('home')  







# Password Reset Views
def password_forget_view(request):
    if request.method == 'POST':
        if 'new-password' in request.POST:
            new_password = request.POST['new-password']
            confirm_password = request.POST['confirm-password']
            user = User.objects.get(id=request.POST['user-id'])

            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "✅ Your password has been successfully updated!")
                return redirect('login')
            else:
                messages.error(request, "❌ New and confirm passwords do not match!")
                return render(request, 'accounts/password_forget.html', {'OTP_Status': 'verified', 'User_Id': user.id})

        elif 'otp' in request.POST:
            user = User.objects.get(id=request.POST['user-id'])
            otp = request.POST['otp']

            if user.password_reset_code == otp:
                return render(request, 'accounts/password_forget.html', {'OTP_Status': 'verified', 'User_Id': user.id, 'success_message': 'OTP is verified'})
            else:
                messages.error(request, "❌ Incorrect OTP!")
                return render(request, 'accounts/password_forget.html', {'OTP_Status': 'generated', 'User_Id': user.id})

        else:
            email = request.POST['email-id']
            if User.objects.filter(email_id=email).exists():
                user = User.objects.get(email_id=email)
                otp = str(randint(100000, 999999))
                user.password_reset_code = otp
                user.save()

                subject = 'One Time Password (OTP) to reset your password'
                message = f"Your OTP to reset your password: {otp}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]

                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    messages.success(request, "✅ OTP has been successfully sent to your registered email!")
                    return render(request, 'accounts/password_forget.html', {'OTP_Status': 'generated', 'User_Id': user.id})
                except Exception:
                    messages.error(request, "❌ Something went wrong. Please try again!")
                    return render(request, 'accounts/password_forget.html')

            else:
                messages.error(request, "❌ Please enter a registered email ID!")
                return render(request, 'accounts/password_forget.html')

    return render(request, 'accounts/password_forget.html')












# Change password view
def change_password_view(request):
    if request.session.get('is_authenticated'):
        if request.method == 'POST':
            user = User.objects.get(email_id=request.session['email_id'])

            if check_password(request.POST['old-password'], user.password):
                if request.POST['new-password'] == request.POST['confirm-password']:
                    user.password = make_password(request.POST['new-password'])
                    user.save()
                    messages.success(request, "✅ Your password has been changed successfully! Please login again.")
                    request.session.flush()
                    return redirect('login')
                else:
                    messages.error(request, "❌ New and Confirm Passwords do not match!")
                    return redirect('accounts/change_password')
            else:
                messages.error(request, "❌ Incorrect Old Password!")
                return redirect('accounts/change_password')

        return render(request, 'accounts/change_password.html')
    else:
        return redirect('login')















# Profile view for authenticated users
def profile_view(request):
    if request.session['is_authenticated']:
        user = User.objects.get(email_id=request.session['email_id'])
        return render(request, 'accounts/profile.html', {'user': user})
    else:
        return redirect('login')











# Edit profile view
def profile_edit_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    try:
        user = User.objects.get(email_id=request.session['email_id'])
    except User.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        user.first_name = request.POST.get('full_name')
        user.phone = request.POST.get('phone')

        if 'image' in request.FILES:
            user.image = request.FILES['image']

        user.save()
        messages.success(request, "✅ Your profile has been successfully updated!")
        return redirect('profile')

    return render(request, 'accounts/profile_edit.html', {'user': user})













# Delete account view
def delete_account_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    try:
        user = User.objects.get(email_id=request.session['email_id'])
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    if request.method == 'POST':
        confirm_text = request.POST.get('confirm_text')
        password = request.POST.get('password')

        if confirm_text != 'DELETE':
            messages.error(request, "❌ You must type 'DELETE' to confirm account deletion.")
            return redirect('delete_account')

        if not check_password(password, user.password):
            messages.error(request, "❌ Incorrect password. Please try again.")
            return redirect('delete_account')

        user.is_active = False
        user.save()

        # Log deletion request
        DeletedAccount.objects.create(user=user)

        request.session.flush()
        messages.success(request, "🕒 Your account will be permanently deleted in 30 days. Log in before then to recover it.")
        return redirect('home')

    return render(request, 'accounts/delete_account.html')
