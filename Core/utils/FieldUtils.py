from Core.game_objects.environment.neutral.Emptiness import Emptiness


class FieldUtils:

    @staticmethod
    def init_field(field_height, field_width):
        field = []
        for i in range(field_height):
            field.append([Emptiness() for _ in range(field_width)])
        return field

