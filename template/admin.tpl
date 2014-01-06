
%if username:
    <p>Logged in as {{username}}</p>
%end
<a href='/admin/students/'>Add and remove students</a>
<a href='/admin/logout/'>Logout</a>

%rebase base.tpl title='Admin Console: Edit Students', css='/static/css/drill.css'
