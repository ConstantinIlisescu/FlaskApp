from flask import Flask
app = Flask(__name__)


store = [
    {
        "name": "My Store",
        "items": [
            {
                "name" : "Chair",
                "price" : 15.99
            }
        ]
    }
]

@app.get("/store")
def get_store():
    return{"store":store}