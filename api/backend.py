from api._wsgi import app
import random

@app.route("/random")
def randomRoute():
    return str(random.randint(1, 100))

if __name__ == "__main__":
    app.run(debug=True)