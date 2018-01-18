from six import itervalues
from flask_marshmallow import Schema


class Parameters(Schema):

    class Meta:
        ordered = True

    def __init__(self, **kwargs):
        super(Parameters, self).__init__(**kwargs)

        for required_field_name in getattr(self.Meta, 'required', []):
            self.fields[required_field_name].required = True

    def __contains__(self, field):
        return field in self.fields

    def make_instance(self, data):
        # pylint: disable=unused-argument
        """
        This is a no-op function which shadows ``ModelSchema.make_instance``
        method (when inherited classes inherit from ``ModelSchema``). Thus, we
        avoid a new instance creation because it is undesirable behaviour for
        parameters (they can be used not only for saving new instances).
        """
        return

class JSONParameters(Parameters):

    LOCATION = 'json'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in itervalues(self.fields):
            if field.dump_only:
                continue
            if not field.metadata.get('location'):
                field.metadata['location'] = self.LOCATION

class QueryParameters(Parameters):

    LOCATION = 'query'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in itervalues(self.fields):
            if field.dump_only:
                continue
            if not field.metadata.get('location'):
                field.metadata['location'] = self.LOCATION
