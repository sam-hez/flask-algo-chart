import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request


app = Flask(__name__)


SUPPORTED_ALGORITHMS = [
    "linear_search",
    "bubble_sort",
    "binary_search",
    "nested_loops",
]

IMAGE_FOLDER = "generated_images"


def calculate_operations(algo, number_of_elements):
    if algo == "linear_search":
        return number_of_elements
    if algo == "bubble_sort":
        return number_of_elements ** 2
    if algo == "binary_search":
        if number_of_elements == 0:
            return 0
        return math.log2(number_of_elements)
    if algo == "nested_loops":
        return number_of_elements ** 2


def create_chart(algo, step, n_max):
    number_of_elements = list(range(0, n_max + 1, step))

    if number_of_elements[-1] != n_max:
        number_of_elements.append(n_max)

    operations = [calculate_operations(algo, n) for n in number_of_elements]

    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    image_path = os.path.join(IMAGE_FOLDER, f"{algo}_chart.png")

    plt.figure(figsize=(8, 5))
    plt.plot(number_of_elements, operations, marker="o")
    plt.title(f"Time Complexity: {algo.replace('_', ' ').title()}")
    plt.xlabel("Number of elements (n)")
    plt.ylabel("Estimated operations")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    return image_path


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

    image_path = create_chart(algo, step, n_max)

    return jsonify({
        "algorithm": algo,
        "step": step,
        "n_max": n_max,
        "image_path": image_path,
        "message": "Chart generated successfully.",
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
