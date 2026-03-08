from data_structures import MinHeap


def heap_sort(arr: list, ascending: bool = True) -> list:
    """Perform heap sort on the given list.

    :param arr: List of elements to be sorted.
    :param ascending: Whether to sort in ascending order (default is True).
    If False, sorts in descending order.
    :return: Sorted list of elements.
    """
    heap = MinHeap(arr)

    sorted_arr = []
    while heap.size > 0:
        min_ele = heap.get_min()
        sorted_arr.append(min_ele[0])

    if not ascending:
        sorted_arr.reverse()

    return sorted_arr
