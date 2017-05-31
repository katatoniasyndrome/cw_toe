import t3 as cstr
import copy
from moon4 import moon
import numpy as np
from t3 import show_elements_in_n as show_all_n
from t3 import list_of_elements as lel
from t3 import list_of_n as ln
from t3 import list_of_nodes as lnodes

#================ Списки новых цепей ===================#
lel1=copy.copy(lel)
lel2=copy.copy(lel)
lel3=copy.copy(lel)
#ln1=copy.copy(ln)
#ln2=copy.copy(ln)
#ln3=copy.copy(ln)
ln1 = []
ln2= []
ln3=[]
lnodes1 = lnodes2 = lnodes3 = []
#lnodes1=copy.copy(lnodes)
#lnodes2=copy.copy(lnodes)
#lnodes3=copy.copy(lnodes)
list = []
circ_type = cstr.circuit_type
B_is_zeros = False
dont_use_moon = False
b1=0
b2=0

def find_source(list_of_elements):
    """
    ищем ИТ или ИН
    :param list_of_elements:
    :return: ИТ или ИН
    """
    global list
    for el in range(len(list_of_elements)):
        if list_of_elements[el].type == 'I' or \
                        list_of_elements[el].type == 'U':
            if list_of_elements[el] not in list:
                source = list_of_elements[el]
    return source

def source_eraser(lel_new):
    """
    делает схему, в которой только el1
    :return: список новых элементов с хх и кз
    """
    global lel, list
    for i in range(len(lel)):
        if lel[i].type == 'L':
            lel_new[i] = copy.copy(lel[i])
            lel_new[i].type = 'xx'
        elif lel[i].type == 'C':
            lel_new[i] = copy.copy(lel[i])
            lel_new[i].type = 'kz'
        else:
            lel_new[i] = copy.copy(lel[i])
    #list.append(lel[0])
    return lel_new

def make_source(lel_new):
    """
    шаги 2 и 3, где оставляем Ic или UL
    :param lel_new:
    :return:
    """
    global lel, list, circ_type
    c=0
    #for i in range(len(lel)):
    if circ_type == 'A':
        new_el = copy.copy(lel[0])
        new_el.type = 'xx'
        new_el.I_value = 0
        lel_new[0] = new_el
    elif circ_type == 'B':
        new_el = copy.copy(lel[0])
        new_el.type = 'kz'
        new_el.R_value = 0
        lel_new[0] = new_el
    for i in range(len(lel)):
        if lel[i].type == 'L' :
            if c !=0 :
                a = copy.copy(lel[i])
                lel_new[i] = a
                lel_new[i].type = 'xx'
            elif lel[i] not in list:
                a = copy.copy(lel[i])
                lel_new[i] = a
                lel_new[i].type = 'I'
                lel_new[i].I_value = 1
                list.append(lel[i])
                c+=1
            else:
                a = copy.copy(lel[i])
                lel_new[i] = a
                lel_new[i].type = 'xx'
        elif lel[i].type == 'C':
            if c !=0:
                a = copy.copy(lel[i])
                lel_new[i] = a
                lel_new[i].type = 'kz'
            elif lel[i] not in list:
                a = copy.copy(lel[i])
                lel_new[i] = a
                lel_new[i].type = 'U'
                lel_new[i].U_value = 1
                list.append(lel[i])
                c+=1
            else:
                a = copy.copy(lel[i])
                lel_new[i] = a
                lel_new[i].type = 'kz'
        #elif lel[i].type != 'I':
         #   new_el = copy.copy(lel[0])
         #   new_el.type = 'xx'
          #  new_el.I_value = 0
            #lel_new[i] = copy.copy(lel[i])

    return lel_new

def analyze_and_build(lel_new, ln_new, lnodes_new):
    global lel, ln, lnodes, list, circ_type, B_is_zeros, dont_use_moon, b1,b2
    el1 = lel_new[0]
    el2 = lel_new[1]
    el3 = lel_new[2]
    el4 = lel_new[3]
    el5 = lel_new[4]
    el6 = lel_new[5]
    lnodes_new.clear()
    ln_new.clear()
    el1.sign = el2.sign =el3.sign =el4.sign =el5.sign =el6.sign = 1
    el1.pointer = el2.pointer =el3.pointer =el4.pointer =el5.pointer =el6.pointer = 1
    source = find_source(lel_new)
    if circ_type == 'A':
        if source == el1 :
            if el2.type == 'xx':
                if el5.type == 'R':
                    if el4.type == 'R':
                        if el3.type == 'xx': #DELETE (1)
                            B_is_zeros = True
                        elif el3.type == 'kz': #(2)
                            ln_new.append([el1, el2,  el4, el6, el3,0])
                            ln_new.append( [el3,el2,el1,el4,el5,0])
                            ln_new.append( [el5,el6,0])
                            lnodes_new.append([ ln_new[1], ln_new[2]])
                            lnodes_new.append([ln_new[0],ln_new[2]])
                            lnodes_new.append([ln_new[0],ln_new[1]])
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.pointer= None
                            el3.cur1 = el1
                            el3.cur1sign = 1
                            el3.cur2 = 0
                            el3.cur2sign = 1
                            el3.set_cur_dir(ln_new[0], ln_new[1])
                            el4.set_cur_dir(ln_new[1], ln_new[0])
                            el5.set_cur_dir(ln_new[1], ln_new[2])
                            el6.set_cur_dir(ln_new[2], ln_new[1])

                    elif el4.type == 'xx': #(3)
                        ln_new.append([el1, el2, el4, el6, 0])
                        ln_new.append([el1, el2, el3, 0])
                        ln_new.append([el3, el4, el5, 0])
                        ln_new.append([el5, el6, 0])
                        lnodes_new.append([ln_new[1],ln_new[2],ln_new[3]])
                        lnodes_new.append([ln_new[2],ln_new[0]])
                        lnodes_new.append([ln_new[0],ln_new[1], ln_new[3]])
                        lnodes_new.append([ln_new[0], ln_new[2]])
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[3], ln_new[0])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[1],ln_new[2])
                        el4.set_cur_dir(ln_new[2],ln_new[0])
                        el5.set_cur_dir(ln_new[2],ln_new[3])

                    elif el4.type == 'kz':  #(4)
                        ln_new.append([el1, el2, el3, el4,   0])
                        ln_new.append([el1, el2, el3,  el4,  0])
                        lnodes_new.append([ln_new[1]])
                        lnodes_new.append([ln_new[0]])
                        #el5.R_value = float('Inf')
                        #el6.R_value = float('Inf')
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[1], ln_new[0])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[1], ln_new[0])
                        el4.set_cur_dir(ln_new[1], ln_new[0])
                        el4.pointer = None
                        el4.cur1 = el1
                        el4.cur1sign = 1
                        el4.cur2 = 0
                        el4.cur2sign = 1
                        el5.set_cur_dir(ln_new[0], ln_new[1])
                elif el5.type == 'xx': #(5)
                    #el6.R_value = float('Inf')
                    ln_new.append([el1, el2, el4,  0])
                    ln_new.append([el1, el2, el3, 0])
                    ln_new.append([el3, el4, el5, 0])
                    ln_new.append([ el5, 0])
                    lnodes_new.append([ln_new[1], ln_new[2], ln_new[3]])
                    lnodes_new.append([ln_new[2], ln_new[0]])
                    lnodes_new.append([ln_new[1], ln_new[3]])
                    lnodes_new.append([ln_new[0], ln_new[1], ln_new[2]])
                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[2], ln_new[0])
                    el2.set_cur_dir(ln_new[1], ln_new[0])
                    el3.set_cur_dir(ln_new[1], ln_new[2])
                    el4.set_cur_dir(ln_new[2], ln_new[0])
                    el5.set_cur_dir(ln_new[2], ln_new[3])
                elif el5.type == 'kz': #(6)
                    ln_new.append([el1, el2, el4, el6,el5, 0])
                    ln_new.append([el1, el2, el3, 0])
                    ln_new.append([el3, el4, el5, el6,0])
                    lnodes_new.append([ln_new[1], ln_new[2]])
                    lnodes_new.append([ln_new[2], ln_new[0]])
                    lnodes_new.append([ln_new[0], ln_new[1]])
                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[2], ln_new[0])
                    el2.set_cur_dir(ln_new[1], ln_new[0])
                    el3.set_cur_dir(ln_new[1], ln_new[2])
                    el4.set_cur_dir(ln_new[2], ln_new[0])
                    el5.set_cur_dir(ln_new[2], ln_new[0])
                    el5.pointer = el6.R_value
            elif el2.type == 'R':
                if el5.type == 'R':
                    if el4.type == 'kz':
                        if el3.type == 'kz':  #(7)
                            el4.I_value = el3.I_value = source.I_value
                            dont_use_moon = True
                            b1 = b2 = source.I_value
                            b1 = b1/el3.C_value
                            b2 = b2/el4.C_value
                        elif el3.type == 'xx':  #(8)
                            dont_use_moon = True
                            b2 = source.I_value*el2.R_value/el4.C_value
                            b1 =0
                            #ln_new.append([el1, el2, el3, el4, el6, el5, 0])
                            #ln_new.append([el1, el2, el3, el5, el4, el6, 0])
                            #lnodes_new.append([ln_new[1]])
                            #lnodes_new.append([ln_new[0]])
                            #el5.R_value = float('Inf')
                            #el6.R_value = float('Inf')
                            #el1.set_cur_dir(ln_new[0], ln_new[1])
                            #el6.set_cur_dir(ln_new[1], ln_new[0])
                            #el2.set_cur_dir(ln_new[1], ln_new[0])
                            #el3.set_cur_dir(ln_new[1], ln_new[0])
                            #el4.set_cur_dir(ln_new[1], ln_new[0])
                            #el5.set_cur_dir(ln_new[0], ln_new[1])
                    elif el4.type == 'xx':
                        if el3.type == 'kz':  #(9)
                            ln_new.append([el1, el2, el4, el6, 0])
                            ln_new.append([el1, el2, el3, 0])
                            ln_new.append([el3, el4, el5, 0])
                            ln_new.append([el5, el6, 0])
                            lnodes_new.append([ln_new[1], ln_new[2], ln_new[3]])
                            lnodes_new.append([ln_new[2], ln_new[0]])
                            lnodes_new.append([ln_new[0], ln_new[1], ln_new[3]])
                            lnodes_new.append([ln_new[0], ln_new[2]])
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[3], ln_new[0])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[1], ln_new[2])
                            el3.pointer = el5.R_value + el6.R_value
                            el4.set_cur_dir(ln_new[2], ln_new[0])
                            el5.set_cur_dir(ln_new[2], ln_new[3])
                        elif el3.type == 'xx':  #(10)
                            dont_use_moon = True
                            b1 = source.I_value*el2.R_value/el3.L_value
                            b2= 0#source.I_value*el2.R_value/el4.L_value
                            ln_new.append([el1, el2, el3, el4,   0])
                            ln_new.append([el1, el2, el3,  el4,  0])
                            lnodes_new.append([ln_new[1]])
                            lnodes_new.append([ln_new[0]])
                            #el5.R_value = float('Inf')
                            #el6.R_value = float('Inf')
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[1], ln_new[0])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[1], ln_new[0])
                            el4.set_cur_dir(ln_new[1], ln_new[0])
                            el5.set_cur_dir(ln_new[0], ln_new[1])

                elif el5.type == 'xx':
                    if el4.type == 'R':
                        if el3.type == 'xx':  #(11)
                            dont_use_moon = True
                            b2=0
                            b1 = source.I_value*el2.R_value/el3.L_value
                            ln_new.append([el1, el2,    el3, 0])
                            ln_new.append([el1, el2, el3, el5,   0])
                            ln_new.append([el5,  0])
                            lnodes_new.append([ln_new[1],ln_new[2]])
                            lnodes_new.append([ln_new[0],ln_new[2]])
                            lnodes_new.append([ln_new[0],ln_new[1]])
                            #el6.R_value = float('Inf')
                            #el4.R_value = float('Inf')
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[1], ln_new[0])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[1], ln_new[0])
                            el4.set_cur_dir(ln_new[1], ln_new[0])
                            el5.set_cur_dir(ln_new[0], ln_new[1])

                        elif el3.type == 'kz': #(12)
                            #el6.R_value = float('Inf')
                            el3.cur1 = el1
                            el3.cur1sign =1
                            el3.cur2 = el2
                            el3.cur2sign = -1
                            el3.pointer = None
                            ln_new.append([el1, el2, el4,  el3, 0])
                            ln_new.append([el1, el2, el3, el5, el4, 0])
                            ln_new.append([el5,  0])
                            lnodes_new.append([ln_new[1]], ln_new[2])
                            lnodes_new.append([ln_new[0], ln_new[2]])
                            lnodes_new.append([ln_new[0], ln_new[1]])
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[2], ln_new[0])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[0], ln_new[1])
                            el4.set_cur_dir(ln_new[1], ln_new[0])
                            el5.set_cur_dir(ln_new[1], ln_new[2])
                    elif el4.type == 'xx': #(13)
                        dont_use_moon = True
                        b1 = source.I_value*el2.R_value/el4.L_value
                        b2 = source.I_value*el2.R_value/el5.L_value
                    elif el4.type == 'kz': #(14)
                        #el6.R_value = float('Inf')
                        ln_new.append([el1, el2, el4,el3, el5, 0])
                        ln_new.append([el1, el2, el3, el4,el5, 0])
                        #ln_new[0] = [el1, el2, el4, el6, 0]
                        #ln_new[1] = [el1, el2, el3, 0]
                        #ln_new[2] = [el3, el4, el5, 0]
                        #ln_new[3] = [el5, el6, 0]
                        lnodes_new.append([ln_new[1]])
                        lnodes_new.append([ln_new[0]])
                        #lnodes_new[0] = [ln_new[1], ln_new[2], ln_new[3]]
                        #lnodes_new[1] = [ln_new[2], ln_new[0]]
                        #lnodes_new[2] = [ln_new[0], ln_new[1], ln_new[3]]
                        #lnodes_new[3] = [ln_new[0], ln_new[2]]
                        el4.pointer = None
                        el4.cur2=0
                        el4.cur2sign=1
                        el4.cur1= el3
                        el4.cur1sign = 1
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[1], ln_new[0])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[1], ln_new[0])
                        el4.set_cur_dir(ln_new[1], ln_new[0])
                        el5.set_cur_dir(ln_new[1], ln_new[0])
                elif el5.type =='kz':
                    if el4.type == 'R':
                        if el3.type == 'xx':
                            dont_use_moon = True #(15)
                            b1 = source.I_value*el2.R_value/el3.L_value
                            b2 =0
                        elif el3.type == 'kz': #(16)
                            ln_new.append([el1, el2, el4,el3, el6, el5, 0])
                            ln_new.append([el1, el2,el3, el4, el5,el6, 0])
                            lnodes_new.append([ln_new[1]])
                            lnodes_new.append([ln_new[0]])
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[1], ln_new[0])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[1], ln_new[0])
                            el3.pointer = None
                            el3.cur1 = el5
                            el3.cur1sign = 1
                            el3.cur2 = el4
                            el3.cur2sign = 1
                            el4.set_cur_dir(ln_new[1], ln_new[0])
                            el5.set_cur_dir(ln_new[1], ln_new[0])
                            el5.pointer = el6.R_value
                    elif el4.type == 'kz':  #(17)
                        ln_new.append([el1, el2, el4, el6, el5, 0])
                        ln_new.append([el1, el2, el3, 0])
                        ln_new.append([el3, el4, el5, el6, 0])
                        lnodes_new.append([ln_new[1], ln_new[2]])
                        lnodes_new.append([ln_new[2], ln_new[0]])
                        lnodes_new.append([ln_new[0], ln_new[1]])
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[2], ln_new[0])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[1], ln_new[2])
                        el4.set_cur_dir(ln_new[2], ln_new[0])
                        el5.set_cur_dir(ln_new[2], ln_new[0])
                        el5.pointer = None
                        el5.cur1sign=   1
                        el5.cur1=el2
                        el5.cur2 =0
                        el5.cur2sign =1
                    elif el4.type == 'xx': #(18)
                        dont_use_moon = True
                        b1 = (source.I_value * (el2.R_value / (el3.R_value + el2.R_value))) / el4.C_value
                        b2 = 0
            elif el2.type == 'kz':
                if el4.type == 'kz': #(50
                    el2.I_value = source.I_value
                    el4.I_value = 0
                elif el4.type == 'R': #(51
                    el2.I_value = source.I_value
                    el5.I_value = 0



            pass
        elif source == el2 :
            if el5.type == 'kz': #(19)
                ln_new.append([el1, el2, el4, el6, el5, 0])
                ln_new.append([el1, el2, el3, 0])
                ln_new.append([el3, el4, el5,el6, 0])
                lnodes_new.append([ln_new[1], ln_new[2]])
                lnodes_new.append([ln_new[2], ln_new[0]])
                lnodes_new.append([ln_new[0], ln_new[1]])
                if source.type == 'I':
                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[0],ln_new[2] )
                    el2.set_cur_dir(ln_new[1], ln_new[0])
                    el3.set_cur_dir(ln_new[2],ln_new[1] )
                    el4.set_cur_dir(ln_new[0],ln_new[2] )
                    el5.set_cur_dir(ln_new[0],ln_new[2] )
                    el5.pointer = None
                    el5.cur1 = el2
                    el5.cur1sign = 1
                    el5.cur2 = el4
                    el5.cur2sign = -1
                    el3.sign = el4.sign =el5.sign =el6.sign = -1
                else:
                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir( ln_new[2],ln_new[0])
                    el2.set_cur_dir(ln_new[0], ln_new[1])
                    el3.set_cur_dir(ln_new[1], ln_new[2])
                    el4.set_cur_dir(ln_new[2], ln_new[0])
                    el5.set_cur_dir(ln_new[2], ln_new[0])
                    el5.pointer = None
                    el5.cur1 = el2
                    el5.cur1sign = 1
                    el5.cur2 = el4
                    el5.cur2sign = -1
                    source.I_value = source.U_value/((el6.R_value*(el3.R_value+el4.R_value))/(el3.R_value+el4.R_value + el6.R_value))
            elif el5.type =='R':
                if el3.type == 'R' and el4.type == 'xx': #(21)
                    ln_new.append([el1, el2, el4, el6,  0])
                    ln_new.append([el1, el2, el3, 0])
                    ln_new.append([el3, el4, el5, 0])
                    ln_new.append([ el5, el6,0])
                    lnodes_new.append([ln_new[1], ln_new[2], ln_new[3]])
                    lnodes_new.append([ln_new[2], ln_new[0]])
                    lnodes_new.append([ln_new[0], ln_new[1], ln_new[3]])
                    lnodes_new.append([ln_new[0], ln_new[2]])
                    if source.type == 'I':
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[0], ln_new[3])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[2], ln_new[1])
                        el4.set_cur_dir(ln_new[0], ln_new[2])
                        el5.set_cur_dir(ln_new[3], ln_new[2])
                        el3.sign = el4.sign = el5.sign = el6.sign = -1
                    else:
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[3], ln_new[0])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[1], ln_new[2])
                        el4.set_cur_dir(ln_new[2], ln_new[0])
                        el5.set_cur_dir(ln_new[2], ln_new[3])
                if el3.type == 'R' and el4.type == 'kz':  #(20)
                    dont_use_moon = True
                    ln_new.append([el1, el2, el3, el4,  0])
                    ln_new.append([el1, el2, el4,  el3,  0])
                    lnodes_new.append([ln_new[1]])
                    lnodes_new.append([ln_new[0]])
                    #el5.R_value = float('Inf')
                    #el6.R_value = float('Inf')
                    el4.pointer = None
                    el4.cur1 = el2
                    el4.cur1sign = 1
                    el4.cur2sign=1
                    el4.cur2=0
                    if source.type == 'I':
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[1], ln_new[0])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[0], ln_new[1])
                        el4.set_cur_dir(ln_new[0], ln_new[1])
                        el5.set_cur_dir(ln_new[0], ln_new[1])
                        el4.sign = el3.sign = -1
                        b1 = source.I_value* el3.R_value/el2.L_value*el2.sign
                        b2 = source.I_value/el4.C_value/el4.sign
                    else:
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[1], ln_new[0])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[1], ln_new[0])
                        el4.set_cur_dir(ln_new[1], ln_new[0])
                        el5.set_cur_dir(ln_new[0], ln_new[1])
                        el2.sign = -1
                        b1 = source.U_value/el3.R_value/el2.C_value*el2.sign
                        b2 = source.U_value/el3.R_value/el4.C_value*el4.sign
                        source.I_value = source.U_value / el3.R_value
            elif el5.type =='xx':  #(22)
                ln_new.append([el1, el2, el4, el5, 0])
                ln_new.append([el1, el2, el3, 0])
                ln_new.append([el3, el4, el6, 0])
                lnodes_new.append([ln_new[1], ln_new[2]])
                lnodes_new.append([ln_new[2], ln_new[0]])
                lnodes_new.append([ln_new[0], ln_new[1]])
                # el6.R_value = float('Inf')
                if source.type == 'U':
                    el3.sign = el4.sign = el2.sign = el6.sign = -1
                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[1], ln_new[0])
                    el2.set_cur_dir(ln_new[0], ln_new[1])
                    el3.set_cur_dir(ln_new[1], ln_new[2])
                    el4.set_cur_dir(ln_new[2], ln_new[0])
                    el5.set_cur_dir(ln_new[2], ln_new[0])


                else:
                    el5.sign = -1
                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[0], ln_new[2])
                    el2.set_cur_dir(ln_new[1], ln_new[0])
                    el3.set_cur_dir(ln_new[2], ln_new[1])
                    el4.set_cur_dir(ln_new[0], ln_new[2])
                    el5.set_cur_dir(ln_new[0], ln_new[2])


        elif source == el3:
            if el2.type == 'R':
                if el4.type == 'R':
                    if el5.type == 'xx': #(23)
                        ln_new.append([el1, el2, el4, el5, 0])
                        ln_new.append([el1, el2, el3, 0])
                        ln_new.append([el3, el4, el6, 0])
                        lnodes_new.append([ln_new[1], ln_new[2]])
                        lnodes_new.append([ln_new[2], ln_new[0]])
                        lnodes_new.append([ln_new[0], ln_new[1]])
                        #el6.R_value = float('Inf')
                        if source.type == 'U':
                            el3.sign = el4.sign = el5.sign = el6.sign = -1

                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[0], ln_new[2])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[2], ln_new[1])
                            el4.set_cur_dir(ln_new[0], ln_new[2])
                            el5.set_cur_dir(ln_new[0], ln_new[2])
                        else:
                            el2.sign = -1

                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[1], ln_new[0])
                            el2.set_cur_dir(ln_new[0], ln_new[1])
                            el3.set_cur_dir(ln_new[1], ln_new[2])
                            el4.set_cur_dir(ln_new[2], ln_new[0])
                            el5.set_cur_dir(ln_new[2], ln_new[0])

                    elif el5.type == 'kz': #(24)
                        ln_new.append([el1, el2, el4,  el6, el5, 0])
                        ln_new.append([el1, el2, el3,  0])
                        ln_new.append([el4, el5, el3, el6, 0])
                        lnodes_new.append([ln_new[1], ln_new[2]])
                        lnodes_new.append([ln_new[0],ln_new[2]])
                        lnodes_new.append([ln_new[0],ln_new[1]])
                        el5.pointer = None
                        el5.cur1 = el6
                        el5.cur1sign =1
                        el5.cur2 = 0
                        el5.cur2sign = -1
                        if source.type == 'U':
                            el3.sign = el4.sign = el5.sign = el6.sign = -1
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[0], ln_new[2])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[2], ln_new[1])
                            el4.set_cur_dir(ln_new[0], ln_new[2])
                            el5.set_cur_dir(ln_new[0], ln_new[2])
                            el3.pointer = None
                            el3.cur1 = el2
                            el3.cur1sign = 1
                            el3.cur2 = 0
                            el3.cur2sign = 1
                            #source.I_value = source.U_value/(el2.R_value + (el6.R_value*el4.R_value)/(el6.R_value+el4.R_value))

                        else:
                            el2.sign = -1
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[2], ln_new[0])
                            el2.set_cur_dir(ln_new[0], ln_new[1])
                            el3.set_cur_dir(ln_new[1], ln_new[2])
                            el4.set_cur_dir(ln_new[2], ln_new[0])
                            el5.set_cur_dir(ln_new[2], ln_new[0])

                elif el4.type == 'xx': #(25)
                    lnodes_new.clear()
                    ln_new.append([el1, el2, el4, el6, 0])
                    ln_new.append([el1, el2, el3, 0])
                    ln_new.append([el3, el4, el5, 0])
                    ln_new.append([el5, el6, 0])
                    lnodes_new.append([ln_new[1], ln_new[2], ln_new[3]])
                    lnodes_new.append([ln_new[2], ln_new[0]])
                    lnodes_new.append([ln_new[0], ln_new[1], ln_new[3]])
                    lnodes_new.append([ln_new[0], ln_new[2]])
                    if source.type == 'U':
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[0], ln_new[3])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[2], ln_new[1])
                        el4.set_cur_dir(ln_new[0], ln_new[2])
                        el5.set_cur_dir(ln_new[3], ln_new[2])
                        el3.sign = el4.sign = el5.sign = el6.sign = -1
                    else:
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[3], ln_new[0])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[1], ln_new[2])
                        el4.set_cur_dir(ln_new[2], ln_new[0])
                        el5.set_cur_dir(ln_new[2], ln_new[3])
                        el2.sign = -1
                elif el4.type == 'kz': #(26)
                    ln_new.append([ el2, el4, 0])
                    ln_new.append([ el2, el3, 0])
                    ln_new.append([ el2, el4, 0])
                    lnodes_new.append([ln_new[1],ln_new[2]])
                    lnodes_new.append([ln_new[0],ln_new[2]])
                    lnodes_new.append([ln_new[0],ln_new[1]])
                    el4.pointer = None
                    el4.cur1=el1
                    dont_use_moon = True
                    if source.type == 'U':
                        b1 = el3.U_value/el2.R_value/el3.C_value * el3.sign
                        b2 = el3.U_value/el4.C_value* el4.sign
                        el3.pointer = el2.R_value
                        el3.sign = el4.sign  = -1
                        source.I_value = source.U_value/el2.R_value
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[1], ln_new[0])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[0], ln_new[1])
                        el4.set_cur_dir(ln_new[0], ln_new[1])
                        el5.set_cur_dir(ln_new[0], ln_new[1])
                        el4.cur2sign=1
                        el4.cur2 =0
                        el4.cur1sign =1
                    else:

                        b1 = el3.I_value*el2.R_value/el3.L_value * el3.sign
                        b2 = el3.I_value*el2.R_value/el4.C_value* el4.sign
                        el2.sign = -1
                        el4.cur2sign=1
                        el4.cur2=0
                        el4.cur1sign =-1
                        el3.U_value = el3.I_value*el2.R_value
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[1], ln_new[0])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[1], ln_new[2])
                        el4.set_cur_dir(ln_new[1], ln_new[0])
                        el5.set_cur_dir(ln_new[1], ln_new[0])
                    #el6.R_value = float('Inf')
                    #el5.R_value = float('Inf')
        elif source == el4:
            if el5.type == 'R':
                if el2.type == 'R':
                    if el3.type == 'xx': #(27)
                        ln_new.append([el1, el2, el3,  el6,  0])
                        ln_new.append([el1, el2, el3,  0])
                        ln_new.append([el3, el5, el4,  0])
                        ln_new.append([el5, el6, 0])
                        lnodes_new.append([ln_new[1], ln_new[2], ln_new[3]])
                        lnodes_new.append([ln_new[2], ln_new[0]])
                        lnodes_new.append([ln_new[0], ln_new[1], ln_new[3]])
                        lnodes_new.append([ln_new[0], ln_new[2]])
                        dont_use_moon = True
                        el5.R_value = 3
                        el6.R_value =1
                        if source.type == 'I':
                            el5.sign = el6.sign= el2.sign = -1
                            b1 = el3.sign*el4.I_value*(el5.R_value+el6.R_value)/el3.L_value
                            b2 = el4.sign*el4.I_value*(el5.R_value+el6.R_value)/el4.L_value
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[0], ln_new[3])
                            el2.set_cur_dir(ln_new[0], ln_new[1])
                            el3.set_cur_dir(ln_new[1], ln_new[2])
                            el4.set_cur_dir(ln_new[2], ln_new[0])
                            el5.set_cur_dir(ln_new[3], ln_new[2])
                        else:
                            el4.sign = -1
                            b1 = el3.sign*el4.U_value/el3.L_value
                            b2 = el4.sign*el4.U_value/(el5.R_value+el6.R_value)/el4.C_value
                            #print("\nb1=", b1, " b2=", b2)
                            #cstr.show_all_el_info(lel,ln)
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[0], ln_new[3])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[2], ln_new[1])
                            el4.set_cur_dir(ln_new[0], ln_new[1])
                            el5.set_cur_dir(ln_new[3], ln_new[2])
                    elif el3.type == 'kz': #(28)
                        ln_new.append([el1, el2, el3, el4, el6,  0])
                        ln_new.append([el1, el2, el3, el5, el4,  0])
                        ln_new.append([el5, el6, 0])
                        lnodes_new.append([ln_new[1],ln_new[2]])
                        lnodes_new.append([ln_new[0],ln_new[2]])
                        lnodes_new.append([ln_new[0],ln_new[1]])
                        el3.pointer=None
                        el3.cur1sign=1
                        el3.cur1 = el4
                        el3.cur2 =el5
                        el3.cur2sign=-1
                        if source.type == 'I':
                            el5.sign = el6.sign = el2.sign = el3.sign= -1

                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[0], ln_new[2])
                            el2.set_cur_dir(ln_new[0], ln_new[1])
                            el3.set_cur_dir(ln_new[0], ln_new[1])
                            el4.set_cur_dir(ln_new[1], ln_new[0])
                            el5.set_cur_dir(ln_new[2], ln_new[1])
                        else:
                            el3.sign = el4.sign= -1
                            #el4.pointer = el2.R_value*(el5.R_value+el6.R_value)/(el2.R_value+el5.R_value+el6.R_value)
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[2], ln_new[0])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[1], ln_new[0])
                            el4.set_cur_dir(ln_new[0], ln_new[1])
                            el5.set_cur_dir(ln_new[1], ln_new[2])
                            source.I_value = source.U_value/(((el5.R_value+el6.R_value)*el2.R_value)/(el5.R_value+el6.R_value+el2.R_value))

                elif el2.type == 'xx': #(29)
                    ln_new.append([el1, el2,  el4, el6, 0])
                    ln_new.append([el1, el2,  el5, el4,  0])
                    ln_new.append([ el5,  el6, 0])
                    lnodes_new.append([ln_new[1],ln_new[2]])
                    lnodes_new.append([ln_new[0],ln_new[2]])
                    lnodes_new.append([ln_new[0],ln_new[1]])
                    el3.R_value = float('Inf')
                    if source.type == 'I':
                        el2.sign = -1

                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[0], ln_new[2])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[0], ln_new[1])
                        el4.set_cur_dir(ln_new[1], ln_new[0])
                        el5.set_cur_dir(ln_new[2], ln_new[1])
                    else:
                        el3.sign = el4.sign = -1
                        source.I_value = source.U_value/(el5.R_value+el6.R_value)
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[2], ln_new[0])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[1], ln_new[0])
                        el4.set_cur_dir(ln_new[0], ln_new[1])
                        el5.set_cur_dir(ln_new[1], ln_new[2])
                elif el2.type == 'kz': #(30)
                    ln_new.append([el1, el2, el3, el4, el6, 0])
                    ln_new.append([el3,  el5, el4,  0])
                    ln_new.append([ el5,  el6, 0])
                    lnodes_new.append([ln_new[1],ln_new[2]])
                    lnodes_new.append([ln_new[0],ln_new[2]])
                    lnodes_new.append([ln_new[0],ln_new[1]])
                    el2.pointer = None
                    el2.cur1=el4
                    el2.cur1sign =1
                    el2.cur2 = el6
                    el2.cur2sign = -1
                    if source.type == 'I':
                        el2.sign = -1

                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[0], ln_new[2])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[0], ln_new[1])
                        el4.set_cur_dir(ln_new[1], ln_new[0])
                        el5.set_cur_dir(ln_new[2], ln_new[1])
                    else:
                        el3.sign = el4.sign = -1

                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[2], ln_new[0])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[1], ln_new[0])
                        el4.set_cur_dir(ln_new[0], ln_new[1])
                        el5.set_cur_dir(ln_new[1], ln_new[2])
                        r1 = el5.R_value + el6.R_value
                        r2 = r1*el3.R_value/( r1+ el3.R_value)
                        source.I_value = source.U_value / r2

            elif el5.type == 'xx': #(31)
                ln_new.append([el5, el2,  el4,  0])
                ln_new.append([el3,  el2, 0])
                ln_new.append([el5,el3,el4,  0])
                lnodes_new.append([ln_new[1], ln_new[2]])
                lnodes_new.append([ln_new[0], ln_new[2]])
                lnodes_new.append([ln_new[0], ln_new[1]])
                if source.type == 'I':
                    el2.sign = el5.sign= -1

                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[0], ln_new[2])
                    el2.set_cur_dir(ln_new[0], ln_new[1])
                    el3.set_cur_dir(ln_new[1], ln_new[2])
                    el4.set_cur_dir(ln_new[2], ln_new[0])
                    el5.set_cur_dir(ln_new[0], ln_new[2])
                else:
                    el3.sign = el4.sign = -1
                    source.I_value = source.U_value/(el2.R_value+el3.R_value)

                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[2], ln_new[0])
                    el2.set_cur_dir(ln_new[1], ln_new[0])
                    el3.set_cur_dir(ln_new[2], ln_new[1])
                    el4.set_cur_dir(ln_new[0], ln_new[2])
                    el5.set_cur_dir(ln_new[2], ln_new[0])

            elif el5.type == 'kz': #(32)
                ln_new.append([el5, el2,  el4,el6,  0])
                ln_new.append([el3,  el2, 0])
                ln_new.append([el5,el3,el4,el6,  0])
                lnodes_new.append([ln_new[1], ln_new[2]])
                lnodes_new.append([ln_new[0], ln_new[2]])
                lnodes_new.append([ln_new[0], ln_new[1]])
                el5.pointer = None
                el5.cur1 = el4
                el5.cur1sign =1
                el5.cur2 = el2
                el5.cur2sign = -1
                if source.type == 'I':
                    el2.sign = el5.sign= el6.sign= -1

                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[0], ln_new[2])
                    el2.set_cur_dir(ln_new[0], ln_new[1])
                    el3.set_cur_dir(ln_new[1], ln_new[2])
                    el4.set_cur_dir(ln_new[2], ln_new[0])
                    el5.set_cur_dir(ln_new[0], ln_new[2])
                else:
                    el3.sign = el4.sign = -1

                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[2], ln_new[0])
                    el2.set_cur_dir(ln_new[1], ln_new[0])
                    el3.set_cur_dir(ln_new[2], ln_new[1])
                    el4.set_cur_dir(ln_new[0], ln_new[2])
                    el5.set_cur_dir(ln_new[2], ln_new[0])
                    source.I_value = source.U_value / (
                    ((el2.R_value + el3.R_value) * el6.R_value) / (el2.R_value + el3.R_value + el6.R_value))

        elif source == el5:
            if el4.type == 'R':
                if el3.type == 'R':
                    if el2.type == 'xx': #(33)
                        ln_new.append([el4,el2,el6,  0])
                        ln_new.append([el2,  el4,el5, 0])
                        ln_new.append([el5,el6,  0])
                        lnodes_new.append([ln_new[1], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[1]])
                        el3.R_value = float('Inf')
                        if source.type == 'I':
                            el2.sign= el4.sign = -1

                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[2], ln_new[0])
                            el2.set_cur_dir(ln_new[0], ln_new[1])
                            el3.set_cur_dir(ln_new[0], ln_new[1])
                            el4.set_cur_dir(ln_new[0], ln_new[1])
                            el5.set_cur_dir(ln_new[1], ln_new[2])


                        else:
                            el5.sign = el6.sign = -1

                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[0], ln_new[2])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[1], ln_new[0])
                            el4.set_cur_dir(ln_new[1], ln_new[0])
                            el5.set_cur_dir(ln_new[2], ln_new[1])
                            el5.I_value = source.U_value/(el6.R_value+el4.R_value)
                    elif el2.type == 'kz': #(34)
                        ln_new.append([el3,el4,el2,el6,  0])
                        ln_new.append([el2,el3,  el4,el5, 0])
                        ln_new.append([el5,el6,  0])
                        lnodes_new.append([ln_new[1], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[1]])
                        el2.pointer=None
                        el2.cur1=el5
                        el2.cur1sign=1
                        el2.cur2 = el4
                        el2.cur2sign=-1
                        if source.type == 'I':
                            el2.sign  = -1

                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[2], ln_new[0])
                            el2.set_cur_dir(ln_new[0], ln_new[1])
                            el3.set_cur_dir(ln_new[0], ln_new[1])
                            el4.set_cur_dir(ln_new[0], ln_new[1])
                            el5.set_cur_dir(ln_new[1], ln_new[2])


                        else:
                            el5.sign = el6.sign= el3.sign= -1
                            R1 = (el3.R_value * el4.R_value)/(el3.R_value + el4.R_value)
                            R2 = el6.R_value+R1
                            el5.I_value=source.U_value/R2
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el6.set_cur_dir(ln_new[0], ln_new[2])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[1], ln_new[0])
                            el4.set_cur_dir(ln_new[1], ln_new[0])
                            el5.set_cur_dir(ln_new[2], ln_new[1])
                elif el3.type == 'xx': #(35)
                    dont_use_moon= True
                    ln_new.append([el3, el4, el6, 0])
                    ln_new.append([el3, el4, el5, 0])
                    ln_new.append([el5, el6, 0])
                    lnodes_new.append([ln_new[1], ln_new[2]])
                    lnodes_new.append([ln_new[0], ln_new[2]])
                    lnodes_new.append([ln_new[0], ln_new[1]])
                    if source.type == 'I':
                        el2.sign = el4.sign = -1
                        b1 = source.I_value*el4.R_value/el3.L_value*el3.sign
                        print(source.I_value,(el4.R_value+el6.R_value),el5.L_value)
                        b2 = source.I_value*(el4.R_value+el6.R_value)/el5.L_value*el5.sign

                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[2], ln_new[0])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[0], ln_new[1])
                        el4.set_cur_dir(ln_new[0], ln_new[1])
                        el5.set_cur_dir(ln_new[1], ln_new[2])


                    else:
                        el5.sign = el6.sign = -1
                        i = source.U_value/(el4.R_value + el6.R_value)
                        b1 = i * el4.R_value / el3.L_value * el3.sign
                        b2 = i/ el5.C_value * el5.sign
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el6.set_cur_dir(ln_new[0], ln_new[2])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[1], ln_new[0])
                        el4.set_cur_dir(ln_new[1], ln_new[0])
                        el5.set_cur_dir(ln_new[2], ln_new[1])
                        el5.I_value = source.U_value / (el6.R_value + el4.R_value)
                elif el3.type == 'kz': #(36) RCRC
                    ln_new.append([el5, el6,  0])
                    ln_new.append([el2, el3,el6, el4,  0])
                    ln_new.append([el3, el2, el4,el5,  0])
                    lnodes_new.append([ln_new[1], ln_new[2]])
                    lnodes_new.append([ln_new[0],ln_new[2]])
                    lnodes_new.append([ln_new[0],ln_new[1]])
                    el5.sign = el3.sign= -1
                    el5.pointer = None
                    el5.cur1 = el6
                    el5.cur1sign = 1
                    el5.cur2 = 0
                    el5.cur2sign = 1
                    el3.pointer = None
                    el3.cur1 = el2
                    el3.cur1sign = 1
                    el3.cur2 = 0
                    el3.cur2sign = 1
                    #r1 = (el2.R_value*el4.R_value)/(el2.R_value+el4.R_value)
                    #source.I_value = source.U_value / (r1+ el6.R_value)

                    el1.set_cur_dir(ln_new[2], ln_new[1])
                    el6.set_cur_dir(ln_new[1], ln_new[0])
                    el2.set_cur_dir(ln_new[2], ln_new[1])
                    el3.set_cur_dir(ln_new[2], ln_new[1])
                    el4.set_cur_dir(ln_new[2], ln_new[1])
                    el5.set_cur_dir(ln_new[0], ln_new[2])
            elif el4.type == 'xx': #(37) RRLL
                ln_new.append([el1, el2, el4, el6, 0])
                ln_new.append([el1, el2, el3, 0])
                ln_new.append([el3, el4, el5, 0])
                ln_new.append([el5, el6, 0])
                lnodes_new.append([ln_new[1], ln_new[2], ln_new[3]])
                lnodes_new.append([ln_new[2], ln_new[0]])
                lnodes_new.append([ln_new[0], ln_new[1], ln_new[3]])
                lnodes_new.append([ln_new[0], ln_new[2]])
                if source.type == 'I':
                    el2.sign =el4.sign= -1

                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el6.set_cur_dir(ln_new[3], ln_new[0])
                    el2.set_cur_dir(ln_new[0], ln_new[1])
                    el3.set_cur_dir(ln_new[1], ln_new[2])
                    el4.set_cur_dir(ln_new[0], ln_new[2])
                    el5.set_cur_dir(ln_new[2], ln_new[3])
            elif el4.type == 'kz': #(38) RRCC
                dont_use_moon = True
                el5.sign = el6.sign = -1
                b1 = source.U_value/el6.R_value*el4.sign/el4.C_value
                b2 = source.U_value/el6.R_value*el5.sign/el5.C_value
                ln_new.append([el1, el2, el3, el4, el6, el5, 0])
                ln_new.append([el1, el2, el3, el5, el4, el6, 0])
                lnodes_new.append([ln_new[1]])
                lnodes_new.append([ln_new[0]])
                el2.R_value = el3.R_value = float('Inf')
                source.I_value = source.U_value/el6.R_value

                el1.set_cur_dir(ln_new[0], ln_new[1])
                el6.set_cur_dir(ln_new[0], ln_new[1])
                el2.set_cur_dir(ln_new[0], ln_new[1])
                el3.set_cur_dir(ln_new[0], ln_new[1])
                el4.set_cur_dir(ln_new[1], ln_new[0])
                el5.set_cur_dir(ln_new[0], ln_new[1])

       # for i in range(len(lel)):
        #    for j in range(len(lel_new)):
         #       if lel[i].number == lel_new[j].number:
          #          list.append(lel[i])

    else:
        if source == el1:
            if el2.type == 'R':
                if el4.type == 'R':
                    if el5.type == 'kz': #(1)
                        dont_use_moon= True
                        b1 = source.U_value/el2.R_value/el3.C_value
                        b2= 0
                    elif el5.type == 'xx':
                        if el3.type == 'xx': #(2)
                            dont_use_moon = True
                            i = source.U_value/(el2.R_value + el4.R_value + el6.R_value)
                            u6 = i*el6.R_value
                            b2 = u6/el5.L_value
                            u4 = i*el4.R_value
                            u3= u4+u6
                            b1 = u3/el3.L_value
                            ln_new.append([el1, el3, el5, el6, 0])
                            ln_new.append([el1, el2,  0])
                            ln_new.append([el3, el4, el2, 0])
                            ln_new.append([el5, el6,el4, 0])
                            lnodes_new.append([ln_new[1], ln_new[2], ln_new[3]])
                            lnodes_new.append([ln_new[2], ln_new[0]])
                            lnodes_new.append([ln_new[0], ln_new[1], ln_new[3]])
                            lnodes_new.append([ln_new[0], ln_new[2]])
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el2.set_cur_dir(ln_new[1], ln_new[2])
                            el3.set_cur_dir(ln_new[2], ln_new[0])
                            el4.set_cur_dir(ln_new[2], ln_new[3])
                            el5.set_cur_dir(ln_new[3], ln_new[0])
                            el6.set_cur_dir(ln_new[3], ln_new[0])
                        elif el3.type == 'kz': #(3)
                            dont_use_moon = True
                            b1 = source.U_value / el2.R_value / el3.C_value
                            b2 = source.U_value/el5.L_value
                elif el4.type == 'xx':
                    if el5.type == 'R':
                        if el3.type == 'kz': #(6)
                            dont_use_moon = True
                            b1 = source.U_value / el2.R_value / el3.C_value
                            b2 = source.U_value / el4.L_value
                        elif el3.type == 'xx': #(4)
                            B_is_zeros = True
                    elif el5.type =='xx':#(5)
                        dont_use_moon = True
                        b1 = (source.U_value / (el2.R_value +el3.R_value))*el3.R_value / el4.L_value
                        b2 = 0
                elif el4.type == 'kz':
                    if el5.type == 'R':
                        if el3.type == 'kz': #(7)
                            dont_use_moon = True
                            b1 = source.U_value / el2.R_value/ el3.C_value
                            b2 = 0
                        elif el3.type == 'xx': #(9)
                            el4.cur1 = el2
                            el4.cur1sign =1
                            el4.cur2 = 0
                            el4.cur2sign = 1
                            ln_new.append([el5, el6, el3,el1, 0])
                            ln_new.append([el2, el1,el4,el3, 0])
                            ln_new.append([el5, el6,el4,el2,el3, 0])
                            lnodes_new.append([ln_new[1], ln_new[2]])
                            lnodes_new.append([ln_new[0], ln_new[2]])
                            lnodes_new.append([ln_new[0], ln_new[1]])
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el2.set_cur_dir(ln_new[1], ln_new[2])
                            el3.set_cur_dir(ln_new[2], ln_new[0])
                            el4.set_cur_dir(ln_new[1], ln_new[2])
                            el5.set_cur_dir(ln_new[2], ln_new[0])
                            el6.set_cur_dir(ln_new[2], ln_new[0])

                    elif el5.type == 'kz': #(8)
                        dont_use_moon= True
                        r5r6 = (el2.R_value*el3.R_value)/(el2.R_value+el3.R_value)
                        #R = r5r6*el3.R_value/(r5r6+el4.R_value)
                        b1 = source.U_value/el2.R_value/el4.C_value
                        b2 = source.U_value / el2.R_value / el5.C_value
            elif el2.type == 'kz':
                if el4.type == 'kz': #(10)
                    dont_use_moon = True
                    b1 = source.U_value /((el5.R_value * el6.R_value)/ (el5.R_value + el6.R_value)) / el2.C_value
                    b2 = source.U_value / ((el5.R_value * el6.R_value)/ (el5.R_value + el6.R_value)) / el4.C_value
                elif el4.type == 'R':
                    if el5.type == 'kz': #(11)
                        dont_use_moon = True
                        Re = el4.R_value* el3.R_value/(el4.R_value+ el3.R_value)
                        b1 = source.U_value/Re/el2.C_value
                        b2 = source.U_value/el4.R_value/el5.C_value
                    elif el5.type == 'xx': #(12)
                        el2.pointer = None
                        el2.cur1 = el3
                        el2.cur1sign = 1
                        el2.cur2 = el4
                        el2.cur2sign = 1
                        ln_new.append([el1, el2, el3, el4, 0])
                        ln_new.append([el5,el6, el2, el1, el3, 0])
                        ln_new.append([el5, el6, el4,  0])
                        lnodes_new.append([ln_new[1], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[1]])
                        el1.set_cur_dir(ln_new[1], ln_new[0])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[0], ln_new[1])
                        el4.set_cur_dir(ln_new[0], ln_new[2])
                        el5.set_cur_dir(ln_new[2], ln_new[1])
                        el6.set_cur_dir(ln_new[2], ln_new[1])
                elif el4.type == 'xx': #(13)
                        dont_use_moon = True
                        b1 = source.U_value/el3.R_value/el2.C_value
                        b2 = source.U_value/el4.L_value
            elif el2.type == 'xx':
                if el4.type == 'xx': #(14)
                    dont_use_moon = True
                    b1 = source.U_value / el2.L_value
                    b2 =0
                elif el4.type == 'R': #(15)
                    B_is_zeros = True
        elif source == el2:
            if el3.type == 'R':
                if el4.type == 'kz': #(16)
                    dont_use_moon = True
                    el2.sign =-1
                    el4.sign = -1
                    R56 = ((el5.R_value * el6.R_value)/ (el5.R_value + el6.R_value))
                    Re = R56*el3.R_value/(R56 + el3.R_value)
                    #R = el5.R_value*el6.R_value/(el5.R_value+el6.R_value)
                    b1 = source.U_value/Re/el2.C_value * el2.sign
                    i2 = source.U_value / Re
                    i3 = i2*R56/(R56 + el3.R_value)
                    i4 = i2 - i3
                    b2 = i4/el4.C_value * el4.sign
                elif el4.type == 'R':
                    if el5.type =='xx': #(21)
                        el2.pointer = None
                        el2.cur1 = el3
                        el2.cur1sign = 1
                        el2.cur2 = el4
                        el2.cur2sign = 1
                        ln_new.append([el5, el6, el3, el2, 0])
                        ln_new.append([el2,  el4, el3, 0])
                        ln_new.append([el5, el6, el4, 0])
                        lnodes_new.append([ln_new[1], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[1]])
                        if source.type == 'U':
                            el2.sign = -1
                            el5.sign = -1
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el2.set_cur_dir(ln_new[1], ln_new[0])
                            el3.set_cur_dir(ln_new[0], ln_new[1])
                            el4.set_cur_dir(ln_new[2], ln_new[1])
                            el5.set_cur_dir(ln_new[0], ln_new[2])
                            el6.set_cur_dir(ln_new[0], ln_new[2])
                        else: #(19) LRRL
                            el1.set_cur_dir(ln_new[0], ln_new[1])
                            el2.set_cur_dir(ln_new[0], ln_new[1])
                            el3.set_cur_dir(ln_new[1], ln_new[0])
                            el4.set_cur_dir(ln_new[1], ln_new[2])
                            el5.set_cur_dir(ln_new[2], ln_new[0])
                            el6.set_cur_dir(ln_new[2], ln_new[0])


                    elif el5.type == 'kz': #(17)
                        dont_use_moon= True
                        el2.sign=el5.sign = -1
                        i2 = source.U_value/(el3.R_value*el4.R_value/(el3.R_value+el4.R_value))
                        b1 = i2/el2.C_value*el2.sign
                        i4= i2*(el3.R_value/(el3.R_value+el4.R_value))
                        b2 = i4*el5.sign/el5.C_value

                elif el4.type == 'xx': #(18) (20)
                    dont_use_moon = True
                    if source.type == 'U':
                        el2.sign = el4.sign = -1
                        b1 = source.U_value/el3.R_value*el2.sign/el2.C_value
                        b2 = source.U_value/el4.L_value* el4.sign
                    else:
                        b1 = source.I_value*el3.R_value*el2.sign/el2.L_value
                        b2 = source.I_value*el3.R_value/el4.L_value* el4.sign

        elif source == el3:
            if el4.type == 'R':
                if el5.type == 'xx': #(24) (26)
                    ln_new.append([el5, el6, el3, el2, 0])
                    ln_new.append([el2, el4, el3, 0])
                    ln_new.append([el5, el6, el4, 0])
                    lnodes_new.append([ln_new[1], ln_new[2]])
                    lnodes_new.append([ln_new[0], ln_new[2]])
                    lnodes_new.append([ln_new[0], ln_new[1]])
                    if source.type == 'U': #(26) RCRL
                        el3.pointer = None
                        el3.cur1 = el2
                        el3.cur1sign = 1
                        el3.cur2 = el4
                        el3.cur2sign = 1
                        el3.sign = -1
                        el5.sign = -1
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[0], ln_new[1])
                        el4.set_cur_dir(ln_new[1], ln_new[2])
                        el5.set_cur_dir(ln_new[2], ln_new[0])
                        el6.set_cur_dir(ln_new[2], ln_new[0])
                    else:  # (24) RLRL
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[1], ln_new[0])
                        el4.set_cur_dir(ln_new[2], ln_new[1])
                        el5.set_cur_dir(ln_new[0], ln_new[2])
                        el6.set_cur_dir(ln_new[0], ln_new[2])
                elif el5.type == 'kz': #(22) RCRC
                    dont_use_moon = True
                    el3.sign = el5.sign = -1
                    b1 = source.U_value/(el2.R_value*el4.R_value/(el2.R_value+el4.R_value))/el3.C_value*el3.sign
                    i3 = source.U_value/(el2.R_value*el4.R_value/(el2.R_value+el4.R_value))
                    b2 = i3*(el2.R_value/(el2.R_value+el4.R_value))/el5.C_value*el5.sign
            elif el4.type =='kz': #(23) (28)
                dont_use_moon = True
                if source.type == 'U': #(23) RCCR
                    el3.sign = -1
                    R56 = el5.R_value*el6.R_value/(el5.R_value+el6.R_value)
                    Re = el2.R_value*R56/(el2.R_value+R56)
                    i3 = source.U_value/Re
                    b1 = i3/el3.C_value*el3.sign
                    Re2 = R56/(el2.R_value+ R56)
                    i2 = i3 * Re2
                    i4 = i3 - i2
                    b2 = i4/el4.C_value/el4.sign
                else: #(28) RLCR
                    dont_use_moon=True
                    el4.sign = -1
                    R56 = el5.R_value * el6.R_value / (el5.R_value + el6.R_value)
                    Re = el2.R_value * R56 / (el2.R_value + R56)
                    i3 = source.I_value
                    Re2 = R56 / (el2.R_value + R56)

                    i2 = i3 * Re2
                    U3 = i2*el2.R_value
                    i4 = i3 - i2
                    b1 = U3 / el3.L_value * el3.sign
                    b2 = i4 / el4.C_value / el4.sign
            elif el4.type =='xx':
                dont_use_moon = True
                if source.type == 'U': #(27) RCLR
                    el3.sign = -1
                    b1 = source.U_value/el2.R_value/el3.C_value*el3.sign
                    b2 = source.U_value/el4.L_value*el4.sign
                else: #(25) RLLR
                    el4.sign = -1
                    b1 = source.I_value * el2.R_value / el3.L_value * el3.sign
                    b2 = source.I_value * el2.R_value / el4.L_value * el4.sign

        elif source == el4:
            if el2.type == 'kz': #(35)
                dont_use_moon = True
                if source.type == 'U': #(29) CRCR
                    el2.sign = el4.sign= -1
                    R56 = el5.R_value * el6.R_value / (el5.R_value + el6.R_value)
                    i2 = source.U_value/R56
                    b1 = i2/el2.C_value*el2.sign
                    b2 = i2/el4.C_value*el4.sign
                else: #(35) CRLR
                    #el4.sign = -1
                    b1 = source.I_value/el2.C_value*el2.sign
                    R56 = el5.R_value * el6.R_value / (el5.R_value + el6.R_value)
                    i2 = source.I_value * R56
                    i5 = i2*(el6.R_value/(el6.R_value+el5.R_value))
                    b2 = i5*el5.R_value/el4.L_value*el4.sign


            elif el2.type =='R':
                if el3.type == 'kz':
                    dont_use_moon = True
                    if source.type == 'U': #(30) RCCR
                        el4.sign = -1
                        R56 = el5.R_value * el6.R_value / (el5.R_value + el6.R_value)
                        i2 = source.U_value / R56
                        b1 = i2 / el3.C_value * el3  .sign
                        b2 = i2 / el4.C_value * el4.sign
                    else: #(36) RCLR
                        el3.sign = -1
                        i5 = source.I_value*el6.R_value/(el6.R_value+el5.R_value)
                        b1 = source.I_value / el3.C_value * el3.sign
                        R56 = el5.R_value * el6.R_value / (el5.R_value + el6.R_value)
                        b2 = i5 * el5.R_value / el4.L_value * el4.sign
                elif el3.type == 'R':
                    if el5.type == 'xx': #(34) RRLL
                        ln_new.append([el5, el6, el3, el2, 0])
                        ln_new.append([el2, el4, el3, 0])
                        ln_new.append([el5, el6, el4, 0])
                        lnodes_new.append([ln_new[1], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[2]])
                        lnodes_new.append([ln_new[0], ln_new[1]])
                        el3.sign = -1
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[0], ln_new[1])
                        el4.set_cur_dir(ln_new[1], ln_new[2])
                        el5.set_cur_dir(ln_new[2], ln_new[0])
                        el6.set_cur_dir(ln_new[2], ln_new[0])
                    elif el5.type == 'kz': #(31) RRCC
                        dont_use_moon = True
                        el4.sign = el5.sign = -1
                        i2 = source.U_value/(el2.R_value*el3.R_value/(el2.R_value+el3.R_value))
                        b1 = i2/el5.C_value*el5.sign
                        b2 = i2/el4.C_value* el4.sign
                elif el3.type == 'xx':
                    ln_new.append([el5, el6, el3, el2, 0])
                    ln_new.append([el2, el4, el3, 0])
                    ln_new.append([el5, el6, el4, 0])
                    lnodes_new.append([ln_new[1], ln_new[2]])
                    lnodes_new.append([ln_new[0], ln_new[2]])
                    lnodes_new.append([ln_new[0], ln_new[1]])
                    if source.type == 'U': #(37) RLCR
                        el4.sign = -1
                        el4.pointer = None
                        el4.cur1 = el2
                        el4.cur2 = 0
                        el4.cur1sign =1
                        el4.cur2sign =1
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el2.set_cur_dir(ln_new[1], ln_new[0])
                        el3.set_cur_dir(ln_new[1], ln_new[0])
                        el4.set_cur_dir(ln_new[2], ln_new[1])
                        el5.set_cur_dir(ln_new[2], ln_new[0])
                        el6.set_cur_dir(ln_new[2], ln_new[0])
                    else: #(33) RLLR
                        el3.sign = -1
                        el1.set_cur_dir(ln_new[0], ln_new[1])
                        el2.set_cur_dir(ln_new[0], ln_new[1])
                        el3.set_cur_dir(ln_new[0], ln_new[1])
                        el4.set_cur_dir(ln_new[1], ln_new[2])
                        el5.set_cur_dir(ln_new[2], ln_new[0])
                        el6.set_cur_dir(ln_new[2], ln_new[0])
            elif el2.type == 'xx': #(32) LRLR
                ln_new.append([el5, el6, el3, el2, 0])
                ln_new.append([el2, el4, el3, 0])
                ln_new.append([el5, el6, el4, 0])
                lnodes_new.append([ln_new[1], ln_new[2]])
                lnodes_new.append([ln_new[0], ln_new[2]])
                lnodes_new.append([ln_new[0], ln_new[1]])
                el3.sign = -1
                el1.set_cur_dir(ln_new[0], ln_new[1])
                el2.set_cur_dir(ln_new[0], ln_new[1])
                el3.set_cur_dir(ln_new[0], ln_new[1])
                el4.set_cur_dir(ln_new[1], ln_new[2])
                el5.set_cur_dir(ln_new[2], ln_new[0])
                el6.set_cur_dir(ln_new[2], ln_new[0])
        elif source == el5:
            if el2.type == 'R':
                if el3.type == 'kz':
                    dont_use_moon = True
                    if source.type =='U': #(38) RCRC
                        el5.sign = -1
                        i5 = source.U_value/(el4.R_value*el6.R_value/(el4.R_value+el6.R_value))
                        i6 = i5*(el4.R_value/(el4.R_value+el6.R_value))
                        i3 = i5 - i6
                        b1 = i3/el3.C_value*el3.sign
                        b2 = i5/el5.C_value*el5.sign
                    else: #(44) RCRL
                        el3.sign = -1
                        i6 = source.I_value * (el4.R_value / (el4.R_value + el6.R_value))
                        i3 = source.I_value - i6
                        U5 = i6*el6.R_value
                        b1 = i3 / el3.C_value * el3.sign
                        b2 = U5 / el5.L_value * el5.sign
                elif el3.type == 'R':
                    if el4.type == 'xx': #(43) RRLL
                        dont_use_moon = True
                        b1 = source.I_value*el6.R_value/el4.L_value*el4.sign
                        b2 = source.I_value*el6.R_value/el5.L_value*el5.sign
                    elif el4.type == 'kz': #(40) RRCC
                        el5.sign = el4.sign = -1
                        dont_use_moon = True
                        R23 =  el2.R_value*el3.R_value/(el2.R_value+el3.R_value)
                        Re = el6.R_value*R23/(el6.R_value+R23)
                        i5 = source.U_value / Re
                        i6 = i5 * (R23 / (el2.R_value + el6.R_value+ el3.R_value))
                        i4 = i5 - i6
                        b1 = i4 / el4.C_value * el4.sign
                        b2 = i5 / el5.C_value * el5.sign

                elif el3.type == 'xx': #(41) RLRL
                    ln_new.append([el5, el6, el3, el2, 0])
                    ln_new.append([el2, el4, el3, 0])
                    ln_new.append([el5, el6, el4, 0])
                    lnodes_new.append([ln_new[1], ln_new[2]])
                    lnodes_new.append([ln_new[0], ln_new[2]])
                    lnodes_new.append([ln_new[0], ln_new[1]])
                    el3.sign = -1
                    el1.set_cur_dir(ln_new[0], ln_new[1])
                    el2.set_cur_dir(ln_new[0], ln_new[1])
                    el3.set_cur_dir(ln_new[0], ln_new[1])
                    el4.set_cur_dir(ln_new[1], ln_new[2])
                    el5.set_cur_dir(ln_new[2], ln_new[0])
                    el6.set_cur_dir(ln_new[2], ln_new[0])
            elif el2.type =='kz':
                if el4.type == 'kz': #(39) CRRC
                    el5.sign = el2.sign = -1
                    dont_use_moon = True
                    Re = el6.R_value * el4.R_value / (el6.R_value + el4.R_value)
                    i5 = source.U_value / Re
                    i6 = i5 * (el4.R_value / ( el6.R_value + el4.R_value))
                    i2 = i5 - i6
                    b1 = i2 / el2.C_value * el2.sign
                    b2 = i5 / el5.C_value * el5.sign
                elif el4.type == 'R': #(45)
                    dont_use_moon = True
                    el6.sign = el5.sign = -1
                    Re = el6.R_value * el4.R_value / (el6.R_value + el4.R_value)
                    i5 = source.I_value
                    i6 = i5 * (el4.R_value / (el6.R_value + el4.R_value))
                    i2 = i5 - i6
                    U5 = i6*el6.R_value
                    b1 = i2 / el2.C_value * el2.sign
                    b2 = U5 / el5.L_value * el5.sign
                    #source.I_value = source.U_value/Re
                    #i6 = source.I_value * (el4.R_value / (el6.R_value + el4.R_value))
                    #U5 = i6 * el6.R_value
                    #i2 = source.I_value - i6
                    #b1 = i2 / el2.C_value * el2.sign
                    #b2 = U5 / el5.C_value * el5.sign
            elif el2.type == 'xx': #(42)
                el3.sign = -1
                ln_new.append([el5, el6, el3, el2, 0])
                ln_new.append([el2, el4, el3, 0])
                ln_new.append([el5, el6, el4, 0])
                lnodes_new.append([ln_new[1], ln_new[2]])
                lnodes_new.append([ln_new[0], ln_new[2]])
                lnodes_new.append([ln_new[0], ln_new[1]])
                el3.sign = -1
                el1.set_cur_dir(ln_new[0], ln_new[1])
                el2.set_cur_dir(ln_new[0], ln_new[1])
                el3.set_cur_dir(ln_new[0], ln_new[1])
                el4.set_cur_dir(ln_new[1], ln_new[2])
                el5.set_cur_dir(ln_new[2], ln_new[0])
                el6.set_cur_dir(ln_new[2], ln_new[0])

    pass

#=================== УС ========================#
A = np.zeros([2, 2], "f")
B = np.zeros([2, 1], "f")

#======= STEP 1 =======#
print('\n',"STEP1\n")
source_eraser(lel1)
analyze_and_build(lel1,ln1,lnodes1)
if not dont_use_moon: moon(lnodes1,ln1,lel1)
else:
    B[0, 0] = b1
    B[1, 0] = b2
cstr.show_all_el_info(lel1, ln1)
if B_is_zeros == True:
    B[0,0] = 0
    B[1,0] = 0
elif B_is_zeros== False and dont_use_moon == False:
    for i in range(len(lel1)):
        if lel1[i].type == 'kz' or lel1[i].type == 'xx':
            this = lel1[i]
            if this.type == 'kz':
                B[0,0] = this.I_value/this.C_value
            else:
                B[0, 0] = this.U_value / this.L_value
            break

    for i in range(len(lel1)):
        if lel1[i] != this:
            if lel1[i].type == 'kz' or lel1[i].type == 'xx':
                this = lel1[i]
                if this.type == 'kz':
                    B[1, 0] = this.I_value / this.C_value
                else:
                    B[1, 0] = this.U_value / this.L_value
                break
print("\nB:\n", B)
dont_use_moon= B_is_zeros = False
b1=b2=None


#======== STEP 2 ======#
print('\n',"STEP 2\n")
make_source(lel2)
analyze_and_build(lel2,ln2,lnodes2)
#cstr.show_all_el_info(lel2, ln2)
from moon4 import G_own
if not dont_use_moon:
    moon(lnodes2,ln2,lel2)
    source = find_source(lel2)
    if source.type == 'U':
        A[0, 0] = source.sign * (source.I_value / source.C_value)
    elif source.type == 'I':
        A[0, 0] = source.sign * (source.U_value / source.L_value)
    for i in range(len(lel2)):
        if lel2[i].type == 'kz' and lel2[i].number != '1':
            A[1, 0] = lel2[i].sign * (lel2[i].I_value / lel2[i].C_value)
        elif lel2[i].type == 'xx' and lel2[i].number != '1':
            A[1, 0] = lel2[i].sign * (lel2[i].U_value / lel2[i].L_value)
else:
    if b1 != None and b2 != None:
        A[0,0] = b1
        A[1,0] = b2
cstr.show_all_el_info(lel2, ln2)
dont_use_moon= B_is_zeros = False
b1=b2=None

print("\nA:\n", A)
#======== STEP 3 ======#
print('\n',"STEP 3\n")
make_source(lel3)
analyze_and_build(lel3,ln3,lnodes3)
#cstr.show_all_el_info(lel3, ln3)
if not dont_use_moon:
    moon(lnodes3,ln3,lel3)
    source = find_source(lel3)
    if source.type == 'U':
        A[1, 1] = source.sign * (source.I_value / source.C_value)
    elif source.type == 'I':
        A[1, 1] = source.sign * (source.U_value / source.L_value)
    for i in range(len(lel3)):
        if lel3[i].type == 'kz' and lel3[i].number != '1':
            A[0, 1] = lel3[i].sign * (lel3[i].I_value / lel3[i].C_value)
        elif lel3[i].type == 'xx' and lel3[i].number != '1':
            A[0, 1] = lel3[i].sign * (lel3[i].U_value / lel3[i].L_value)
else:
    if b1 != None and b2 != None:
        A[0,1] = b1
        A[1,1] =b2
cstr.show_all_el_info(lel3, ln3)

print("\nA:\n", A)
#======== STEP 4 =======#
#print("\nA:\n",A, "\nB:\n", B)
