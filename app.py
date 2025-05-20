from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num1 = int(request.form["num1"])
        num2 = int(request.form["num2"])
        operation = request.form["operation"]

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        else:
            result = "Invalid operation"

        return render_template("results.html", result=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
