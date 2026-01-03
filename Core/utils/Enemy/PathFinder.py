import heapq
from Core.utils.Enemy.Node import Node

class PathFinder:

    @staticmethod
    def find_path(map_, start, target):
        open_heap = []
        open_set = {}
        closed_set = set()

        start.g = 0
        start.h = PathFinder.heuristic(start, target)

        heapq.heappush(open_heap, (start.f, start))
        open_set[(start.x, start.y)] = start.f

        while open_heap:
            _, current = heapq.heappop(open_heap)
            open_set.pop((current.x, current.y), None)

            if current.x == target.x and current.y == target.y:
                path = []
                while current:
                    path.append(current)
                    current = current.parent
                path.reverse()
                return path

            closed_set.add((current.x, current.y))

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                nx, ny = current.x + dx, current.y + dy

                if not PathFinder.is_valid_cell(nx, ny, map_):
                    continue
                if not map_[ny][nx]:
                    continue
                if (nx, ny) in closed_set:
                    continue

                tentative_g = current.g + 1

                neighbor = Node(nx, ny)
                neighbor.g = tentative_g
                neighbor.h = PathFinder.heuristic(neighbor, target)
                neighbor.parent = current

                if (nx, ny) in open_set:
                    if tentative_g >= neighbor.g:
                        continue

                heapq.heappush(open_heap, (neighbor.f, neighbor))
                open_set[(nx, ny)] = neighbor.f

        return None

    @staticmethod
    def heuristic(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    @staticmethod
    def is_valid_cell(x, y, map_):
        return 0 <= y < len(map_) and 0 <= x < len(map_[0])
