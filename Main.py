class minify_js():
    def __init__(self, f1, f2):
        self.in_file = f1
        self.out_file = f2
        self.h = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.spf = ['const', 'var', 'let', 'function', 'new', 'class']
        self.nm = {}

    def checking(self, f):
        for line in f:
            ln = line
            while '\t' in ln: ln=ln.replace('\t','')
            while '\n' in ln: ln=ln.replace('\n', '')
            ln=ln.split(' ')
            t = 1
            for i in range(len(ln)):
                if ln[i] in ['', ' ', '\t']: continue
                if ln[i][0] in ['\'', '\"']: t = 0
                if ln[i][-1] in ['\'', '\"']: t = 1
                if ln[i] in self.spf and t == 1: self.nm[ln[i + 1]] = ''

    def naming(self):
        i = 0
        q = 52
        for key in self.nm:
            s = ''
            if i == 0: s = 'a'
            while i > 0:
                s += self.h[i % q]
                i //= q
            self.nm[key] = ' '+s
            if '(' in key:
                for j in range(len(key)):
                    if key[j]=='(':
                        self.nm[key] += key[j:]
                        break
            i+=1

    def short(self, s):
        ln = s
        while '\t' in ln: ln = ln.replace('\t', '')
        while '\n' in ln: ln = ln.replace('\n', '')
        ln = ln.split(' ')
        t = 1
        out = ''
        for i in range(len(ln)):
            if ln[i] in ['', ' ', '\t']: continue
            if ln[i][:2] == '//': break
            if ln[i][0] in ['\'', '\"']: t = 0
            if ln[i][-1] in ['\'', '\"']: t = 1
            if ln[i] in self.spf and t == 1: ln[i+1] = self.nm[ln[i + 1]]
            out += ln[i]
            if t==0: out += ' '
        return out

    def main(self):
        f = open(self.in_file, 'r')
        l = [line.strip() for line in f]
        self.checking(l)
        self.naming()

        out = ''
        for line in l:
            out += self.short(line)
            if len(out) > 0 and out[-1] not in ['(',',','{', '}', ';']: out += ';'

        fl = open(self.out_file, 'w')
        f.close()
        fl.close()

minify_js('./js_in.txt','./js_out.txt').main()