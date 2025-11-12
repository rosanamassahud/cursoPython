def maior(a,b):
    if(a>b):
        print('{} é maior que {}'.format(a,b))
    elif(b>a):
        print('{} é maior que {}'.format(b,a))
    else:
        print('Os números são iguais')

# função que soma 2 numeros
def soma(a,b):
    return a+b

def mult(a,b):
    return a*b

def divide(a,b):
    if(b==0):
        print('ERRO!')
        return 0
    else:
        return a/b

#maior(10,10) # chamada da função maior

#resultado = soma(10,5.6)
#print('A soma é {}'.format(resultado))

x = float(input('Digite o primeiro número: '))
op = input('+ - * /')
y = float(input('Digite o segundo número: '))

if(op == '+' or op == '-'):
    if(op== '+'):
        resultado = soma(x,y)
    else:
        resultado = soma(x, -y)
elif(op == '*'):
    resultado = mult(x,y)
elif(op == '/'):
    resultado = divide(x,y)
else:
    print('ERRO! Esta operação não existe na calculadora')

print(f'{resultado:.2f}')