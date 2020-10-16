import random
import datetime
import requests

class Pessoa:

    def __init__(self):
        self.sexo = "M" if random.random() > 0.5 else "F"
        self.cpf = self.criarCPF()
        self.nome = self.gerarNome(self.sexo) if random.random() > 0.5 else ' '.join((self.gerarNome(self.sexo),self.gerarNome(self.sexo)))
        self.sobrenome = self.gerarSobrenome()
        self.data_nascimento = self.gerarDataNascimento()
        self.idade = abs(int(self.data_nascimento.split("-")[0]) - datetime.datetime.now().year)
        self.telefone = self.gerarNumeroTelefone()
        
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
        file = '01_nomes_masculinos.csv' if sexo == "M" else '01_nomes_femininos.csv'
        rand = random.randint(0,1000)
        with open(file, 'r') as lista:
            for i, line in enumerate(lista):
                if i == rand:
                    nome = line.split(',')[0].title()
                    return nome 

    def gerarSobrenome(self):
        rand = random.randrange(90) if random.random() > 0.5 else random.randrange(1800)
        with open('01_listadesobrenomesbrasileiros.txt', 'r', encoding = 'utf=8') as nomes:
            for i, line in enumerate(nomes):
                if i == rand:
                    return line.split(',')[0]

    def gerarDataNascimento(self):
        return f"{random.randrange(1970, 2002)}-{str(random.randrange(1,12)).zfill(2)}-{str(random.randrange(1,28)).zfill(2)}"

    def gerarNumeroTelefone(self, ddd=41, fixo=False):
        tipo = ' ' if fixo else ' 9'
        numero = f'{ddd}{tipo}'
        numero += str(random.randint(1,9))
        for n in range(7):
            numero += str(random.randint(0,9))
        return numero

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
            "telefone" : f"{novaPessoa.telefone}"
        }
        
        r = requests.post(url, json=dados, headers=headers)
        print(r)
