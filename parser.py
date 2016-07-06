from lexer import Token, scan


"""
alist -> head items
head -> key keys
keys -> indent key | indent :key | e
key -> string

items -> item items | e
item -> value values
values -> indent value | indent key::value | e
value -> string
"""
class Parser(object):
    def __init__(self, f, *args, **kwargs):
        self.f = f  # fp
        self.look = None
        self.parsed_keys     = []  # keys
        self.parsed_posikeys = []  # positional keys
        self.data            = []  # list of tuples
        super(Parser, self).__init__(*args, **kwargs)

    def move(self):
        self.look = scan(self.f)

    # alist -> head items
    def alist(self):
        posikeys, keys = self.head()
        self.items()
        print self.data

    # head -> key keys
    def head(self):
        self.move()
        first_key = self.key()
        posikeys, keys = self.keys()
        return [first_key] + posikeys, keys

    # keys -> indent key | indent :key | e
    def keys(self):
        self.move()
        posikeys = []
        keys     = []
        while self.look[0] == Token.Indent:
            self.move()
            if self.look[0] == Token.Colon:
                self.move()
                keys.append(self.key())
            else:
                posikeys.append(self.key())
            self.move()
        return posikeys, keys

    # key -> string
    def key(self):
        if self.look[0] == Token.String:
            return self.look[1]
        raise Exception('Expected string')

    # items -> item items | e
    def items(self):
        self.item()
        # self.items()
    
    # item -> value values
    def item(self):
        first_val = self.value()
        print 'first_val %s' % first_val
        values = self.values()
    
    # values -> indent value | indent key::value | e
    def values(self):
        self.move()
        rn = 0

        while self.look[0] == Token.Indent:
            self.move()
            part1 = self.value()
            if self.look[0] == Token.Colon:
                self.move()
                if self.look[0] == Token.Colon:
                    if part1 not in self.parsed_keys:
                        raise Exception('No such key "%s".' % part1)                    
                    value = self.value()
                    self.data.append((part1, value))
                else:
                    raise Exception("Single ':' should be '::'")
            else:
                if len(self.parsed_posikeys) > rn:
                    self.data.append((self.parsed_posikeys[rn], part1))
                else:
                    raise Exception('Extr a positional value in item.')

            self.move()
            rn += 1
    
    # value -> string
    def value(self):
        if self.look[0] == Token.String:
            return self.look[1]
        raise Exception('Expected string')


with open('test.list', 'U') as f:
    p = Parser(f)
    p.alist()
