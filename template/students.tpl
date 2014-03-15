%if username:
    <header>
    <span>Logged in as {{username}}</span>
    
    <a style="color:white; float:right;" href="/admin/logout/">Logout</a>
    </header>
%end

<form action="submit/" method="post">
    <table>
    <tr><th>Student</th><th>Delete</th></tr>
    % for student in students:
    <tr>
    <td>{{student[0]}}:</td> <td><input type="checkbox" name="{{student[0]}}_delete" value="del"></td>
    </tr>
    % end
    </table>
    <textarea name="add_students" cols="40" rows="5" placeholder="Input one name on each line"></textarea>
    <input type="submit" value="Submit"> 
</form>

%rebase base.tpl title='Admin Console: Edit Students', css='/static/css/admin.css'
