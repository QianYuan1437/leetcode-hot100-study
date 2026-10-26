"""Representative executable tests for high-risk reference implementations."""
from __future__ import annotations

from solutions import SOLUTIONS


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class RandomNode:
    def __init__(self, val=0, next=None, random=None):
        self.val, self.next, self.random = val, next, random


def namespace(problem_id: str) -> dict[str, object]:
    scope = {"ListNode": ListNode, "TreeNode": TreeNode, "Node": RandomNode}
    exec(SOLUTIONS[problem_id], scope)
    return scope


def solution(problem_id: str):
    return namespace(problem_id)["Solution"]()


def linked(values):
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def linked_values(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values


def main() -> None:
    assert solution("1").twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert sorted(solution("15").threeSum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
    assert solution("42").trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert solution("239").maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert solution("76").minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert solution("41").firstMissingPositive([3, 4, -1, 1]) == 2

    matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    solution("73").setZeroes(matrix)
    assert matrix == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    assert solution("54").spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]

    assert linked_values(solution("25").reverseKGroup(linked([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    lru_type = namespace("146")["LRUCache"]
    cache = lru_type(2)
    cache.put(1, 1); cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)
    assert cache.get(2) == -1

    root = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert solution("124").maxPathSum(root) == 42
    assert solution("207").canFinish(2, [[1, 0]]) is True
    assert solution("207").canFinish(2, [[1, 0], [0, 1]]) is False
    trie_type = namespace("208")["Trie"]
    trie = trie_type(); trie.insert("apple")
    assert trie.search("apple") and not trie.search("app") and trie.startsWith("app")

    queens = solution("51").solveNQueens(4)
    assert len(queens) == 2 and all(len(board) == 4 for board in queens)
    assert solution("4").findMedianSortedArrays([1, 3], [2]) == 2
    assert solution("84").largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10

    median_type = namespace("295")["MedianFinder"]
    finder = median_type(); finder.addNum(1); finder.addNum(2)
    assert finder.findMedian() == 1.5
    finder.addNum(3)
    assert finder.findMedian() == 2

    assert solution("45").jump([2, 3, 1, 1, 4]) == 2
    assert solution("32").longestValidParentheses(")()())") == 4
    assert solution("72").minDistance("horse", "ros") == 3
    assert solution("287").findDuplicate([1, 3, 4, 2, 2]) == 2
    print("PASS: representative algorithm executions (arrays, windows, lists, trees, graphs, design, DP)")


if __name__ == "__main__":
    main()

