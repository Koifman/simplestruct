"""Fancier field subclasses."""


__all__ = [
    'TypedField',
]


from .struct import Field
from .type import TypeChecker


class TypedField(Field, TypeChecker):
    
    """A field with dynamically-checked type constraints.
    
    kind is a class or tuple of classes, as described in type.py.
    If seq is False, the field value must satisfy kind. Otherwise,
    the field value must be a sequence of elements that satisfy kind.
    The sequence gets converted to a tuple if it isn't already.
    If unique is also True, the elements must be distinct (as
    determined by kind.__eq__()).
    
    If or_none is True, None is a valid value.
    """
    
    def __init__(self, kind, *,
                 seq=False, unique=False, or_none=False, **kargs):
        super().__init__(**kargs)
        self.kind = kind
        self.seq = seq
        self.unique = unique
        self.or_none = or_none
    
    def copy(self):
        return type(self)(self.kind, seq=self.seq, unique=self.unique,
                          or_none=self.or_none, default=self.default)
    
    @property
    def kind(self):
        return self._kind
    @kind.setter
    def kind(self, k):
        self._kind = self.normalize_kind(k)
    
    def check(self, inst, value):
        """Raise TypeError if value doesn't satisfy the constraints
        for use on instance inst.
        """
        if not (self.or_none and value is None):
            if self.seq:
                self.checktype_seq(value, self.kind,
                                   unique=self.unique, inst=inst)
            else:
                self.checktype(value, self.kind, inst=inst)
    
    def normalize(self, inst, value):
        """Return value or a normalized form of it for use on
        instance inst.
        """
        if (not (self.or_none and value is None) and
            self.seq):
            value = tuple(value)
        return value
    
    def __set__(self, inst, value):
        self.check(inst, value)
        value = self.normalize(inst, value)
        super().__set__(inst, value)
