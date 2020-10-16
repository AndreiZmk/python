import random
import datetime
import requests
import buscacep

class Pessoa:

    def __init__(self):
        self.sexo = "M" if random.random() > 0.5 else "F"
        self.cpf = self.criarCPF()
        self.nome = self.gerarNome(self.sexo) if random.random() > 0.5 else ' '.join((self.gerarNome(self.sexo),self.gerarNome(self.sexo)))
        self.sobrenome = self.gerarSobrenome()
        self.data_nascimento = self.gerarDataNascimento()
        self.idade = abs(int(self.data_nascimento.split("-")[0]) - datetime.datetime.now().year)
        self.telefone = self.gerarNumeroTelefone()
        self.geraEndereço()
        self.tipoSanguineo = ['A-', 'A+', 'B-', 'B+', 'AB-', 'AB+', 'O-', 'O+'][random.randrange(8)]
        
    def criarCPF(self):
        def calcula_digito(digs):
           s = 0
           qtd = len(digs)
           for i in range(qtd):
              s += n[i] * (1+qtd-i)
           res = 11 - s % 11
           if res >= 10: return 0
           return res                                                                              
        n = [random.randrange(10) for i in range(9)]
        n.append(calcula_digito(n))
        n.append(calcula_digito(n))
        return ''.join(map(str, n))

    def gerarNome(self, sexo):
        file = 'nomes_masculinos.csv' if sexo == "M" else 'nomes_femininos.csv'
        rand = random.randint(0,1000)
        with open(file, 'r') as lista:
            for i, line in enumerate(lista):
                if i == rand:
                    nome = line.split(',')[0].title()
                    return nome 

    def gerarSobrenome(self):
        rand = random.randrange(90) if random.random() > 0.5 else random.randrange(1800)
        with open('listadesobrenomesbrasileiros.txt', 'r', encoding = 'utf=8') as nomes:
            for i, line in enumerate(nomes):
                if i == rand:
                    return line.split(',')[0]

    def gerarDataNascimento(self):
        return f"{random.randrange(1970, 2002)}-{str(random.randrange(1,12)).zfill(2)}-{str(random.randrange(1,28)).zfill(2)}"

    def gerarNumeroTelefone(self, fixo=False):
        tipo = '' if fixo else '9'
        numero = f'{tipo}'
        numero += str(random.randint(1,9))
        for n in range(7):
            numero += str(random.randint(0,9))
        return numero

    def geraEndereço(self):
        rand = random.randint(0,732763)
        with open("lista_ceps.txt", "r", encoding="utf-8") as ceps:
            for linha, cep in enumerate(ceps):
                if rand == linha:
                    cep_aleatorio = cep
        
        endereço= buscacep.busca_cep_correios_as_dict(cep_aleatorio[:8])
        self.rua = endereço['logradouro']
        self.cidade, self.estado = endereço['localidade'].split("/")
        self.bairro = endereço['bairro']
        self.cep = endereço['cep']
        self.numero = random.randint(1,700)

if __name__ == "__main__":
    
    headers = {'content-type': 'application/json'}
    url = "URL_POST"
    for i in range(5):
        novaPessoa = Pessoa()
        dados = {
            "nome" : f"{' '.join((novaPessoa.nome, novaPessoa.sobrenome))}",
            "sexo" : f"{novaPessoa.sexo}",
            "cpf" : f"{novaPessoa.cpf}",
            "idade" : f"{novaPessoa.idade}",
            "nascimento" : f"{novaPessoa.data_nascimento}",
            "telefone" : f"{novaPessoa.telefone}",
            "rua" : f"{novaPessoa.rua}",
            "número": f"{novaPessoa.numero}",
            "cidade" : f"{novaPessoa.cidade}",
            "bairro" : f"{novaPessoa.bairro}",
            "cep" : f"{novaPessoa.cep}",
            "tipo sanguíneo" : f"{novaPessoa.tipoSanguineo}"
        }
        
        #r = requests.post(url, json=dados, headers=headers)
        print(dados)
