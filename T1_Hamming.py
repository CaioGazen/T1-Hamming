from functools import reduce
from rich.console import Console
from rich.table import Table
from os import system

def get_binary_bits():                                              #Função que recebe bits enviados pelo usuário em formato
    bits = input("Digite sem espaços os bits que deseja enviar: ")  
    if bits.isnumeric() == False:                                   #Checa se a string recebida é composta apenas de números 
        print("Digite apenas números binários")                     #caso não seja, chama a função novamente
        return get_binary_bits()                                    
    bits = [int(x) for x in str(bits)]                              #transforma a string em lista de inteiros 
    for i in range(len(bits)):
        if bits[i] != 0 and bits[i] != 1:                           #checa se os bits recebidos são binários
            print("Digite apenas números binários")                 #caso não seja, chama a função novamente
            return get_binary_bits()
    return bits                                                     #retorna a lista de bits recebida

def get_decimal_bits():                                             #Função que recebe bits enviados pelo usuário em formato decimal e converte para binário
    bits = input("Digite os bits: ")
    if bits.isnumeric() == False:                                   #checa se a string recebida é composta apenas de números
        print("Digite apenas números")                              #caso não seja, chama a função novamente
        return get_binary_bits()
    bits = int(bits)                                                #converte de string para inteiro
    return [int(i) for i in bin(bits)[2:]]                          #converte de inteiro para decimal e faz uma lista com os bits resultantes

def get_parity_bits(bits):                                                                      #Função que gera os bits de paridade
    parity_bits = reduce(lambda x, y: x ^ y, [i + 1 for i, j in enumerate(bits) if j])          #
    return parity_bits

def send_bits(bits):                                                #Função que pega os bits de dados, calcula os bits de paridade e insere os mesmos
    l = len(bits)                                                       
    i, p = 0, 0
    while p < l:                                                    #Insere zeros nas posições dos bits de paridade
        bits.insert(p, 0)
        i += 1
        l += 1
        p = (2**i) - 1

    parity_bits = get_parity_bits(bits)                             #chama a função que calcula os bits de paridade
    parity_bits = [int(i) for i in bin(parity_bits)[2:]]            #separa os bits de paridade em uma lista
    parity_bits.reverse()                                           #inverte a lista dos bits de paridade

    for i in range(len(parity_bits)):
        bits[(2**i) - 1] = parity_bits[i]                           #insere os bits de paridade em suas devidas posições
    return bits

def receive_bits(bits):                                                                     #Função que recebe um grupo de bits e verifica os bits de paridade
    parity_bits = get_parity_bits(bits)                                                     #chama a função que calcula os bits de paridade
    if parity_bits == 0:                                                                    #se a função get_parity_bits(bits); retornar 0 significa que os bits de paridade estão corretos
        print_bits(bits, None, -1, "Nenhum erro encontrado nos bits")
        return bits                                                                         #Já que não foi encontrado nenhum erro os bits são retornados sem nenhuma alteração
    print_bits(bits, None, parity_bits - 1, "Erro encontrado no bit " + str(parity_bits))   #Imprime a posição do erro encontrado
    print("\n")
    if input("deseja tentar corrigir o bit? (s/n): ") == "n":                               #Pergunta ao usuário se ele deseja tentar resolver o erro
        return print("Bits não corrigidos")
    bits2 = list(bits)                                                                      #salva o estado atual dos bits
    bits[parity_bits - 1] = bits[parity_bits - 1] ^ 1                                       #Inverte o valor que está na posição com erro
    print_bits(bits2, bits, parity_bits - 1, "bit corrigido")                               #Imprime o estado anterior dos bits, o estado atual e desta a bit que foi modificado
    return bits                                                                             #retorna os bits corrigidos

def modify_bits(bits):                                                      #Função que permite alterar de forma arbitraria os bits armazenados
    bits2 = list(bits)                                                      #salva o estado atual dos bits 
    print_bits(bits, None, -1, "Bits Atuais")                               
    print("\n")
    m = int(input("Digite a posição do bit que deseja modificar: ")) - 1    #seleciona o bit a ser modificado
    bits[m] = bits[m] ^ 1                                                   #modifica o bit selecionado
    print_bits(bits2, bits, m, "Bit modificado")                            #imprime os bits antes e depois da modificação

def escolher():                                     #Função que permite ao usuário escolher uma das opções
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

def main():                                                     #Main
    bits = []
    while True:                                                 #Loop principal    
        match escolher():                                       
            case "1":
                bits = get_binary_bits()
                bits = send_bits(bits)
                print_bits(bits, None, -1, "Bits enviados")
            case "2":
                bits = get_binary_bits()
                receive_bits(bits)
            case "3":
                modify_bits(bits)
            case "4":
                bits = receive_bits(bits)
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