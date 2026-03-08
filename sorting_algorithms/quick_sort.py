def quick_sort(arr: list) -> list:
    """Sorts an array using the quick sort algorithm.

    :param arr: List of elements to be sorted.
    :return: Sorted list of elements.
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)
