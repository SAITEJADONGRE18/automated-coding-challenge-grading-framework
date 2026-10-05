def range_sum_queries(nums: list[int], queries: list[list[int]]) -> list[int]:
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    return [prefix[right + 1] - prefix[left] for left, right in queries]
