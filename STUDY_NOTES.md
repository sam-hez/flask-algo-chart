# Big-O primer

Big-O describes an upper bound on how the work grows as the input size n grows.
It does not tell us the exact number of seconds. We usually compare worst cases
and ignore constant factors and smaller terms: 3n is O(n), and n² + n is O(n²).

| Big-O | Basic example |
| --- | --- |
| O(1) | Looking at the top of a stack |
| O(log n) | Binary search in a sorted list; halve the search area each time |
| O(n) | Searching every item once |
| O(n log n) | Merge sort |
| O(n²) | Two loops that each grow with n |

Our duplicate-removal function can compare each user with all earlier unique
users, so its worst case is O(n²). Its result uses O(n) extra space.
Our stack reversal and stack search take O(n) time, including building the stack.
Processing our list-based Queue takes O(n²) time because every dequeue shifts
the remaining items. All three algorithms use O(n) extra space.

A queue with a different implementation can have O(1) dequeue, so processing
all its items can be O(n). The data structure implementation matters.

Reading: [Brown University: Big-O and Sorting](https://cs.brown.edu/courses/cs015/lecture/pdf/CS15.Lecture_17_BigO_and_Sorting.10.31.24.pdf).

# Stability in sorting

A stable sort keeps items with equal sorting keys in their original relative order.

For example, sort these students by mark:

```text
Before: (Ann, 80), (Ben, 70), (Chris, 80)
After:  (Ben, 70), (Ann, 80), (Chris, 80)
```

Ann stays before Chris because they both have 80 and Ann was first originally.
An unstable sort might put Chris before Ann, even though the marks are sorted.
Stability helps when earlier ordering matters, such as sorting by name first,
then doing a stable sort by mark to preserve name order within equal marks.

Bubble sort is stable if it only swaps when the left key is strictly greater
than the right key. Swapping equal keys can break stability.
Python's built-in sorting is stable. Stability and Big-O describe different things:
one is about equal-key order, the other is about growth in work.

Our duplicate-removal function preserves input order, but it is not a sorting algorithm.

Reading: [OpenDSA: Sorting Terminology and Notation](https://opendsa.org/OpenDSA/Books/Catalog/html/SortNotation.html).
