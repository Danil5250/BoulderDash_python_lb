import heapq
from Core.utils.Enemy.Node import Node

class PathFinder:

    @staticmethod
    def find_path(map, start, target):
        # пріоритетна черга, з якої дістаємо вузол з найменшим f
        open_heap = []
        # словник для швидкої перевірки що координати відкриті
        open_set = {}
        # множина координат, які повністю опрацьовані
        closed_set = set()
    
        # початкова вартість шляху від початку до цієї клітинки = 0
        start.g = 0
        start.h = PathFinder.heuristic(start, target)

        # кладемо завжди мінімальний елемент
        heapq.heappush(open_heap, (start.f, start))
        # перевірка чи розглядається дана координата
        open_set[(start.x, start.y)] = start.f

        while open_heap:
        # прибираємо координати з відкритих бо більше не розглядається вузол з найменшим f
            _, current = heapq.heappop(open_heap)
            open_set.pop((current.x, current.y), None)

        # перевірка чи досягли цілі, якщо досягли - будуємо шлях назад з батьків
            if current.x == target.x and current.y == target.y:
                path = []
                while current:
                    path.append(current)
                    current = current.parent
                path.reverse()
                return path

        # розглядаємо сусідів (вгору, вниз, вліво, вправо)
        # перегляаємо що вони валідні, прохідні і не в закритому списку (не розглянуті ранішу)
            closed_set.add((current.x, current.y))

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                nx, ny = current.x + dx, current.y + dy

                if not PathFinder.is_valid_cell(nx, ny, map):
                    continue
                if not map[ny][nx]:
                    continue
                if (nx, ny) in closed_set:
                    continue
                
        # прихід із сусіда на 1 більший
                #tentative_g = 
                
        # посилання на сусідній вузол
                neighbor = Node(nx, ny)
                if (nx, ny) in open_set:
                    if current.g + 1 >= neighbor.g:
                        continue
                neighbor.g = current.g + 1
                neighbor.h = PathFinder.heuristic(neighbor, target)
                neighbor.parent = current
                 
        # відкидаємо довгі шляхи
                
                    
        # коротший шлях знайдено, додаємо в відкриті для подальшого розгляду
                heapq.heappush(open_heap, (neighbor.f, neighbor))
                open_set[(nx, ny)] = neighbor.f

        return None

    # евристична функція (Манхеттенська відстань) для знаходження вартості від поточної клітинки до цільової
    @staticmethod
    def heuristic(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    # чи клітинка в межах поля
    @staticmethod
    def is_valid_cell(x, y, map_):
        return 0 <= y < len(map_) and 0 <= x < len(map_[0])
