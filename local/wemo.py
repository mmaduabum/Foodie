from ouimeaux.environment import Environment

def on_switch(switch):
    print "Switch found!", switch.name

def on_motion(motion):
    print "Motion found!", motion.name

env = Environment(on_switch, on_motion)
env.start()

#env.list_switches()

switch = env.get_switch('ymcmb')
print switch.on()
