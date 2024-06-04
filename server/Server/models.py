from . import db
from sqlalchemy import func

# Define a helper table for the many-to-many relationship
document_routes = db.Table('document_routes',
                           db.Column('document_id', db.Integer,
                                     db.ForeignKey('documents.id')),
                           db.Column('route_id', db.Integer,
                                     db.ForeignKey('route.id'))
                           )

document_notifications = db.Table('document_notifications',
                                  db.Column('document_id', db.Integer,
                                            db.ForeignKey('documents.id')),
                                  db.Column('notification_id', db.Integer,
                                            db.ForeignKey('notification.id'))
                                  )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    previlage = db.Column(db.String(20), nullable=False)
    user_img = db.Column(db.String(200_000), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    institute = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(20), nullable=False)
    program = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    last_password_reset_request = db.Column(db.DateTime, default=None)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    notification_count = db.Column(db.Integer, nullable=False, default=0)
    registered_date = db.Column(db.DateTime(), default=func.now())
    template_access = db.relationship("Template")
    document_access = db.relationship("Documents")


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(120), nullable=False)


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(500), nullable=True)
    program = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    institute = db.Column(db.String(10), nullable=True)
    dean_office_institute = db.Column(db.String(10), nullable=True)
    attemp = db.Column(db.Integer, nullable=True, default=0)
    pending = db.Column(db.Boolean, default=True)
    pending_date = db.Column(db.DateTime(), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    routes = db.relationship(
        'Route', secondary=document_routes, backref=db.backref('documents', lazy=True))
    notifications = db.relationship(
        'Notification', secondary=document_notifications, backref=db.backref('documents', lazy=True))


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"))


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    processing = db.Column(db.Boolean, default=True)
    disapproved_date = db.Column(db.DateTime(), nullable=True)
    rej_comment = db.Column(db.String(50), nullable=True)
    remarks = db.Column(db.String(50), nullable=True)
    approved_date = db.Column(db.DateTime(), nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_date = db.Column(db.DateTime(), nullable=True)
    finished = db.Column(db.Boolean, default=False)
    finished_date = db.Column(db.DateTime(), nullable=True)
    complete = db.Column(db.Boolean, default=False)
    complete_date = db.Column(db.DateTime(), nullable=True)
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"))


class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Captcha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(120), nullable=False)
    value = db.Column(db.String(5), nullable=False)


class Revoked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(300), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime(timezone=True), nullable=False)


class Resend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(120), nullable=False)


class Reset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(120), nullable=False)
