# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from .models import SignupStates
from .forms import Step1Form, Step2Form, Step3Form

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def members():
    """List members."""
    
    current_state = current_user.state
        
    if request.method == "GET":
        if current_state == SignupStates.STEP_1:
            form = Step1Form(request.form)
            return render_template("users/step1.html", form=form)
        elif current_state == SignupStates.STEP_2:
            form = Step2Form(request.form)
            return render_template("users/step2.html", form=form)
        elif current_state == SignupStates.STEP_3:
            form = Step3Form(request.form)
            return render_template("users/step3.html", form=form)
        elif current_state == SignupStates.COMPLETE:
            return render_template("users/complete.html")
    elif request.method == "POST":
        if current_state == SignupStates.STEP_1:
            form = Step1Form(request.form)
        elif current_state == SignupStates.STEP_2:
            form = Step2Form(request.form)
        elif current_state == SignupStates.STEP_3:
            form = Step3Form(request.form)
            
        if form.validate_on_submit():
            print(f"Text: {form.text}")
            current_user.go_next()
            return redirect(url_for("user.members"))


@blueprint.route("/next")
@login_required
def next():
    """List members."""
    current_user.go_next()
    return render_template("users/members.html")


@blueprint.route("/prev")
@login_required
def prev():
    """List members."""
    can_go_prev = current_user.go_prev()
    if can_go_prev:
        return render_template("users/members.html", )
    else:
        return render_template("users/members.html")