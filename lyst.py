class ValidationError(Exception):
    pass

class Lyst(object):
    def __init__(self, p_keys, opt_keys):
        self.p_keys   = p_keys
        self.opt_keys = opt_keys
        self.items    = []

    def dump(self):
        for item in self.items:
            for x in item:
                print '%s: %s' % x
            print ''

    def add_item(self, p_vals, opt_vals):
        delta = len(p_vals) - len(self.p_keys)
        if delta:
            raise ValidationError('"%s" Number of positional values off by %u' % (p_vals[0], delta))
        
        item = set()
        for i, key in enumerate(self.p_keys):
            item.add((key, p_vals[i]))

        for key, val in opt_vals:
            if key not in self.opt_keys:
                raise ValidationError('"%s" Undefined optional key "%s"' % (p_vals[0], key))
            item.add((key, val))

        self.items.append(item)
