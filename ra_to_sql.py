def ra_to_sql(str):

    def format(str):

        while True:
            if str[0] == '(':
                str = str.lstrip('(')
                str = str.rstrip(')')
            else:
                break

        str = str.replace(" ", "")
        temp = [ch for ch in str]
        for i in range(len(temp)):
            if temp[i] == '(':
                temp[i] = " ( "
            elif temp[i] == ')':
                temp[i] = " ) "
            elif temp[i] == 'σ':
                temp[i] = "σ "
            elif temp[i] == 'π':
                temp[i] = "π "
        final = "".join(temp)
        return final.strip()

    def columns(str):
        list = str.split(' ')
        return list[1]

    def conditions(str):
        list = str.split(' ')

        if list[3] != 'σ':
            return ""

        temp = [ch for ch in list[4]]

        for i in range(len(temp)):
            if temp[i] == '^':
                temp[i] = " and "
            if temp[i] == '∨':
                temp[i] = " or "

        final = "".join(temp)
        return final

    def tables(str):
        list = str.split(' ')

        if len(list) == 1:
            return list[0]
        elif list[3] == 'σ':
            temp = [ch for ch in list[6]]
        else:
            temp = [ch for ch in list[3]]

        for i in range(len(temp)):
            if temp[i] == 'X':
                temp[i] = ","

        final = "".join(temp)
        return final

    def stringify(list):

        if len(list) == 1:
            return '\nSQL Query :\n'+list[0]

        str = '\nSteps :\n'

        for x in list[:-1]:
            str += x
            str += '\n'

        str += '\nSQL Query :\n'+list[-1]
        return str

    def solve(str):

        str = format(str)
        # print(format(str))
        table = tables(str)

        # select * from table' --> query
        pi = str.find('π')
        sigma = str.find('σ')

        if pi == -1:
            if sigma == -1:
                # sqlcmd = "select"+col+" from "+table+";"
                return ["select * from "+table+";"]
            else:
                list = str.split(' ')

                temp = [ch for ch in list[1]]

                for i in range(len(temp)):
                    if temp[i] == '^':
                        temp[i] = " and "
                    if temp[i] == '∨':
                        temp[i] = " or "

                final = "".join(temp)

                sql = []
                sql.append('σ '+list[1]+' --> '+'where '+final)
                sql.append('select * from '+table+' where '+final+';')
                # sqlcmd = "select * from "+table+";"
                return sql

        col = columns(str)
        cond = conditions(str)

        if cond:
            sql = []
            list = str.split(' ')

            sql.append('π '+list[1]+' --> select '+col)
            sql.append('σ '+list[4]+' --> where '+cond)
            sql.append(list[6]+' --> from '+table)
            sql.append("select "+col+" from "+table+" where "+cond+";")
            # sqlcmd = "select "+col+" from "+table+" where "+cond+";"

            return sql

        else:
            sql = []
            list = str.split(' ')

            sql.append('π '+list[1]+' --> select '+col)
            sql.append(list[3]+' --> from '+table)
            sql.append("select "+col+" from "+table+";")
            # sqlcmd = "select"+col+" from "+table+";"

            return sql

    union = str.find('U')

    if union != -1:
        sql1 = solve(str[:union])
        str1 = sql1[-1]
        sql1 = sql1[:-1]

        sql2 = solve(str[union+1:])
        str2 = sql2[-1]
        sql2 = sql2[:-1]

        sql = sql1
        sql.append('U --> union')
        sql += sql2
        sql.append(str1[:-1] + " union "+str2)
        return stringify(sql)

    intersect = str.find('∩')

    if intersect != -1:
        sql1 = solve(str[:intersect])
        str1 = sql1[-1]
        sql1 = sql1[:-1]

        sql2 = solve(str[intersect+1:])
        str2 = sql2[-1]
        sql2 = sql2[:-1]

        sql = sql1
        sql.append('∩ --> intersect')
        sql += sql2
        sql.append(str1[:-1] + " intersect "+str2)
        return stringify(sql)

    minus = str.find('-')

    if minus != -1:
        sql1 = solve(str[:minus])
        str1 = sql1[-1]
        sql1 = sql1[:-1]

        sql2 = solve(str[minus+1:])
        str2 = sql2[-1]
        sql2 = sql2[:-1]

        sql = sql1
        sql.append('- --> minus')
        sql += sql2
        sql.append(str1[:-1] + " minus "+str2)
        return stringify(sql)

    rev_output = stringify(solve(str))[::-1]
    sqlcmd = ''
    check = 0
    for i in rev_output:
        if(i == '\n' and check == 1):
            break
        check = 1
        sqlcmd += i
    sqlcmd = sqlcmd[::-1]
    return stringify(solve(str)), sqlcmd


# ans=ra_to_sql("π a,b,c(σ a='xyz' ^ b=12 (table1Xtable2))")
# ans=ra_to_sql("π a,b,c(σ a='xyz' ^ b=12 (table1)) U π c (table2)")
# ans=ra_to_sql("(table1)")
# ans=ra_to_sql('σ a="xyz"(abc)')
print(ra_to_sql("π a, b(aru)"))

# print(ans)
