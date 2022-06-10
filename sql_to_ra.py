def sql_to_ra(str):

    def format(str):
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
            elif temp[i] == 'X':
                temp[i] = " X "
        final = "".join(temp)
        return final.strip()

    def parts(str):
        str = str[:-1]
        from_ind = str.find('from')
        where_ind = str.find('where')

        if where_ind != -1:
            return str[:from_ind], str[from_ind:where_ind], str[where_ind:]
        else:
            return str[:from_ind], str[from_ind:], ""

    def stringify(list):

        if len(list) == 1:
            return '\nRA Query :\n'+list[0]

        str = '\nSteps :\n'

        for x in list[:-1]:
            str += x
            str += '\n'

        str += '\nRA Query :\n'+list[-1]
        return str

    def solve(str):
        sql = []
        select_clause, from_clause, where_clause = parts(str)

        # print(select_clause,from_clause,where_clause,sep="\n")

        select_clause1 = select_clause.replace('select', 'π')
        sql.append(select_clause+' --> '+select_clause1)

        from_clause1 = from_clause.replace('from', '(')
        from_clause1 = from_clause1.replace(',', ' X ')
        sql.append(from_clause+' --> '+from_clause1+' )')

        where_clause1 = where_clause.replace('where', 'σ')
        where_clause1 = where_clause1.replace('and', '^')
        where_clause1 = where_clause1.replace('or', '∨')

        star = select_clause.find('*')
        if star != -1:
            if where_clause == '':
                return [from_clause1+' )']
            else:
                sql = []
                sql.append(where_clause+' --> '+where_clause1)
                sql.append(where_clause1+from_clause1+')')
        elif where_clause1 == "":
            sql.append(format(select_clause1+from_clause1+')'))
        else:
            sql.append(where_clause+' --> '+where_clause1)
            sql.append(
                format(select_clause1+'('+where_clause1+from_clause1+'))'))
        return sql

    union = str.find('union')

    if union != -1:
        sql1 = solve(str[:union])
        str1 = sql1[-1]
        sql1 = sql1[:-1]

        sql2 = solve(str[union+5:])
        str2 = sql2[-1]
        sql2 = sql2[:-1]

        sql = sql1
        sql.append('union --> U')
        sql += sql2
        sql.append(str1[:-1] + " U "+str2)
        return stringify(sql)
        # return format(solve(str[:union])) + "U " + format(solve(str[union+5:]))

    intersect = str.find('intersect')

    if intersect != -1:
        sql1 = solve(str[:intersect])
        str1 = sql1[-1]
        sql1 = sql1[:-1]

        sql2 = solve(str[intersect+9:])
        str2 = sql2[-1]
        sql2 = sql2[:-1]

        sql = sql1
        sql.append('intersect --> ∩')
        sql += sql2
        sql.append(str1[:-1] + " ∩ "+str2)
        return stringify(sql)
        # return format(solve(str[:intersect])) + "∩ " + format(solve(str[intersect+9:]))

    minus = str.find('minus')

    if minus != -1:
        sql1 = solve(str[:minus])
        str1 = sql1[-1]
        sql1 = sql1[:-1]

        sql2 = solve(str[minus+5:])
        str2 = sql2[-1]
        sql2 = sql2[:-1]

        sql = sql1
        sql.append('minus --> -')
        sql += sql2
        sql.append(str1[:-1] + " - "+format(str2))
        return stringify(sql)
        # return format(solve(str[:minus])) + "- " + format(solve(str[minus+5:]))

    return stringify(solve(str))


print(sql_to_ra('select * from abc;'))
# print(sql_to_ra("select a,b,c from xyz,def where c=3 and a='abc';"))
# print(sql_to_ra("select a,b,c from xyz;"))
# sql_to_ra("select a,b,c from xyz;")
