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
    pass


def findaddr(input):
    pass

def top(stack):
    return len(stack) - 1

def code_generation(action, input):
    global PB_counter
    global address
    global scope
    if action == "#PUSH_SS":
        ss.append(input)

    elif action == "#ADDSUB":
        t = gettemp()
        if ss.get(ss.top - 1) == "+":
            PB[PB_counter] = (ADD, ss.get(ss.top), ss.get(ss.top - 1), t)
        elif ss.get(ss.top - 1) == "-":
            PB[PB_counter] = (SUB, ss.get(ss.top), ss.get(ss.top - 1), t)
        PB_counter += 1
        ss.pop(3)
        ss.push(t)
        return
    elif action == "MULT":
        t = gettemp()
        PB[PB_counter] = (MULT, ss.get(ss.top), ss.get(ss.top - 1), t)
        PB_counter += 1
        ss.pop(2)
        ss.push(t)
        return
    elif action == "#FUN_ADDR":
        fun_id = ss.pop()
        fun_dict = symbol_table[fun_id]
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
        var_dict = symbol_table[ss.pop()]
        var_dict['addr'] = address
        address += 32
        return
    elif action == "#ARR_ADDR":
        arr_dict = symbol_table[ss.pop()]
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
        param_dict = symbol_table[input]
        param_dict['addr'] = address
        fun_dict = symbol_table[ss[top(ss)]]
        fun_dict['params_count'] += 1
        fun_dict['params'].append(address)
        address += 32
        return
    elif action == "#DEC_SCOPE":
        scope -= 1
        return
    elif action == "#ASSIGN_RET":
        fun_dict = symbol_table[ss[top(ss) - 1]]
        PB[PB_counter] = '(ASSIGN, #' + str(ss.pop()) + ',' + str(fun_dict['ret_val']) + ', )'
        PB_counter += 1
        return
    elif action == "#JMP_CALLER":
        fun_dict = symbol_table[ss[top(ss)]]
        PB[PB_counter] = '(JP, ' + str(fun_dict['ret_addr']) + ', , )'
        return
    elif action == "#POP_SS":
        ss.pop()
        return
    elif action == "#SAVE":
        ss.push(PB_counter)
        PB_counter += 1
        return
    elif action == "#LABEL":
        ss.push(PB_counter)
        return
    elif action == "#SAVE_CONTINUE":
        whiles.append(([PB_counter], []))
        return
    elif action == "#WHILE":
        PB[ss.get(ss.top)] = (JPF, ss.get(ss.top - 1), PB_counter + 1, )
        PB[PB_counter] = (JP, ss.get(ss.top - 2), ,)
        PB_counter += 1
        last_loop_breaks = whiles[-1][1]
        for i in last_loop_breaks:
            PB[i] = (JP, PB_counter, ,)
        whiles.pop()
        ss.pop(3)
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
        PB[ss.get(ss.top)] = (JPF, ss.get(ss.top-1), PB_counter+1)
        ss.pop(2)
        ss.push(PB_counter)
        PB_counter += 1
        return
    elif action == "#JP":
        PB[ss.get(ss.top)] = (JP, PB_counter, ,)
        ss.pop()
        return
    elif action == "#JPT_SAVE":
        pass
    elif action == "#COMPARE_CASE":
        t = gettemp()
        PB[PB_counter] = (EQ, int(input), ss.get(ss.top - 1), t)
        PB_counter += 1
        ss.push(t)
        return
    elif action == "#JPF":
        PB[ss.get(ss.top)] = JPF(ss.get(ss.top - 1), PB_counter, ,)
        ss.pop(2)
        return
    elif action == "#PUSH_INPUT":
        ss.push(input)
        return
    elif action == "#RELOP":
        t = gettemp()
        if ss.get(ss.top - 1) == "<":
            PB[PB_counter] = (LT, ss.get(ss.top - 2), ss.get(ss.top), t)
        elif ss.get(ss.top - 1) == "==":
            PB[PB_counter] = (EQ, ss.get(ss.top - 2), ss.get(ss.top), t)
        PB_counter += 1
        ss.pop(3)
        ss.push(t)
        return
    elif action == "#RET_ADDR":
        pass
    elif action == "#JP_CALL":
        pass
    elif action == "#ASS_ARG":
        pass