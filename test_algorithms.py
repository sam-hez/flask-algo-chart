import unittest

from not_optimized import remove_duplicate_users
from stack_queue_algorithms import stack_reverse, stack_search, queue_process


class TestAlgorithms(unittest.TestCase):
    def test_remove_duplicates_keeps_first_user_and_order(self):
        users = [{"id": 2, "name": "Ann"}, {"id": 1},
                 {"id": 2, "name": "Bob"}]
        self.assertEqual(remove_duplicate_users(users), users[:2])
        self.assertEqual(len(users), 3)

    def test_duplicate_edge_cases(self):
        for users in [[], [{"id": 1}], [{"id": 1}, {"id": 2}]]:
            self.assertEqual(remove_duplicate_users(users), users)
        self.assertEqual(remove_duplicate_users([{"id": 1}] * 4), [{"id": 1}])

    def test_stack_reverse(self):
        for values in [[], [1], [1, 2, 3], [2, 2, -1], ["a", "b"]]:
            original = values.copy()
            result, operations = stack_reverse(values)
            self.assertEqual(result, values[::-1])
            self.assertEqual(operations, 2 * len(values))
            self.assertEqual(values, original)

    def test_stack_search(self):
        values = [10, 20, 30]
        self.assertEqual(stack_search(values, 30), (True, 5))
        self.assertEqual(stack_search(values, 20), (True, 7))
        self.assertEqual(stack_search(values, 10), (True, 9))
        self.assertEqual(stack_search(values, 40), (False, 9))
        self.assertEqual(values, [10, 20, 30])

    def test_stack_search_edge_cases(self):
        self.assertEqual(stack_search([], 1), (False, 0))
        self.assertEqual(stack_search([1], 1), (True, 3))
        self.assertEqual(stack_search([1], 2), (False, 3))
        self.assertEqual(stack_search([2, 2], 2), (True, 4))
        self.assertEqual(stack_search([None], None), (True, 3))

    def test_queue_process(self):
        for values in [[], [1], [1, 2, 3], [2, 2, -1], ["a", None]]:
            original = values.copy()
            result, operations = queue_process(values)
            self.assertEqual(result, original)
            self.assertEqual(values, original)
            n = len(values)
            self.assertEqual(operations, n + n * (n + 1) // 2)


if __name__ == "__main__":
    unittest.main()
