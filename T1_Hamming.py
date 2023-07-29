from functools import reduce
from rich.console import Console
from rich.table import Table
from os import system

def get_binary_bits():
    bits = input("Digite sem espacos os bits que deseja enviar: ")
    if bits.isnumeric() == False:
        print("Digite apenas numeros binarios")
        return get_binary_bits()
    bits = [int(x) for x in str(bits)]
    for i in range(len(bits)):
        if bits[i] != 0 and bits[i] != 1:
            print("Digite apenas numeros binarios")
            return get_binary_bits()
    return bits

def get_decimal_bits():
    bits = input("Digite os bits: ")
    if bits.isnumeric() == False:
        print("Digite apenas numeros")
        return get_binary_bits()
    bits = int(bits)
    return [int(i) for i in bin(bits)[2:]]

def get_parity_bits(bits):
    parity_bits = reduce(lambda x, y: x ^ y, [i + 1 for i, j in enumerate(bits) if j])
    return parity_bits

def send_bits(bits):
    l = len(bits)
    i, p = 0, 0
    while p < l:
        bits.insert(p, 0)
        i += 1
        l += 1
        p = (2**i) - 1

    parity_bits = get_parity_bits(bits)
    parity_bits = [int(i) for i in bin(parity_bits)[2:]]
    parity_bits.reverse()

    for i in range(len(parity_bits)):
        bits[(2**i) - 1] = parity_bits[i]
    return bits

def recieve_bits(bits):
    parity_bits = get_parity_bits(bits)
    if parity_bits == 0:
        print_bits(bits, None, -1, "Nenhum erro encontrado nos bits")
        return bits
    print_bits(bits, None, parity_bits - 1, "Erro encontrado no bit " + str(parity_bits))
    print("\n")
    if input("deseja tentar corrigir o bit? (s/n): ") == "n":
        return print("Bits nao corrigidos")
    bits2 = list(bits)
    bits[parity_bits - 1] = bits[parity_bits - 1] ^ 1
    print_bits(bits2, bits, parity_bits - 1, "bit corrigido")
    return bits

def modify_bits(bits):
    bits2 = list(bits)
    print_bits(bits, None, -1, "Bits Atuais")
    print("\n")
    m = int(input("Digite a posição do bit que deseja modificar: ")) - 1
    bits[m] = bits[m] ^ 1
    print_bits(bits2, bits, m, "Bit modificado")

def escolher():
   e = input("""
Digite o que você deseja fazer:
1) Enviar um grupo de bits
2) Receber um grupo de bits
3) Modificar um grupo de bits previamente enviado
4) Receber um grupo de bits previamente enviado
5) Enviar um grupo de bits em decimal
6) Imprimir Grupo de bits atual
Opção: """)
   return e

def print_bits(bits, bits2, position, title):
    system('clear||cls')
    print("\n")
    table = Table(show_lines=True, title=title)
    Pr = []
    j = 0
    for i in range(len(bits)):
        if (2**j) - 1 == i and i == position:
            table.add_column("[bold red]" + str(i + 1) + "[/bold red]", justify="center", style="red")
            j += 1
            Pr.append("[bold]P" + str(j) + "[/bold]")
        elif i == position:
            table.add_column("[bold red]" + str(i + 1) + "[/bold red]", justify="center", style="red")
            Pr.append(" ")
        elif (2**j) - 1 == i:
            table.add_column(str(i + 1), justify="center", style="green")
            j += 1
            Pr.append("[bold]P" + str(j) + "[/bold]")
        else:
            table.add_column(str(i + 1), justify="center", style="blue")
            Pr.append(" ")
    table.add_row(*((str(Pr).strip("[]").replace("'","")).split(",")))
    table.add_row(*((str(bits).strip("[]")).split(",")))
    if bits2 != None:
        table.add_row(*((str(bits2).strip("[]")).split(",")))
    console = Console()
    console.print(table)

def main():
    bits = []
    while True:    
        match escolher():
            case "1":
                bits = get_binary_bits()
                bits = send_bits(bits)
                print_bits(bits, None, -1, "Bits enviados")
            case "2":
                bits = get_binary_bits()
                recieve_bits(bits)
            case "3":
                modify_bits(bits)
            case "4":
                bits = recieve_bits(bits)
            case "5":
                bits = get_decimal_bits()
                bits = send_bits(bits)
                print_bits(bits, None, -1, "Bits enviados")
            case "6":
                print_bits(bits, None, -1, "Bits atuais")
            case _:
                print("Opção inválida")

if __name__ == '__main__':
    main()