""" Descriptors for attributes and methods for work thread classes in
mlpyqtgraph """


class AbstractDescriptor:
    """
    Abstract descriptor class that serves as base class for Descriptors
    """
    controller = None

    @classmethod
    def with_controller(cls, controller):
        """ Define a Descriptor class with defined controller """
        cls.controller = controller
        return cls

    def __init__(self):
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner=None):
        raise NotImplementedError

    def __repr__(self):
        return f'Descriptor(controller={repr(self.controller)}'


class AttributeDescriptor(AbstractDescriptor):
    """
    Custom descriptor for setting and getting class attributes in the main event
    loop

    This descriptor enables setting and getting object instance attributes using
    a controller. It expects the presence of a controller object and index on
    its parent object instance.
    """
    def __get__(self, obj, owner=None):
        return self.controller.request(obj.index, self.name)[0]

    def __set__(self, obj, value):
        kwargs = {self.name: value}
        self.controller.modify(obj.index, **kwargs)

    def __repr__(self):
        return 'Attribute' + super().__repr__()


class MethodDescriptor(AbstractDescriptor):
    """
    Custom descriptor for calling methods in the main event loop

    This descriptor enables calling method of an object instance using a custom
    controller. It expects the presence of a controller object and index on its
    parent object instance.
    """
    def __init__(self):
        super().__init__()
        self.index = None

    def __get__(self, obj, owner=None):
        try:
            self.index = obj.index
        except AttributeError:
            pass
        return self

    def __call__(self, *args, **kwargs):
        return self.controller.method(self.index, self.name, *args, **kwargs)

    def __repr__(self):
        return 'Method' + super().__repr__()



class DescriptorFactory:
    """
    Factory for attribute and method descriptors that correlate to attributes and methods of a class
    in another thread. Interaction is organized through a controller, which is required by the
    attribute and method descriptors.

    Note that we need to copy the classes AttributeDescriptor and MethodDescriptor (using
    inheritance) to avoid controller clashes with other factory instances.
    """
    def __init__(self, controller):
        self.controller = controller
        self.attribute_descriptor_class = self.copy_class(AttributeDescriptor)
        self.method_descriptor_class = self.copy_class(MethodDescriptor)

    @staticmethod
    def copy_class(original_class):
        """ Creates a copy of a class using inheritance """
        class ClassCopy(original_class):
            """ Copy of Class original_class """
        return ClassCopy

    def __repr__(self):
        return f'DescriptorFactory(controller={self.controller})'

    @property
    def attribute(self):
        """ Produce attribute descriptor class """
        return self.attribute_descriptor_class.with_controller(self.controller)

    @property
    def method(self):
        """ Produce attribute descriptor class """
        return self.method_descriptor_class.with_controller(self.controller)
