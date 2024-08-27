import sys
import threading
from tqdm import tqdm
import time
import random
import heapq

#Classe de processos e seus atributos
class Process():
    def __init__(self, name, PID, time_exec, prioridade):
        # Inicializando os atributos da classe de processos
        self.name =name
        self.pid = int(PID)
        self.priority = int(prioridade)
        self.time_exec = int(time_exec)
        self.time_processed = 0
        self.tempo_usado = 0
        self.tempo_virtual = 0  # Tempo virtual inicial

    def __lt__(self, other):
        return self.tempo_virtual < other.tempo_virtual

    def __repr__(self):
        return f"{self.nome} (PID: {self.pid}, Tempo Desejado: {self.tempo_desejado}, Tempo Usado: {self.tempo_usado}, Tempo Virtual: {self.tempo_virtual})"

        
    def discount_quantum(self,quantum):
        for i in tqdm(range(quantum)):
            time.sleep(0.5)
        
        self.time_processed = self.time_processed + quantum
        self.time_exec = self.time_exec-quantum
        
#Função para pegar o Quantum do arquivo e qual o escalonador utilizado no cabeçalho do arquivo
def file_stats(filename):
    # Abre o arquivo com os processos .
    with open(filename) as file_object:
        # Le o cabecalho do arquivo
        header = file_object.readline()
        escalonador, quantum = header.split("|")
        quantum=int(quantum)
        # Le o resto do arquivo com os processos
        file = file_object.readlines()        
        return(header,escalonador,quantum,file)


def listar_processos(file):
    processos = []
    
    for line in file:
        name, pid, time_exec, prioridade = line.split("|")
        processo = Process(name, pid, time_exec, prioridade)
        processos.append(processo)
        
    return processos

def check_states(processos, finalizados = []):
    prontos = []
    n = len(processos)
    
    for i in range(n):
        if processos[i].time_exec == 0:
            finalizados.append(processos[i])
        elif processos[i].time_exec > 0:
            prontos.append(processos[i])
        else:
            print("ERRO NO MÓDULO:      check_states")
            
    return prontos, finalizados
    


def round_robin(file):
    
    sys.stdout.write("\nInicio do escalonamento\n###################\n")
    processos = listar_processos(file)
    
    prontos, finalizados = check_states(processos)
    
    tam_processos = len(processos)
    while True:
        sys.stdout.write("Quantidade de processos: {}\n".format(len(prontos)))
        sys.stdout.write("####### CPU #######\n")
        for proc in prontos:
            sys.stdout.write("\n## Processo: {}\n".format(proc.name))
            sys.stdout.write("Tempo antes de processar: {}\n".format(proc.time_exec))
            sys.stdout.write("Processando...\n")
            
            proc.discount_quantum(quantum)
            
            sys.stdout.write("Tempo restante: {}\n".format(proc.time_exec))
        
        prontos, finalizados = check_states(processos=prontos,finalizados=finalizados)
        
        if len(finalizados) == tam_processos:
            sys.stdout.write("Todos os processos finalizados")
            break
        
        
    
    
def select_ticket(processos):
    # Criar uma lista de bilhetes onde cada processo aparece na quantidade de bilhetes que possui
    bilhetes = []
    for processo in processos:
        bilhetes.extend([processo] * processo.priority)
    # Selecionar um bilhete aleatório
    processo_escolhido = random.choice(bilhetes)
    return processo_escolhido


def lotery(file):
    sys.stdout.write("\nInicio do escalonamento\n###################\n")
    processos = listar_processos(file)
    
    prontos, finalizados = check_states(processos)

    tam_processos = len(processos)
    while True:
        sys.stdout.write("Quantidade de processos: {}\n".format(len(prontos)))
        sys.stdout.write("####### CPU #######\n")
        processo_escolhido = select_ticket(prontos)
        sys.stdout.write("\n## Processo: {}\n".format(processo_escolhido.name))
        sys.stdout.write("Tempo antes de processar: {}\n".format(processo_escolhido.time_exec))
        sys.stdout.write("Processando...\n")
            
        processo_escolhido.discount_quantum(quantum)

        sys.stdout.write("Tempo restante: {}\n".format(processo_escolhido.time_exec))

        prontos, finalizados = check_states(processos)

        if len(finalizados) == tam_processos:
            sys.stdout.write("Todos os processos finalizados")
            break


#Prioridade premptiva, em caso de empate de prioridades, o PID decide
def priority(file):
    sys.stdout.write("\nInicio do escalonamento\n###################\n")
    processos = listar_processos(file)
    
    prontos, finalizados = check_states(processos)
    processos_ordenados = sorted(prontos, key=lambda processo: (-processo.priority,processo.pid))
    # Ordena por prioridade (decrescente) e depois por PID (crescente)

    tam_processos = len(processos)
    while True:
        processos_ordenados = sorted(prontos, key=lambda processo: (-processo.priority,processo.pid))
        sys.stdout.write("Quantidade de processos: {}\n".format(len(prontos)))
        sys.stdout.write("####### CPU #######\n")
        for proc in processos_ordenados:
            sys.stdout.write("\n## Processo: {}\n".format(proc.name))
            sys.stdout.write("Tempo antes de processar: {}\n".format(proc.time_exec))
            sys.stdout.write("Processando...\n")
                
            proc.discount_quantum(quantum)

            sys.stdout.write("Tempo restante: {}\n".format(proc.time_exec))

            prontos, finalizados = check_states(processos)


        if len(finalizados) == tam_processos:
            sys.stdout.write("Todos os processos finalizados")
            break

def cfs(file, quantum):
    sys.stdout.write("\nInicio do escalonamento\n###################\n")
    processos = listar_processos(file)
    
    prontos, finalizados = check_states(processos)

    if not prontos:
        sys.stdout.write("Nenhum processo pronto para ser executado.\n")
        return

    heapq.heapify(prontos)  # Cria uma heap baseada no tempo virtual dos processos
    tam_processos = len(prontos)
    
    # Barra de progresso geral
    with tqdm(total=tam_processos, desc="Progresso Geral", unit="processo", leave=False) as pbar:
        while prontos:
            sys.stdout.write("Quantidade de processos: {}\n".format(len(prontos)))
            sys.stdout.write("####### CPU #######\n")
            
            if prontos:
                processo_atual = heapq.heappop(prontos)
            else:
                break  # Se a lista estiver vazia, saia do loop
            
            tempo_execucao = min(quantum, processo_atual.time_exec - processo_atual.tempo_usado)
            print(f"Executando {processo_atual.name} (PID: {processo_atual.pid}) por {tempo_execucao} unidades de tempo")
            
            # Barra de progresso individual para o processo
            with tqdm(total=tempo_execucao, desc=f"Processo {processo_atual.name}", unit="tempo", leave=False) as proc_bar:
                while tempo_execucao > 0:
                    time.sleep(0.5)  # Simula o tempo de execução (0.5 segundos)
                    processo_atual.tempo_usado += 1
                    tempo_execucao -= 1
                    processo_atual.time_exec -= 1
                    proc_bar.update(1)  # Atualiza a barra com 1 unidade de tempo
                    
                    if processo_atual.time_exec <= 0:
                        finalizados.append(processo_atual)  # Processo finalizado
                        pbar.update(1)  # Atualiza o progresso geral
                        break

            if len(finalizados) == tam_processos:
                sys.stdout.write("Todos os processos finalizados\n")
                break
            else:
                processo_atual.tempo_virtual += quantum  # Atualiza o tempo virtual
                heapq.heappush(prontos, processo_atual)  # Reinsere o processo na heap
    sys.stdout.write("\nInicio do escalonamento\n###################\n")
    processos = listar_processos(file)
    
    prontos, finalizados = check_states(processos)

    if not prontos:
        sys.stdout.write("Nenhum processo pronto para ser executado.\n")
        return

    heapq.heapify(prontos)  # Cria uma heap baseada no tempo virtual dos processos
    tam_processos = len(prontos)
    
    # Barra de progresso geral
    with tqdm(total=tam_processos, desc="Progresso Geral", unit="processo", leave=False) as pbar:
        while prontos:
            sys.stdout.write("Quantidade de processos: {}\n".format(len(prontos)))
            sys.stdout.write("####### CPU #######\n")
            
            if prontos:
                processo_atual = heapq.heappop(prontos)
            else:
                break  # Se a lista estiver vazia, saia do loop
            
            tempo_execucao = min(quantum, processo_atual.time_exec - processo_atual.tempo_usado)
            print(f"Executando {processo_atual.name} (PID: {processo_atual.pid}) por {tempo_execucao} unidades de tempo")
            
            # Barra de progresso individual para o processo
            with tqdm(total=processo_atual.time_exec, desc=f"Processo {processo_atual.name}", unit="tempo", leave=False) as proc_bar:
                while tempo_execucao > 0:
                    time.sleep(0.5)  # Simula o tempo de execução
                    processo_atual.tempo_usado += tempo_execucao
                    processo_atual.time_exec -= tempo_execucao
                    proc_bar.update(tempo_execucao)
                    
                    if processo_atual.time_exec > 0:
                        processo_atual.tempo_virtual += tempo_execucao  # Atualiza o tempo virtual
                        heapq.heappush(prontos, processo_atual)  # Reinsere o processo na heap
                        break  # O processo será reescalonado
                    else:
                        finalizados.append(processo_atual)  # Processo finalizado
                        pbar.update(1)  # Atualiza o progresso geral
                        break

            if len(finalizados) == tam_processos:
                sys.stdout.write("Todos os processos finalizados\n")
                break



if __name__ == "__main__":
    arquivo = sys.argv[1]
    global file
    header,type, quantum, file = file_stats(arquivo)
    print("Cabecalho do arquivo: {0}\nEscalonador: {1}\nQuantum: {2}".format(header, type, quantum))
    
    if type == "alternanciaCircular":
        round_robin(file)
    elif(type == "loteria"):
        lotery(file)
    elif(type == "prioridade"):
        priority(file)
    elif(type == "CFS"):
        cfs(file,quantum)




