# Flask Algorithm Chart

A simple Flask project that visualizes the time complexity of common algorithms.

## Setup

1. Open a terminal in this project folder.
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install Flask: `pip install -r requirements.txt`
5. Start the server: `python app.py`

The server runs at `http://localhost:8000`.

## Test the endpoint

Open this URL in a browser:

`http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10000`

Supported algorithms are `linear_search`, `bubble_sort`, `binary_search`, and `nested_loops`.

Each request saves a PNG chart in the `generated_images` folder.
