from flask import render_template, session
from app.utils.auth import login_required
from app.models import it_employee_dashboard_data as it_emp_dashboard  # ✅ Correct and cleaner
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # No GUI rendering
import matplotlib.pyplot as plt


def register_it_employee_routes(app):

    @app.route("/it_employee")
    @login_required
    def it_employee_dashboard():
        user = session.get("user")
        emp_id = user.get("id")

        # 1. Card Data (top 5 metrics)
        card_data = it_emp_dashboard.get_it_employee_ticket_stats(emp_id)

        # 2. Pie Chart - Ticket Status Distribution
        pie_chart = None
        status_distribution = it_emp_dashboard.get_status_distribution_for_employee(emp_id)

        if status_distribution:
            labels = list(status_distribution.keys())
            sizes = list(status_distribution.values())
            colors = ['#fbbf24', '#34d399', '#60a5fa', '#9ca3af', '#ef4444']

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors[:len(sizes)])
            ax.axis('equal')
            plt.title("My Ticket Status Distribution")
            plt.tight_layout()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            pie_chart = base64.b64encode(img.getvalue()).decode()
            plt.close(fig)

        # 3. Line Chart - Monthly Ticket Creation
        line_chart = None
        months, counts = it_emp_dashboard.get_monthly_ticket_counts_for_employee(emp_id)
        if months and counts:
            fig2, ax2 = plt.subplots()
            ax2.plot(months, counts, marker='o', color='blue')
            ax2.set_title("My Tickets Created Per Month")
            ax2.set_xlabel("Month")
            ax2.set_ylabel("Tickets")
            ax2.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            img2 = io.BytesIO()
            fig2.savefig(img2, format='png')
            img2.seek(0)
            line_chart = base64.b64encode(img2.getvalue()).decode()
            plt.close(fig2)

        # 4. Recent Tickets
        recent_tickets = it_emp_dashboard.get_recent_tickets_for_employee(emp_id)

        return render_template(
            "dashboard/it_employee.html",
            user=user,
            card_data=card_data,
            pie_chart=pie_chart,
            line_chart=line_chart,
            recent_tickets=recent_tickets
        )
