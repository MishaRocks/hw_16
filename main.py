
import json
from flask import Flask, jsonify, request
from app.__init__ import db, app
from app.models import User, Offer, Order


def get_table(cls, filename):
    """
    Преобразует json файл и заполняет таблицу
    """
    with open(filename, "r", encoding='UTF-8') as file:
        json_list = json.load(file)
        for element in json_list:
            table_element = cls(**element)
            db.session.add(table_element)
        db.session.commit()


get_table(User, "data/users.json")
get_table(Order, "data/orders.json")
get_table(Offer, "data/offers.json")


@app.route("/users", methods=["GET", "POST"])
def get_users():
    """
    Метод GET: Возвращает json файл с всеми юзерами
    Метод POST: добавляет юзера в таблицу
    """
    if request.method == "GET":
        users_list = User.query.all()

        user_response = []
        for user in users_list:
            user_response.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "role": user.role,
                "phone": user.phone
            })
        return jsonify(user_response)

    elif request.method == "POST":
        user_added = request.json
        new_user = User(**user_added)
        db.session.add(new_user)
        db.session.commit()
        return f'{user_added["first_name"]} {user_added["last_name"]} added'


@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def get_user(uid):
    """
        Метод GET: Возвращает юзера по id
        Метод PUT: добавляет изменения в профиль юзера по id
        Метод DELETE: удаляет пользователя по id
        """

    if request.method == "GET":
        user = User.query.get(uid)
        if user is None:
            return jsonify("Нет такого заказчика")
        return jsonify(({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "role": user.role,
                "phone": user.phone
            }))

    elif request.method == "PUT":
        recieved_user = request.json
        updated_user = User.query.get(uid)

        updated_user.first_name = recieved_user["first_name"]
        updated_user.last_name = recieved_user["last_name"]
        updated_user.age = recieved_user["age"]
        updated_user.email = recieved_user["email"]
        updated_user.role = recieved_user["role"]
        updated_user.phone = recieved_user["phone"]

        db.session.commit()
        return f'{updated_user.first_name} {updated_user.last_name} обновлен'

    elif request.method == "DELETE":
        user_deleted = User.query.get(uid)
        db.session.delete(user_deleted)
        db.session.commit()
        return f'{user_deleted.first_name} {user_deleted.last_name} удален'


@app.route("/orders", methods=["GET"])
def get_orders():
    """
        Метод GET: Возвращает json файл с всеми заказами
    """
    if request.method == "GET":
        orders_list = Order.query.all()
        orders_response = []
        for order in orders_list:
            orders_response.append({
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "price": order.price,
                "customer_id": order.customer_id,
                "executor_id": order.executor_id,
            })
        return jsonify(orders_response)


@app.route("/orders/<int:oid>", methods=["GET"])
def get_order(oid):
    """
        Метод GET: Возвращает заказы по id
    """
    order = Order.query.get(oid)
    if order is None:
        return jsonify("Нет такого заказа")
    return jsonify({
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id,
             })


@app.route("/offers", methods=["GET"])
def get_offers():
    """
        Метод GET: Возвращает json файл с всеми предложениями
    """
    offers_list = Offer.query.all()

    offers_response = []
    for offer in offers_list:
        offers_response.append({
            "id": offer.id,
            "order_id": offer.id,
            "executor_id": offer.executor_id,
                })
    return jsonify(offers_response)


@app.route("/offers/<int:ofid>", methods=["GET"])
def get_offer(ofid):
    """
        Метод GET: Возвращает предложения  по  id
    """
    offer = Offer.query.get(ofid)
    if offer is None:
        return jsonify("Нет такого заказа")
    return jsonify({
            "id": offer.id,
            "order_id": offer.id,
            "executor_id": offer.executor_id,
            })


@app.route("/orders", methods=["POST"])
def add_order():
    """
        Метод POST: добавляет заказ в таблицу
    """
    order_added = request.json
    new_order = User(**order_added)
    db.session.add(new_order)
    db.session.commit()
    return f'Заказ {order_added["description"]} добавлен'


@app.route("/orders/<int:oid>", methods=["PUT"])
def update_order(oid):
    """
        Метод PUT: добавляет изменения в профиль закза по id
    """
    recieved_order = request.json
    updated_order = Order.query.get(oid)

    updated_order.name = recieved_order["name"]
    updated_order.description = recieved_order["description"]
    updated_order.start_date = recieved_order["start_date"]
    updated_order.end_date = recieved_order["end_date"]
    updated_order.address = recieved_order["address"]
    updated_order.price = recieved_order["price"]
    updated_order.customer_id = recieved_order["customer_id"]
    updated_order.executor_id = recieved_order["executor_id"]

    db.session.commit()
    return 'Заказ обновлен'


@app.route("/orders/<int:oid>", methods=["DELETE"])
def delete_order(oid):
    """
        Метод DELETE: удаляет пользователя по id
    """
    order_deleted = Order.query.get(oid)
    db.session.delete(order_deleted)
    db.session.commit()
    return f'Заказ {order_deleted.description} удален'


@app.route("/offers", methods=["POST"])
def add_offer():
    """
        Метод POST: добавляет заказ в таблицу
    """
    offer_added = request.json
    new_offer = Offer(**offer_added)
    db.session.add(new_offer)
    db.session.commit()
    return 'Предложение добавлено'


@app.route("/offers/<int:ofid>", methods=["PUT"])
def update_offer(ofid):
    """
        Метод PUT: добавляет изменения в профиль предложения по id
    """
    recieved_offer = request.json
    updated_offer = Offer.query.get(ofid)

    updated_offer.order_id = recieved_offer["order_id"]
    updated_offer.executor_id = recieved_offer["executor_id"]

    db.session.commit()
    return 'Предложение обновлено'


@app.route("/offers/<int:ofid>", methods=["DELETE"])
def delete_offer(ofid):
    """
        Метод DELETE: удаляет пользователя по id
    """
    offer_deleted = Offer.query.get(ofid)
    db.session.delete(offer_deleted)
    db.session.commit()
    return 'Предложение  удалено'


if __name__ == "__main__":
    app.run()
