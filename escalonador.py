

class Process():
    def __init__(self,cpu_frac,name,pid,time_exec,priority):
        # Inicializando os atributos da classe de processos
        self.name =name
        self.pid = pid
        self.priority = priority
        self.cpu_frac = cpu_frac
        self.time_exec = time_exec

def file_stats(filename):
    # Abre o arquivo com os processos .
    with open(filename) as file_object:
        # Le o cabecalho do arquivo
        header = file_object.readline()
        escalonador, quantum = header.split("|")
        quantum=int(quantum)
        # Le o resto do arquivo com os processos
        file = file_object.readlines()        
        return(header,escalonador,quantum)


def round_robin():
    listar_processos()

def lotery():
    pass

def priority():
    pass

def cfs():
    pass



if __name__ == "__main__":
    diretorio_processos = '/media/teteu/HdGrande/Faculdade/Sistemas Operacionais/escalonador_teteu/'
    arquivo = 'alternance.txt'
    filename = diretorio_processos + arquivo
    
    header,type, quantum = file_stats(filename)
    print("Cabecalho do arquivo: {0}\nEscalonador: {1}\nQuantum: {2}".format(header, type, quantum))

    if type == "alternanciaCircular":
        round_robin()
    elif(type == "loteria"):
        lotery()
    elif(type == "prioridade"):
        priority()
    elif(type == "CFS"):
        cfs()




