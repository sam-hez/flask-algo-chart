from stack_queue import Stack, Queue


def stack_reverse(values):
    stack = Stack()
    operations = 0
    for value in values:
        stack.push(value)
        operations += 1

    result = []
    while not stack.is_empty():
        result.append(stack.pop())
        operations += 1

    return result, operations


def stack_search(values, target):
    stack = Stack()
    operations = 0
    for value in values:
        stack.push(value)
        operations += 1

    while not stack.is_empty():
        value = stack.pop()
        operations += 2  # One pop and one comparison.
        if value == target:
            return True, operations

    return False, operations


def queue_process(values):
    queue = Queue()
    operations = 0
    for value in values:
        queue.enqueue(value)
        operations += 1

    result = []
    while not queue.is_empty():
        # One removal plus shifting the remaining items in the list.
        operations += queue.size()
        result.append(queue.dequeue())

    return result, operations
