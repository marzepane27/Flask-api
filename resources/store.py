from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoreModel
from schemas import StoreSchema
from db import db

blp = Blueprint("stores", "stores", url_prefix="/stores")

@blp.route("/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the store.")
        return {"message": "Store deleted."}

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get_or_404(store_id)
        
        # Оновлення даних магазину
        if "name" in store_data:
            store.name = store_data["name"]
        
        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the store.")
        
        return store

@blp.route("/")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store.")
        return store
