
def collect_form_errors(form):
    errors = []
    if '__all__' in form.errors:
        errors.append('\n'.join(form.errors['__all__']))


    for field, _errors in form.errors.iteritems():
        if field.startswith('_'):
            continue
        errors.append(u'%s: %s' % (field, u'\n'.join(_errors)))

    return u'\n'.join(errors)
