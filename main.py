#Importação de módulos
import time
from colorama import init, Fore, Style
init(autoreset=True)


#Declaração de funções
def menu_e_escolha():
    #Inicialização/Menu
    iniciar = True
    while iniciar == True:
        print(f"""\n---------------------{Fore.GREEN}MENU PRINCIPAL{Style.RESET_ALL}---------------------
| [1] - Cadastrar novo paciente                        |
| [2] - Listar pacientes internados                    |
| [3] - Realizar procedimento no paciente              |
| [4] - Dar alta ao paciente e calcular custo          |
| [5] - Sair                                           |
--------------------------------------------------------""")
        
        #Entrada da escolha do que o usuário quer fazer com os dados
        escolha = int(input("Sua escolha:"))
        if escolha == 5: #Encerra o programa
            iniciar = False
        elif escolha not in (1,2,3,4,5): #Verificação de escolha incorreta
            print(f"{Fore.RED}Escolha incoreta, repita.{Style.RESET_ALL}")
        
        elif escolha == 1: #Cadastro de novo paciente
            while True:
                try:       
                    with open("cadastro.csv", "r+", encoding="utf-8")as arquivo:
                        dados = arquivo.readlines()
                        print("Informe abaixo os dados do paciente.")
                        arquivo.write(str((len(dados)+1)) + ";" + input("Nome do paciente: ") + ";" + input("Espécie: ") + ";" + input("Raça: ") + ";")
                        arquivo.write(input("Data de nascimento (dd/mm/aaaa): ") + ";")
                        arquivo.write(input("Idade: ") + ";" + input("Sexo: ") + ";" + input("Castrado ou fértil: ") + ";" + input("Vacinas [Sim ou não]: ") + ";" + input("Informe a baia o animal será internado: ") + ";" + input("Nome do tutor: ") + ";" + input("Telefone: ") + ";" + input("Endereço: ") + ";")
                        arquivo.write(input("Informe a data de entrada do paciente (dd/mm/aaaa): ") + ";" + "0" + "\n")
                        time.sleep(1)
                        print(f"\n{Fore.GREEN}Dados gravados com sucesso.{Style.RESET_ALL}")
                        break

                except FileNotFoundError:
                    with open("cadastro.csv", "w", encoding="utf-8")as arquivo:
                        time.sleep(1)

        elif escolha == 2: #Listagem dos paciente
            listar_pacientes()
            time.sleep(2)
    
        elif escolha == 3:  #Listagem para escolha do paciente que será realizado o procedimento
            if not listar_pacientes():
                continue        
            with open("cadastro.csv", "r", encoding="utf-8") as arquivo:
                dados = arquivo.readlines()
            while True: #Escolha do paciente e verificação se o index está correto
                escolha_paciente = int(input("Informe o número referente ao paciente: "))
                if 0 < escolha_paciente <= len(dados):
                    escolha_paciente -= 1
                    break
                else:
                    time.sleep(1)
                    print(f"{Fore.RED}Escolha incoreta, repita.{Style.RESET_ALL}")
                    time.sleep(1)

            #Menu de procedimentos    
            print("\nQual procedimento deseja adiconar ao arquivo do paciente?\n")
            print(f"{'[1] - Aplicação de medicação intravenosa.':<32} Custo: R$80,00.")
            print(f"{'[2] - Curativos.':<41} Custo: R$40,00.")
            print(f"{'[3] - Exames laboratoriais.':<41} Custo: R$25,00.")
            print(f"{'[4] - Banho terapêutico.':<41} Custo: R$60,00.")
            print(f"{'[5] - Alimentação assistida.':<41} Custo: R$70,00.")
            while True: #Escolha do procedimento e verificação se a mesma está coreta
                escolha_procedimento = int(input("\nSua escolha: "))
                if escolha_procedimento in (1,2,3,4,5):
                    break
                else:
                    print(f"\n{Fore.RED}Escolha incoreta, repita.{Style.RESET_ALL}")
            
            #Passagem de argumento para a função conforme a escolha do usuário
            if escolha_procedimento == 1:
                inserir_procedimento(escolha_paciente, 80)
            elif escolha_procedimento == 2:
                inserir_procedimento(escolha_paciente, 40)
            elif escolha_procedimento == 3:
                inserir_procedimento(escolha_paciente, 25)
            elif escolha_procedimento == 4:
                inserir_procedimento(escolha_paciente, 60)
            else:
                inserir_procedimento(escolha_paciente, 70)


        elif escolha == 4: #Listagem para escolha do paciente que receberá alta e cálculo de custos
            if not listar_pacientes():
                continue 
            while True:
                try: #Verifica a existência do arquivo
                    with open("cadastro.csv", "r", encoding="utf-8") as arquivo: 
                        dados = arquivo.readlines() #Ponteiro parou no final do arquivo
                        while True: #Escolha do paciente e verificação se o index está correto
                            escolha_paciente = int(input("Informe o número referente ao paciente: "))
                            if 0 < escolha_paciente <= len(dados):
                                escolha_paciente -= 1
                                break
                            else:
                                time.sleep(1)
                                print(f"{Fore.RED}Escolha incoreta, repita.{Style.RESET_ALL}")
                                time.sleep(1)
                        arquivo.seek(0) #Retorna o ponteiro pro início do arquivo      
                        lista = arquivo.readlines()
                        diarias = int(input("Informe quantos dias o paciente ficou internado: "))  
                        
                        #Cálculo do custo da internação
                        for c, linha in enumerate(lista):
                            if escolha_paciente == c:
                                dados = linha.strip().split(";")
                                valor_total = int(dados[14]) + 150 * diarias
                                lista.pop(escolha_paciente)
                        #Exclusão do paciente do cadastro
                        nova_lista = list()    
                        for i, linha in enumerate(lista, start=1): 
                            dados = linha.strip().split(";")
                            dados[0] = str(i)
                            nova_linha = ";".join(dados) + "\n"
                            nova_lista.append(nova_linha)

                    with open('cadastro.csv', 'w', encoding="utf-8") as arquivo:
                        arquivo.writelines(nova_lista)
                except FileNotFoundError: #Se o arquivo não existir, cria um novo.
                    with open('cadastro.csv', 'w', encoding="utf-8") as arquivo:
                        pass
                finally:
                    break
            time.sleep(1)
            print(f"\nO valor a ser pago é de {Fore.GREEN}R$ {valor_total:.2f}{Style.RESET_ALL}.\n")
            time.sleep(2)
            print("""Qual será a forma de pagamento?
[1] dinheiro (10% de desconto)
[2] débito
[3] crédito (5% de acréscimo):""", end=" ")
            while True:
                pagamento = int(input())
                if pagamento in (1,2,3):
                    if pagamento == 1: valor_total -= (valor_total * 5 /100)
                    if pagamento == 3: valor_total += (valor_total * 5 /100)
                    break
                else:
                    time.sleep(1)
                    print(f"{Fore.RED}Escolha incorreta, repita.{Style.RESET_ALL}")
                    time.sleep(1)
            time.sleep(1)
            print(f"\nValor final de {Fore.GREEN}R$ {valor_total:.2f}{Style.RESET_ALL}.")
            time.sleep(2)
def listar_pacientes():
    while True:
        try:
            with open("cadastro.csv", "r", encoding="utf-8")as arquivo:
                dados = arquivo.readlines()
                if len(dados) == 0:
                    time.sleep(1)
                    print(f"\n{Fore.RED}Não há paciente internados. Escolha a opção [1] para cadastrar um novo paciente.{Style.RESET_ALL}")
                    time.sleep(2)
                    return False
                else:
                    print()
                    print("-" * 113, f"{Fore.GREEN}Listagem dos pacientes{Style.RESET_ALL}", "-" * 121)
                    print(f"|{'Nº':^4}|{'Nome do paciente':^25}|{'Espécie':^20}|{'Raça':^20}|{'Data de nascimento':^20}|{'Idade':^7}|{'Sexo':^11}|{'Fertilidade':^13}|{'Vacinado':^10}|{'Baia':^6}|{'Tutor':^20}|{'Telefone':^15}|{'Endereço':^40}|{'Data de entrada':^16}|{'Valor Gasto':^15}|")
                    arquivo.seek(0)
                    for linha in arquivo:
                        dados = linha.strip().split(";")
                        print(f"|{dados[0]:^4}|{dados[1]:^25}|{dados[2]:^20}|{dados[3]:^20}|{dados[4]:^20}|{dados[5]:^7}|{dados[6]:^11}|{dados[7]:^13}|{dados[8]:^10}|{dados[9]:^6}|{dados[10]:^20}|{dados[11]:^15}|{dados[12]:^40}|{dados[13]:^16}|{int(dados[14]):^15.2f}|")
                    print("-" * 258)
                    return True
        except FileNotFoundError:
            with open("cadastro.csv", "w", encoding="utf-8")as arquivo:
                time.sleep(1)
                
            
    
            
def inserir_procedimento(escolha_paciente, valor_procedimento):
    with open("cadastro.csv", "r", encoding="utf-8")as arquivo: 
        lista = arquivo.readlines()
        for c, linha in enumerate(lista):
            if escolha_paciente == c:
                dados = linha.strip().split(";")
                dados[14] = str(int(dados[14]) + valor_procedimento)
                lista[c] = ";".join(dados) + "\n"  
    with open("cadastro.csv", "w", encoding="utf-8") as arquivo:
        arquivo.writelines(lista)
    print(f"\nProcedimento de R$ {valor_procedimento:.2f} adicionado ao paciente de índice {escolha_paciente+1}.")

#Inicialização
menu_e_escolha()


#Finalização do programa
print(f"{Fore.RED}Encerrando{Style.RESET_ALL}", end='')
for c in range(0,3):
    time.sleep(1)
    print(f"{Fore.RED}.{Style.RESET_ALL}", end='')
