class RoleMiddleware:
    
# In Django, middleware is a small plugin(software add-on) that runs in the background while the request and
#  response are being processed. The application's middleware is utilized to complete a task.
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print(request.user.is_authenticated)
        # print(request.user)
        # print(user.staff_master.STAFF_ROLE.role_id)
        if request.user.is_authenticated:
            # .staff_master.STAFF_ROLE.role_id
            if request.user.is_staff == 1:
                
                request.role_links = [
                        {'ec': 'e_contact', 'title': 'Emergency Contacts','url': '/e_contact/'},
                        {'r': 'roles_list','title': 'Roles', 'url': '/roles_list/'},
                        {'s': 'staff','title': 'Staff', 'url': '/staff/'},
                        {'v': 'visitor','title': 'Visitor Log', 'url': '/visitor_ledger/'},
                        {'i': 'incident','title': 'Incident History', 'url': '/incidents/'},
                        {'c': 'cctv','title': 'CCTV Footages', 'url': '/cctv_page/'},
                        {'p': 'call_mysql_procedure','title': 'Procedures', 'url': '/call_mysql_procedure/'},
                        {'p': 'duty','title': 'Duty Roster', 'url': '/duty/'},
                        {'sh': 'shift','title': 'Shift Master', 'url': '/shift/'},
                        {'a': 'audit','title': 'Audit Table', 'url': '/audit/'},
                    ]
            else:
                request.role_links = [
                    {'ec': 'e_contact', 'title': 'Emergency Contacts','url': '/e_contact/'},
                    {'v': 'visitor', 'title': 'Visitor Log', 'url': '/visitor_ledger/'},
                    {'i': 'incident','title': 'Incident History', 'url': '/incidents/'},
                ]
        else:
            request.role_links = []  # No links for unauthenticated users

        response = self.get_response(request)
        return response
