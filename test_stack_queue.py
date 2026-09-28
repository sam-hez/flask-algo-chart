import unittest

from stack_queue import Stack, Queue


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_new_stack(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)

    def test_push_and_pop_order(self):
        for value in [10, 20, 30]:
            self.stack.push(value)
        self.assertEqual(self.stack.size(), 3)
        self.assertFalse(self.stack.is_empty())
        for value in [30, 20, 10]:
            self.assertEqual(self.stack.pop(), value)
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)

    def test_peek_does_not_remove(self):
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.peek(), 20)
        self.assertEqual(self.stack.peek(), 20)
        self.assertEqual(self.stack.size(), 2)

    def test_empty_errors(self):
        with self.assertRaises(IndexError):
            self.stack.pop()
        with self.assertRaises(IndexError):
            self.stack.peek()

    def test_mixed_operations_and_reuse(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.stack.push(3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 1)
        self.stack.push(4)
        self.assertEqual(self.stack.pop(), 4)

    def test_duplicates_and_different_values(self):
        values = [0, -1, "hello", None, 0]
        for value in values:
            self.stack.push(value)
        for value in reversed(values):
            self.assertEqual(self.stack.pop(), value)

    def test_separate_stacks(self):
        other = Stack()
        self.stack.push(1)
        self.assertTrue(other.is_empty())


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_new_queue(self):
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)

    def test_enqueue_and_dequeue_order(self):
        for value in [10, 20, 30]:
            self.queue.enqueue(value)
        self.assertEqual(self.queue.size(), 3)
        self.assertFalse(self.queue.is_empty())
        for value in [10, 20, 30]:
            self.assertEqual(self.queue.dequeue(), value)
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)

    def test_peek_does_not_remove(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.peek(), 10)
        self.assertEqual(self.queue.peek(), 10)
        self.assertEqual(self.queue.size(), 2)

    def test_empty_errors(self):
        with self.assertRaises(IndexError):
            self.queue.dequeue()
        with self.assertRaises(IndexError):
            self.queue.peek()

    def test_mixed_operations_and_reuse(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.dequeue(), 1)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)
        self.queue.enqueue(4)
        self.assertEqual(self.queue.dequeue(), 4)

    def test_duplicates_and_different_values(self):
        values = [0, -1, "hello", None, 0]
        for value in values:
            self.queue.enqueue(value)
        for value in values:
            self.assertEqual(self.queue.dequeue(), value)

    def test_separate_queues(self):
        other = Queue()
        self.queue.enqueue(1)
        self.assertTrue(other.is_empty())


if __name__ == "__main__":
    unittest.main()
