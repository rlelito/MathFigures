import abc


# descriptor - provides more functionality
class AutoStorage:
    _count = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls._count
        self.storage_name = f'_{prefix}#{index}'
        cls._count += 1

    def __get__(self, instance, owner):
        # if the call is not made by the instance, it returns the descriptor itself,
        # otherwise return the value of the managed attribute
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        # validation is delegated to the Validated class
        # (actually to classes inheriting it)
        setattr(instance, self.storage_name, value)


# abstract class but inherits from Auto Storage
class Validated(abc.ABC, AutoStorage):
    # __set__ delegates validation to the validate method
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)  # calling the parent class method (actual data recording)

    @abc.abstractmethod
    def validate(self, instance, value):
        """Returns a verified value or throws a ValueError exception"""


class Quantity(Validated):
    """Checks if the number is greater than the number given or zero by default"""

    def __init__(self, number=0):
        super().__init__()
        self.number = number

    def validate(self, instance, value):
        if value > self.number:
            return value
        else:
            raise ValueError(f"Value must be greater than {self.number}")


class NonBlank(Validated):
    """Checks for a non-empty string"""

    def validate(self, instance, value):
        if len(value.strip()) > 0:
            return value
        else:
            raise ValueError("Value must be a non-empty string")


class Range(Validated):
    """Checks if the number is in the range"""

    def __init__(self, start, end):
        super().__init__()
        self.range = (start, end)

    def validate(self, instance, value):
        start, end = self.range
        if start < value < end:
            return value
        else:
            raise ValueError(f"Value must be in the range ({start}, {end})")


class TypeAndQuantity(Validated):
    """Checks the type and whether the number is greater than the number (defaults to zero)"""

    def __init__(self, data_type=None, number=0):
        super().__init__()
        self.data_type = data_type
        self.number = number

    def validate(self, instance, value):
        if self.data_type is not None and isinstance(value, self.data_type) and value > self.number:
            return value
        elif self.data_type is not None:
            raise ValueError(f"Value must be a number greater than {self.number} and be of type {self.data_type.__name__}")
        # else:
        #     raise ValueError("Value must be a number greater than zero!")
