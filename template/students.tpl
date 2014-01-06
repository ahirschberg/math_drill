%if username:
    <header>
    <span>Logged in as {{username}}</span>
    
    <a style="color:white; float:right;" href="/admin/logout/">Logout</a>
    </header>
%end

<form action="submit/" method="post">
    % for student in students:
    {{student[0]}}: <input type="checkbox" name="{{student[0]}}_delete" value="del"><br>
    % end
    <textarea name="add_students" cols="40" rows="5" placeholder="Input one name on each line"></textarea>
    <input type="submit" value="Submit"> 
</form>

%rebase base.tpl title='Admin Console: Edit Students', css='/static/css/admin.css'
