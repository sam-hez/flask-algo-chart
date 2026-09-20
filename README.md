# Flask Algorithm Chart

A simple Flask project that visualizes the time complexity of common algorithms.

## Setup

1. Open a terminal in this project folder.
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install Flask: `pip install -r requirements.txt`
5. Start the server: `python app.py`

The server runs at `http://localhost:8000`.

## Use the endpoint

Open this URL in a browser:

`http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10,000`

Supported algorithms are `linear_search`, `bubble_sort`, `binary_search`, and `nested_loops`.

Each request starts at `n = 0`, saves a PNG chart in the `generated_images` folder, and returns JSON like this:

```json
{
  "algorithm": "linear_search",
  "step": 10,
  "n_max": 10000,
  "image_path": "generated_images/linear_search_chart.png",
  "image_base64": "iVBORw0KGgo...",
  "message": "Chart generated successfully."
}
```

`image_base64` is the Base64-encoded content of the saved PNG image.

## Invalid requests

The API returns a `400` error if `algo` is unsupported, `step` is not positive, or `n_max` is negative.
