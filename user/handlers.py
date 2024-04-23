import re
from abc import ABC, abstractmethod

# Precompile regular expressions
ALPHANUMERIC_PATTERN = re.compile(r'[a-zA-Z0-9_]+')
EMAIL_PATTERN = re.compile(r'.+@.+\..+')

class ValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)

class ValidationHandler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, value, field_name):
        pass

class LengthValidationHandler(ValidationHandler):
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, value, field_name):
        value = value.strip() if value is not None else None
        if value is None:
            raise ValidationException(f"{field_name} must be set")
        if len(value) < self.min:
            raise ValidationException(f"{field_name} must be more than {self.min} characters")
        if len(value) > self.max:
            raise ValidationException(f"{field_name} must be less than {self.max} characters")
        if self.next_handler is not None:
            self.next_handler.handle(value, field_name)

class AlphanumericValidationHandler(ValidationHandler):
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, value, field_name):
        if not ALPHANUMERIC_PATTERN.match(value):
            raise ValidationException(f"{field_name} must have only alphanumeric or underscore characters")
        if self.next_handler is not None:
            self.next_handler.handle(value, field_name)

class EmailValidationHandler(ValidationHandler):
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, value, field_name):
        if not EMAIL_PATTERN.match(value):
            raise ValidationException(f"{field_name} must be an email")
        if self.next_handler is not None:
            self.next_handler.handle(value, field_name)