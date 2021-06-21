def saludar():
    print("hola")

def despedir():
    print("chau")

def limpiar():
    print('limpio')

dic = {'f1': saludar, 'f2': despedir, 'limpiar': limpiar}

comando = input('ingrese funcion')
dic[comando]()

