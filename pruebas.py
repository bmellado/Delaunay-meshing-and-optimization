a=0
b=3
def dos(a):
    if(a==3):
        return 5
    else:
        a+=1
        return dos(a)
        return dos(b)

hola = dos(a)
print(hola)
lista = [3,4,3,4,6,3,5,3,4,3,4,3,4,3,4,5,3,3]
while(lista.count(3)>1):
    lista.remove(3)
print(lista)