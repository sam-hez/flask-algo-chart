from flask import Flask, jsonify, request


app = Flask(__name__)


SUPPORTED_ALGORITHMS = [
    "linear_search",
    "bubble_sort",
    "binary_search",
    "nested_loops",
]


@app.route("/")
def home():
    return jsonify({"message": "Time Complexity Visualizer API"})


@app.route("/analyze")
def analyze():
    algo = request.args.get("algo")
    step = request.args.get("step", type=int)
    n_max = request.args.get("n_max", type=int)

    if algo not in SUPPORTED_ALGORITHMS:
        return jsonify({
            "error": "Please choose a supported algorithm.",
            "supported_algorithms": SUPPORTED_ALGORITHMS,
        }), 400

    if step is None or step <= 0:
        return jsonify({"error": "step must be a positive whole number."}), 400

    if n_max is None or n_max < 0:
        return jsonify({"error": "n_max must be zero or a positive whole number."}), 400

    return jsonify({
        "algorithm": algo,
        "step": step,
        "n_max": n_max,
        "message": "Parameters accepted. Chart generation will be added next.",
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
