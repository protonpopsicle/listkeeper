from lexer import Token, scan


"""
list     -> head items
head     -> key p_keys opt_keys
p_keys   -> p_key p_keys | e
opt_keys -> opt_key opt_keys | e
p_key    -> indent key
opt_key  -> indent :key
key      -> string

items    -> item items | e
item     -> val p_vals opt_vals
p_vals   -> p_val p_vals | e
opt_vals -> opt_val opt_vals | e
p_val    -> indent val
opt_val  -> indent key::val
val      -> string
"""
class Parser(object):
    def __init__(self, f, *args, **kwargs):
        self.f    = f # fp
        self.look = None
        super(Parser, self).__init__(*args, **kwargs)

    def move(self):
        self.look = scan(self.f)

    def match(self, token):
        self.move()
        if self.look[0] != token:
            raise Exception('Expected %s, got %s' % (token, self.look[0]))

    # alist -> head items
    def alist(self):
        self.head()
        self.items()

    # head -> p_keys opt_keys
    def head(self):
        self.move()
        positional_key = self.key()
        positinal_keys, keys = self.keys()

    # keys -> indent key | indent :key | e
    def keys(self):
        self.move()
        while self.look[0] == Token.Indent:
            self.move()
            if self.look[0] == Token.Colon:
                self.move()
                self.parsed_keys.append(self.key())
            else:
                self.parsed_posikeys.append(self.key())
            self.move()

    # key -> string
    def key(self):
        if self.look[0] == Token.String:
            return self.look[1]
        raise Exception('Expected string')


    # items -> item items | e
    def items(self):
        while True:
            item = self.item()
            if not item:
                break
    
    # item -> value values
    def item(self):
        self.data.append([(self.parsed_keys[0], self.value())])
        self.values()
    
    # values -> indent value | indent key::value | e
    def values(self):
        self.move()
        pos = 0

        while self.look[0] == Token.Indent:
            self.move()
            lhs = self.value()
            self.move()

            if self.look[0] == Token.Colon:
                self.match(Token.Colon)
                self.move()
                if lhs not in self.parsed_keys:
                    raise Exception('No such key "%s".' % lhs)
                rhs = self.value()
                self.data[-1].append((lhs, rhs))
            else:
                if len(self.parsed_posikeys) > pos:
                    self.data[-1].append((self.parsed_posikeys[pos], lhs))
                else:
                    raise Exception('Extra positional value in item.')

            pos += 1
    
    # value -> string
    def value(self):
        if self.look[0] == Token.String:
            return self.look[1]
        raise Exception('Expected string, got %s' % self.look[0])

with open('test.list', 'U') as f:
    p = Parser(f)
    p.alist()
