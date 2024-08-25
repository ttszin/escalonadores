import sys
import threading
from tqdm import tqdm
import time

class Process():
    def __init__(self, name, PID, time_exec, prioridade):
        # Inicializando os atributos da classe de processos
        self.name =name
        self.pid = int(PID)
        self.priority = int(prioridade)
        self.time_exec = int(time_exec)
        self.time_processed = 0
        
    def discount_quantum(self,quantum):
        for i in tqdm(range(quantum)):
            time.sleep(0.5)
        
        self.time_processed = self.time_processed + quantum
        self.time_exec = self.time_exec-quantum
        

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
        bilhetes.extend([processo.nome] * processo.prioridade)
    # Selecionar um bilhete aleatório
    processo_escolhido = random.choice(bilhetes)
    return processo_escolhido


def lotery():
    sys.stdout.write("\nInicio do escalonamento\n###################\n")
    processos = listar_processos(file)
    
    prontos, finalizados = check_states(processos)

    while True:
        sys.stdout.write("Quantidade de processos: {}\n".format(len(prontos)))
        sys.stdout.write("####### CPU #######\n")
        processo_escolhido = select_ticket(prontos)
        sys.stdout.write("\n## Processo: {}\n".format(processo_escolhido.name))
        sys.stdout.write("Tempo antes de processar: {}\n".format(processo_escolhido.time_exec))
        sys.stdout.write("Processando...\n")
            
        processo_escolhido.discount_quantum(quantum)

        sys.stdout.write("Tempo restante: {}\n".format(processo_escolhido.time_exec))

        if len(finalizados) == tam_processos:
            sys.stdout.write("Todos os processos finalizados")
            break



def priority():
    pass

def cfs():
    pass



if __name__ == "__main__":
    arquivo = sys.argv[1]
    global file
    header,type, quantum, file = file_stats(arquivo)
    print("Cabecalho do arquivo: {0}\nEscalonador: {1}\nQuantum: {2}".format(header, type, quantum))
    
    if type == "alternanciaCircular":
        round_robin(file)
    elif(type == "loteria"):
        lotery()
    elif(type == "prioridade"):
        priority()
    elif(type == "CFS"):
        cfs()




