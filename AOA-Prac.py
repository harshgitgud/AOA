# PRACTICAL 01: SORTING ALGORITHMS

# 1. Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


numbers = [10, 45, 60, 90, 35, 40, 41]
print("Merge Sort")
print("Unsorted array:", numbers)
print("Sorted array:", merge_sort(numbers))


# 2. Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]
    left = [x for x in arr[:-1] if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr[:-1] if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


numbers = [10, 45, 60, 90, 35, 40, 41]
print("\nQuick Sort")
print("Unsorted array:", numbers)
print("Sorted array:", quick_sort(numbers))


# 3. Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


numbers = [12, 11, 13, 5, 6]
print("\nInsertion Sort")
print("Unsorted array:", numbers)
print("Sorted array:", insertion_sort(numbers.copy()))


# 4. Bubble Sort
def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


numbers = [64, 34, 25, 12, 22, 11, 90]
print("\nBubble Sort")
print("Unsorted array:", numbers)
print("Sorted array:", bubble_sort(numbers.copy()))


# 5. Selection Sort
def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


numbers = [64, 25, 12, 22, 11]
print("\nSelection Sort")
print("Unsorted array:", numbers)
print("Sorted array:", selection_sort(numbers.copy()))

# PRACTICAL 02: DIVIDE AND CONQUER ALGORITHMS

import timeit


# 1. Matrix Multiplication
def matrix_multiply(A, B):
    if not A or not B or len(A[0]) != len(B):
        raise ValueError("Incompatible matrix dimensions.")

    if any(len(row) != len(A[0]) for row in A):
        raise ValueError("Matrix A must be rectangular.")

    if any(len(row) != len(B[0]) for row in B):
        raise ValueError("Matrix B must be rectangular.")

    return [
        [
            sum(A[i][k] * B[k][j] for k in range(len(B)))
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


rA, cA = map(int, input("Enter rows and columns of Matrix A: ").split())
rB, cB = map(int, input("Enter rows and columns of Matrix B: ").split())

if cA != rB:
    print("Matrix multiplication is not possible.")
else:
    print("Enter Matrix A:")
    A = [list(map(int, input().split())) for _ in range(rA)]

    print("Enter Matrix B:")
    B = [list(map(int, input().split())) for _ in range(rB)]

    if any(len(row) != cA for row in A) or any(len(row) != cB for row in B):
        raise ValueError("Enter the correct number of elements in each row.")

    result = matrix_multiply(A, B)
    print("\nMatrix Multiplication Result:")
    for row in result:
        print(row)

    elapsed = timeit.timeit(lambda: matrix_multiply(A, B), number=1000)
    print(f"Execution time for 1000 runs: {elapsed:.6f} seconds")


# 2. Strassen Matrix Multiplication
def add_matrix(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def subtract_matrix(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def strassen(A, B):
    n = len(A)

    if n == 0 or n != len(B) or any(len(row) != n for row in A + B):
        raise ValueError("Strassen multiplication requires square matrices of equal size.")

    if n == 1:
        return [[A[0][0] * B[0][0]]]

    if n % 2 != 0:
        raise ValueError("Matrix size must be a power of 2 for this implementation.")

    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    M1 = strassen(add_matrix(A11, A22), add_matrix(B11, B22))
    M2 = strassen(add_matrix(A21, A22), B11)
    M3 = strassen(A11, subtract_matrix(B12, B22))
    M4 = strassen(A22, subtract_matrix(B21, B11))
    M5 = strassen(add_matrix(A11, A12), B22)
    M6 = strassen(subtract_matrix(A21, A11), add_matrix(B11, B12))
    M7 = strassen(subtract_matrix(A12, A22), add_matrix(B21, B22))

    C11 = add_matrix(subtract_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(add_matrix(subtract_matrix(M1, M2), M3), M6)

    return [C11[i] + C12[i] for i in range(mid)] + [
        C21[i] + C22[i] for i in range(mid)
    ]


n = int(input("\nEnter size of square matrix (power of 2): "))
if n <= 0 or n & (n - 1):
    print("Size must be a positive power of 2.")
else:
    print("Enter elements of Matrix A:")
    A = [list(map(int, input(f"Row {i + 1}: ").split())) for i in range(n)]
    print("Enter elements of Matrix B:")
    B = [list(map(int, input(f"Row {i + 1}: ").split())) for i in range(n)]

    if any(len(row) != n for row in A + B):
        raise ValueError("Each row must contain exactly n elements.")

    result = strassen(A, B)
    print("\nStrassen Multiplication Result:")
    for row in result:
        print(row)

    elapsed = timeit.timeit(lambda: strassen(A, B), number=100)
    print(f"Execution time for 100 runs: {elapsed:.6f} seconds")


# 3. Matrix Multiplication Using NumPy
def numpy_matrix_multiply():
    import numpy as np

    A = [[1, 2], [3, 4]]
    B = [[1, 2], [3, 4]]
    return np.dot(A, B)


try:
    print("\nNumPy Matrix Multiplication:")
    for row in numpy_matrix_multiply():
        print(row)
except ImportError:
    print("NumPy is not installed. Install it using: python -m pip install numpy")

# PRACTICAL 03: PROBABILISTIC AND RANDOMIZED ALGORITHMS

import random


# 1. Hiring Problem
def hire_one_of_ten(verbose=True):
    n = 10
    k = 3
    candidates = [random.randint(1, 10) for _ in range(n)]
    random.shuffle(candidates)
    actual_best = max(candidates)

    look_phase = candidates[:k]
    baseline = max(look_phase)

    if verbose:
        print("--- INTERVIEW PROCESS ---")
        print(f"Interviewed candidates 1 to {k}: {look_phase}")
        print(f"Rejected them all. Benchmark: {baseline}\n")

    selected = None

    for i, score in enumerate(candidates[k:], start=k + 1):
        if verbose:
            print(f"Candidate {i} score: {score}", end=" ")

        if score > baseline:
            selected = score
            if verbose:
                print("HIRED!")
            break

        if verbose:
            print("Rejected.")

    if selected is None:
        selected = candidates[-1]
        if verbose:
            print(f"\nNobody exceeded the benchmark. Candidate 10 is selected.")

    if verbose:
        print("\n--- SUMMARY ---")
        print("All candidate scores:", candidates)
        print("Actual best score:", actual_best)
        print("Selected score:", selected)
        print("SUCCESS" if selected == actual_best else "The best candidate was not selected.")

    return selected == actual_best


if __name__ == "__main__":
    hire_one_of_ten()

# PRACTICAL 04: SORTING AND ORDER STATISTICS

# 1. Counting Sort (supports negative integers)
def counting_sort(arr):
    if not arr:
        return []

    min_value = min(arr)
    max_value = max(arr)
    count = [0] * (max_value - min_value + 1)

    for num in arr:
        count[num - min_value] += 1

    result = []
    for index, frequency in enumerate(count):
        result.extend([index + min_value] * frequency)

    return result


numbers = [4, 2, 2, 8, 3, 3, 1]
print("Counting Sort")
print("Original Array:", numbers)
print("Sorted Array:", counting_sort(numbers))


# 2. Radix Sort (supports non-negative integers)
def counting_sort_by_digit(arr, exp):
    output = [0] * len(arr)
    count = [0] * 10

    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for num in reversed(arr):
        digit = (num // exp) % 10
        output[count[digit] - 1] = num
        count[digit] -= 1

    return output


def radix_sort(arr):
    if not arr:
        return []

    if any(num < 0 for num in arr):
        raise ValueError("Radix Sort in this  accepts non-negative integers only.")

    result = arr.copy()
    exp = 1
    max_value = max(result)

    while max_value // exp > 0:
        result = counting_sort_by_digit(result, exp)
        exp *= 10

    return result


numbers = [170, 45, 75, 90, 802, 24, 2, 66]
print("\nRadix Sort")
print("Original Array:", numbers)
print("Sorted Array:", radix_sort(numbers))


# 3. Bucket Sort
def bucket_sort(arr):
    if not arr:
        return []

    min_value = min(arr)
    max_value = max(arr)

    if min_value == max_value:
        return arr.copy()

    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]

    for num in arr:
        index = int((num - min_value) / (max_value - min_value) * (bucket_count - 1))
        buckets[index].append(num)

    result = []
    for bucket in buckets:
        result.extend(sorted(bucket))

    return result


numbers = [42, 32, 33, 52, 37, 47, 51]
print("\nBucket Sort")
print("Original Array:", numbers)
print("Sorted Array:", bucket_sort(numbers))


# 4. Find K-th Smallest and K-th Largest Elements
n = int(input("\nEnter the number of elements: "))
arr = [int(input(f"Element {i + 1}: ")) for i in range(n)]
k = int(input("Enter the value of k: "))

if k <= 0 or k > n:
    print("Invalid value of k.")
else:
    sorted_arr = sorted(arr)
    print("Sorted Array:", sorted_arr)
    print(f"{k}-th Smallest Element =", sorted_arr[k - 1])
    print(f"{k}-th Largest Element =", sorted_arr[-k])

# PRACTICAL 05: ADVANCED DATA STRUCTURES

# 1. Binary Tree Traversal - Inorder, Preorder and Postorder
class TraversalNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def inorder(root):
    if root:
        inorder(root.left)
        print(root.data, end=" ")
        inorder(root.right)


def preorder(root):
    if root:
        print(root.data, end=" ")
        preorder(root.left)
        preorder(root.right)


def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.data, end=" ")


root = TraversalNode(1)
root.left = TraversalNode(2)
root.right = TraversalNode(3)

print("Inorder:")
inorder(root)
print("\nPreorder:")
preorder(root)
print("\nPostorder:")
postorder(root)


# 2. Iterative Traversal and Search in a Binary Tree
class IterativeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def traversal(root):
    if root is None:
        return

    stack = [root]
    while stack:
        node = stack.pop()
        print(node.data, end=" ")

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)


def search_tree(root, key):
    if root is None:
        return False

    stack = [root]
    while stack:
        node = stack.pop()

        if node.data == key:
            return True
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return False


root = IterativeNode(int(input("\n\nEnter root: ")))
root.left = IterativeNode(int(input("Enter left child: ")))
root.right = IterativeNode(int(input("Enter right child: ")))
print("Traversal:", end=" ")
traversal(root)

key = int(input("\nEnter value to search: "))
print("Value found" if search_tree(root, key) else "Value not found")


# 3. Counting Nodes in a Binary Tree
class CountNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def count_nodes(root):
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def count_leaf(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaf(root.left) + count_leaf(root.right)


def count_internal(root):
    if root is None or (root.left is None and root.right is None):
        return 0
    return 1 + count_internal(root.left) + count_internal(root.right)


root = CountNode(1)
root.left = CountNode(2)
root.right = CountNode(3)
root.left.left = CountNode(4)
root.left.right = CountNode(5)

print("\n\nTotal nodes:", count_nodes(root))
print("Leaf nodes:", count_leaf(root))
print("Internal nodes:", count_internal(root))


# 4. Find Minimum and Maximum in a Binary Tree
class MinMaxNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def find_min(root):
    if root is None:
        return float("inf")
    return min(root.data, find_min(root.left), find_min(root.right))


def find_max(root):
    if root is None:
        return float("-inf")
    return max(root.data, find_max(root.left), find_max(root.right))


root = MinMaxNode(10)
root.left = MinMaxNode(5)
root.right = MinMaxNode(20)
root.left.left = MinMaxNode(3)
root.left.right = MinMaxNode(7)

print("\nMinimum:", find_min(root))
print("Maximum:", find_max(root))


# 5. Binary Search Tree and Searching
class BSTNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def insert(root, data):
    if root is None:
        return BSTNode(data)

    if data < root.data:
        root.left = insert(root.left, data)
    else:
        root.right = insert(root.right, data)

    return root


def search_bst(root, key):
    if root is None:
        return False
    if root.data == key:
        return True
    if key < root.data:
        return search_bst(root.left, key)
    return search_bst(root.right, key)


root = None
n = int(input("\nEnter number of BST nodes: "))
for _ in range(n):
    root = insert(root, int(input("Enter value: ")))

key = int(input("Enter element to search: "))
print("Element found" if search_bst(root, key) else "Element not found")

# PRACTICAL 06: GRAPH ALGORITHMS

from collections import defaultdict, deque
import heapq


# 1. Breadth-First Search (BFS)
class BFSGraph:
    def __init__(self):
        self.adj = defaultdict(list)

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)


def bfs(graph, start):
    visited = {start}
    order = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


g = BFSGraph()
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]
for u, v in edges:
    g.add_edge(u, v)
print("BFS traversal from A:", bfs(g, 'A'))


# 2. Depth-First Search (DFS)
class DFSGraph:
    def __init__(self):
        self.adj = defaultdict(list)

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)


def dfs(graph, start):
    visited = set()
    order = []
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)

            for neighbor in reversed(graph.adj[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return order


def dfs_recursive(graph, start, visited=None, order=None):
    if visited is None:
        visited = set()
        order = []

    visited.add(start)
    order.append(start)

    for neighbor in graph.adj[start]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)

    return order


g = DFSGraph()
for u, v in edges:
    g.add_edge(u, v)
print("\nDFS (iterative) from A:", dfs(g, 'A'))
print("DFS (recursive) from A:", dfs_recursive(g, 'A'))


# 3. Dijkstra's Shortest Path Algorithm
class WeightedGraph:
    def __init__(self):
        self.adj = defaultdict(list)
        self.nodes = set()

    def add_edge(self, u, v, weight):
        if weight < 0:
            raise ValueError("Dijkstra's algorithm does not support negative weights.")
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))
        self.nodes.update([u, v])


def dijkstra(graph, start):
    if start not in graph.nodes:
        raise ValueError("Starting node is not in the graph.")

    dist = {node: float('inf') for node in graph.nodes}
    prev = {node: None for node in graph.nodes}
    dist[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        distance, node = heapq.heappop(pq)
        if node in visited:
            continue

        visited.add(node)

        for neighbor, weight in graph.adj[node]:
            new_dist = distance + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

    return dist, prev


def reconstruct_path(prev, start, target):
    if target not in prev:
        return []

    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()
    return path if path and path[0] == start else []


g = WeightedGraph()
weighted_edges = [
    ('A', 'B', 4), ('A', 'C', 1), ('C', 'B', 2),
    ('B', 'D', 5), ('C', 'D', 8), ('D', 'E', 3), ('C', 'E', 10)
]
for u, v, weight in weighted_edges:
    g.add_edge(u, v, weight)

dist, prev = dijkstra(g, 'A')
print("\nShortest distances from A:", dist)
print("Shortest path A -> E:", reconstruct_path(prev, 'A', 'E'))


# 4. Kruskal's Algorithm (Minimum Spanning Tree)
class KruskalGraph:
    def __init__(self):
        self.edges = []
        self.nodes = set()

    def add_edge(self, u, v, weight):
        self.edges.append((u, v, weight))
        self.nodes.update([u, v])


class DisjointSet:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        return True


def kruskal(graph):
    disjoint_set = DisjointSet(graph.nodes)
    mst = []
    total_weight = 0

    for u, v, weight in sorted(graph.edges, key=lambda edge: edge[2]):
        if disjoint_set.union(u, v):
            mst.append((u, v, weight))
            total_weight += weight

    return mst, total_weight


kg = KruskalGraph()
for u, v, weight in weighted_edges:
    kg.add_edge(u, v, weight)
mst, total_weight = kruskal(kg)
print("\nKruskal MST edges:", mst)
print("Total weight:", total_weight)


# 5. Prim's Algorithm (Minimum Spanning Tree)
def prim(graph, start=None):
    if not graph.nodes:
        return [], 0

    if start is None:
        start = next(iter(graph.nodes))
    if start not in graph.nodes:
        raise ValueError("Starting node is not in the graph.")

    visited = {start}
    mst = []
    total_weight = 0
    edge_heap = [(weight, start, neighbor) for neighbor, weight in graph.adj[start]]
    heapq.heapify(edge_heap)

    while edge_heap and len(visited) < len(graph.nodes):
        weight, u, v = heapq.heappop(edge_heap)
        if v in visited:
            continue

        visited.add(v)
        mst.append((u, v, weight))
        total_weight += weight

        for next_v, next_weight in graph.adj[v]:
            if next_v not in visited:
                heapq.heappush(edge_heap, (next_weight, v, next_v))

    if len(visited) != len(graph.nodes):
        raise ValueError("The graph is disconnected; no spanning tree exists.")

    return mst, total_weight


mst, total_weight = prim(g, 'A')
print("\nPrim MST edges:", mst)
print("Total weight:", total_weight)


# PRACTICAL 07: STRING MATCHING ALGORITHMS

# 1. Naive String Matching Algorithm
def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)

    if m == 0:
        print("Empty pattern matches at every index.")
        return

    found = False
    for i in range(n - m + 1):
        j = 0

        while j < m and text[i + j] == pattern[j]:
            j += 1

        if j == m:
            print("Pattern found at index:", i)
            found = True

    if not found:
        print("Pattern not found.")


text = input("Enter the text: ")
pattern = input("Enter the pattern: ")
naive_search(text, pattern)


# 2. Knuth-Morris-Pratt (KMP) Algorithm
def create_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    if m == 0:
        print("Empty pattern matches at every index.")
        return

    lps = create_lps(pattern)
    i = j = 0
    found = False

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                print("Pattern found at index:", i - j)
                found = True
                j = lps[j - 1]
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

    if not found:
        print("Pattern not found.")


text = input("\nEnter the text for KMP: ")
pattern = input("Enter the pattern for KMP: ")
kmp_search(text, pattern)


# PRACTICAL 08: DYNAMIC PROGRAMMING

# 1. Rod Cutting
def rod_cutting(prices, n):
    if n < 0 or n > len(prices):
        raise ValueError("Rod length must be between 0 and the number of prices.")

    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        max_value = float("-inf")

        for j in range(1, i + 1):
            max_value = max(max_value, prices[j - 1] + dp[i - j])

        dp[i] = max_value

    return dp[n]


prices = [1, 5, 8, 9]
rod_length = 4
print("Rod Cutting")
print(f"Maximum profit for length {rod_length}: {rod_cutting(prices, rod_length)}")


# 2. Matrix Chain Multiplication
def matrix_chain_order(dimensions):
    n = len(dimensions) - 1
    if n <= 0:
        return 0

    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for chain_length in range(2, n + 1):
        for i in range(1, n - chain_length + 2):
            j = i + chain_length - 1
            dp[i][j] = float("inf")

            for k in range(i, j):
                cost = (
                    dp[i][k]
                    + dp[k + 1][j]
                    + dimensions[i - 1] * dimensions[k] * dimensions[j]
                )
                dp[i][j] = min(dp[i][j], cost)

    return dp[1][n]


dimensions = [10, 30, 5, 60]
print("\nMatrix Chain Multiplication")
print("Minimum multiplication operations:", matrix_chain_order(dimensions))


# 3. Longest Common Subsequence (LCS)
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs_chars = []
    i, j = m, n

    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], "".join(reversed(lcs_chars))


seq1 = "BATMAN"
seq2 = "CATWOMAN"
length, sequence = longest_common_subsequence(seq1, seq2)
print("\nLongest Common Subsequence")
print(f"LCS Length: {length}, Subsequence: '{sequence}'")


# PRACTICAL 09: GREEDY ALGORITHMS
# This practical heading is inferred from the two algorithms in the supplied journal.

import heapq


# 1. Huffman Coding
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def print_huffman_codes(node, current_code=""):
    if node is None:
        return

    if node.char is not None:
        print(f"Character: {node.char} | Huffman Code: {current_code or '0'}")

    print_huffman_codes(node.left, current_code + "0")
    print_huffman_codes(node.right, current_code + "1")


def huffman_coding(chars, freqs):
    if len(chars) != len(freqs) or not chars:
        raise ValueError("Characters and frequencies must have the same non-zero length.")

    if len(set(chars)) != len(chars) or any(freq < 0 for freq in freqs):
        raise ValueError("Characters must be unique and frequencies non-negative.")

    nodes = []
    for char, freq in zip(chars, freqs):
        heapq.heappush(nodes, HuffmanNode(char, freq))

    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)

        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(nodes, merged)

    print("\n--- Huffman Codes ---")
    print_huffman_codes(nodes[0])


# 2. Activity Selection Algorithm
def activity_selection(activities):
    if not activities:
        return []

    sorted_activities = sorted(activities, key=lambda activity: activity[1])
    selected = [sorted_activities[0]]
    last_finish_time = sorted_activities[0][1]

    for start_time, finish_time in sorted_activities[1:]:
        if start_time >= last_finish_time:
            selected.append((start_time, finish_time))
            last_finish_time = finish_time

    return selected


if __name__ == "__main__":
    characters = ['A', 'B', 'C', 'D', 'E', 'F']
    frequencies = [5, 9, 12, 13, 16, 45]
    huffman_coding(characters, frequencies)

    activities = [
        (1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9),
        (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)
    ]
    result = activity_selection(activities)
    print("\n--- Activity Selection ---")
    print("Maximum number of activities:", len(result))
    print("Selected Activities (Start, Finish):")
    for activity in result:
        print(f"Start: {activity[0]}, Finish: {activity[1]}")


# PRACTICAL 10: APPROXIMATION ALGORITHM - VERTEX COVER

def approximate_vertex_cover(edges):
    visited = set()
    vertex_cover = []

    for u, v in edges:
        if u not in visited and v not in visited:
            visited.add(u)
            visited.add(v)
            vertex_cover.extend([u, v])

    return vertex_cover


# Main Program
print("Approximation Algorithm - Vertex Cover")

try:
    vertices_count = int(input("Enter number of vertices: ").strip())
    edges_count = int(input("Enter number of edges: ").strip())

    if vertices_count < 0 or edges_count < 0:
        raise ValueError("Counts cannot be negative.")

    edges = []
    print(f"Enter {edges_count} edges (format: u v):")

    for _ in range(edges_count):
        u, v = map(int, input().split())
        if not (0 <= u < vertices_count and 0 <= v < vertices_count):
            raise ValueError("Vertex number is outside the specified range.")
        edges.append((u, v))

    vertex_cover = approximate_vertex_cover(edges)
    print("\nApproximate Vertex Cover:", sorted(vertex_cover))
    print("Size of Vertex Cover:", len(vertex_cover))

except (ValueError, IndexError):
    print("\nError: Invalid input. Enter valid integer counts and edge pairs.")
