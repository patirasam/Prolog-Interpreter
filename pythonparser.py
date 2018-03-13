


def var_check(body):
    c_var = False
    var_p = []

    for word in body:
        if word[0].isupper():
            c_var = True
            var_p.append(True)
        else:
            var_p.append(False)

    return c_var,var_p


def unify_relation(db_rl, db_rul, name, body):
    if len(body) != len(db_rl[name][0]):
        return "Error: Number of arguments incorrect"

    c_var, var_p = var_check(body)
    matches = []

    if c_var:

        for relation in db_rl[name]:
            match = True
            for pos, var, rel in zip(var_p, body, relation):
                if pos:
                    continue
                elif var == rel:
                    continue
                else:
                    match = False
            if match:
                matches.append(relation)

        return (name, matches)

    if body in db_rl[name]:
        return "yes"
    return "no"


def unify_rule(db_rl, db_rul, name, body):

    local_env = dict(zip(db_rul[name]["vars"], body))

    for rel in db_rul[name]["body"]:
        rel = list(rel)
        rel[1] = rel[1]

        for i, v in enumerate(rel[1]):
            if v in local_env:
                rel[1][i] = local_env[v]
            elif v[0].isupper:
                print("INTERMEDIATE VARIABLE")

        ans = unify_prolog(db_rl, db_rul, rel[0], rel[1])

        if ans == "no":
            return ans
        else:
            continue

    return "yes"


def unify_prolog(db_rl, db_rul, name, body):
    matches = []

    if name in db_rl:
        return unify_relation(db_rl, db_rul, name, body)

    elif name in db_rul:
        return unify_rule(db_rl, db_rul, name, body)

    else:
        return "Error: {} not found in environment.".format(name)




def env_setup():
    db_rl = {}
    db_rul = {}

    return db_rl, db_rul




def parse_imp(astr):
    res_prolog={}
    if astr == '#store':
        res_prolog["res_prolog"]="store"
    elif astr == '#stop':
        res_prolog["res_prolog"]="stop"
    elif(astr[-1]=='.'):
        if(astr.find(":-")!=-1):
            res_prolog["res_prolog"]="rule"
            pRULEName=''
            pRULEName = astr[:astr.find("(")]
            temp = astr[astr.find("(") + 1:astr.find(")")]
            temp2 = temp.split(",")
            pGroup = (temp2)
            decl1 = (pRULEName, pGroup)
            decl2 = ":-"
            rule_cond=astr[astr.find(":-")+2:-1]

            # regex=r"([a-zA-Z])+\(([a-zA-Z]+\,*)+\)"
            #rule_cond_list=re.split(regex,rule_cond)

            rule_cond_list = rule_cond.split("),")
            if len(rule_cond_list) > 1:
                for i in range(0,len(rule_cond_list)-1):
                    rule_cond_list[i]=rule_cond_list[i]+")"

            count=len(rule_cond_list)
            rule_cond_list_pases=[]
            for i in range(0,count):
                condname=rule_cond_list[i][:rule_cond_list[i].find("(")]
                convar=rule_cond_list[i][rule_cond_list[i].find("(")+1:rule_cond_list[i].find(")")]
                convars=convar.split(",")
                prulegroup=(convars)
                declrule=(condname,prulegroup)
                rule_cond_list_pases.append(declrule)

            decl3=(rule_cond_list_pases)
            decl4=[]
            decl4.append(decl1)
            decl4.append(decl2)
            decl4.append(decl3)
            decl4.append(".")

            decl5=(decl4)
            res_prolog["rule"]=decl5
        else:
            res_prolog["res_prolog"]="fact"
            pName = astr[:astr.find("(")]
            temp = astr[astr.find("(") + 1:astr.find(")")]
            temp2 = temp.split(",")
            pGroup = (temp2)
            decl1 = (pName, pGroup)
            res_prolog['decl'] = decl1

    elif(astr[-1]=='?'):
        pName = astr[:astr.find("(")]
        temp = astr[astr.find("(") + 1:astr.find(")")]
        temp2 = temp.split(",")
        pGroup = (temp2)
        decl1 = (pName, pGroup)
        res_prolog['stmt'] = decl1
        res_prolog["res_prolog"]="query"
    return res_prolog


def prolog():

    print("Prolog Interpreter")
    print("#store for database")
    print("#stop to quit")
    db_rl, db_rul = env_setup()

    while True:
        inp = input(">>>> ")

        try:
            res_prolog = parse_imp(inp)
            print res_prolog
            if res_prolog["res_prolog"] == "query":
                head, body = res_prolog["stmt"]
                v = unify_prolog(db_rl, db_rul, head, body)

                if v == "yes" or v == "no" or v[0:5] == "Error":
                    print(v)
                else:
                    for i in v[1]:
                        print("{}{}.".format(v[0], tuple(i)))

            elif res_prolog["res_prolog"] == "stop":
                return

            elif res_prolog["res_prolog"] == "store":
                print("db_rl:")
                print(db_rl)
                print("db_rul:")
                print(db_rul)

            elif res_prolog["res_prolog"] == "rule":
                res = res_prolog["rule"]
                res = (res[0], res[2])
                db_rul[res[0][0]] = {"vars": res[0][1],"body": res[1]}
                print("Rule {} defined".format(res[0][0]))

            elif res_prolog["res_prolog"] == "fact":

                (name, constants) = res_prolog["decl"]
                c_var = False
                for constant in constants:
                    if constant[0].isupper():
                        c_var = True
                        break

                if c_var:
                    print("Error: Can't define a fact with a variable!")
                elif name in db_rl:
                    if len(constants) != len(db_rl[name][0]):
                        print("Error: Fact {} takes {} argument(s), {} given.".format(name,len(db_rl[name][0]),len(constants)))
                    else:
                        db_rl[name].append(constants)
                else:
                    db_rl[name] = [constants]
                    print("Fact {} defined".format(name))

        except Exception as e:
            print("Exception: {}".format(e))


if __name__ == '__main__':
    prolog()


