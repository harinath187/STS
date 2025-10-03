from flask import render_template, request, jsonify
from app.utils.auth import login_required
from app.models.support_history import (
    historylist,
    assignlist,
    notassignlist,
    get_ticket_by_id,
    update_ticket,
    delete_ticket,
    get_employees_by_department
)


def test_routes(app):
    @app.route("/tickets")
    @login_required
    def test_view():
        return render_template("employee/test.html")
    

def supporthistory(app):
    @app.route("/supporthistory")
    @login_required
    def histlist_view():
        listitem = historylist()
        return render_template("support_ticket/support_historylist.html", historylist=listitem)



def suppassignlist(app):
    @app.route("/assignhistory")
    @login_required
    def asslist_view():
        listitem = assignlist()
        return render_template("support_ticket/support_history_assignlist.html", assignlist=listitem)



def notsuppassignlist(app):
    @app.route("/notassignhistory")
    @login_required
    def notasslist_view():
        listitem = notassignlist()
        return render_template("support_ticket/support_history_notassign_list.html", notassignlist=listitem)



def ticket_detail_route(app):
    @app.route("/ticket/<int:ticket_id>", methods=["GET", "POST"])
    @login_required
    def ticket_detail_view(ticket_id):
        if request.method == "GET":
            ticket = get_ticket_by_id(ticket_id)
            if ticket:
                return jsonify(ticket)
            else:
                return jsonify({"error": "Ticket not found"}), 404

        elif request.method == "POST":
            data = request.get_json()
            print("Received POST data:", data) 

            
            required_fields = [
                "assigned_to", "assigned_by", "dept_id", "duration",
                "comments", "problem_description", "priority",
                "start_date", "status"
            ]

            
            missing_fields = [field for field in required_fields if field not in data or data[field] in [None, ""]]
            if missing_fields:
                return jsonify({
                    "error": "Missing required fields",
                    "fields": missing_fields
                }), 400

            
            if "end_date" not in data:
                data["end_date"] = None

            try:
                update_ticket(ticket_id, data)
                return jsonify({"message": "Ticket updated successfully"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500



def ticket_delete_route(app):
    @app.route("/ticket/<int:ticket_id>/delete", methods=["POST"])
    @login_required
    def ticket_delete_view(ticket_id):
        try:
            delete_ticket(ticket_id)
            return jsonify({"message": "Ticket deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500



def employee_routes(app):
    @app.route("/employees/<dept_name>")
    @login_required
    def employees_by_dept(dept_name):
        try:
            employees = get_employees_by_department(dept_name)
            return jsonify(employees)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
