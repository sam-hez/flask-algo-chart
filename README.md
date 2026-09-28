# Flask Algorithm Chart

A simple Flask project that visualizes the time complexity of common algorithms.

## Setup

1. Open a terminal in this project folder.
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install the packages: `pip install -r requirements.txt`
5. Start the server: `python app.py`

The server runs at `http://localhost:8000`.

## Use the endpoint

Open this URL in a browser:

`http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10,000`

Supported algorithms are `linear_search`, `bubble_sort`, `binary_search`,
`nested_loops`, `stack_reverse`, `stack_search`, and `queue_process`.

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

## Save an analysis to the database

Install the requirements and start the server using the setup steps above.
The app automatically creates `instance/analyses.db`, a local SQLite database.
The `Analysis` table stores `id`, `algorithm`, `step`, and `n_max`.
Flask-SQLAlchemy creates the table and saves rows using Python, with no raw SQL.

Send a POST request from another terminal:

```bash
curl -X POST http://localhost:8000/save_analysis \
  -H 'Content-Type: application/json' \
  -d '{"algorithm": "stack_reverse", "step": 10, "n_max": 100}'
```

The response has status `201` and looks like:

```json
{
  "id": 1,
  "algorithm": "stack_reverse",
  "step": 10,
  "n_max": 100,
  "message": "Analysis saved successfully."
}
```

Use the `algorithm`, `step`, and `n_max` values returned by `/analyze`.
Each POST saves a new row. It saves the analysis settings, not the chart image.
The response is JSON, but the saved data goes into SQLite, not a JSON file.
The database keeps the saved rows when the server restarts and is ignored by Git.

Send `step` and `n_max` as JSON integers, without quotes or commas.
Missing or invalid values return `400`. A database error returns `500`.

## Home activity

`not_optimized.py` removes duplicate users by ID using nested loops.
It keeps the first user with each ID and keeps the original order.
Run the example with `python not_optimized.py`.

`stack_queue.py` has two basic classes using Python lists:

- Stack: last in, first out. Methods: `push`, `pop`, `peek`, `size`, `is_empty`.
- Queue: first in, first out. Methods: `enqueue`, `dequeue`, `peek`, `size`, `is_empty`.

Removing or peeking when empty raises `IndexError`. Each instance has its own list.

`stack_queue_algorithms.py` has three algorithms. Each returns the result and
an operation count. They create their own structure and leave the input unchanged.

| Algorithm | Example | Count used in the chart | Big-O |
| --- | --- | --- | --- |
| `stack_reverse` | `[1, 2, 3]` becomes `[3, 2, 1]` | n pushes + n pops = 2n | O(n) |
| `stack_search` | Search for a value, starting at the top | n pushes + n pops + n comparisons = 3n when missing | O(n) |
| `queue_process` | Serve `[1, 2, 3]` in that same order | n enqueues + removals and list shifts = n + n(n+1)/2 | O(n²) |

The Queue uses `pop(0)`, which shifts the remaining list items. That is why
processing the whole queue is quadratic in this implementation.
Stack pushes and queue enqueues use list append, which is O(1) amortized
(constant cost on average over many appends).

Start the server, then try these URLs:

- http://localhost:8000/analyze?algo=stack_reverse&step=10&n_max=100
- http://localhost:8000/analyze?algo=stack_search&step=10&n_max=100
- http://localhost:8000/analyze?algo=queue_process&step=10&n_max=100

Open the returned `image_path` in the project folder to see each chart.
The stack charts are straight lines. The queue chart curves upward.
These new options run the algorithms at each input size. Stack search uses a
missing target to show the worst case. Counts include the selected operations
above, not every Python instruction or elapsed time. The original four options
still plot theoretical estimates. Use small inputs first, especially for the queue.

## Run all tests

With the virtual environment activated, run:

```bash
python -m unittest discover -v
```

The tests cover all Stack and Queue methods, ordering, empty errors, repeated
values, mixed operations, reuse, and separate instances. They also check duplicate
removal, algorithm results and counts, and PNG generation through the Flask API.
Test charts are saved in a temporary folder and cleaned up afterward.
Database tests use a temporary SQLite database to check saving, persistence,
invalid requests, and recovery after a failed save.

See [STUDY_NOTES.md](STUDY_NOTES.md) for the Big-O and sorting stability reading.
