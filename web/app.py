import os

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")

# เชื่อมต่อไปยัง mongo container ผ่านชื่อ service/container ใน docker network
client = MongoClient(mongo_uri)
db = client[db_name]
routers_col = db["routers"]

@app.route("/")
def main():
    # ดึงข้อมูล router ทั้งหมดจาก MongoDB
    routers = list(routers_col.find())
    return render_template("index.html", data=routers)

@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        routers_col.insert_one({
            "ip": ip,
            "username": username,
            "password": password
        })
    return redirect(url_for("main"))

@app.route("/delete/<idx>", methods=["POST"])
def delete_router(idx):
    try:
        routers_col.delete_one({"_id": ObjectId(idx)})
    except Exception as e:
        print(f"Delete Error: {e}")
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)