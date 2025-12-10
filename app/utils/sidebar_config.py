from copy import deepcopy

BASE_SIDEBAR_CLASSES = {
    "wrapper": "w-64 min-h-screen bg-white/95 shadow-lg flex flex-col fixed top-0 left-0 bottom-0 border-r border-blue-100 z-20",
    "header": "px-6 pt-8 pb-4 flex items-center gap-3 text-2xl font-extrabold text-blue-600",
    "header_icon": "text-blue-400",
    "nav": "flex-1 px-6 py-4 space-y-3 text-blue-700 font-semibold",
    "link": "flex items-center gap-3 px-4 py-3 rounded-2xl bg-white text-blue-700 visited:text-blue-700 shadow-sm border border-blue-100 hover:bg-blue-50 transition w-full focus:outline-none focus:ring-0",
    "dropdown_button": "flex items-center justify-between w-full px-4 py-3 rounded-2xl bg-white text-blue-700 visited:text-blue-700 shadow-sm border border-blue-100 focus:outline-none focus:ring-0",
    "child_link": "flex items-center gap-2 px-4 py-2 rounded-xl bg-white text-blue-600 visited:text-blue-600 border border-blue-50 focus:outline-none focus:ring-0",
    "logout_container": "px-6 pb-8 mt-auto",
    "logout_button": "flex items-center gap-3 px-4 py-3 w-full rounded-2xl font-bold text-red-600 visited:text-red-600 bg-red-50 border border-red-100 shadow-sm hover:bg-red-100 focus:outline-none focus:ring-0",
}

SIDEBAR_CONFIGS = {
    "employee": {
        "title": "Employee Dashboard",
        "title_icon": "fa fa-user-circle",
        "items": [
            {"label": "Home", "icon": "fa fa-home text-xl", "href": "/employee"},
            {"label": "Tickets", "icon": "fa fa-ticket-alt text-xl", "href": "/test"},
            {
                "label": "Comments",
                "icon": "fa fa-comments",
                "children": [
                    {"label": "Tasks", "icon": "fa fa-tasks w-4", "href": "/create_task_comment"},
                    {"label": "Support Ticket", "icon": "fa fa-ticket-alt w-4", "href": "/create_support_comment"},
                ],
            },
            {"label": "Task Updation", "icon": "fa fa-ticket text-xl", "href": "/task_update"},
            {"label": "Open Tickets", "icon": "fa fa-file-alt text-xl", "endpoint": "open_tickets"},
        ],
    },
    "admin": {
        "title": "Dashboard",
        "title_icon": "fa fa-user-circle",
        "items": [
            {"label": "Employee Details", "icon": "fa fa-users text-xl", "href": "/employeeslist"},
            {"label": "Client Details", "icon": "fa fa-users text-xl", "href": "/client_list"},
            {"label": "Add Employee", "icon": "fa fa-user-plus text-xl", "href": "/addemployee"},
            {"label": "Add Client", "icon": "fa fa-user-plus text-xl", "href": "/save_client"},
        ],
    },
    "it_employee": {
        "title": "Dashboard",
        "title_icon": "fa fa-user-circle",
        "items": [
            {"label": "Home", "icon": "fa fa-home text-xl", "href": "/employee"},
            {"label": "Assigned Team", "icon": "fa fa-users text-xl", "href": "/project_manager/team"},
            {"label": "Analytics", "icon": "fa fa-chart-line text-xl", "href": "/analytics"},
            {"label": "Settings", "icon": "fa fa-cog text-xl", "href": "/settings"},
        ],
    },
    "it_manager": {
        "title": "Support Manager",
        "title_icon": "fa fa-user-circle",
        "items": [
            {"label": "Home", "icon": "fa fa-home text-xl", "href": "/it_manager"},
            {"label": "Assigned Tickets", "icon": "fa fa-tasks text-xl", "href": "/assignhistory"},
            {"label": "Not Assign Tickets", "icon": "fa fa-folder-open text-xl", "href": "/notassignhistory"},
            {"label": "Support Ticket History", "icon": "fa fa-comments text-xl", "href": "/supporthistory"},
            {"label": "Support Ticket Team", "icon": "fa fa-users text-xl", "href": "/employee_tickets"},
        ],
    },
    "project_manager": {
        "title": "Dashboard",
        "title_icon": "fa fa-user-circle",
        "items": [
            {"label": "Home", "icon": "fa fa-home text-xl", "href": "/manager"},
            {"label": "Assigned Team", "icon": "fa fa-users text-xl", "href": "/project_manager/team"},
            {"label": "Projects", "icon": "fa fa-briefcase text-xl", "href": "/projects"},
            {"label": "Tasks", "icon": "fa fa-list-check text-xl", "href": "/task"},
        ],
    },
}

DEFAULT_LOGOUT = {
    "label": "Logout",
    "href": "/logout",
    "icon": "fa fa-sign-out-alt text-xl",
}

for config in SIDEBAR_CONFIGS.values():
    config.setdefault("logout", DEFAULT_LOGOUT.copy())
    classes = deepcopy(BASE_SIDEBAR_CLASSES)
    custom = config.get("classes") or {}
    classes.update(custom)
    config["classes"] = classes
