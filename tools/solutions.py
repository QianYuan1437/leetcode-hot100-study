"""Original, concise Python 3 reference implementations for the HOT 100 set."""

SOLUTIONS = {
"1": '''class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, x in enumerate(nums):
            need = target - x
            if need in seen:
                return [seen[need], i]
            seen[x] = i''',
"49": '''from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs):
        groups = defaultdict(list)
        for word in strs:
            count = [0] * 26
            for ch in word:
                count[ord(ch) - ord("a")] += 1
            groups[tuple(count)].append(word)
        return list(groups.values())''',
"128": '''class Solution:
    def longestConsecutive(self, nums):
        values = set(nums)
        best = 0
        for x in values:
            if x - 1 not in values:
                length = 1
                while x + length in values:
                    length += 1
                best = max(best, length)
        return best''',
"283": '''class Solution:
    def moveZeroes(self, nums):
        write = 0
        for x in nums:
            if x != 0:
                nums[write] = x
                write += 1
        while write < len(nums):
            nums[write] = 0
            write += 1''',
"11": '''class Solution:
    def maxArea(self, height):
        left, right = 0, len(height) - 1
        answer = 0
        while left < right:
            answer = max(answer, (right - left) * min(height[left], height[right]))
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return answer''',
"15": '''class Solution:
    def threeSum(self, nums):
        nums.sort()
        answer = []
        for i in range(len(nums) - 2):
            if nums[i] > 0:
                break
            if i and nums[i] == nums[i - 1]:
                continue
            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    answer.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
        return answer''',
"42": '''class Solution:
    def trap(self, height):
        left, right = 0, len(height) - 1
        left_max = right_max = water = 0
        while left <= right:
            if left_max <= right_max:
                left_max = max(left_max, height[left])
                water += left_max - height[left]
                left += 1
            else:
                right_max = max(right_max, height[right])
                water += right_max - height[right]
                right -= 1
        return water''',
"3": '''class Solution:
    def lengthOfLongestSubstring(self, s):
        last = {}
        left = answer = 0
        for right, ch in enumerate(s):
            if ch in last:
                left = max(left, last[ch] + 1)
            last[ch] = right
            answer = max(answer, right - left + 1)
        return answer''',
"438": '''from collections import Counter

class Solution:
    def findAnagrams(self, s, p):
        need = Counter(p)
        window = Counter()
        answer = []
        left = 0
        for right, ch in enumerate(s):
            window[ch] += 1
            if right - left + 1 > len(p):
                old = s[left]
                window[old] -= 1
                if window[old] == 0:
                    del window[old]
                left += 1
            if window == need:
                answer.append(left)
        return answer''',
"560": '''from collections import defaultdict

class Solution:
    def subarraySum(self, nums, k):
        count = defaultdict(int)
        count[0] = 1
        prefix = answer = 0
        for x in nums:
            prefix += x
            answer += count[prefix - k]
            count[prefix] += 1
        return answer''',
"239": '''from collections import deque

class Solution:
    def maxSlidingWindow(self, nums, k):
        queue = deque()
        answer = []
        for i, x in enumerate(nums):
            while queue and queue[0] <= i - k:
                queue.popleft()
            while queue and nums[queue[-1]] <= x:
                queue.pop()
            queue.append(i)
            if i >= k - 1:
                answer.append(nums[queue[0]])
        return answer''',
"76": '''from collections import Counter, defaultdict

class Solution:
    def minWindow(self, s, t):
        if not t:
            return ""
        need = Counter(t)
        window = defaultdict(int)
        formed = left = 0
        best_len, best_left = float("inf"), 0
        for right, ch in enumerate(s):
            window[ch] += 1
            if ch in need and window[ch] == need[ch]:
                formed += 1
            while formed == len(need):
                if right - left + 1 < best_len:
                    best_len, best_left = right - left + 1, left
                old = s[left]
                window[old] -= 1
                if old in need and window[old] < need[old]:
                    formed -= 1
                left += 1
        return "" if best_len == float("inf") else s[best_left:best_left + best_len]''',
"53": '''class Solution:
    def maxSubArray(self, nums):
        current = best = nums[0]
        for x in nums[1:]:
            current = max(x, current + x)
            best = max(best, current)
        return best''',
"56": '''class Solution:
    def merge(self, intervals):
        intervals.sort(key=lambda pair: pair[0])
        merged = []
        for start, end in intervals:
            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
        return merged''',
"189": '''class Solution:
    def rotate(self, nums, k):
        n = len(nums)
        k %= n

        def reverse(left, right):
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1

        reverse(0, n - 1)
        reverse(0, k - 1)
        reverse(k, n - 1)''',
"238": '''class Solution:
    def productExceptSelf(self, nums):
        answer = [1] * len(nums)
        prefix = 1
        for i, x in enumerate(nums):
            answer[i] = prefix
            prefix *= x
        suffix = 1
        for i in range(len(nums) - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]
        return answer''',
"41": '''class Solution:
    def firstMissingPositive(self, nums):
        n = len(nums)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                target = nums[i] - 1
                nums[i], nums[target] = nums[target], nums[i]
        for i, x in enumerate(nums):
            if x != i + 1:
                return i + 1
        return n + 1''',
"73": '''class Solution:
    def setZeroes(self, matrix):
        rows, cols = len(matrix), len(matrix[0])
        first_col_zero = any(matrix[r][0] == 0 for r in range(rows))
        for r in range(rows):
            for c in range(1, cols):
                if matrix[r][c] == 0:
                    matrix[r][0] = matrix[0][c] = 0
        for r in range(rows - 1, -1, -1):
            for c in range(cols - 1, 0, -1):
                if matrix[r][0] == 0 or matrix[0][c] == 0:
                    matrix[r][c] = 0
            if first_col_zero:
                matrix[r][0] = 0''',
"54": '''class Solution:
    def spiralOrder(self, matrix):
        if not matrix:
            return []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        answer = []
        while top <= bottom and left <= right:
            answer.extend(matrix[top][left:right + 1])
            top += 1
            for r in range(top, bottom + 1):
                answer.append(matrix[r][right])
            right -= 1
            if top <= bottom:
                answer.extend(reversed(matrix[bottom][left:right + 1]))
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    answer.append(matrix[r][left])
                left += 1
        return answer''',
"48": '''class Solution:
    def rotate(self, matrix):
        n = len(matrix)
        for r in range(n):
            for c in range(r + 1, n):
                matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
        for row in matrix:
            row.reverse()''',
"240": '''class Solution:
    def searchMatrix(self, matrix, target):
        if not matrix or not matrix[0]:
            return False
        row, col = 0, len(matrix[0]) - 1
        while row < len(matrix) and col >= 0:
            value = matrix[row][col]
            if value == target:
                return True
            if value > target:
                col -= 1
            else:
                row += 1
        return False''',
"160": '''class Solution:
    def getIntersectionNode(self, headA, headB):
        a, b = headA, headB
        while a is not b:
            a = a.next if a else headB
            b = b.next if b else headA
        return a''',
"206": '''class Solution:
    def reverseList(self, head):
        previous, current = None, head
        while current:
            nxt = current.next
            current.next = previous
            previous, current = current, nxt
        return previous''',
"234": '''class Solution:
    def isPalindrome(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        previous = None
        while slow:
            nxt = slow.next
            slow.next = previous
            previous, slow = slow, nxt
        left, right = head, previous
        while right:
            if left.val != right.val:
                return False
            left, right = left.next, right.next
        return True''',
"141": '''class Solution:
    def hasCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False''',
"142": '''class Solution:
    def detectCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                seeker = head
                while seeker is not slow:
                    seeker = seeker.next
                    slow = slow.next
                return seeker
        return None''',
"21": '''class Solution:
    def mergeTwoLists(self, list1, list2):
        dummy = ListNode()
        tail = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next, list1 = list1, list1.next
            else:
                tail.next, list2 = list2, list2.next
            tail = tail.next
        tail.next = list1 or list2
        return dummy.next''',
"2": '''class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode()
        tail, carry = dummy, 0
        while l1 or l2 or carry:
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0
            carry, digit = divmod(x + y + carry, 10)
            tail.next = ListNode(digit)
            tail = tail.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next''',
"19": '''class Solution:
    def removeNthFromEnd(self, head, n):
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n + 1):
            fast = fast.next
        while fast:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return dummy.next''',
"24": '''class Solution:
    def swapPairs(self, head):
        dummy = ListNode(0, head)
        previous = dummy
        while previous.next and previous.next.next:
            first = previous.next
            second = first.next
            first.next = second.next
            second.next = first
            previous.next = second
            previous = first
        return dummy.next''',
"25": '''class Solution:
    def reverseKGroup(self, head, k):
        dummy = ListNode(0, head)
        group_previous = dummy
        while True:
            kth = group_previous
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next
            group_next = kth.next
            previous, current = group_next, group_previous.next
            while current is not group_next:
                nxt = current.next
                current.next = previous
                previous, current = current, nxt
            old_head = group_previous.next
            group_previous.next = kth
            group_previous = old_head''',
"138": '''class Solution:
    def copyRandomList(self, head):
        current = head
        while current:
            clone = Node(current.val, current.next)
            current.next = clone
            current = clone.next
        current = head
        while current:
            current.next.random = current.random.next if current.random else None
            current = current.next.next
        dummy = Node(0)
        clone_tail = dummy
        current = head
        while current:
            clone = current.next
            current.next = clone.next
            clone_tail.next = clone
            clone_tail = clone
            current = current.next
        return dummy.next''',
"148": '''class Solution:
    def sortList(self, head):
        if not head or not head.next:
            return head
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        right = slow.next
        slow.next = None
        left = self.sortList(head)
        right = self.sortList(right)
        dummy = ListNode()
        tail = dummy
        while left and right:
            if left.val <= right.val:
                tail.next, left = left, left.next
            else:
                tail.next, right = right, right.next
            tail = tail.next
        tail.next = left or right
        return dummy.next''',
"23": '''import heapq
from itertools import count

class Solution:
    def mergeKLists(self, lists):
        heap = []
        serial = count()
        for node in lists:
            if node:
                heapq.heappush(heap, (node.val, next(serial), node))
        dummy = ListNode()
        tail = dummy
        while heap:
            _, _, node = heapq.heappop(heap)
            tail.next = node
            tail = node
            if node.next:
                heapq.heappush(heap, (node.next.val, next(serial), node.next))
        return dummy.next''',
"146": '''class Node:
    def __init__(self, key=0, value=0):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_first(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self._remove(node)
        self._add_first(node)
        return node.value

    def put(self, key, value):
        if key in self.nodes:
            self._remove(self.nodes[key])
        node = Node(key, value)
        self.nodes[key] = node
        self._add_first(node)
        if len(self.nodes) > self.capacity:
            old = self.tail.prev
            self._remove(old)
            del self.nodes[old.key]''',
"94": '''class Solution:
    def inorderTraversal(self, root):
        answer, stack = [], []
        current = root
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            answer.append(current.val)
            current = current.right
        return answer''',
"104": '''class Solution:
    def maxDepth(self, root):
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))''',
"226": '''class Solution:
    def invertTree(self, root):
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root''',
"101": '''class Solution:
    def isSymmetric(self, root):
        def mirror(left, right):
            if not left or not right:
                return left is right
            return (left.val == right.val
                    and mirror(left.left, right.right)
                    and mirror(left.right, right.left))
        return mirror(root.left, root.right) if root else True''',
"543": '''class Solution:
    def diameterOfBinaryTree(self, root):
        answer = 0
        def depth(node):
            nonlocal answer
            if not node:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            answer = max(answer, left + right)
            return 1 + max(left, right)
        depth(root)
        return answer''',
"102": '''from collections import deque

class Solution:
    def levelOrder(self, root):
        if not root:
            return []
        queue = deque([root])
        answer = []
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            answer.append(level)
        return answer''',
"108": '''class Solution:
    def sortedArrayToBST(self, nums):
        def build(left, right):
            if left > right:
                return None
            mid = (left + right) // 2
            root = TreeNode(nums[mid])
            root.left = build(left, mid - 1)
            root.right = build(mid + 1, right)
            return root
        return build(0, len(nums) - 1)''',
"98": '''class Solution:
    def isValidBST(self, root):
        def valid(node, low, high):
            if not node:
                return True
            if not low < node.val < high:
                return False
            return valid(node.left, low, node.val) and valid(node.right, node.val, high)
        return valid(root, float("-inf"), float("inf"))''',
"230": '''class Solution:
    def kthSmallest(self, root, k):
        stack = []
        current = root
        while True:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            k -= 1
            if k == 0:
                return current.val
            current = current.right''',
"199": '''from collections import deque

class Solution:
    def rightSideView(self, root):
        if not root:
            return []
        queue = deque([root])
        answer = []
        while queue:
            for i in range(len(queue)):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            answer.append(node.val)
        return answer''',
"114": '''class Solution:
    def flatten(self, root):
        previous = None
        def visit(node):
            nonlocal previous
            if not node:
                return
            visit(node.right)
            visit(node.left)
            node.right = previous
            node.left = None
            previous = node
        visit(root)''',
"105": '''class Solution:
    def buildTree(self, preorder, inorder):
        positions = {value: i for i, value in enumerate(inorder)}
        pre_index = 0
        def build(left, right):
            nonlocal pre_index
            if left > right:
                return None
            value = preorder[pre_index]
            pre_index += 1
            root = TreeNode(value)
            mid = positions[value]
            root.left = build(left, mid - 1)
            root.right = build(mid + 1, right)
            return root
        return build(0, len(inorder) - 1)''',
"437": '''from collections import defaultdict

class Solution:
    def pathSum(self, root, targetSum):
        count = defaultdict(int)
        count[0] = 1
        def visit(node, prefix):
            if not node:
                return 0
            prefix += node.val
            answer = count[prefix - targetSum]
            count[prefix] += 1
            answer += visit(node.left, prefix) + visit(node.right, prefix)
            count[prefix] -= 1
            return answer
        return visit(root, 0)''',
"236": '''class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root or root is p or root is q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left or right''',
"124": '''class Solution:
    def maxPathSum(self, root):
        answer = float("-inf")
        def gain(node):
            nonlocal answer
            if not node:
                return 0
            left = max(0, gain(node.left))
            right = max(0, gain(node.right))
            answer = max(answer, node.val + left + right)
            return node.val + max(left, right)
        gain(root)
        return answer''',
"200": '''class Solution:
    def numIslands(self, grid):
        rows, cols = len(grid), len(grid[0])
        def flood(row, col):
            if not (0 <= row < rows and 0 <= col < cols) or grid[row][col] != "1":
                return
            grid[row][col] = "0"
            flood(row + 1, col)
            flood(row - 1, col)
            flood(row, col + 1)
            flood(row, col - 1)
        answer = 0
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == "1":
                    answer += 1
                    flood(row, col)
        return answer''',
"994": '''from collections import deque

class Solution:
    def orangesRotting(self, grid):
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh = 0
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 2:
                    queue.append((row, col))
                elif grid[row][col] == 1:
                    fresh += 1
        minutes = 0
        while queue and fresh:
            for _ in range(len(queue)):
                row, col = queue.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))
            minutes += 1
        return minutes if fresh == 0 else -1''',
"207": '''from collections import deque

class Solution:
    def canFinish(self, numCourses, prerequisites):
        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)
            indegree[course] += 1
        queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
        completed = 0
        while queue:
            node = queue.popleft()
            completed += 1
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        return completed == numCourses''',
"208": '''class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def _find(self, text):
        node = self.root
        for ch in text:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._find(word)
        return bool(node and node.is_end)

    def startsWith(self, prefix):
        return self._find(prefix) is not None''',
"46": '''class Solution:
    def permute(self, nums):
        answer, path = [], []
        used = [False] * len(nums)
        def backtrack():
            if len(path) == len(nums):
                answer.append(path.copy())
                return
            for i, x in enumerate(nums):
                if used[i]:
                    continue
                used[i] = True
                path.append(x)
                backtrack()
                path.pop()
                used[i] = False
        backtrack()
        return answer''',
"78": '''class Solution:
    def subsets(self, nums):
        answer, path = [], []
        def backtrack(start):
            answer.append(path.copy())
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()
        backtrack(0)
        return answer''',
"17": '''class Solution:
    def letterCombinations(self, digits):
        if not digits:
            return []
        letters = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
        }
        answer, path = [], []
        def backtrack(index):
            if index == len(digits):
                answer.append("".join(path))
                return
            for ch in letters[digits[index]]:
                path.append(ch)
                backtrack(index + 1)
                path.pop()
        backtrack(0)
        return answer''',
"39": '''class Solution:
    def combinationSum(self, candidates, target):
        candidates.sort()
        answer, path = [], []
        def backtrack(start, remain):
            if remain == 0:
                answer.append(path.copy())
                return
            for i in range(start, len(candidates)):
                value = candidates[i]
                if value > remain:
                    break
                path.append(value)
                backtrack(i, remain - value)
                path.pop()
        backtrack(0, target)
        return answer''',
"22": '''class Solution:
    def generateParenthesis(self, n):
        answer, path = [], []
        def backtrack(left, right):
            if len(path) == 2 * n:
                answer.append("".join(path))
                return
            if left < n:
                path.append("(")
                backtrack(left + 1, right)
                path.pop()
            if right < left:
                path.append(")")
                backtrack(left, right + 1)
                path.pop()
        backtrack(0, 0)
        return answer''',
"79": '''class Solution:
    def exist(self, board, word):
        rows, cols = len(board), len(board[0])
        def search(row, col, index):
            if index == len(word):
                return True
            if not (0 <= row < rows and 0 <= col < cols) or board[row][col] != word[index]:
                return False
            saved = board[row][col]
            board[row][col] = "#"
            found = (search(row + 1, col, index + 1) or
                     search(row - 1, col, index + 1) or
                     search(row, col + 1, index + 1) or
                     search(row, col - 1, index + 1))
            board[row][col] = saved
            return found
        return any(search(r, c, 0) for r in range(rows) for c in range(cols))''',
"131": '''class Solution:
    def partition(self, s):
        answer, path = [], []
        def is_palindrome(left, right):
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True
        def backtrack(start):
            if start == len(s):
                answer.append(path.copy())
                return
            for end in range(start, len(s)):
                if is_palindrome(start, end):
                    path.append(s[start:end + 1])
                    backtrack(end + 1)
                    path.pop()
        backtrack(0)
        return answer''',
"51": '''class Solution:
    def solveNQueens(self, n):
        answer = []
        queens = [-1] * n
        columns, diagonal1, diagonal2 = set(), set(), set()
        def backtrack(row):
            if row == n:
                answer.append(["." * col + "Q" + "." * (n - col - 1) for col in queens])
                return
            for col in range(n):
                if col in columns or row - col in diagonal1 or row + col in diagonal2:
                    continue
                queens[row] = col
                columns.add(col); diagonal1.add(row - col); diagonal2.add(row + col)
                backtrack(row + 1)
                columns.remove(col); diagonal1.remove(row - col); diagonal2.remove(row + col)
        backtrack(0)
        return answer''',
"35": '''class Solution:
    def searchInsert(self, nums, target):
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left''',
"74": '''class Solution:
    def searchMatrix(self, matrix, target):
        rows, cols = len(matrix), len(matrix[0])
        left, right = 0, rows * cols
        while left < right:
            mid = (left + right) // 2
            value = matrix[mid // cols][mid % cols]
            if value < target:
                left = mid + 1
            else:
                right = mid
        return left < rows * cols and matrix[left // cols][left % cols] == target''',
"34": '''class Solution:
    def searchRange(self, nums, target):
        def lower_bound(value):
            left, right = 0, len(nums)
            while left < right:
                mid = (left + right) // 2
                if nums[mid] < value:
                    left = mid + 1
                else:
                    right = mid
            return left
        left = lower_bound(target)
        if left == len(nums) or nums[left] != target:
            return [-1, -1]
        return [left, lower_bound(target + 1) - 1]''',
"33": '''class Solution:
    def search(self, nums, target):
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1''',
"153": '''class Solution:
    def findMin(self, nums):
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        return nums[left]''',
"4": '''class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        left_size = (m + n + 1) // 2
        low, high = 0, m
        while low <= high:
            i = (low + high) // 2
            j = left_size - i
            a_left = nums1[i - 1] if i else float("-inf")
            a_right = nums1[i] if i < m else float("inf")
            b_left = nums2[j - 1] if j else float("-inf")
            b_right = nums2[j] if j < n else float("inf")
            if a_left <= b_right and b_left <= a_right:
                if (m + n) % 2:
                    return max(a_left, b_left)
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
            if a_left > b_right:
                high = i - 1
            else:
                low = i + 1''',
"20": '''class Solution:
    def isValid(self, s):
        expected = {"(": ")", "[": "]", "{": "}"}
        stack = []
        for ch in s:
            if ch in expected:
                stack.append(expected[ch])
            elif not stack or stack.pop() != ch:
                return False
        return not stack''',
"155": '''class MinStack:
    def __init__(self):
        self.values = []
        self.minimums = []

    def push(self, val):
        self.values.append(val)
        self.minimums.append(val if not self.minimums else min(val, self.minimums[-1]))

    def pop(self):
        self.minimums.pop()
        return self.values.pop()

    def top(self):
        return self.values[-1]

    def getMin(self):
        return self.minimums[-1]''',
"394": '''class Solution:
    def decodeString(self, s):
        stack = []
        current = []
        repeat = 0
        for ch in s:
            if ch.isdigit():
                repeat = repeat * 10 + int(ch)
            elif ch == "[":
                stack.append((current, repeat))
                current, repeat = [], 0
            elif ch == "]":
                prefix, times = stack.pop()
                current = prefix + current * times
            else:
                current.append(ch)
        return "".join(current)''',
"739": '''class Solution:
    def dailyTemperatures(self, temperatures):
        answer = [0] * len(temperatures)
        stack = []
        for i, value in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < value:
                previous = stack.pop()
                answer[previous] = i - previous
            stack.append(i)
        return answer''',
"84": '''class Solution:
    def largestRectangleArea(self, heights):
        values = [0] + heights + [0]
        stack = []
        answer = 0
        for i, height in enumerate(values):
            while stack and values[stack[-1]] > height:
                h = values[stack.pop()]
                width = i - stack[-1] - 1
                answer = max(answer, h * width)
            stack.append(i)
        return answer''',
"215": '''import heapq

class Solution:
    def findKthLargest(self, nums, k):
        heap = []
        for x in nums:
            heapq.heappush(heap, x)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]''',
"347": '''from collections import Counter

class Solution:
    def topKFrequent(self, nums, k):
        count = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for value, frequency in count.items():
            buckets[frequency].append(value)
        answer = []
        for frequency in range(len(buckets) - 1, 0, -1):
            for value in buckets[frequency]:
                answer.append(value)
                if len(answer) == k:
                    return answer''',
"295": '''import heapq

class MedianFinder:
    def __init__(self):
        self.low = []   # 最大堆：存负数
        self.high = []  # 最小堆

    def addNum(self, num):
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2''',
"121": '''class Solution:
    def maxProfit(self, prices):
        minimum = float("inf")
        answer = 0
        for price in prices:
            answer = max(answer, price - minimum)
            minimum = min(minimum, price)
        return answer''',
"55": '''class Solution:
    def canJump(self, nums):
        farthest = 0
        for i, step in enumerate(nums):
            if i > farthest:
                return False
            farthest = max(farthest, i + step)
            if farthest >= len(nums) - 1:
                return True
        return True''',
"45": '''class Solution:
    def jump(self, nums):
        jumps = end = farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == end:
                jumps += 1
                end = farthest
        return jumps''',
"763": '''class Solution:
    def partitionLabels(self, s):
        last = {ch: i for i, ch in enumerate(s)}
        answer = []
        start = end = 0
        for i, ch in enumerate(s):
            end = max(end, last[ch])
            if i == end:
                answer.append(end - start + 1)
                start = i + 1
        return answer''',
"70": '''class Solution:
    def climbStairs(self, n):
        if n <= 2:
            return n
        previous2, previous1 = 1, 2
        for _ in range(3, n + 1):
            previous2, previous1 = previous1, previous1 + previous2
        return previous1''',
"118": '''class Solution:
    def generate(self, numRows):
        triangle = []
        for i in range(numRows):
            row = [1] * (i + 1)
            for j in range(1, i):
                row[j] = triangle[-1][j - 1] + triangle[-1][j]
            triangle.append(row)
        return triangle''',
"198": '''class Solution:
    def rob(self, nums):
        previous2 = previous1 = 0
        for money in nums:
            previous2, previous1 = previous1, max(previous1, previous2 + money)
        return previous1''',
"279": '''class Solution:
    def numSquares(self, n):
        dp = [0] + [float("inf")] * n
        square = 1
        while square * square <= n:
            value = square * square
            for total in range(value, n + 1):
                dp[total] = min(dp[total], dp[total - value] + 1)
            square += 1
        return dp[n]''',
"322": '''class Solution:
    def coinChange(self, coins, amount):
        dp = [0] + [amount + 1] * amount
        for coin in coins:
            for total in range(coin, amount + 1):
                dp[total] = min(dp[total], dp[total - coin] + 1)
        return -1 if dp[amount] == amount + 1 else dp[amount]''',
"139": '''class Solution:
    def wordBreak(self, s, wordDict):
        words = set(wordDict)
        dp = [False] * (len(s) + 1)
        dp[0] = True
        for end in range(1, len(s) + 1):
            for start in range(end):
                if dp[start] and s[start:end] in words:
                    dp[end] = True
                    break
        return dp[-1]''',
"300": '''from bisect import bisect_left

class Solution:
    def lengthOfLIS(self, nums):
        tails = []
        for x in nums:
            index = bisect_left(tails, x)
            if index == len(tails):
                tails.append(x)
            else:
                tails[index] = x
        return len(tails)''',
"152": '''class Solution:
    def maxProduct(self, nums):
        maximum = minimum = answer = nums[0]
        for x in nums[1:]:
            if x < 0:
                maximum, minimum = minimum, maximum
            maximum = max(x, maximum * x)
            minimum = min(x, minimum * x)
            answer = max(answer, maximum)
        return answer''',
"416": '''class Solution:
    def canPartition(self, nums):
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        dp = [True] + [False] * target
        for x in nums:
            for value in range(target, x - 1, -1):
                dp[value] = dp[value] or dp[value - x]
        return dp[target]''',
"32": '''class Solution:
    def longestValidParentheses(self, s):
        stack = [-1]
        answer = 0
        for i, ch in enumerate(s):
            if ch == "(":
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    answer = max(answer, i - stack[-1])
        return answer''',
"62": '''class Solution:
    def uniquePaths(self, m, n):
        dp = [1] * n
        for _ in range(1, m):
            for col in range(1, n):
                dp[col] += dp[col - 1]
        return dp[-1]''',
"64": '''class Solution:
    def minPathSum(self, grid):
        rows, cols = len(grid), len(grid[0])
        dp = [0] * cols
        dp[0] = grid[0][0]
        for col in range(1, cols):
            dp[col] = dp[col - 1] + grid[0][col]
        for row in range(1, rows):
            dp[0] += grid[row][0]
            for col in range(1, cols):
                dp[col] = min(dp[col], dp[col - 1]) + grid[row][col]
        return dp[-1]''',
"5": '''class Solution:
    def longestPalindrome(self, s):
        best_left = best_right = 0
        def expand(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return left + 1, right - 1
        for center in range(len(s)):
            for left, right in (expand(center, center), expand(center, center + 1)):
                if right - left > best_right - best_left:
                    best_left, best_right = left, right
        return s[best_left:best_right + 1]''',
"1143": '''class Solution:
    def longestCommonSubsequence(self, text1, text2):
        rows, cols = len(text1), len(text2)
        dp = [[0] * (cols + 1) for _ in range(rows + 1)]
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[rows][cols]''',
"72": '''class Solution:
    def minDistance(self, word1, word2):
        rows, cols = len(word1), len(word2)
        dp = [[0] * (cols + 1) for _ in range(rows + 1)]
        for i in range(rows + 1):
            dp[i][0] = i
        for j in range(cols + 1):
            dp[0][j] = j
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[rows][cols]''',
"136": '''class Solution:
    def singleNumber(self, nums):
        answer = 0
        for x in nums:
            answer ^= x
        return answer''',
"169": '''class Solution:
    def majorityElement(self, nums):
        candidate = None
        count = 0
        for x in nums:
            if count == 0:
                candidate = x
            count += 1 if x == candidate else -1
        return candidate''',
"75": '''class Solution:
    def sortColors(self, nums):
        left = index = 0
        right = len(nums) - 1
        while index <= right:
            if nums[index] == 0:
                nums[left], nums[index] = nums[index], nums[left]
                left += 1
                index += 1
            elif nums[index] == 1:
                index += 1
            else:
                nums[index], nums[right] = nums[right], nums[index]
                right -= 1''',
"31": '''class Solution:
    def nextPermutation(self, nums):
        pivot = len(nums) - 2
        while pivot >= 0 and nums[pivot] >= nums[pivot + 1]:
            pivot -= 1
        if pivot >= 0:
            successor = len(nums) - 1
            while nums[successor] <= nums[pivot]:
                successor -= 1
            nums[pivot], nums[successor] = nums[successor], nums[pivot]
        left, right = pivot + 1, len(nums) - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1''',
"287": '''class Solution:
    def findDuplicate(self, nums):
        slow = nums[0]
        fast = nums[nums[0]]
        while slow != fast:
            slow = nums[slow]
            fast = nums[nums[fast]]
        finder = 0
        while finder != slow:
            finder = nums[finder]
            slow = nums[slow]
        return finder''',
}

