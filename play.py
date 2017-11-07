import bdb
import inspect
import sys

class Tdb(bdb.Bdb):
    def user_line(self, frame):
        if frame.f_code.co_name == "<module>":
            return
        print("\n\n")
        printSource(frame, 16)
        fancyTable(frame.f_locals, 16)
        input()
        # self.set_next(frame)
        #self.set_continue()
    def user_call(self, frame, args):
        pass #print('user_call', frame, args)
    def user_return(self, frame, return_value):
        if frame.f_code.co_name == "<module>":
            return
        s = "{} returned {}".format(frame.f_code.co_name, return_value)
        s = s.center(34, ' ')
        print(' '*16 + '***{}***'.format(s))
    def user_exception(self, frame, exc_info):
        pass #print('user_exception', frame, exc_info)

def printSource(frame, pad):
    source, startno = inspect.getsourcelines(frame.f_code)
    for n, line in enumerate(source):
        lineno = n+startno
        linenostr = str(lineno).ljust(3)
        symbol = ":   " if lineno != frame.f_lineno else "# >>"
        print(" "*pad + "{}{}{}".format(linenostr, symbol, line.rstrip()))

def fancyTable(locs, pad):
    items = [(k, type(locs[k]).__name__, str(locs[k])) for k in sorted(locs.keys()) if "__" not in k]
    if not items:
        items = [('', '', '')]
    nameW = max(max([len(k) for k, t, v in items]), 4)
    typeW = max(max([len(t) for k, t, v in items]), 4)
    valW = max(max([len(v) for k, t, v in items]), 4)
    if (nameW+typeW+valW+10 < 40):
        valW = 40 - nameW - typeW - 10
    w = nameW + typeW + valW  + 10 # dividers + padding
    table = " "*pad + "| {} | {} | {} |"
    join = " "*pad + "+-{}-+-{}-+-{}-+".format('-'*nameW, '-'*typeW, '-'*valW)
    print(join)
    print(table.format("var".center(nameW), "type".center(typeW), "val".center(valW)))
    print(join)
    for k, t, v in items:
        print(table.format(k.rjust(nameW), t.ljust(typeW), v.ljust(valW)))
    print(join)

if len(sys.argv) < 1:
    print("help")
pyfile = sys.argv[1]
with open(pyfile, 'r') as f:
    source = compile(f.read(), pyfile, 'exec')
    dbg = Tdb()
    dbg.run(source)
