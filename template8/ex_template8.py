#############################
#
# HTMLのテンプレートを利用する
#
#############################
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    obj = {
      "title": "最初",
      "p":"これは最初のページです. 以下のリンクで移動してください",
      }
    return(render_template("template8.html", d=obj))

@app.route("/html2")
def html2():
    obj = {
      "title": "次",
      "p":"これは次のページです. 以下のリンクで移動してください",
      }
    return(render_template("template8.html", d=obj))

@app.route("/html3")
def html3():
    obj = {
      "title": "最後",
      "p":"これは最後のページです. 以下のリンクで移動してください",
      }
    return(render_template("template8.html", d=obj))

if __name__ == '__main__':
    app.run(debug=True)




















































