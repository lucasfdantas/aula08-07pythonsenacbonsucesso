from django.shortcuts import get_object_or_404, redirect, render
import platform
import subprocess
from .models import Usuarios
# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def cadastro(request):
    return render(request, 'cadastro/index.html')

def usuarios(request):
    if request.method == "POST":
        novo_usuario = Usuarios()
        novo_usuario.nome = request.POST.get('nome')
        novo_usuario.email = request.POST.get('email')
        novo_usuario.setor = request.POST.get('setor')
        novo_usuario.save()

    usuarios = {
        'usuarios': Usuarios.objects.all()
    }

    return render(request, 'usuarios/index.html', usuarios)


def editarUsuario(request, id):
    user = get_object_or_404(Usuarios, pk=id)
    editarUser = {
        'editarUser':user
    }
    if request.method == "POST":
        edit_usuario = get_object_or_404(Usuarios, pk=id)
        edit_usuario.nome = request.POST.get('nome')
        edit_usuario.email = request.POST.get('email')
        edit_usuario.setor = request.POST.get('setor')
        edit_usuario.save()
        return redirect('../usuarios/')
    else:
        return render(request, 'editarUsuario/index.html', editarUser)



def sistema(request):
    sistema = platform.system()
    
    if sistema == "Linux":
        # 1. Nome do Servidor
        nome = subprocess.check_output("hostname", shell=True).decode().strip()
        
        # 2. Processador (Modelo e quantidade de núcleos)
        proc_cmd = "lscpu | grep 'Model name' | cut -d: -f2"
        processador = subprocess.check_output(proc_cmd, shell=True).decode().strip()
        
        # 3. Memória (Exibe o total, usado e disponível em formato legível)
        memoria = subprocess.check_output("free -h", shell=True).decode()
        
        # 4. Status de Rede (Interfaces ativas e IPs)
        rede = subprocess.check_output("ip -br addr show", shell=True).decode()

    elif sistema == "Windows":
        # 1. Nome do Servidor
        nome = subprocess.check_output("hostname", shell=True).decode().strip()
        
        # 2. Processador
        proc_cmd = "wmic cpu get name /value"
        processador = subprocess.check_output(proc_cmd, shell=True).decode().replace("Name=", "").strip()
        
        # 3. Memória (Total visível pelo sistema)
        mem_cmd = "wmic computersystem get TotalPhysicalMemory /value"
        mem_raw = subprocess.check_output(mem_cmd, shell=True).decode().replace("TotalPhysicalMemory=", "").strip()
        # Converte bytes para GB de forma simples
        if mem_raw.isdigit():
            memoria = f"Total de Memória Física: {round(int(mem_raw) / (1024**3), 2)} GB"
        else:
            memoria = "Não foi possível ler a memória."
        
        # 4. Status de Rede (Configuração de IP detalhada)
        rede = subprocess.check_output("ipconfig", shell=True).decode(errors='ignore')
        
    else:
        nome = "Sistema Desconhecido"
        processador = "N/A"
        memoria = "N/A"
        rede = "N/A"

    context = {
        'sistema': sistema,
        'nome_servidor': nome,
        'processador': processador,
        'memoria': memoria,
        'rede': rede
    }

    return render(request, 'sistema/index.html', context)


def deletarUsuario(request, id):
    delete_user = get_object_or_404(Usuarios, pk=id)
    delete_user.delete()
    return redirect('../usuarios/')

