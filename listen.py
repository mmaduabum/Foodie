import sh


def do_stuff(reply):
    f = open('replies.txt', 'a+')
    f.write(reply)
    f.write('\n')
    f.close()


while True:
    reply = str(sh.nc('-l', '-w', '1', '80'))
    do_stuff(reply)

