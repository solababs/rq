from abc import ABCMeta
from functools import partial
from .exceptions import UnpickleError, DeserializationError

try:
    import cPickle as pickle
except ImportError:  # noqa  # pragma: no cover
    import pickle


class BaseSerializer(object):
    __metaclass__ = ABCMeta

    def serialize(self, value):
        raise NotImplementedError('This method must be implemented')

    def deserialize(self, value):
        raise NotImplementedError('This method must be implemented')


class DefaultSerializer(BaseSerializer):
    """DefaultSerializer Class that uses the pickle module."""
    def __init__(self):
        self.serializer = pickle

    def serialize(self, data):
        try:
            serialized_data = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)(data)
        except Exception as e:
            raise UnpickleError('Unpickleable return value', data, e)

        return serialized_data

    def deserialize(self, pickled_string):
        try:
            obj = self.serializer.loads(pickled_string)
        except Exception as e:
            raise UnpickleError('Could not unpickle', pickled_string, e)

        return obj


class CustomSerializer(BaseSerializer):
    """CustomSerializer Class that uses the user specified serializer module."""
    def __init__(self, serializer):
        self.serializer = serializer

    def serialize(self, data):
        try:
            serialized_data = self.serializer.dumps(data)
        except Exception as e:
            raise DeserializationError("Unserializable return value", data, e)

        return serialized_data

    def deserialize(self, serialized_string):
        try:
            obj = self.serializer.loads(serialized_string)
        except Exception as e:
            raise DeserializationError('Could not deserialize', serialized_string, e)

        return obj


def resolve_serializer(serializer):
    """This function checks the user defined serializer for ('dumps', 'loads') methods
    It returns a DefaultSerializer if not found else it returns a CustomSerializer
    The returned serializer objects implement ('serialize', 'deserialize') methods
    for the ('dumps', 'loads') methods respectively
    """
    if not serializer:
        return DefaultSerializer()

    default_serializer_methods = ('dumps', 'loads')

    for instance_method in default_serializer_methods:
        if not hasattr(serializer, instance_method):
            return DefaultSerializer()

    return CustomSerializer(serializer)
