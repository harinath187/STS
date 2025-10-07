# app/routes/project_dashboard_routes.py
from flask import Blueprint, render_template, session
from app.models.project_task_dashboard import ProjectTaskDashboard
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

project_dashboard_bp = Blueprint('project_dashboard_bp', __name__)

def generate_task_status_chart():
    results = ProjectTaskDashboard.get_task_status_counts()
    if not results:
        return None
    
    labels = [r['status'] for r in results]
    sizes = [r['count'] for r in results]
    colors = ['#34d399', '#fbbf24']
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    plt.title("Task Status Distribution")
    plt.tight_layout()
    
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    chart = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    return chart

def generate_monthly_tasks_chart():
    results = ProjectTaskDashboard.get_monthly_task_counts()
    if not results:
        return None
    
    results.reverse()
    months = [r['month'] for r in results]
    counts = [r['count'] for r in results]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(months, counts, marker='o', color='#3b82f6', linewidth=2)
    ax.set_title('Tasks Created Per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Tasks')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    chart = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    return chart

@project_dashboard_bp.route('/project-dashboard')
def project_dashboard():
    user = session.get('user')
    
    stats = ProjectTaskDashboard.get_dashboard_stats()
    recent_tasks = ProjectTaskDashboard.get_recent_tasks(6)
    pie_chart = generate_task_status_chart()
    line_chart = generate_monthly_tasks_chart()
    
    return render_template(
        'dashboard/project_task_dashboard.html',
        user=user,
        stats=stats,
        recent_tasks=recent_tasks,
        pie_chart=pie_chart,
        line_chart=line_chart
    )