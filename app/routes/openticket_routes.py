from flask import Flask, render_template, session, redirect
from app.models.opentickets import get_support_tickets_by_employee

def register_open_ticket_routes(app: Flask):
    @app.route('/opentickets', methods=['GET'])
    def open_tickets():
        user = session.get("user")
        if not user:
            return redirect("/login")

        emp_id = user.get("id")
        tickets = get_support_tickets_by_employee(emp_id)

        return render_template("employee/opentickets.html", tickets=tickets, user=user)
