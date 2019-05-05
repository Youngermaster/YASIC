from sly import Lexer
from sly import Parser


class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ }
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    # Define tokens
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FOR = r'FOR'
    FUN = r'FUN'
    TO = r'TO'
    ARROW = r'->'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    EQEQ = r'=='

    @_(r'\d+')
    def NUMBER(self, token):
        token.value = int(token.value)
        return token

    @_(r'#.*')
    def COMMENT(self, token):
        pass

    @_(r'\n+')
    def newline(self,token):
        self.lineno = token.value.count('\n')


class BasicParser(Parser):
    tokens = BasicLexer.tokens
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UNMINUS'),
    )

    def __init__(self):
        self.env = { }

    @_('')
    def statement(self, parser):
        pass

    @_('FOR var_assign TO expr THEN statement')
    def statement(self, parser):
        return ('for_loop', ('for_loop_setup', parser.var_assign, parser.expr), parser.statement)

    @_('IF condition THEN statement ELSE statement')
    def statement(self, parser):
        return ('if_stmt', parser.condition, ('branch', p.statement0, p.statement1))

    @_('FUN NAME "(" ")" ARROW statement')
    def statement(self, parser):
        return ('fun_def', parser.NAME, parser.statement)

    @_('NAME "(" ")"')
    def statement(self, parser):
        return ('fun_call', parser.NAME)

    @_('expr EQEQ expr')
    def condition(self, parser):
        return ('condition_eqeq', parser.expr0, parser.expr1)

    @_('var_assign')
    def statement(self, parser):
        return parser.var_assign

    @_('NAME "=" expr')
    def var_assign(self, parser):
        return ('var_assign', parser.NAME, parser.expr)

    @_('NAME "=" STRING')
    def var_assign(self, parser):
        return ('var_assign', parser.NAME, parser.STRING)

    @_('expr')
    def statement(self, parser):
        return (parser.expr)

    @_('expr "+" expr')
    def expr(self, parser):
        return ('add', parser.expr0, parser.expr1)

    @_('expr "-" expr')
    def expr(self, parser):
        return ('sub', parser.expr0, parser.expr1)

    @_('expr "*" expr')
    def expr(self, parser):
        return ('mul', parser.expr0, parser.expr1)

    @_('expr "/" expr')
    def expr(self, parser):
        return ('div', parser.expr0, parser.expr1)

    @_('"-" expr %prec UNMINUS')
    def expr(self, parser):
        return parser.expr

    @_('NAME')
    def expr(self, parser):
        return ('var', parser.NAME)

    @_('NUMBER')
    def expr(self, parser):
        return ('num', parser.NUMBER)

    
class BasicExecute:
    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isInstance(result, int):
            print(result)
        if isInstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):
        if isInstance(node, int):
            return node
        if isInstance(node, int):
            return node
        if node is None:
            return None
        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])
        if node[0] == 'num':
            return node[1]
        if node[0] == 'str':
            return node[1]
        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])
        if node[0] == 'condition_eqeq':
            return self.walkTree(node[1]) == self.walkTree(node[2])
        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]
        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0
        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        if node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        if node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        if node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        if node[0] == 'var_assign':
            self.env[node[1] = self.walkTree(node[2])]
            return node[1]
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError as identifier:
                print("Undefined variable '" + node[1] + "' found!")
                return 0
        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])
                loop_count = self.env[loop_setup[0]]
                loop_limit = looṕ_setup[1]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('basic > ')
        except EOFError:
            break
        if text:
            # With the code below you can see the Tokens line by line.
            """
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
            """
            tree = parser.parse(lexer.tokenize(text))
            # print(tree)
            BasicExecute(tree, env)
            # print(env)