class Node:
    def __init__(self, x: int, y: int):
        # координати клітинки
        self.x = x
        self.y = y
        # вартість шляху від початку до цієї клітинки
        self.g = 0
        # евристика вартість від цієї клітинки до кінця
        self.h = 0
        # посилання на попередній вузол
        self.parent = None
    
    # пріоритет вузла (чим менше тим більша пріоритет)
    @property
    def f(self):
        return self.g + self.h

    # порівняння вузлів за пріоритетом f
    def __lt__(self, other):
        return self.f < other.f
