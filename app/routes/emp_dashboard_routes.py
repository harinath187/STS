from flask import render_template, session, redirect
from app.models import emp_dashboard
import io, base64
import matplotlib
matplotlib.use("Agg") 

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering
import matplotlib.pyplot as plt


def register_employee_routes(app):

    @app.route("/employee")
    
    def employee_dashboard_view():
        
        user = session.get("user")
        if not user:
            return redirect("/login")

        emp_id = user["id"]

        # --- Top cards ---
        card_data = {
            "total_tasks": emp_dashboard.get_total_tasks(emp_id),
            "pending_tasks": emp_dashboard.get_pending_tasks(emp_id),
            "completed_tasks": emp_dashboard.get_completed_tasks(emp_id),
            "support_tickets": emp_dashboard.get_support_tickets(emp_id)
        }

        # --- Line chart ---
        months, completed_tasks = emp_dashboard.get_monthly_completed_tasks(emp_id)
        fig1, ax1 = plt.subplots()
        ax1.plot(months, completed_tasks, marker='o', color='blue')
        ax1.set_title('Tasks Completed Per Month')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Completed Tasks')
        ax1.grid(True)
        plt.xticks(rotation=45)
        img1 = io.BytesIO()
        plt.tight_layout()
        fig1.savefig(img1, format='png')
        img1.seek(0)
        line_chart = base64.b64encode(img1.getvalue()).decode()
        plt.close(fig1)

        # --- Pie chart ---
        pending = card_data["pending_tasks"]
        completed = card_data["completed_tasks"]
        overdue_tasks_list = emp_dashboard.get_overdue_tasks(emp_id)
        overdue = len(overdue_tasks_list)

        sizes = [pending, completed, overdue]
        labels = ['Pending', 'Completed', 'Overdue']
        colors = ['#fbbf24', '#34d399', '#f87171']

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
        else:
            pie_chart = None  # No tasks yet

        # --- Recent tasks ---
        recent_tasks = emp_dashboard.get_recent_tasks(emp_id)

        return render_template(
            "dashboard/employee.html",
            user=user,
            card_data=card_data,
            line_chart=line_chart,
            pie_chart=pie_chart,
            recent_tasks=recent_tasks
        )
