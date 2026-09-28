import base64
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request
from not_optimized import remove_duplicate_users
from stack_queue_algorithms import stack_reverse, stack_search, queue_process


app = Flask(__name__)


SUPPORTED_ALGORITHMS = [
    "linear_search",
    "bubble_sort",
    "binary_search",
    "nested_loops",
    "stack_reverse",
    "stack_search",
    "queue_process",
]

IMAGE_FOLDER = "generated_images"

users = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 2}]
unique_users = remove_duplicate_users(users)


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
    if algo == "stack_reverse":
        result, operations = stack_reverse(range(number_of_elements))
        return operations
    if algo == "stack_search":
        # -1 is missing, so we search the whole stack (worst case).
        result, operations = stack_search(range(number_of_elements), -1)
        return operations
    if algo == "queue_process":
        result, operations = queue_process(range(number_of_elements))
        return operations


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


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_number_argument(argument_name):
    value = request.args.get(argument_name)

    if value is None:
        return None

    try:
        return int(value.replace(",", ""))
    except ValueError:
        return None


@app.route("/")
def home():
    return jsonify({"message": "Time Complexity Visualizer API"})


@app.route("/analyze")
def analyze():
    algo = request.args.get("algo")
    step = get_number_argument("step")
    n_max = get_number_argument("n_max")

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
    image_base64 = encode_image(image_path)

    return jsonify({
        "algorithm": algo,
        "step": step,
        "n_max": n_max,
        "image_path": image_path,
        "image_base64": image_base64,
        "message": "Chart generated successfully.",
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
