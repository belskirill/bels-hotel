def func2(**kwargs):
    for key, value in kwargs.items():
        print(key, value)


def func(**kwargs):
    func2(**kwargs)



print(func(k=5, l=4))