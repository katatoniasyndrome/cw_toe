
class Element:
    """

    """

    def __init__(self):
        self.type = None
        self.number = None
        self.C_value = None
        self.R_value = None
        self.L_value = None
        self.I_value = None
        self.U_value = None
        self.cur_dir_goes_from = None
        self.cur_dir_goes_to = None

    def show_info(self, list_of_n):
        fromm = ''
        to = ''
        if len(list_of_n) == 4:
            if self.cur_dir_goes_from == list_of_n[0]: fromm = "n1"
            if self.cur_dir_goes_from == list_of_n[1]: fromm = "n2"
            if self.cur_dir_goes_from == list_of_n[2]: fromm = "n3"
            if self.cur_dir_goes_from == list_of_n[3]: fromm = "n4"
            if self.cur_dir_goes_to == list_of_n[0]: to = "n1"
            if self.cur_dir_goes_to == list_of_n[1]: to = "n2"
            if self.cur_dir_goes_to == list_of_n[2]: to = "n3"
            if self.cur_dir_goes_to == list_of_n[3]: to = "n4"
        if len(list_of_n) == 3:
            if self.cur_dir_goes_from == list_of_n[0]: fromm = "n1"
            if self.cur_dir_goes_from == list_of_n[1]: fromm = "n2"
            if self.cur_dir_goes_from == list_of_n[2]: fromm = "n3"
            if self.cur_dir_goes_to == list_of_n[0]: to = "n1"
            if self.cur_dir_goes_to == list_of_n[1]: to = "n2"
            if self.cur_dir_goes_to == list_of_n[2]: to = "n3"
        if len(list_of_n) == 2:
            if self.cur_dir_goes_from == list_of_n[0]: fromm = "n1"
            if self.cur_dir_goes_from == list_of_n[1]: fromm = "n2"
            if self.cur_dir_goes_to == list_of_n[0]: to = "n1"
            if self.cur_dir_goes_to == list_of_n[1]: to = "n2"
        print(str("Элемент " + str(self.type) + str(self.number) + ":"),
              str("I" + str(self.number) + "=" + str(self.I_value)).rjust(9),
              str("U" + str(self.number) + "=" + str(self.U_value)).rjust(9),
              str("R" + str(self.number) + "=" + str(self.R_value)).rjust(9),
              str("L" + str(self.number) + "=" + str(self.L_value)).rjust(9),
              str("C" + str(self.number) + "=" + str(self.C_value)).rjust(9),
              str("from " + fromm + " to " + to).rjust(9))

    def count_U_value(self):
        if self.R_value != 0 and self.R_value != float('inf'):  # если R элемент
            self.U_value = self.I_value * self.R_value
        elif self.U_value is None or self.U_value == 0:  # если не R элемент
            # (self.cur_dir_goes_from[-1], self.cur_dir_goes_to[-1])
            self.U_value = self.cur_dir_goes_from[-1] - self.cur_dir_goes_to[-1]

    def count_I_value(self):
        if self.R_value != 0:
            self.I_value = self.U_value / self.R_value

    def count_R_value(self):
        if self.I_value != 0:
            self.R_value = self.U_value / self.I_value

    def set_R_elem(self, R_val):
        self.type = 'R'
        self.I_value = None
        self.U_value = None
        self.R_value = R_val
        self.L_value = 0
        self.C_value = 0

    def set_L_elem(self, L_val):
        self.type = 'L'
        self.I_value = None
        self.U_value = None
        self.R_value = 0
        self.L_value = L_val
        self.C_value = 0

    def set_C_elem(self, C_val):
        self.type = 'C'
        self.I_value = None
        self.U_value = None
        self.R_value = 0
        self.L_value = 0
        self.C_value = C_val

    def set_I_elem(self, I_val):
        self.type = 'I'
        self.I_value = I_val
        self.U_value = None
        self.R_value = 0
        self.L_value = 0
        self.C_value = 0

    def set_U_elem(self, U_val):
        self.type = 'U'
        self.I_value = None
        self.U_value = U_val
        self.R_value = 0
        self.L_value = 0
        self.C_value = 0

    def set_xx_elem(self):
        self.type = 'xx'
        self.I_value = 0
        self.U_value = None
        self.R_value = float('Inf')
        self.L_value = 0
        self.C_value = 0

    def set_kz_elem(self):
        self.type = 'kz'
        self.I_value = None
        self.U_value = 0
        self.R_value = 0
        self.L_value = 0
        self.C_value = 0

    def set_cur_dir(self, from1, to1):
        self.cur_dir_goes_from = from1
        self.cur_dir_goes_to = to1

    def set_number_element(self, number):
        self.number = number

    pass


# ======================= Ввод цепи ======================= #
el1 = Element()
el2 = Element()
el3 = Element()
el4 = Element()
el5 = Element()
el6 = Element()

circuit_type = input("Тип цепи(А или B): ")
if circuit_type == 'A':
    el1.has_parallel = el2
    el2.has_parallel = el1
    list_of_elements = [el1, el2, el3, el4, el5, el6]
    Uvalue1 = 0
    Uvalue2 = 0
    Uvalue3 = 0
    Uvalue4 = 0
    n1 = [el1, el2, el4, el6, Uvalue1]  # = c1.node_el_connection[0]
    n2 = [el1, el2, el3, Uvalue2]  # = c1.node_el_connection[1]
    n3 = [el3, el4, el5, Uvalue3]  # = c1.node_el_connection[2]
    n4 = [el5, el6, Uvalue4]  # = c1.node_el_connection[3]
    list_of_n = [n1, n2, n3, n4]
    # список связей узлов
    node1 = [n2, n3, n4]
    node2 = [n3, n1]
    node3 = [n1, n2, n4]
    node4 = [n1, n3]
    list_of_nodes = [node1, node2, node3, node4]

    # el1 это ИТ
    el1.set_I_elem(1.0)
    el1.set_number_element('1')
    el1.set_cur_dir(n1, n2)

    # el6 это R нагрузки
    el6.set_R_elem(1.0)
    el6.set_number_element('6')
    el6.set_cur_dir(n4, n1)

    el2.set_number_element('2')
    el2.set_cur_dir(n2, n1)
    el_type = input("Введите тип элемента1 (R, L, C): ")
    el_val = float(input("Введите значение данного элемента: "))
    if el_type == 'R':
        el2.set_R_elem(el_val)
    elif el_type == 'L':
        el2.set_L_elem(el_val)
    elif el_type == 'C':
        el2.set_C_elem(el_val)

    el3.set_number_element('3')
    el3.set_cur_dir(n2, n3)
    el_type = input("Введите тип элемента2 (R, L, C): ")
    el_val = float(input("Введите значение данного элемента: "))
    if el_type == 'R':
        el3.set_R_elem(el_val)
    elif el_type == 'L':
        el3.set_L_elem(el_val)
    elif el_type == 'C':
        el3.set_C_elem(el_val)

    el4.set_number_element('4')
    el4.set_cur_dir(n3, n1)
    el_type = input("Введите тип элемента3 (R, L, C): ")
    el_val = float(input("Введите значение данного элемента: "))
    if el_type == 'R':
        el4.set_R_elem(el_val)
    elif el_type == 'L':
        el4.set_L_elem(el_val)
    elif el_type == 'C':
        el4.set_C_elem(el_val)

    el5.set_number_element('5')
    el5.set_cur_dir(n3, n4)
    el_type = input("Введите тип элемента4 (R, L, C): ")
    el_val = float(input("Введите значение данного элемента: "))
    if el_type == 'R':
        el5.set_R_elem(el_val)
    elif el_type == 'L':
        el5.set_L_elem(el_val)
    elif el_type == 'C':
        el5.set_C_elem(el_val)

else:
    el5.has_parallel = el6
    el6.has_parallel = el5
    list_of_elements = [el1, el2, el3, el4, el5, el6]
    Uvalue1 = 0
    Uvalue2 = 0
    Uvalue3 = 0
    Uvalue4 = 0
    n1 = [el1, el2, Uvalue1]  # = c1.node_el_connection[0]
    n2 = [el1, el3, el5, el6, Uvalue2]  # = c1.node_el_connection[1]
    n3 = [el2, el3, el4, Uvalue3]  # = c1.node_el_connection[2]
    n4 = [el4, el5, el6, Uvalue4]  # = c1.node_el_connection[3]
    list_of_n = [n1, n2, n3, n4]
    # список связей узлов
    node1 = [n3, n2]
    node2 = [n1, n3, n4]
    node3 = [n1, n2, n4]
    node4 = [n2, n3]
    list_of_nodes = [node1, node2, node3, node4]

    el1.set_U_elem(1.0)
    el1.set_number_element('1')
    el1.set_cur_dir(n2, n1)

    el6.set_R_elem(1.0)
    el6.set_number_element('6')
    el6.set_cur_dir(n4, n2)

    el2.set_number_element('2')
    el2.set_cur_dir(n1, n3)
    el_type = input("Введите тип элемента1 (R, L, C): ")
    el_val = float(input("Введите значение данного элемента: "))
    if el_type == 'R':
        el2.set_R_elem(el_val)
    elif el_type == 'L':
        el2.set_L_elem(el_val)
    elif el_type == 'C':
        el2.set_C_elem(el_val)

    el3.set_number_element('3')
    el3.set_cur_dir(n3, n2)
    el_type = input("Введите тип элемента2 (R, L, C): ")
    el_val = float(input("Введите значение данного элемента: "))
    if el_type == 'R':
        el3.set_R_elem(el_val)
    elif el_type == 'L':
        el3.set_L_elem(el_val)
    elif el_type == 'C':
        el3.set_C_elem(el_val)

    el4.set_number_element('4')
    el4.set_cur_dir(n3, n4)
    el_type = input("Введите тип элемента3 (R, L, C): ")
    el_val = float(input("Введите значение данного элемента: "))
    if el_type == 'R':
        el4.set_R_elem(el_val)
    elif el_type == 'L':
        el4.set_L_elem(el_val)
    elif el_type == 'C':
        el4.set_C_elem(el_val)

    el5.set_number_element('5')
    el5.set_cur_dir(n4, n2)
    el_type = input("Введите тип элемента4 (R, L, C): ")
    el_val = float(input("Введите значение данного элемента: "))
    if el_type == 'R':
        el5.set_R_elem(el_val)
    elif el_type == 'L':
        el5.set_L_elem(el_val)
    elif el_type == 'C':
        el5.set_C_elem(el_val)

'''
# =================== Иниц-я элементов тип А =============================#

el1.number = '1'
el1.type = 'xx'
el1.I_value = 0#1
el1.U_value = None
el1.R_value = float('Inf') # 0
el1.L_value = 0
el1.C_value = 0
el1.cur_dir_goes_from = n1
el1.cur_dir_goes_to = n2

el2.number = '2'
el2.type = 'xx'#'I'
el2.I_value = 0#None
el2.U_value = None
el2.R_value = float('Inf')
el2.L_value = 1
el2.C_value = 0
el2.cur_dir_goes_from = n2
el2.cur_dir_goes_to = n1

el3.number = '3'
el3.type = 'kz'
el3.I_value = 0
el3.U_value = None
el3.R_value = 1
el3.L_value = 0
el3.C_value = 0
el3.cur_dir_goes_from = n2
el3.cur_dir_goes_to = n3

el4.number = '4'
el4.type = 'I'
el4.I_value = 1
el4.U_value = None
el4.R_value = 0#float('Inf')
el4.L_value = 2
el4.C_value = 0
el4.cur_dir_goes_from = n3
el4.cur_dir_goes_to = n1

el5.number = '5'
el5.type = 'R'
el5.I_value = None
el5.U_value = None
el5.R_value = 2
el5.L_value = 0
el5.C_value = 0
el5.cur_dir_goes_from = n3
el5.cur_dir_goes_to = n4

el6.number = '6'
el6.type = 'R'
el6.I_value = None
el6.U_value = None
el6.R_value = 1
el6.L_value = 0
el6.C_value = 0
el6.cur_dir_goes_from = n4
el6.cur_dir_goes_to = n1

# ===================== 3 узла===================#
el1.number = '1'
el1.type = 'xx'
el1.I_value = 0  # 1
el1.U_value = None
el1.R_value = float('Inf')  # 0
el1.L_value = 0
el1.C_value = 0
el1.cur_dir_goes_from = n1
el1.cur_dir_goes_to = n2

el2.number = '2'
el2.type = 'xx'  # 'I'
el2.I_value = 0  # None
el2.U_value = None
el2.R_value = float('Inf')
el2.L_value = 1
el2.C_value = 0
el2.cur_dir_goes_from = n2
el2.cur_dir_goes_to = n1

el3.number = '3'
el3.type = 'kz'
el3.I_value = 0
el3.U_value = None
el3.R_value = 1
el3.L_value = 0
el3.C_value = 0
el3.cur_dir_goes_from = n2
el3.cur_dir_goes_to = n3

el4.number = '4'
el4.type = 'I'
el4.I_value = 1
el4.U_value = None
el4.R_value = 0  # float('Inf')
el4.L_value = 2
el4.C_value = 0
el4.cur_dir_goes_from = n2
el4.cur_dir_goes_to = n1

el5.number = '5'
el5.type = 'R'
el5.I_value = None
el5.U_value = None
el5.R_value = 2
el5.L_value = 0
el5.C_value = 0
el5.cur_dir_goes_from = n3
el5.cur_dir_goes_to = n2

el6.number = '6'
el6.type = 'R'
el6.I_value = None
el6.U_value = None
el6.R_value = 1
el6.L_value = 0
el6.C_value = 0
el6.cur_dir_goes_from = n1
el6.cur_dir_goes_to = n3

# =================== Иниц-я цепи тип В ============================#

e1 = Element()
e2 = Element()
e3 = Element()
e4 = Element()
e5 = Element()
e6 = Element()
list_of_elements2 = [e1, e2, e3, e4, e5, e6]
# Uvalue1=0
# Uvalue2=0
# Uvalue3=0
# Uvalue4=0
# m1 = [e1, e3, e5, e6, Uvalue1]  # = c1.node_el_connection[0]
# m2 = [e1, e2, Uvalue2]  # = c1.node_el_connection[1]
# m3 = [e2, e3, e4, Uvalue3]  # = c1.node_el_connection[2]
# m4 = [e4, e5, e6, Uvalue4]  # = c1.node_el_connection[3]
# list_of_n2 = [m1, m2, m3, m4]
# список связей узлов
# nod1 = [m2, m3, m4]
# nod2 = [m3, m1]
# nod3 = [m1, m2, m4]
# nod4 = [m1, m3]
# list_of_nodes2 = [nod1, nod2, nod3, nod4]
# print(n2 in node2)
# ============== для мун 2 узла ==================#
Uvalue1 = 0
Uvalue2 = 0
m1 = [e1, e2, e3, e4, e5, e6, Uvalue1]
m2 = [e1, e2, e3, e4, e5, e6, Uvalue2]
list_of_n2 = [m1, m2]
# список связей узлов
nod1 = [m2]
nod2 = [m1]
list_of_nodes2 = [nod1, nod2]
# =================== Иниц-я элементов тип В =============================#

e1.number = '1'
e1.type = 'U'
e1.I_value = None
e1.U_value = 1
e1.R_value = 0
e1.L_value = 0
e1.C_value = 0
e1.cur_dir_goes_from = m2
e1.cur_dir_goes_to = m1

e2.number = '2'
e2.type = 'kz'  # 'C'
e2.I_value = None
e2.U_value = 0
e2.R_value = 0
e2.L_value = 0  # 1
e2.C_value = 4
e2.cur_dir_goes_from = m1
e2.cur_dir_goes_to = m2

e3.number = '3'
e3.type = 'R'
e3.I_value = None
e3.U_value = None
e3.R_value = 1
e3.L_value = 0
e3.C_value = 0
e3.cur_dir_goes_from = m1
e3.cur_dir_goes_to = m2

e4.number = '4'
e4.type = 'kz'  # 'C'
e4.I_value = None
e4.U_value = 0
e4.R_value = 0
e4.L_value = 0
e4.C_value = 1
e4.cur_dir_goes_from = m1
e4.cur_dir_goes_to = m2

e5.number = '5'
e5.type = 'R'
e5.I_value = None
e5.U_value = None
e5.R_value = 0.5
e5.L_value = 0
e5.C_value = 0
e5.cur_dir_goes_from = m1
e5.cur_dir_goes_to = m2

e6.number = '6'
e6.type = 'R'
e6.I_value = None
e6.U_value = None
e6.R_value = 1
e6.L_value = 0
e6.C_value = 0
e6.cur_dir_goes_from = m1
e6.cur_dir_goes_to = m2




# =================     ====================================#

'''


def show_all_el_info(list_of_el, ln):
    for i in range(len(list_of_el)):
        list_of_el[i].show_info(ln)


def find_all_U(list_of_el):
    for i in range(len(list_of_el)):
        list_of_el[i].count_U_value()

show_all_el_info(list_of_elements, list_of_n)

def show_elements_in_n(ln, lel):

    for i in range(len(ln)):
        s1 = "\nn" + str(i+1) + ' '

        for j in range(len(ln[i])-1):
            if ln[i][j] in lel:
                s1 = s1+ str(ln[i][j].type) + str(ln[i][j].number) + ' '
        print(s1)