import os

from bson import ObjectId
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
db = client[db_name]

routers_col = db["routers"]
status_col = db["interface_status"]


@app.route("/")
def main():
    routers = list(routers_col.find())
    return render_template("index.html", data=routers)


@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        routers_col.insert_one({"ip": ip, "username": username, "password": password})
    return redirect(url_for("main"))


@app.route("/delete/<idx>", methods=["POST"])
def delete_router(idx):
    try:
        routers_col.delete_one({"_id": ObjectId(idx)})
    except Exception as e:
        print(f"Delete Error: {e}")
    return redirect(url_for("main"))


@app.route("/router/<router_ip>")
def router_detail(router_ip):
    records = list(status_col.find({"router_ip": router_ip}).sort("timestamp", -1))
    return render_template("router_detail.html", router_ip=router_ip, records=records)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
