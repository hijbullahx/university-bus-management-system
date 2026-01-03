from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages

def authority_required(view_func):
    """Decorator to check if user has AUTHORITY role"""
    return user_passes_test(lambda u: hasattr(u, 'profile') and u.profile.role == 'AUTHORITY')(view_func)

# The authority global settings view has been removed as GlobalSettings is no longer used.