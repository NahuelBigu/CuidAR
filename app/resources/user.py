from flask import redirect, render_template, request, url_for, session, abort,flash
from app.models.user import User
from app.models.forms.user import RegisterForm, EditForm
from app.models.role import Role
from app.models.configuration import Configuration
from app.helpers.control_decorator import control
from app.helpers.permission import check as has_permission
from app.helpers.auth import authenticated

# Protected resources
@control
def index():
    if not has_permission(session,"user_index"): # Check permission
        return redirect(url_for("home")) 
    
    elementsPerPage=Configuration.last().elementsPerPage
    users = User.all()
    return render_template("user/index.html", users=users,elementsPerPage=elementsPerPage)

@control
def new():
    if not has_permission(session,"user_new"): # Check permission
        return redirect(url_for("home")) 
    form = RegisterForm()
    roles=Role.allTuples()
    form.roles.choices= roles
    return render_template("user/new.html", form=form)

@control
def create():
    if not has_permission(session,"user_new"): # Check permission
        return redirect(url_for("home")) 
    form = RegisterForm()
    roles=Role.allTuples()
    form.roles.choices= roles
    if form.validate_on_submit():
        user=User.create(form)
        flash("Se creo el usuario "+str(form.username.data) ,category="success")
        return redirect(url_for("user_index"))
    
    return render_template("user/new.html", form=form)

@control
def activate(user_id):
    if not has_permission(session,"user_update"): # Check permission
        return redirect(url_for("home")) 
    User.activate(user_id)
    return redirect(url_for("user_index"))

@control
def deactivate(user_id):
    if not has_permission(session,"user_update"): # Check permission
        return redirect(url_for("home")) 
    User.deactivate(user_id)
    return redirect(url_for("user_index"))

@control
def delete(user_id):
    if not has_permission(session,"user_delete"): # Check permission
        return redirect(url_for("home")) 
    if user_id==session["user_id"]: 
        flash('No podes eliminar el usuario que estas utilizando en este momento', category="error")
        return redirect(url_for("user_index"))
    User.delete_user(user_id)
    flash('Usuario eliminado correctamente', category="success")
    return redirect(url_for("user_index"))

@control
def edit(username):
    if not has_permission(session,"user_update"): # Check permission
        return redirect(url_for("home")) 
    user=User.find_by_username(username)
    if user is None: # Check user
        return redirect(url_for("home"))
    form = EditForm(obj=user)
    form.user_id.data=user.id
    roles=Role.allTuples()
    form.roles.choices= roles
    form.roles.data= [int(rol.id) for rol in user.roles] 
    #form.password.data=user.password
    
    return render_template("user/edit.html", form=form, roles=roles, user=user)

@control
def post_edit():
    if not has_permission(session,"user_update"): # Check permission
        return redirect(url_for("home")) 
    form = EditForm()
    
    user=User.find_by_id(form.user_id.data)
    roles=Role.allTuples()
    form.roles.choices= roles
    
    
    if form.validate_on_submit():
        flash("Usuario editado correctamente",category="success")
        User.edit_us(form)
        return redirect(url_for("user_index"))
    form.user_id.data=user.id
    
    form.roles.data= [int(rol.id) for rol in user.roles]
    return render_template("user/edit.html", form=form, roles=roles, user=user)

@control
def profile(): 
    user=User.find(session.get("user_id"))
    return render_template("user/profile.html", user=user)


