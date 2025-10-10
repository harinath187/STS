from flask import render_template, session, redirect
import io, base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.models import manager_dashboard

def register_manager_routes(app):
    @app.route("/manager")
    def manager_dashboard_view():
        user = session.get("user")
        if not user:
            return redirect("/login")

        manager_id = user["id"]

        # Top Cards
        card_data = {
            "total_projects": manager_dashboard.get_total_projects(manager_id),
            "total_tasks": manager_dashboard.get_total_tasks(manager_id),
            "completed_tasks": manager_dashboard.get_completed_tasks(manager_id),
            "in_progress_tasks": manager_dashboard.get_in_progress_tasks(manager_id),
            "unassigned_tasks": manager_dashboard.get_unassigned_tasks(manager_id)
        }

        # Line Chart
        months, counts = manager_dashboard.get_monthly_task_counts(manager_id)
        fig1, ax1 = plt.subplots()
        ax1.plot(months, counts, marker='o', color='green')
        ax1.set_title('Tasks Created Per Month')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Count')
        ax1.grid(True)
        plt.xticks(rotation=45)
        img1 = io.BytesIO()
        plt.tight_layout()
        fig1.savefig(img1, format='png')
        img1.seek(0)
        line_chart = base64.b64encode(img1.getvalue()).decode()
        plt.close(fig1)

        # Pie Chart
        sizes = [
            card_data["completed_tasks"],
            card_data["in_progress_tasks"],
            card_data["unassigned_tasks"]
        ]
        labels = ['Completed', 'In Progress', 'Unassigned']
        colors = ['#34d399', '#fbbf24', '#f87171']
        pie_chart = None
        if sum(sizes) > 0:
            fig2, ax2 = plt.subplots()
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax2.axis('equal')
            plt.title("Task Status")
            img2 = io.BytesIO()
            plt.tight_layout()
            fig2.savefig(img2, format='png')
            img2.seek(0)
            pie_chart = base64.b64encode(img2.getvalue()).decode()
            plt.close(fig2)

        # Recent Tasks
        recent_tasks = manager_dashboard.get_recent_tasks(manager_id)

        return render_template(
            "dashboard/pm.html",
            user=user,
            card_data=card_data,
            line_chart=line_chart,
            pie_chart=pie_chart,
            recent_tasks=recent_tasks
        )
