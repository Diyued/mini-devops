"""API mínima con Flask: /health y /calc/<op>?a=..&b=.."""
import os

from flask import Flask, jsonify, request

from src import calculator

app = Flask(__name__)

OPERATIONS = {
    "add": calculator.add,
    "subtract": calculator.subtract,
    "multiply": calculator.multiply,
    "divide": calculator.divide,
}


@app.get("/health")
def health():
    return jsonify(status="ok", version=os.getenv("APP_VERSION", "dev"))


@app.get("/calc/<op>")
def calc(op: str):
    func = OPERATIONS.get(op)
    if func is None:
        return jsonify(error=f"Operación '{op}' no soportada"), 404
    try:
        a = float(request.args["a"])
        b = float(request.args["b"])
    except (KeyError, ValueError):
        return jsonify(error="Parámetros 'a' y 'b' numéricos requeridos"), 400
    try:
        return jsonify(op=op, a=a, b=b, result=func(a, b))
    except ValueError as exc:
        return jsonify(error=str(exc)), 422


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
