ss = []
add_flag = 0
PB_SIZE = 10
PB = [] * PB_SIZE
PB_counter = 0
whiles = []
address = 10000
#TODO remove symbol table after merge
symbol_table = []

def gettemp():
    global address
    address += 32
    return address - 32


def findaddr(input):
    pass

def top(stack):
    return len(stack) - 1

def convertToStr(func, par1='', par2='', par3=''):
    return '(' + func + ', ' + str(par1) + ', ' + str(par2) + ', ' + str(par3) + ')'

def code_generation(action, input):
    global PB_counter
    global address
    global scope
    if action == "#PUSH_SS":
        ss.append(input)

    elif action == "#ADDSUB":
        t = gettemp()
        if ss[top(ss) - 1] == "+":
            PB[PB_counter] = (ADD, ss[top(ss)], ss[top(ss) - 1], t)
        elif ss[top(ss) - 1] == "-":
            PB[PB_counter] = (SUB, ss[top(ss)], ss[top(ss) - 1], t)
        PB_counter += 1
        for i in range(3):
            ss.pop()
        ss.append(t)
        return
    elif action == "MULT":
        t = gettemp()
        PB[PB_counter] = (MULT, ss[top(ss)], ss[top(ss) - 1], t)
        PB_counter += 1
        ss.pop()
        ss.pop()
        ss.append(t)
        return
    elif action == "#FUN_ADDR":
        fun_id = ss.pop()
        fun_dict = symbol_table[fun_id].values()[0]
        fun_dict['addr'] = PB_counter
        fun_dict['params'] = []
        fun_dict['params_count'] = 0
        fun_dict['ret_addr'] = address
        ss.append(fun_dict['ret_addr'])
        address+= 32
        fun_dict['ret_val'] = address
        address += 32
        PB_counter += 1
        ss.append(fun_id)
        return
    elif action == "#VAR_ADDR":
        var_dict = symbol_table[ss.pop()].values()[0]
        var_dict['addr'] = address
        address += 32
        return
    elif action == "#ARR_ADDR":
        arr_dict = symbol_table[ss.pop()].values()[0]
        arr_dict['addr'] = address
        address += 32
        PB[PB_counter] = '(ASSIGN, #' + str(address) + ',' + str(arr_dict['addr']) + ', )'
        PB_counter += 1
        address += 32 * input
        return
    elif action == "#INC_SCOPE":
        scope +=1
        return
    elif action == "#PAR_ADDR":
        param_dict = symbol_table[input].values()[0]
        param_dict['addr'] = address
        fun_dict = symbol_table[ss[top(ss)]].values()[0]
        fun_dict['params_count'] += 1
        fun_dict['params'].append(address)
        address += 32
        return
    elif action == "#DEC_SCOPE":
        scope -= 1
        return
    elif action == "#ASSIGN_RET":
        fun_dict = symbol_table[ss[top(ss) - 1]].values()[0]
        PB[PB_counter] = '(ASSIGN, #' + str(ss.pop()) + ',' + str(fun_dict['ret_val']) + ', )'
        PB_counter += 1
        return
    elif action == "#JMP_CALLER":
        fun_dict = symbol_table[ss[top(ss)]].values()[0]
        PB[PB_counter] = '(JP, ' + str(fun_dict['ret_addr']) + ', , )'
        return
    elif action == "#POP_SS":
        ss.pop()
        return
    elif action == "#SAVE":
        ss.append(PB_counter)
        PB_counter += 1
        return
    elif action == "#LABEL":
        ss.append(PB_counter)
        return
    elif action == "#SAVE_CONTINUE":
        whiles.append(([PB_counter], []))
        return
    elif action == "#WHILE":
        PB[ss[top(ss)]] = (JPF, ss[top(ss) - 1], PB_counter + 1, )
        PB[PB_counter] = (JP, ss[top(ss) - 2], ,)
        PB_counter += 1
        last_loop_breaks = whiles[-1][1]
        for i in last_loop_breaks:
            PB[i] = (JP, PB_counter, ,)
        whiles.pop()
        for i in range(3):
            ss.pop()
        return
    elif action == "#JMP_BEGIN":
        # PB[PB_counter] = (JP, ss.get(ss.top))
        PB[PB_counter] = (JP, whiles[-1][0][-1])
        PB_counter += 1
        return
    elif action == "#JMP_END":
        whiles[-1][1].append(PB_counter)
        PB_counter += 1
        return
    elif action == "#JPF_SAVE":
        PB[ss[top(ss)]] = (JPF, ss[top(ss)-1], PB_counter+1)
        ss.pop()
        ss.pop()
        ss.append(PB_counter)
        PB_counter += 1
        return
    elif action == "#JP":
        PB[ss[top(ss)]] = (JP, PB_counter, ,)
        ss.pop()
        return
    elif action == "#JPT_SAVE":
        pass
    elif action == "#COMPARE_CASE":
        t = gettemp()
        PB[PB_counter] = (EQ, int(input), ss[top(ss) - 1], t)
        PB_counter += 1
        ss.append(t)
        return
    elif action == "#JPF":
        PB[ss[top(ss)]] = JPF(ss[top(ss) - 1], PB_counter, ,)
        ss.pop()
        ss.pop()
        return
    elif action == "#PUSH_INPUT":
        ss.append(input)
        return
    elif action == "#RELOP":
        t = gettemp()
        if ss[top(ss) - 1] == "<":
            PB[PB_counter] = (LT, ss[top(ss) - 2], ss[top(ss)], t)
        elif ss[top(ss) - 1] == "==":
            PB[PB_counter] = (EQ, ss[top(ss) - 2], ss[top(ss)], t)
        PB_counter += 1
        for i in range(3):
            ss.pop()
        ss.append(t)
        return
    elif action == "#RET_ADDR":
        fun_dict = symbol_table[ss.pop()].values()[0]
        fun_dict['ret_addr'] = PB_counter
        return
    elif action == "#JP_CALL":
        ss.pop()
        fun_dict = symbol_table[ss[top(ss)]].values()[0]
        PB.append(convertToStr("JP", fun_dict['addr']))
        PB_counter += 1
        return
    elif action == "#PARAM_CNT":
        fun_dict = symbol_table[ss[top(ss)]].values()[0]
        ss.append(fun_dict["params_count"])
        return
    elif action == "#ASS_ARG":
        fun_dict = symbol_table[ss[top(ss) - 2]].values()[0]
        param_num = fun_dict["params_count"] - ss[top(ss) -1]
        PB.append(convertToStr("ASSIGN", ss.pop(), fun_dict["params"][param_num]))
        PB_counter += 1
        ss.append(ss.pop() - 1)
        return
    elif action == "#ARR_READ":
        arr_dict = symbol_table[ss[top(ss) - 1]].values()[0]
        t1 = gettemp()
        PB.append(convertToStr("ADD", arr_dict["addr"], ss.pop(), t1))
        PB_counter += 1
        t2 = gettemp()
        PB.append(convertToStr("ASSIGN", str('@') + str(t1), t2))
        PB_counter += 1
        ss.pop()
        ss.append(t2)
        return
    elif action == "#PUSH_NUM":
        t1 = gettemp()
        PB.append(convertToStr("ASSIGN", '#' + str(input), t1))
        PB_counter += 1
        ss.append(t1)
        return