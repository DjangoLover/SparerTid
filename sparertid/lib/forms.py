class FieldAttributesFormMixin(object):
    placeholders = {}
    widget_attrs = {}

    def __init__(self, *args, **kwargs):
        super(FieldAttributesFormMixin, self).__init__(*args, **kwargs)

        for field, placeholder in self.placeholders.iteritems():
            self.fields[field].widget.attrs['placeholder'] = placeholder

        for field, attrs in self.widget_attrs.iteritems():
            for attrib, value in attrs.iteritems():
                if isinstance(value, (list, tuple)):
                    value = ' '.join(value)
                self.fields[field].widget.attrs[attrib] = value
