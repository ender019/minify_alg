import re

class minify_js():
    def __init__(self, f1, f2):
        self.in_file = f1
        self.out_file = f2
        self.h = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.spf = ['const', 'var', 'let', 'this', 'function', 'new', 'class']
        self.nm = {'\n':'', '\t':''}
        self.t=1

    def checking(self, f):
        for line in f:
            ln = re.sub(r'[\'\"].*[\'\"]','',line)
            pr=re.findall(r'(?:(?:let |var |const |this.)[\d\w]+|\([\d\w]+\))', ln)
            fn = re.findall(r'(?:function|class)(?: [\d\w]+)?\(.*\)', ln)

            for el in pr:
                p=re.findall(r'[\d\w]+', el)
                for nk in p:
                    if nk not in self.spf: self.nm[nk]=''

            for el in fn:
                p=re.findall(r'[\d\w]+', el)
                for i in range(1,len(p)): self.nm[p[i]]=''

    def naming(self):
        i = 0
        q = 52
        for key in self.nm:
            if key in['\n','\t']: continue
            s = ''
            n=i
            if i == 0: s = 'a'
            while n > 0:
                s += self.h[n % q]
                n //= q
            self.nm[key] = s
            i+=1

    def short(self, s):
        out = s
        for key in self.nm:
            out=out.replace(key,self.nm[key])

        ln=out.split(' ')
        out=''
        for el in ln:
            if el=='': continue
            if self.t==1 and re.fullmatch(r"[^\'\"]*[\'\"][^\'\"]*",el)!=None: self.t=0
            elif re.fullmatch(r"[^\'\"]*[\'\"][^\'\"]*",el)!=None: self.t = 1
            if self.t==0 or el in self.spf: out+=el+' '
            elif self.t==1: out += el


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
        fl.write(out)
        f.close()
        fl.close()

minify_js('./js_in.txt','./js_out.txt').main()