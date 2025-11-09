from abc import abstractmethod, ABC

from Core.game_objects.base.Interectable import Interectable


class PlayerCollection(Interectable, ABC):
    def __init__(self, view, foreground):
        super().__init__(view, foreground)

    @abstractmethod
    def can_be_destroyed(self, game_entity):
        pass