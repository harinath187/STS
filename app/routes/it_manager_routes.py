from flask import render_template, session
from app.utils.auth import login_required
from app.models import support_dashboard
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering
import matplotlib.pyplot as plt


def register_support_routes(app):

    @app.route("/it_manager")
    @login_required
    def it_manager_dashboard():
        user = session.get("user")

        # Fetch ticket stats for dashboard cards
        card_data = {
            "total_tickets": support_dashboard.get_total_tickets(),
            "pending_tickets": support_dashboard.get_open_tickets(),
            "resolved_tickets": support_dashboard.get_resolved_tickets(),
            "completed_tickets": support_dashboard.get_closed_tickets(),
            "unassigned_tickets": support_dashboard.get_unassigned_tickets(),
        }

        # Pie chart data
        labels = ['Pending (Open)', 'Resolved', 'Completed (Closed)', 'Unassigned']
        sizes = [
            card_data['pending_tickets'],
            card_data['resolved_tickets'],
            card_data['completed_tickets'],
            card_data['unassigned_tickets']
        ]
        colors = ['#fbbf24', '#34d399', '#60a5fa', '#9ca3af']

        pie_chart = None
        if sum(sizes) > 0:
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')
            plt.title("Ticket Status Distribution")
            plt.tight_layout()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            pie_chart = base64.b64encode(img.getvalue()).decode()
            plt.close(fig)

        # Line chart data - monthly ticket creation
        months, ticket_counts = support_dashboard.get_monthly_ticket_counts()
        line_chart = None
        if months and ticket_counts:
            fig2, ax2 = plt.subplots()
            ax2.plot(months, ticket_counts, marker='o', color='blue')
            ax2.set_title('Tickets Created Per Month')
            ax2.set_xlabel('Month')
            ax2.set_ylabel('Number of Tickets')
            ax2.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            img2 = io.BytesIO()
            fig2.savefig(img2, format='png')
            img2.seek(0)
            line_chart = base64.b64encode(img2.getvalue()).decode()
            plt.close(fig2)

        # Recent tickets
        recent_tickets = support_dashboard.get_recent_tickets()

        return render_template(
            "dashboard/it_manager.html",
            user=user,
            card_data=card_data,
            pie_chart=pie_chart,
            line_chart=line_chart,
            recent_tickets=recent_tickets
        )
