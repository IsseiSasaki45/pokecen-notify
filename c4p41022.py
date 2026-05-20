############################################
#
# 課題
#
############################################
from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    html = """検索したいキーワードを入力してください
    <form action="/" method="POST">
    <input name="key"></input>
    <button type="submit">送信</button>
    </form>
    <hr>
    {results}
    """

    if request.method == "POST":
        key = request.form.get("key")
        res = getWiki(key)
        
        results = ""
        for item in res["pages"]:
            title = item["title"]
            url = "https://ja.wikipedia.org/wiki/" + title

            results += f'<a href="{url}">{title}</a><br>'
        return html.format(results=results)

def getWiki(key):
    url = 'https://ja.wikipedia.org/w/rest.php/v1/search/title'
    params = {
        'q': key,
        'limit': '5'
    }
    response = requests.get(url, params=params, headers={"User-Agent": "test-app"})
    data = response.json()
    return data

if __name__ == '__main__':
    app.run(debug=True)






































