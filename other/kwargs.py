def card_save(name, *args):
    print(name)
    print(type(args))
    for i in args:
        print(i)

card_save('Animals','cat', 'dog', 'parrot')