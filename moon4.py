#import t3_n as cstr
from t3 import find_all_U
from t3 import show_all_el_info
import numpy as np
from numpy.linalg import inv
from t3 import show_elements_in_n as show_all_n
#from F2 import B_is_zeros
#from F2 import dont_use_moon
#from t3_n import show_all_el_info
#from t3_n import list_of_elements as lel
#from t3_n import list_of_n as ln
#from t3_n import list_of_nodes as lnodes
#from t3_n import list_of_elements2 as lel2
#from t3_n import list_of_n2 as ln2
#from t3_n import list_of_nodes2 as lnodes2


# ========================================================#
def find_source(list_of_elements):
    """
    ищем ИТ или ИН
    :param list_of_elements:
    :return: ИТ или ИН
    """
    for el in range(len(list_of_elements)):
        if list_of_elements[el].type == 'I' or \
                        list_of_elements[el].type == 'U':
            source = list_of_elements[el]
    # print (source.type)
    return source


def find_index(ln, base):
    for i in range(len(ln)):
        if ln[i] == base:
            index = i
            break
    return index


def G_own(n, lel):
    """
    нах. собст. пров-ть
    :param n: узел из списка 'n'
    :return: g_own
    """
    g_own = 0
    g_each = 0
    for el in range(len(n)):  # смотрим в списке 'n', какие элементы связаны с узлом#or n[el] in lel2
        if n[el] in lel and n[el].R_value != float('inf') and n[el].R_value != 0 and n[el].type == 'R':
            g_each = 1 / n[el].R_value
            g_own += g_each

    return g_own

def find_g_sm(ln1,ln2, lel):
    g_sm =0
    list=[]
    list.clear()
    for i in range(len(lel)):
        if lel[i].type == 'R' and lel[i] in ln1 and lel[i] in ln2 and lel[i] not in list:
            #print(lel[i].number)
            g_sm += 1/lel[i].R_value
            list.append(lel[i])
    g_sm = -1*g_sm
    #print("g_sm=", g_sm)
    return g_sm




def make_G_matrix(lnode, ln, G, lel):
    if len(lnode) == 4:
        for i in range(len(lnode) - 1):
            for k in range(len(ln) - 1):
                if ln[k] in lnode[i]:
                    for el in range(len(ln[i])):
                        for element in range(len(ln[k])):
                            if ln[k][element] == ln[i][el] and \
                               ln[k][element] in lel and \
                               ln[k][element].R_value != float('inf') and \
                               ln[k][element].R_value != 0:
                                G[i, k] = -1 / ln[k][element].R_value
                else:
                    G[i, i] = G_own(ln[i],lel)

        print("Матрица проводимостей G: \n", G)
    else:
        G[0, 0] = G_own(ln[0], lel)
        G[1, 1] = G_own(ln[1],lel)
        if ln[0] in lnode[1]:
            for el in range(len(ln[0])):
                for elm in range(len(ln[1])):
                    if ln[0][el] == ln[1][elm] and ln[0][el] and \
                       ln[0][el].R_value != float('Inf') and ln[0][el].R_value != 0 and \
                       ln[0][el].type == 'R':
                        G[0,1] = -1 / ln[0][el].R_value
                        G[1,0] = float(G[0,1])

        print("Матрица проводимостей G: \n", G)


def make_I_matrix(ln, I, lel):
    """
    втекающий ток со знаком '+', вытекающий '-'
    :param ln: список узлов list_of_n
    :param I: м-ца узловых токов
    :return: I
    """
    #print("\nABRAKADABRA\n")
    #show_all_n(ln,lel)
    #print("\nABRAKADABRA\n")
    for i_ln in range(len(ln) - 1):  # индекс n узла
        current = 0  # ток
        for i_el in range(len(ln[i_ln])):  # индекс элемента, подключ к узлу
            p = ln[i_ln][i_el]  #
            if p in lel and p.cur_dir_goes_from == ln[i_ln] and p.type == 'I':  # если ток течет ИЗ узла, который мы сейчас рассматриваем
                current -= p.I_value  # то мы берём его со знаком минус
            elif p in lel and p.type == 'I':
                current += p.I_value
        I[i_ln] = current  # записываем в матрицу токов
    print("Матрица узловых токов I: \n", I)


def find_R_currents(lel, ln):
    c=0
   # for i in range(len(ln)):
   #     for k in range(len(ln)):
   #         if ln[i] != ln[k]:
   #             for el in range(len(ln[i])):
   #                 for ell in range(len(ln[k])):
   #                     if ln[k][ell] in lel and ln[i][el] in lel and ln[k][ell].type == 'R' and ln[i][el].type == 'R' and ln[i][el].R_value != float('Inf') \
   #                             and ln[i][el].R_value !=0 and ln[k][ell].R_value != float('Inf') \
   #                             and ln[k][ell].R_value !=0:
   #                         R_value = ln[i][el].R_value + ln[k][ell].R_value
   #                         c+=1
    for el in range(len(lel)):
        if lel[el].type == 'R' and lel[el].R_value != float('Inf') and \
                        lel[el].R_value != 0:
           # if c == 0 :
                lel[el].I_value = (lel[el].cur_dir_goes_from[-1] - lel[el].cur_dir_goes_to[-1]) / lel[el].R_value
           # else:
            #    lel[el].I_value = (lel[el].cur_dir_goes_from[-1] - lel[el].cur_dir_goes_to[-1]) / R_value
                #c=0


def find_C_currents(lel):
    this =0
    for el in range(len(lel)):
        if lel[el].C_value != 0 and lel[el].I_value == None and lel[el].type != 'U' and lel[el].pointer != None:
            lel[el].I_value = lel[el].U_value / lel[el].pointer
            lel[el].U_value = 0
            this = lel[el]
        elif lel[el].C_value !=0 and lel[el].I_value != None and lel[el].type != 'U':
            lel[el].U_value = 0
    for el in range(len(lel)):
        if this != 0:
            if lel[el].C_value !=0 and  lel[el].I_value == None and lel[el].pointer == None and lel[el]!=this:
                if lel[el].cur2:
                    lel[el].I_value = (lel[el].cur1.I_value*lel[el].cur1sign + lel[el].cur2.I_value*lel[el].cur2sign )
                else:
                    lel[el].I_value = lel[el].cur1.I_value * lel[el].cur1sign
        else:
            if lel[el].C_value != 0 and lel[el].I_value == None and lel[el].pointer == None:
                if lel[el].cur2:
                    lel[el].I_value = (lel[el].cur1.I_value*lel[el].cur1sign + lel[el].cur2.I_value*lel[el].cur2sign )
                else:
                    lel[el].I_value = lel[el].cur1.I_value * lel[el].cur1sign


def find_U_values(lel):
    for el in range(len(lel)):
        if lel[el].type == 'R' and lel[el].R_value != float('Inf'):
            lel[el].U_value = lel[el].I_value * lel[el].R_value
        else:
            lel[el].U_value = lel[el].cur_dir_goes_from[-1] - lel[el].cur_dir_goes_to[-1]


# ====================== МУН ===================#
def moon_for_U(ln, source,lel):
    G = np.zeros([1, 1], "f")
    I = np.zeros([1, 1], "f")
    if len(ln) == 3:
        #base = source.cur_dir_goes_from
        source.cur_dir_goes_from[-1] = 0
        source.cur_dir_goes_to[-1] = source.U_value
        for i in range(len(ln)):
            if ln[i] != source.cur_dir_goes_from and ln[i] != source.cur_dir_goes_to:
                this = ln[i]
        G_this = G_own(this, lel)
        g_sm = find_g_sm(this,source.cur_dir_goes_to, lel )
        print ("\n G_own=",G_this, " g_sm=", g_sm, '\n')
        #source_g = G_own(source.cur_dir_goes_to,lel)
        #I_this = 0#source.U_value*G_this
        #source_i = source.U_value*source_g

        #A= G_this**(-1)
        #A=A*I_this
        A = -(g_sm*source.U_value/G_this)
        this[-1] = A
        print ("\nMOON, U =", this[-1], '\n')
        find_R_currents(lel,ln)
        find_all_U(lel)
        find_C_currents(lel)

    elif len(ln) == 2:
        source.cur_dir_goes_from[-1] = 0
        source.cur_dir_goes_to[-1] = source.U_value
        for i in range(len(ln)):
            for el in range(len(ln[i])):
                if ln[i][el] in lel and ln[i][el].type == 'R':
                    ln[i][el].I_value = (ln[i][el].cur_dir_goes_from[-1] - ln[i][el].cur_dir_goes_to[-1] ) / ln[i][el].R_value
        find_all_U(lel)
        find_C_currents(lel)
    elif len(ln) == 4:
        source.cur_dir_goes_from[-1] = 0
        source.cur_dir_goes_to[-1] = source.U_value
        pass
        #show_all_el_info(lel)
    #U = inv(G) @ I
    #print("Матрица узловых напряжений U:\n", U)
    pass


def moon_for_I(lnodes, ln,lel):
    if len(ln) == 4:
        G = np.zeros([3, 3], "f")
        I = np.zeros([3, 1], "f")
        base = ln[3]
        base[-1] = 0
        make_G_matrix(lnodes, ln, G,lel)
        make_I_matrix(ln, I,lel)
        U = inv(G) @ I
        print("Матрица узловых напряжений U:\n", U)
        ln[0][-1] = float(U[0])
        ln[1][-1] = float(U[1])
        ln[2][-1] = float(U[2])
        ln[3][-1] = 0
        find_R_currents(lel,ln)
        find_U_values(lel)
        find_C_currents(lel)
        show_all_el_info(lel, ln)
    elif len(ln) == 3:
        G = np.zeros([2, 2], "f")
        I = np.zeros([2, 1], "f")
        base = ln[2]
        base[-1] = 0
        make_G_matrix(lnodes, ln, G,lel)
        make_I_matrix(ln, I,lel)
        U = inv(G) @ I
        print("Матрица узловых напряжений U:\n", U)
        ln[0][-1] = float(U[0])
        ln[1][-1] = float(U[1])
        ln[2][-1] = 0
        find_R_currents(lel,ln)
        find_U_values(lel)
        find_C_currents(lel)
        #show_all_el_info(lel)
    elif len(ln) == 2:
        ln[1][-1] = 0
        G_this = G_own(ln[0], lel)
        source = find_source(lel)
        if source.cur_dir_goes_from == ln[0]:
            I_this = -1*source.I_value
        else:
            I_this = source.I_value
        ln[0][-1] = I_this/G_this
        find_R_currents(lel,ln)
        find_U_values(lel)
        find_C_currents(lel)

    pass


def moon(lnodes, ln, lel):
    source = find_source(lel)
    if source.type == 'I':
        show_all_el_info(lel,ln)
        moon_for_I(lnodes, ln, lel)
    else:
        moon_for_U(ln, source, lel)
    pass


#moon(lnodes, ln, lel)
