def summarize_ranges(numbers):
    """
    Given a list of integers, returns a list of strings that summarize consecutive ranges.
    For example: [1, 2, 3, 5, 6, 9] => ["1-3", "5-6", "9"]
    """
    if not numbers:
        return []

    numbers = sorted(set(numbers))
    summarized = []

    start = prev = numbers[0]

    for num in numbers[1:]:
        if num == prev + 1:
            prev = num
        else:
            if start == prev:
                summarized.append(str(start))
            else:
                summarized.append(f"{start}-{prev}")
            start = prev = num

    if start == prev:
        summarized.append(str(start))
    else:
        summarized.append(f"{start}-{prev}")

    return summarized