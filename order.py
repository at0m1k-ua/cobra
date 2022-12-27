from abc import ABC, abstractmethod
from random import Random


class Order(ABC):
    @abstractmethod
    def __init__(self, _length: int, _current_id: int):
        pass

    @abstractmethod
    def move_forward(self):
        pass

    @abstractmethod
    def move_back(self):
        pass

    @abstractmethod
    def current_id(self):
        pass

    @abstractmethod
    def set_current_id(self, current_id: int):
        pass


class StraightOrder(Order):
    def __init__(self, length: int, current_id: int):
        self._length = length
        self._current_id = current_id

    def move_forward(self):
        self._current_id = (self._current_id + 1) % self._length

    def move_back(self):
        self._current_id = (self._current_id - 1) % self._length

    def current_id(self):
        return self._current_id

    def set_current_id(self, current_id: int):
        self._current_id = current_id


class ReverseOrder(StraightOrder):
    def move_forward(self):
        super().move_back()

    def move_back(self):
        super().move_forward()


class RandomOrder(Order):
    def __init__(self, length: int, current_id: int):
        self._length = length
        self._current_id = 0
        self.__current_index = 0

        self.__generate_random_order(length)
        self.set_current_id(current_id)

    def move_forward(self):
        self.__current_index = (self.__current_index + 1) % self._length
        self._current_id = self.__random_order[self.__current_index]

    def move_back(self):
        self.__current_index = (self.__current_index - 1) % self._length
        self._current_id = self.__random_order[self.__current_index]

    def __generate_random_order(self, length: int):
        straight_order = list(range(length))
        self.__random_order = list()
        random = Random()
        for i in range(length - 1, -1, -1):
            index = random.randint(0, i)
            self.__random_order.append(straight_order[index])
            del straight_order[index]

    def current_id(self):
        return self._current_id

    def set_current_id(self, current_id: int):
        self._current_id = current_id
        for i in range(len(self.__random_order)):
            if self.__random_order[i] == current_id:
                self.__current_index = i
