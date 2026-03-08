def merge_sort(arr: list) -> list:
    """Sorts an array using the merge sort algorithm.

    :param arr: List of elements to be sorted
    :return: Sorted list of elements
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)


def merge(left: list, right: list) -> list:
    """Merges two sorted lists into a single sorted list.

    :param left: First sorted list
    :param right: Second sorted list
    :return: Merged sorted list
    """
    merged = []
    left_index, right_index = 0, 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    # Append any remaining elements from both lists
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])

    return merged
