from collections import OrderedDict

from graphene.utils.get_unbound_function import get_unbound_function
from graphene.utils.props import props
from graphene.types.field import Field
from graphene.types.objecttype import ObjectType, ObjectTypeOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene.utils.deprecated import warn_deprecation


class FieldResolverOptions(ObjectTypeOptions):
    arguments = None  # type: Dict[str, Argument]
    output = None  # type: Type[ObjectType]
    resolver = None  # type: Callable


class FieldResolver(ObjectType):
    @classmethod
    def __init_subclass_with_meta__(cls, resolver=None, output=None, arguments=None,
                                    _meta=None, **options):
        if not _meta:
            _meta = FieldResolverOptions(cls)

        output = output or getattr(cls, 'Output', None)
        fields = {}
        if not output:
            # If output is defined, we don't need to get the fields
            fields = OrderedDict()
            for base in reversed(cls.__mro__):
                fields.update(
                    yank_fields_from_attrs(base.__dict__, _as=Field)
                )
            output = cls

        if not arguments:
            input_class = getattr(cls, 'Arguments', None)
            if input_class:
                arguments = props(input_class)
            else:
                arguments = {}

        if not resolver:
            _resolver = getattr(cls, 'resolve', None)
            assert _resolver, 'All field resolvers must define a resolve method'
            resolver = get_unbound_function(_resolver)

        if _meta.fields:
            _meta.fields.update(fields)
        else:
            _meta.fields = fields

        _meta.output = output
        _meta.resolver = resolver
        _meta.arguments = arguments

        super(FieldResolver, cls).__init_subclass_with_meta__(
            _meta=_meta, **options)

    @classmethod
    def Field(cls, name=None, description=None, deprecation_reason=None, required=False):
        return Field(
            cls._meta.output,
            args=cls._meta.arguments,
            resolver=cls._meta.resolver,
            name=name,
            description=description,
            deprecation_reason=deprecation_reason,
            required=required,
        )
