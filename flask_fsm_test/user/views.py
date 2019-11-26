# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from transitions import Machine

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")

@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route("/next")
@login_required
def next():
    """List members."""
    can_go_next = current_user.go_next()
    if can_go_next:
        return render_template("users/members.html")
    else:
        return render_template("users/members.html")
    

@blueprint.route("/prev")
@login_required
def prev():
    """List members."""
    can_go_prev = current_user.go_prev()
    if can_go_prev:
        return render_template("users/members.html")
    else:
        return render_template("users/members.html")