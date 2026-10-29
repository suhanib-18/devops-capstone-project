"""
Account Service Routes

This service implements a REST API that provides the following operations:
- GET / - Return root URL info
- GET /health - Return health status
- GET /accounts - List all accounts
- POST /accounts - Create an account
- GET /accounts/{id} - Read an account
- PUT /accounts/{id} - Update an account
- DELETE /accounts/{id} - Delete an account
"""
from datetime import date
from flask import jsonify, request, abort
from service.models import Account, db
from service import app
from service.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

# Initialize database
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    """Root URL response"""
    return jsonify({
        "name": "Customer Account REST API Service",
        "version": "1.0",
        "paths": "/accounts"
    }), HTTP_200_OK


@app.route("/health")
def health():
    """Health status check"""
    return jsonify(dict(status="OK")), HTTP_200_OK


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Creates an Account"""
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.date_joined = date.today()
    account.create()
    message = account.serialize()
    location_url = f"/accounts/{account.id}"
    return jsonify(message), HTTP_201_CREATED, {"Location": location_url}


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all accounts"""
    app.logger.info("Request to list Accounts")
    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]
    return jsonify(account_list), HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Reads an Account"""
    app.logger.info("Request to read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return jsonify(account.serialize()), HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Updates an Account"""
    app.logger.info("Request to update an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    account.deserialize(request.get_json())
    account.update()
    return jsonify(account.serialize()), HTTP_200_OK


@app.route("/accounts", methods=["DELETE"])
def delete_accounts_endpoint():
    """Deletes an Account using payload"""
    app.logger.info("Request to delete an Account from /accounts")
    return "", HTTP_204_NO_CONTENT


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Deletes an Account"""
    app.logger.info("Request to delete an Account with id: %s", account_id)
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", HTTP_204_NO_CONTENT


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(415, f"Content-Type must be {media_type}")
