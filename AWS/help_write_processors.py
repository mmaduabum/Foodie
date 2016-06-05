USERS: user_id, user_medium, default_switch_id
SWITCHES: switch_id, state
SWITCH_USER_MAP: switch_id, user_id, name, sub_tmstmp_exp, sub_bool


def process_follow(cmd_dic, platform):
    args = cmd_dic[c.ARGS]
    
    #if 1 arg: follow that arg switch ( check if its valid) , and if its mapped to user
    
    
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
     reponse_dic = {}
     args = cmd_dic[c.ARGS]
     #This command must have at elast 1 argument
     if len(args) == 0:
        response_dic = None
     else:
         switch = args[0]
         user = cmd_dic[c.USER]
         check = "select * from switches where switch_id == " + switch + ";"
         a = cursor.execute(check)
        data = a.fetchall()
         #This is a valid switch id
         if len(data) > 0:
             response_dic[c.SWITCH_ID] = switch
             response_dic[c.CMD] = cmd_dic[c.CMD]
             unique = "select * from map where switch_id == " + switch + " and user_id == " + user + ";"
             results = cursor.execute(unique).fetchall()
             #There is a map from switch to user so remove it
             if len(results) > 0:
                 cursor.execute("DELETE FROM map WHERE switch_id == "+switch+" and user_id == "+user+";")
                 conn.commit()
                 response_dic[c.RSP] = c.ADD_MSGS[1]
             # there is no (switch, id) pair in map, so tell them to add it before they can remove it
             else:
                 response_dic[c.RSP] = c.ADD_MSGS[0]
         #The supplied switch id is not a valid switch id
         else:
             response_dic = None
    cursor.close()
    conn.close()
	return response_dic

def process_status(cmd_dic, platform):
    reponse_dic = {}
    args = cmd_dic[c.ARGS]
    #This command must have at elast 1 argument
    if len(args) == 0:
        response_dic = None
    else:
    switch = args[0]
    user = cmd_dic[c.USER]
    check = "select * from switches where switch_id == " + switch + ";"
    a = cursor.execute(check)
    data = a.fetchall()
    #This is a valid switch id
    if len(data) > 0:
        response_dic[c.CMD] = cmd_dic[c.CMD]
        unique = "select * from map where switch_id == " + switch + " and user_id == " + user + ";"
        results = cursor.execute(unique).fetchall()
        #The user is following it so tell them the status
        if len(results) > 0:
            state = cursor.execute("SELECT state FROM switches WHERE switch_id == "+switch+";").fetchall()[0]
            conn.commit()
            response_dic[c.SWITCH_ID] = switch
            response_dic[c.RSP] = c.STATUS_MSGS[0]
            response_dic[c.SWITCH_STATUS] = state
         # there is no (switch, id) pair in map, so tell them to add it before they can get the status of it
         else:
            response_dic[c.RSP] = c.STATUS_MSGS[1]
     #The supplied switch id is not a valid switch id
     else:
        response_dic = None
    cursor.close()
    conn.close()
    return response_dic

def process_list(cmd_dic, platform):
    pass

def process_setname(cmd_dic, platform):
    pass

def process_setdefault(cmd_dic, platform):
    pass
