import re


class minify_js():
    def __init__(self, f1, f2):
        self.in_file = f1
        self.out_file = f2
        self.h = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'     # алфавит для названий
        self.spf = ['const', 'var', 'let', 'this', 'function', 'new', 'class']     # особые имена
        self.nm = {}     # словарь в котором указано что на что менять
        self.t = 1     # можно ли что-то менять(созданно для string)

    def checking(self, f):     # заполнение имен переменных(nm)
        for line in f:     # идем по строкам
            ln = re.sub(r'(?:[\'\"].*[\'\"]|//.*)', '', line)     # убираем string они могут помешать
            pr = re.findall(r'(?:(?:let |var |const |this.)[\d\w_]+|\([\d\w_]+\))', ln)     # ищем все объявления переменных
            fn = re.findall(r'(?:function|class)(?: [\d\w_]+)?\(.*\)', ln)     # ищем все объявления функций

            for el in pr:     # идем по найденным переменным
                p = re.findall(r'[\d\w_]+', el)     # делим на оператор и имя
                for nk in p:     # ищем имя
                    if nk not in self.spf: self.nm[nk] = ''     # если имя записываем

            for el in fn:     # теперь для функций
                p = re.findall(r'[\d\w_]+', el)
                for i in range(1, len(p)): self.nm[p[i]] = ''

    def naming(self):     # создаем имена
        i = 0
        q = 52     # букв в алфавите
        for key in self.nm:     # перебираем ключи
            s = ''     # имя
            n = i
            if i == 0: s = 'a'     # первое имя а
            while n > 0:     # переводи в сс 52
                s += self.h[n % q]
                n //= q
            self.nm[key] = s     # новое имя готово
            i += 1     # следующий номер


    def func_par(self,m):
        if ' ' in m[0]:
            im=m[0].split(' ')
            im=im[0]+' '+self.nm[im[1]]
            m[0]=im

        for i in range(1,len(m)):
            if "'"in m[i] or "\"" in m[i] or m[i]=='': continue
            m[i]=re.sub(r' ', '', m[i])
            if m[i] in self.nm.keys(): m[i] = self.nm[m[i]]
            else:
                m[i]=eval(m[i])
        print(m)



    def short(self, s):     # преобразование строки кода
        out = re.sub(r'//.*', '', s)

        if re.search(r"\(.*\)",out):
            sp=re.split(r"[\(\)\[\]\{\},\.]",out)
            self.func_par(sp)
        else:
            pass

        return out

    def main(self):     # главная функция
        f = open(self.in_file, 'r')     # открываем файл с исходным кодом
        l = [line.strip() for line in f]      # получаем массив строк кода
        self.checking(l)     # какие есть имена
        self.naming()     # создаем новые имена

        out = ''     # для вывода
        for line in l:     # идем по строкам
            out += self.short(line)     # добавляем новую строку
            if self.t==1 and len(out) > 0 and out[-1] not in ['(', ',', '{', '}', ';']: out += ';'      # если нужно добавляем

        f.close()   # закрываем файл с иходным кодом
        # fl = open(self.out_file, 'w')     # открываем выходной файл
        # fl.write(out)     # записываем новый код
        # fl.close()   # закрываем файл


minify_js('./js_in.txt', './js_out.txt').main()  # вызов
