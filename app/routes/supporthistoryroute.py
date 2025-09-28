from flask import render_template
from app.utils.auth import login_required  # <- import once
from app.models.support_history import historylist,assignlist,notassignlist
def test_routes(app):
    @app.route("/tickets")
    @login_required  # ✅ This replaces the if-check!
    def test():
        return render_template("employee/test.html")


def supporthistory(app):
    @app.route("/supporthistory")
    @login_required
    def histlist():
        listitem=historylist()
        return render_template("dashboard/support_historylist.html",historylist=listitem)


def suppassignlist(app):
    @app.route("/assignhistory")
    @login_required
    def asslist():
        listitem=assignlist()
        return render_template("dashboard/support_history_assignlist.html",assignlist=listitem)
    

def notsuppassignlist(app):
    @app.route("/notassignhistory")
    @login_required
    def notasslist():
        listitem=notassignlist()
        print(listitem)
        return render_template("/dashboard/support_history_notassign_list.html",notassignlist=listitem)



    
    # @app.route("/assignhistory")
    # def assignlist():
    #     user = session.get("user")
    #     listitem=historylist()
    #     print(listitem)
    #     if not user:
    #         return redirect("/login")
    #     return render_template("dashboard/support_history_assignlist.html")