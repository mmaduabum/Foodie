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
    response_dic = {}
    args = cmd_dic[c.ARGS]
    if len(args) == 0:
       response_dic = None
    else:
	switch = args[0]
        user = cmd_dic[c.USER]
    	check = "select * from switches where switch_id == " + switch + ";"
	a = cursor.execute(check)
	data = a.fetchall()
        if len(data) > 0:
            c.execute("INSERT INTO map (switch_id, user_id, switch_name, sub_timeout, fetty_flag) VALUES ("+switch+","+user+",null,null,0);")
            c.commit()
            response_dic[c.RSP] = c.ADD_MSGS[0]
            response_dic[c.CMD] = cmd_dic[c.CMD]
            response_dic[c.SWITCH_ID] = switch
        else:
            response_dic = None
    connection.close()
    cursor.close()
    return response_dic

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
