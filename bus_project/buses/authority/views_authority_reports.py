from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import BusRoute, BusSchedule, BusLocation, IssueReport, UserProfile
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO

def authority_required(view_func):
    """Decorator to check if user has AUTHORITY role"""
    return user_passes_test(lambda u: hasattr(u, 'profile') and u.profile.role == 'AUTHORITY')(view_func)

@login_required
@authority_required
def reports_analytics(request):
    """Reports & Analytics dashboard for authority"""
    # Default date range: last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        report_type = request.POST.get('report_type')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Generate report data based on type
        report_data = generate_report_data(report_type, start_date, end_date)
        if report_data:
            report_data['formatted_type'] = report_data['type'].replace('_', ' ').title()
    else:
        report_data = None

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'report_data': report_data,
    }
    return render(request, 'buses/authority/reports_analytics.html', context)

def generate_report_data(report_type, start_date, end_date):
    """Generate data for the selected report type"""
    if report_type == 'route_popularity':
        return get_route_popularity_data(start_date, end_date)
    elif report_type == 'on_time_performance':
        return get_on_time_performance_data(start_date, end_date)
    elif report_type == 'driver_incident_logs':
        return get_driver_incident_logs_data(start_date, end_date)
    elif report_type == 'user_feedback_summary':
        return get_user_feedback_summary_data(start_date, end_date)
    return None

def get_route_popularity_data(start_date, end_date):
    """Route popularity based on bus locations/tracking"""
    # This is a simplified implementation
    routes = BusRoute.objects.all()
    route_data = []

    for route in routes:
        # Count active tracking sessions for this route
        tracking_count = BusLocation.objects.filter(
            bus__route=route,
            timestamp__date__range=[start_date, end_date]
        ).count()

        route_data.append({
            'route': route.bus_number,
            'tracking_count': tracking_count
        })

    return {
        'type': 'route_popularity',
        'data': route_data,
        'chart_type': 'bar'
    }

def get_on_time_performance_data(start_date, end_date):
    """On-time performance analysis"""
    # Simplified: compare scheduled vs actual times
    schedules = BusSchedule.objects.filter(
        route__isnull=False,
        is_active=True
    )

    performance_data = []
    for schedule in schedules:
        # This would need actual tracking data to compare
        # For now, placeholder
        on_time_percentage = 85  # Placeholder
        performance_data.append({
            'route': schedule.route.bus_number,
            'schedule': f"{schedule.departure_time.strftime('%H:%M')} - {schedule.arrival_time.strftime('%H:%M') if schedule.arrival_time else 'N/A'}",
            'on_time_percentage': on_time_percentage
        })

    return {
        'type': 'on_time_performance',
        'data': performance_data,
        'chart_type': 'line'
    }

def get_driver_incident_logs_data(start_date, end_date):
    """Driver incident logs from issue reports"""
    incidents = IssueReport.objects.filter(
        created_at__date__range=[start_date, end_date],
        reported_by__profile__role='DRIVER'
    ).order_by('-created_at')

    incident_data = []
    for incident in incidents:
        incident_data.append({
            'date': incident.created_at.strftime('%Y-%m-%d'),
            'driver': incident.reported_by.username,
            'issue_type': incident.get_issue_type_display(),
            'description': incident.description,
            'status': incident.get_status_display()
        })

    return {
        'type': 'driver_incident_logs',
        'data': incident_data,
        'chart_type': 'table'
    }

def get_user_feedback_summary_data(start_date, end_date):
    """User feedback summary - placeholder for future feedback system"""
    # Placeholder data
    feedback_data = [
        {'category': 'Service Quality', 'positive': 45, 'negative': 5},
        {'category': 'Punctuality', 'positive': 38, 'negative': 12},
        {'category': 'Cleanliness', 'positive': 50, 'negative': 0},
        {'category': 'Safety', 'positive': 42, 'negative': 8}
    ]

    return {
        'type': 'user_feedback_summary',
        'data': feedback_data,
        'chart_type': 'pie'
    }

@login_required
@authority_required
def export_report_pdf(request):
    """Export the current report as PDF"""
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    report_type = request.GET.get('report_type')

    if not all([start_date_str, end_date_str, report_type]):
        return HttpResponse('Invalid parameters', status=400)

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    report_data = generate_report_data(report_type, start_date, end_date)

    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph(f"{report_type.replace('_', ' ').title()} Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Date range
    date_info = Paragraph(f"Date Range: {start_date} to {end_date}", styles['Normal'])
    story.append(date_info)
    story.append(Spacer(1, 12))

    # Data table
    if report_data and 'data' in report_data:
        data = report_data['data']
        if data:
            headers = list(data[0].keys())
            table_data = [headers] + [list(item.values()) for item in data]

            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)

    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report.pdf"'
    return response