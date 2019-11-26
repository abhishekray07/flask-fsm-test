# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from enum import auto, Enum

from flask_login import UserMixin

from flask_fsm_test.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)
from flask_fsm_test.extensions import bcrypt

from transitions import Machine
from transitions.core import MachineError


class SignupStates(Enum):
    STEP_1 = auto()
    STEP_2 = auto()
    STEP_3 = auto()
    COMPLETE = auto()


UI_RENDER = {
    SignupStates.STEP_1: ["Next"],
    SignupStates.STEP_2: ["Next", "Prev"],
    SignupStates.STEP_3: ["Next", "Prev"],
    SignupStates.COMPLETE: [],
}

SIGNUP_TRANSITIONS = [
    ["next", SignupStates.STEP_1, SignupStates.STEP_2],
    ["next", SignupStates.STEP_2, SignupStates.STEP_3],
    ["next", SignupStates.STEP_3, SignupStates.COMPLETE],
    ["prev", SignupStates.STEP_3, SignupStates.STEP_2],
    ["prev", SignupStates.STEP_2, SignupStates.STEP_1],
]


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    status = db.Column(
        db.Enum(SignupStates), default=SignupStates.STEP_1
    )

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None
    
    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def state(self):
        return self.status

    @state.setter
    def state(self, value):
        self.status = value
        db.session.add(self)
        db.session.commit()
    
    def go_next(self):
        
        machine = Machine(
            model=self, states=SignupStates, transitions=SIGNUP_TRANSITIONS, initial=self.state
        )

        try:
            self.next()
            return True
        except MachineError:
            return False
        
    def go_prev(self):
        machine = Machine(
            model=self, states=SignupStates, transitions=SIGNUP_TRANSITIONS, initial=self.state
        )

        try:
            self.prev()
            return True
        except MachineError:
            return False
        
    def button_renders(self):
        return UI_RENDER[self.state]

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"
