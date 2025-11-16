from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import deque

@dataclass
class Employee:
    name: str
    email: str

class SecretSantaAssigner:
    """
    Build bipartite graph and do maximum matching (Hopcroft-Karp).
    """

    def __init__(self, employees: List[Employee], previous: Optional[Dict[str, str]] = None):
        if not employees:
            raise ValueError("Employee list is empty.")
        # ensure emails unique
        emails = [e.email for e in employees]
        if len(set(emails)) != len(emails):
            raise ValueError("Duplicate employee emails in input.")
        self.employees = employees
        self.prev = previous or {}
        self.N = len(employees)
        # mapping email to index
        self.left_index = {e.email: i for i, e in enumerate(employees)}
        self.right_index = {e.email: i for i, e in enumerate(employees)}
        self.graph = [[] for _ in range(self.N)]
        self._build_graph()

    def _build_graph(self):
        for giver in self.employees:
            gi = self.left_index[giver.email]
            for recipient in self.employees:
                ri = self.right_index[recipient.email]
                if giver.email == recipient.email:
                    continue  # no self
                if giver.email in self.prev and self.prev[giver.email] == recipient.email:
                    continue  # avoid previous year's recipient
                self.graph[gi].append(ri)

    # Hopcroft-Karp implementation
    def maximum_matching(self) -> Dict[int, int]:
        N_left = self.N
        N_right = self.N
        pairU = [-1] * N_left
        pairV = [-1] * N_right
        dist = [-1] * N_left

        INF = 10**9

        def bfs() -> bool:
            queue = deque()
            for u in range(N_left):
                if pairU[u] == -1:
                    dist[u] = 0
                    queue.append(u)
                else:
                    dist[u] = INF
            found = False
            while queue:
                u = queue.popleft()
                for v in self.graph[u]:
                    if pairV[v] == -1:
                        found = True  # free node on right found at next layer
                    else:
                        if dist[pairV[v]] == INF:
                            dist[pairV[v]] = dist[u] + 1
                            queue.append(pairV[v])
            return found

        def dfs(u) -> bool:
            for v in self.graph[u]:
                if pairV[v] == -1 or (dist[pairV[v]] == dist[u] + 1 and dfs(pairV[v])):
                    pairU[u] = v
                    pairV[v] = u
                    return True
            dist[u] = INF
            return False

        matching = 0
        while bfs():
            for u in range(N_left):
                if pairU[u] == -1:
                    if dfs(u):
                        matching += 1

        # return mapping u->v for matched pairs
        result = {}
        for u in range(N_left):
            if pairU[u] != -1:
                result[u] = pairU[u]
        return result

    def assign(self) -> List[Tuple[Employee, Employee]]:
        matching = self.maximum_matching()
        if len(matching) != self.N:
            raise RuntimeError("No valid full assignment found given constraints.")
        assignments = []
        for giver_idx, recipient_idx in matching.items():
            giver = self.employees[giver_idx]
            recipient = self.employees[recipient_idx]
            assignments.append((giver, recipient))
        return assignments
