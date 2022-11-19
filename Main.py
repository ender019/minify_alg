import re

# код алгоритма minify, предназначенного для уменьшения размера файла javascript
# !!!работает только с отформатированным кодом
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


    def cond_par(self,m):
        if m[0][-1]==' ':m[0]=m[0][:-1]     # убераем пробел после оператора
        for i in range(1,len(m)):     # смотримм условия
            if m[i]=='': continue     # пропускаем пыстые строки
            if m[i]==' ': continue     #
            if not re.search(r"[+*/<>=-]{1,2}", m[i]):     # если не выражение
                if m[i] in self.nm.keys(): m[i] = self.nm[m[i]];      # меняем имя переменной
                continue  # идем к следующему аргументу
            vz = re.findall(r"[<>=]{1,2}", m[i])[0]     # ищем операторы
            vr=re.split(r" [<>=]{1,2} ", m[i])     # разбиваем на части
            if vr[0] in self.nm.keys(): vr[0]=self.nm[vr[0]]     # меняем имя переменной
            if vr[1] in self.nm.keys(): vr[1]=self.nm[vr[1]]     # меняем имя переменной
            elif "\'" in m[i] or "\"" in m[i]:  # если строки
                sa = re.split(r' \+ ', m[i])  # разбираем на части
                for j in range(len(sa)):  # перебираем ищя переменные
                    if sa[j] in self.nm.keys(): sa[j] = self.nm[sa[j]]  # заменяем переменные
                m[i] = ''
                for j in range(len(sa) - 1):
                    m[i] += sa[j] + '+'  # соединяем
                m[i] += sa[-1]
                continue  # идем к следующему аргументу
            else:
                vr[1] = re.sub(r' ', '', vr[1])  # убираем лишние пробелы
                sz=re.findall(r"[+*/\(\)-]{1,2}", vr[1])     # ищем операторы
                sl=re.split(r"[+*/\(\)-]{1,2}", vr[1])     # разбираем на части
                f=1     # есть ли изменения
                for j in range(len(sl)):
                    if sl[j] in self.nm.keys(): vr[0]=self.nm[sl[j]]; f=0     # замена переменных
                vr[1]=''
                for j in range(len(sz)):
                    vr[1] += sl[j]+sz[j]     # сбор врыжения
                vr[1] += sl[-1]
                if f: vr[1]=str(eval(vr[1]))     # если выражние арифметическое и без переменных вычисляем
            m[i]=vr[0]+vz+vr[1]     # обновляем
        return m


    def func_par(self,m):
        if ' ' in m[0] and m[0][-1]!=' ':     # если объявление функции
            im=m[0].split(' ')     # разбираем
            im=im[0]+' '+self.nm[im[1]]     # собираем с замененным именем
            m[0]=im
        elif m[0] in self.nm.keys():     # если вызов
            m[0]=self.nm[m[0].replace(' ','')]     # заменяем имя

        for i in range(1,len(m)):     # идем по аргументам
            if m[i]=='' or m[i]==' ': m[i]=''; continue     # пропускаем пустые строки
            if "\'"in m[i] or "\"" in m[i]:     # если строки
                sa=re.split(r' \+ ', m[i])     # разбираем на части
                for j in range(len(sa)):     # перебираем ищя переменные
                    if sa[j] in self.nm.keys(): sa[j]=self.nm[sa[j]]     # заменяем переменные
                m[i]=''
                for j in range(len(sa)-1):
                    m[i]+=sa[j]+'+'     # соединяем
                m[i]+=sa[-1]
                continue     # идем к следующему аргументу
            m[i]=re.sub(r' ', '', m[i])     # убираем лишние пробелы
            if m[i] in self.nm.keys(): m[i] = self.nm[m[i]]     # если имя переменной заменяем
            elif not re.search(r"[\w&%$#]+",m[i]):
                m[i]=str(eval(m[i]))     # если выражение заменяем на результат

        return m



    def short(self, s):     # преобразование строки кода
        if s=='': return ''     # пропускаем пустые строки
        out = re.sub(r'//.*', '', s)     # убираем коментарии
        out = re.sub(r'[\t\n;]', '', out)     # убираем лишние символы

        if re.search(r"\(.*\)",out):     # усли связано с функцией
            out=re.sub(r', ',',',out)
            if re.search(r"(?:if|else if|while|for)",out):
                sp = re.split(r"(?:\(|\)|and|or)",out)     # разбиваем на составляющие
                zn = re.findall(r"(?:\(|\)|and|or)", out)  # запоминаем по чему разделяли
                sp=self.cond_par(sp)
            else:
                sp=re.split(r"[\(\)\[\]\{\},\.]",out)     # разбиваем на составляющие
                zn=re.findall(r"[\(\)\[\]\{\},\.]",out)     # запоминаем по чему разделяли
                sp=self.func_par(sp)     # обрабатываем
            out=''
            for i in range(len(zn)):
                out+=sp[i]+zn[i]     # собираем
            if sp[-1]==' {': sp[-1]='{'
            out+=sp[-1]

        elif re.search(r"[+*/<>=-]{1,2}",out):     # если переменная
            op=re.findall(r"[+*/<>=-]{1,2}",out)[0]
            out=re.split(r" [+*/<>=-]{1,2} ",out)     # разделяем на 2 части
            if ' ' in out[0]:     # если опроеделение
                fp=out[0].split(' ')
                out[0]=fp[0]+' '+self.nm[fp[1]]
            else: out[0]=self.nm[out[0]]     # если изменение

            if "\'"in out[1] or "\"" in out[1]:     # если в аргументе стока
                sa = re.split(r' \+ ', out[1])     # делим на слогаемые
                for j in range(len(sa)):     # ищем переменные
                    if sa[j] in self.nm.keys(): sa[j] = self.nm[sa[j]]     # заменяем переменные
                out[1] = ''
                for j in range(len(sa) - 1):
                    out[1] += sa[j] + ' + '     # собираем выражение
                out[1] += sa[-1]
            elif re.search(r"[\We]+",out[1]): out[1]=str(eval(out[1]))     # если арифметика выполняем
            out=out[0]+op+out[1]     # соединяем

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
        print(out)
        f.close()   # закрываем файл с иходным кодом
        fl = open(self.out_file, 'w')     # открываем выходной файл
        fl.write(out)     # записываем новый код
        fl.close()   # закрываем файл


minify_js('./js_in.txt', './js_out.txt').main()  # вызов
