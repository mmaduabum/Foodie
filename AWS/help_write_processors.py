USERS: user_id, user_medium, default_switch_id
SWITCHES: switch_id, state
SWITCH_USER_MAP: switch_id, user_id, name, sub_tmstmp_exp, sub_bool





def process_follow(cmd_dic, platform):
    args = cmd_dic[c.ARGS]
    
    //if 1 arg: follow that arg switch ( check if its valid) , and if its mapped to user
    
    
    check = "select * from maps where "

def process_unfollow(cmd_dic, platform):
    args = cmd_dic[c.ARGS]
    if len(args) == 0:

    else:
	switch = args[0]
	
    pass

def process_add(cmd_dic, platform):
    args = cmd_dic[c.ARGS]
    if len(args) == 0:
       //ERROR
    else:
	switch = args[0]
    	check = "select * from switches where switch_id == " + switch + ";"
	a = cursor.execute(check)
	data = a.fetchall()
        if len(data) > 0:
            c.execute("INSERT INTO map (switch_id,"+switch+","+"null,null){idf}, {cn}) VALUES('some_id1', DATE('now'))"\
         .format(tn=table_name, idf=id_field, cn=date_col))
    connection.close()
    cursor.close()

def process_remove(cmd_dic, platform):
    pass

def process_status(cmd_dic, platform):
    pass

def process_list(cmd_dic, platform):
    pass

def process_setname(cmd_dic, platform):
    pass

def process_setdefault(cmd_dic, platform):
    pass
