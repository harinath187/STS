Ticket Management System
========================

Overview
--------

This repository contains a Flask 3.1 based ticket management platform that drives multiple role-specific dashboards from a MySQL database. Session data is stored server-side and every request that needs authentication checks `session["user"]`, which is created by `app.routes.login_routes.register_routes`. Users are redirected to the correct dashboard by inspecting `user["dep_name"]`:

* `HR` → `/admin`
* `Backend Team`, `Frontend Team`, `QA / Testing`, `Database / Data`, `Security` → `/employee`
* `Project Manager` → `/manager`
* `IT Team`, `Support / IT Helpdesk` → `/it_employee`
* `IT Project Manager` → `/it_manager`

Key Features
------------

* **Role-aware dashboards**:  
  * `/admin` renders `hr/list_of_employees.html` with department (`departmentlist`) and role (`roleslist`) data.  
  * `/employee` loads KPI cards, monthly trends and a recent task table produced by `app.models.emp_dashboard`.  
  * `/manager`, `/it_manager`, `/it_employee` receive their own dashboards via dedicated route modules.
* **Support ticket life cycle** (`app/routes/support_ticket_routes.py`, `app/routes/supporthistoryroute.py`):  
  * Employees submit tickets through `/create_support_ticket`. Attachments are stored under `app/static/uploads/support_attachment`.  
  * IT managers review assigned/unassigned history at `/assignhistory`, `/notassignhistory`, `/supporthistory`, `/employee_tickets`.
* **Project and task management** (`app/routes/project_routes.py`, `app/routes/project_task_routes.py`, `app/routes/task_update_routes.py`):  
  * Managers can list, add and edit tasks via the `task_bp` blueprint and the `project_management` template set.  
  * Employees update task progress at `/task_update`.
* **Analytics**: Matplotlib (headless via `Agg`) renders PNG charts inline for dashboards (`emp_dashboard_routes`, `it_manager_routes`, `register_it_employee_routes`). Plotly outputs are exported with Kaleido where required.
* **Profile management**: `/profile_data` returns JSON for the navbar modal. `/update_profile` enforces a password rule of at least two digits and two `@`/`#` characters.

Project Structure
-----------------

```
run.py                        # Flask entry point (debug server)
app/
  __init__.py                 # creates the app and wires routes/blueprints
  models/                     # database access helpers (MySQL)
  routes/                     # Flask views grouped by feature
  templates/                  # Jinja2 templates (Tailwind + Bootstrap)
  static/                     # assets and uploaded files
  utils/                      # auth guard and logger setup
logs/                         # application log output
requirements.txt              # Python dependencies
```

Database & Configuration
------------------------

Database connections use `mysql.connector` and read credentials from environment variables. Create a `.env` file alongside `run.py` with:

```
DB_HOST=<mysql-host>
DB_USER=<mysql-user>
DB_PASSWORD=<mysql-password>
DB_NAME=<ticket-management-db>
```

The schema referenced throughout the code expects these tables (see SQL in `app/models` and `app/routes`):

* `employee`, `department`, `roles` – HR management
* `support_ticket`, `support_assign`, `support_comments` – support workflow
* `project`, `project_task`, `task_comments` – project planning

Any endpoint that modifies data closes cursors and connections explicitly to avoid leaks.

Installation
------------

```
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

The dependency list includes:

* Flask, Flask-WTF, Flask-Login, Flask-Migrate, Flask-SQLAlchemy (not all modules use SQLAlchemy yet; MySQL access is primarily direct)
* mysql-connector-python and PyMySQL for database connectivity
* Matplotlib, Plotly, Kaleido for chart generation
* Pandas for data summarisation in analytics routes
* SpaCy (see `requirements.txt`) for text processing features referenced in support modules

Running the Server
------------------

```
export FLASK_DEBUG=1              # optional
python run.py
```

`run.py` prints the resolved template and static directories, then serves the app on `http://127.0.0.1:5000/`.

Static Assets & Uploads
-----------------------

* Global styles/scripts leverage CDN versions of Tailwind, Bootstrap, DataTables, Font Awesome, Chart.js and Alpine.js (see `templates/base.html` and individual templates).  
* Support ticket attachments are saved to `app/static/uploads/support_attachment` and are exposed in the UI through `url_for('static', filename=...)`.

Testing & Logging
-----------------

There is no automated test suite. Logging is centralised in `app/utils/logger.py`; modules import `logger` and record successes/failures for DB operations (`project_db`, `supporthistoryroute`, etc.). Runtime issues appear both in stdout and the rotating files under `logs/`.

Extending the Application
-------------------------

* To add a new protected view, register it inside `create_app()` and protect it with `app.utils.auth.login_required`.
* To keep the side navigation consistent, wrap new content templates with the fixed-width `<aside>` markup already used in the dashboards and include the matching partial from `templates/common/`.
* Data access helpers should live in `app/models` and must call `get_db_connection()` to ensure `.env` credentials are honoured.
