def my_gen():
    yield 1
    yield 2
    yield 3
    return 4


def my_fun():
    return 4


print(my_fun())

mygen = my_gen()
print(next(mygen))
print(next(mygen))
