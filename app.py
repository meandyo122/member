import pymongo 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from flask import *
import os

url= "mongodb+srv://a0910134517:Rot123@myusers.mizc7.mongodb.net/?retryWrites=true&w=majority&appName=MyUsers"
client=pymongo.MongoClient(url, server_api=ServerApi('1'))
db=client.member_system
print("資料庫連線成功")


app =Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)


app.secret_key="any string"



@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html",nickname=session["nickname"])
    else:
        return redirect("/")
    
@app.route("/error")
def error():
    message=request.args.get("msg","發生錯誤，請聯繫客服")
    return render_template("error.html",message=message)

@app.route("/signup",methods=["POST"])
def signup():
    #從前端接收資料
    nickname=request.form["nickname"]
    email=request.form["email"]
    password=request.form["password"]
    #根據接收到的資料
    collection=db.user
    result=collection.find_one({
        "email":email
    })
    if result != None:
        return redirect ("/error?msg=信箱已經被註冊")
    collection.insert_one({
        "nickname":nickname,
        "email":email,
        "password":password
    })
    return redirect("/")

@app.route("/signin",methods=["POST"])
def signin():
    email=request.form["email"]
    password=request.form["password"]
    #和資料庫作互動
    collection=db.user
    #檢查信箱密碼是否正確
    result=collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    #找不到對應的錯誤頁面
    if result == None:
        return redirect("/error?msg=帳號密碼錯誤")
    #登入成功 在seeion紀錄會員資訊
    session["nickname"]=result["nickname"]
    print(session["nickname"])
    return redirect("/member")

@app.route("/signout")
def signout():
    #移除session 中的會員資訊
    del session["nickname"]
    return redirect("/")



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render 提供的 PORT 環境變數
    app.run(host="0.0.0.0", port=port)
