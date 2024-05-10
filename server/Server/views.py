from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from typing import List

from .models import User, Revoked, Documents, Route, Notification
from .static.predef_function.user_validation import Sanitizer, RegisterEntryValidator
from .static.predef_function.image_compressor import compress_image
from . import db


views = Blueprint("views", __name__)


@views.route("/update_count", methods=["POST"])
@jwt_required()
def update_count():
    data = request.json
    current_user = get_jwt_identity()
    user: User = User.query.filter_by(id=current_user).first()
    user.notification_count = data["count"]
    db.session.commit()
    return jsonify({})


@views.route("/get_users", methods=["GET", "POST"])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    user: User = User.query.filter_by(id=current_user).first()
    if user.previlage != "admin":
        return jsonify({"error": "You do not have the privilage to access this route!"})

    if request.method == "GET":
        data = {
            "users": []
        }

        users: List[User] = User.query.all()
        for user in users:
            if user.previlage == "admin":
                continue

            user_credentials = {
                "id": user.id,
                "previlage": user.previlage,
                "userImg": user.user_img,
                "fullName": user.full_name,
                "institute": user.institute,
                "program": user.program,
                "email": user.email,
                "employeeID": user.employee_id,
                "unit": user.designation,
                "full_ver_val": user.verified,
                "emailConfirmed": user.confirmed,
                "registeredDate": user.registered_date
            }

            data["users"].append(user_credentials)

        return jsonify(data)

    if request.method == "POST":
        data = request.json

        user: User = User.query.filter_by(email=data["email"]).first()
        user.verified = True
        user.previlage = data["previlage"]
        db.session.commit()

        print(user.previlage)
        return jsonify({})

    return jsonify({})


@views.route("/get_all", methods=["GET"])
@jwt_required()
def get_all_documents() -> dict:
    current_user = get_jwt_identity()
    data = {}

    user: User = User.query.filter_by(id=current_user).first()

    if user:
        data = {
            "previlage": user.previlage,
            "userImg": user.user_img,
            "fullName": user.full_name,
            "institute": user.institute,
            "program": user.program,
            "email": user.email,
            "EmployeeID": user.employee_id,
            "unit": user.designation,
            "full_ver_val": user.verified,
            "registeredDate": user.registered_date
        }

    if user.previlage == "Secretary":
        users: List[User] = User.query.all()
        data["users"] = []
        for user in users:
            if user.previlage != "Secretary" and user.previlage != "admin" and user.verified:
                credential_of_user = {
                    "id": user.id,
                    "email": user.email,
                    "fullName": user.full_name,
                    "institute": user.institute,
                    "program": user.program,
                    "userImg": user.user_img,
                    "designation": user.designation,
                    "documents": []
                }

                documents: List[Documents] = Documents.query.filter_by(
                    user_id=user.id).all()

                for document in documents:
                    routes: List[Route] = Route.query.filter_by(
                        document_id=document.id).all()

                    document_data = {
                        "documentID": document.id,
                        "documentName": document.name,
                        "documentInstitute": document.institute,
                        "attemps": document.attemp,
                        "documentProgram": document.program,
                        "codeData": document.code,
                        "documentDescription": document.description,
                        "pending": document.pending,
                        "pendingDate": document.pending_date,
                        "documentPath": [{
                            "pathID": route.id,
                            "name": route.name,
                            "approved": route.approved,
                            "disapprovedDate": route.disapproved_date,
                            "comment": route.rej_comment,
                            "processing": route.processing,
                            "approvedDate": route.approved_date,
                            "confirmed": route.confirmed,
                            "confirmedDate": route.confirmed_date,
                            "finished": route.finished,
                            "finishedDate": route.finished_date,
                            "complete": route.complete,
                            "completeDate": route.complete_date
                        } for route in routes]
                    }

                    credential_of_user["documents"].append(document_data)

                data["users"].append(credential_of_user)

    return jsonify(data)


@views.route("/document_approval", methods=["POST"])
@jwt_required()
def document_approval() -> dict:
    if request.method == "POST":
        data = request.json
        print(data)
        document: Documents = Documents.query.filter_by(
            code=data["codeData"]).first()

        if not document:
            return jsonify({"error": "There's no document assciated with this document!"})

        route: Route = Route.query.filter_by(
            document_id=document.id, name=data["unit"]).first()
        notification: Notification = Notification.query.filter_by(
            document_id=document.id).first()

        if data["approval"] == "approved":
            new_route: Route = Route(
                document_id=document.id,
                name=data["unit"],
                approved=True,
                disapproved_date=None,
                rej_comment=None,
                processing=True,
                approved_date=datetime.now(),
                confirmed=False,
                confirmed_date=None,
                finished=False,
                finished_date=None,
                complete=False,
                complete_date=None,
            )

            db.session.add(new_route)

            new_notification: Notification = Notification(
                title=f"Approved!... By {data['unit']}",
                body=f"Your {document.name} has been Approved!",
                date=datetime.now(),
                document_id=document.id,
            )

            db.session.add(new_notification)
            db.session.commit()

        elif data["approval"] == "disapproved":
            if len(data["comment"]) == 0 or len(data["comment"]) < 5:
                return jsonify({"error": "Comment is to short!"})

            new_route: Route = Route(
                document_id=document.id,
                name=data["unit"],
                approved=False,
                disapproved_date=datetime.now(),
                rej_comment=data["comment"],
                processing=False,
                approved_date=None,
                confirmed=False,
                confirmed_date=None,
                finished=False,
                finished_date=None,
                complete=False,
                complete_date=None,
            )

            db.session.add(new_route)

            new_notification: Notification = Notification(
                title="Rejected",
                body=f"Your {document.name} has been Rejected!",
                date=datetime.now(),
                document_id=document.id,
            )

            db.session.add(new_notification)
            db.session.commit()

        elif data["approval"] == "confirm":
            if not route:
                return jsonify({"error": "There's no document, please register one first!"})

            route.confirmed = True
            route.confirmed_date = datetime.now()

            new_notification: Notification = Notification(
                title=f"{data['unit']} is done!",
                body=f"Your {document.name} is now waiting to be approved by the next route.",
                date=datetime.now(),
                document_id=document.id,
            )

            db.session.add(new_notification)
            db.session.commit()

        elif data["approval"] == "finish":
            if not route:
                return jsonify({"error": "There's no document, please register one first!"})

            route.confirmed = True
            route.confirmed_date = datetime.now()
            route.finished = True
            route.finished_date = datetime.now()

            new_notification: Notification = Notification(
                title="Waiting",
                body=f"You can now go ahead and get your {document.name} at {data['unit']}",
                date=datetime.now(),
                document_id=document.id,
            )

            db.session.add(new_notification)
            db.session.commit()

        elif data["approval"] == "complete":
            if not route:
                return jsonify({"error": "There's no document, please register one first!"})

            route.complete = True
            route.complete_date = datetime.now()

            new_notification: Notification = Notification(
                title="Complete",
                body=f"Your {document.name}'s process is complete",
                date=datetime.now(),
                document_id=document.id,
            )

            db.session.add(new_notification)
            db.session.commit()

        else:
            if not route:
                return jsonify({"error": "There's no document, please register one first!"})

            db.session.delete(route)
            document.attemp += 1

            db.session.commit()

    return jsonify({"success": "Success!"})


@views.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        data = request.json

        to_delete: Documents = Documents.query.filter_by(
            code=data["codeData"]).first()
        associated_routes: Route = Route.query.filter_by(
            document_id=to_delete.id).all()

        for route in associated_routes:
            db.session.delete(route)

        db.session.delete(to_delete)
        db.session.commit()

    return jsonify({})


@views.route("/index", methods=["GET"])
@jwt_required()
def index():
    data = {}

    current_user = get_jwt_identity()
    user: User = User.query.filter_by(id=current_user).first()

    if user:
        data = {
            "id": user.id,
            "previlage": user.previlage,
            "userImg": user.user_img,
            "fullName": user.full_name,
            "program": user.program,
            "institute": user.institute,
            "email": user.email,
            "EmployeeID": user.employee_id,
            "unit": user.designation,
            "full_ver_val": user.verified,
            "registeredDate": user.registered_date,
            "notificationCount": user.notification_count
        }

    data["documents"] = []

    if user.previlage == "User":
        documents: List[Documents] = Documents.query.filter_by(
            user_id=current_user).all()

        for document in documents:
            document_data = {
                "documentID": document.id,
                "documentName": document.name,
                "documentProgram": document.program,
                "documentInstitute": document.institute,
                "attemps": document.attemp,
                "codeData": document.code,
                "documentDescription": document.description,
                "pending": document.pending,
                "pendingDate": document.pending_date,
            }

            routes: List[Route] = Route.query.filter_by(
                document_id=document.id).all()
            document_data["documentPath"] = [{
                "name": route.name,
                "approved": route.approved,
                "processing": route.processing,
                "approvedDate": route.approved_date,
                "disapprovedDate": route.disapproved_date,
                "comment": route.rej_comment,
                "confirmed": route.confirmed,
                "confirmedDate": route.confirmed_date,
                "finished": route.finished,
                "finishDate": route.finished_date,
                "complete": route.complete,
                "completeDate": route.complete_date,
            } for route in routes]

            notifications: List[Notification] = Notification.query.filter_by(
                document_id=document.id).all()
            document_data["notifications"] = [{
                "id": notification.id,
                "title": notification.title,
                "body": notification.body,
                "date": notification.date,
            } for notification in notifications]

            data["documents"].append(document_data)

    return jsonify(data)


@views.route("/logout", methods=["GET"])
@jwt_required()
def logout() -> dict:
    jti = get_jwt()["jti"]
    now = datetime.now()
    revoked_token = Revoked(jti=jti, revoked_at=now)
    db.session.add(revoked_token)
    db.session.commit()
    return jsonify({})


@views.route("/scan", methods=["POST"])
@jwt_required()
def scan():
    empty_code_data = "QR code cannot be found!"
    associated_document = "There's no document associated with the QR Code!"

    if request.method == "POST":
        scan_data = request.json

        if len(scan_data["codeData"]) == 0:
            return jsonify({"error": empty_code_data})

        document: Documents = Documents.query.filter_by(
            code=scan_data["codeData"]).first()

        if not document:
            return jsonify({"error": associated_document})

        return jsonify({"documentName": document.name, "documentDescription": document.description, "codeData": document.code, "regAt": document.doc_reg_at})

    return jsonify({})


@views.route("/document_register", methods=["POST"])
@jwt_required()
def document_register():
    insertion_error: str = "Sorry, something went wrong!. Please try again."

    current_user = get_jwt_identity()

    if request.method == "POST":
        data = request.json

        code = data["codeData"]
        document_name = data["documentName"]
        document_program = data["documentProgram"]
        document_institute = data["documentInstitute"]
        description = data["documentDescription"]
        edit = data["edit"]

        print(data)

        entry_validate: RegisterEntryValidator = RegisterEntryValidator(
            code, document_name, document_program, document_institute, description).validate()

        if isinstance(entry_validate, dict):
            return jsonify(entry_validate)

        sanitize: bool | dict = Sanitizer(
            {"Document Name": document_name, "Document Program": document_program, "Document Institute": document_institute, "Document Code": code,
                "Document Descripttion": description}
        ).validate()

        if isinstance(sanitize, dict):
            return jsonify(sanitize)

        if edit:
            document: Documents = Documents.query.filter_by(code=code).first()

            if not document:
                return jsonify({"error": "There's no document assciated with this document!"})

            document.name = document_name
            document.program = document_program
            document.institute = document_institute
            document.description = description

            db.session.commit()
            return jsonify({"success": "Saved Successfully!"})

        try:
            document: Documents = Documents(
                name=document_name,
                program=document_program,
                institute=document_institute,
                code=code,
                attemp=0,
                description=description,
                user_id=current_user
            )

            db.session.add(document)
            db.session.commit()

        except Exception as e:
            return jsonify({"error": insertion_error})

    return jsonify({})


# @views.route("/add_route", methods=["POST"])
# @jwt_required()
# def add_route():
#     if request.method == "POST":
#         route = request.json
#         name = route["routeName"]
#         current_user = get_jwt_identity()

#         document = Documents.query.filter_by(name=name).first()

#         if document:
#             return jsonify({"error": "There's already a Route for this Document!"})

#         new_document = Documents(name=name, user_id=current_user)
#         db.session.add(new_document)
#         db.session.commit()

#         for name in route["documentPath"].values():
#             new_route = Route(name=name,
#                               document_id=new_document.id)
#             db.session.add(new_route)

#         db.session.commit()
#     return jsonify({})
