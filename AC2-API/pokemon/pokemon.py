import requests
from pprint import pprint


"""
Instruções para TODOS os exercícios/funções abaixo:
1. Veja as instruções de como instalar o treinador e os testes no documento entregue junto com este arquivo.
2. Se um determinado parâmetro de uma função deve ser inteiro, então esta função deve rejeitar valores não-numéricos ou numerais não-inteiros nesse parâmetro.
3. Da mesma forma, se um parâmetro de uma função deve ser uma string, então esta função deve rejeitar valores que não sejam do tipo string nesse parâmetro.
4. Strings em branco são sempre consideradas inválidas.
5. Todos os nomes de pokémons que aparecerem como parâmetros devem ser aceitos em minúsculas, MAIÚSCULAS ou até mesmo MiStUrAdO. Lembre-se dos métodos lower() e upper() da classe string.
6. Todos os nomes de pokémons, cores, jogos, movimentos, etc. recebidos e devolvidos pela PokeAPI estão em letras minúsculas e assim devem ser mantidas.

Alguns exemplos de URLs que podem servir de inspiração:
http://pokeapi.co/api/v2/

http://pokeapi.co/api/v2/pokemon/39/
http://pokeapi.co/api/v2/pokemon/jigglypuff/

http://pokeapi.co/api/v2/pokemon-species/39/
http://pokeapi.co/api/v2/pokemon-species/jigglypuff/

http://pokeapi.co/api/v2/evolution-chain/11/
http://pokeapi.co/api/v2/growth-rate/1/
http://pokeapi.co/api/v2/pokemon-color/2/
"""

"""
Não altere esta URL. Ela é utilizada para conectar no PokeAPI.
"""
site_pokeapi = "https://pokeapi.co"

"""
Vamos precisar destas quatro exceções personalizadas.
Abaixo, criamos excessões com nomes personalizados.
"""

class PokemonNaoExisteException(Exception):
    pass #nao faça nada aqui nem nas Exceptions seguintes
         # ela já está pronta, só é um "nome" novo

class PokemonNaoCadastradoException(Exception):
    pass

class TreinadorNaoCadastradoException(Exception):
    pass

class PokemonJaCadastradoException(Exception):
    pass

"""
Esta função certifica-se de que seu parâmetro é um número inteiro e lança uma ValueError se não for.
"""
def check_int(a):
    if type(a) is not int:
        raise ValueError()

"""
Esta função certifica-se de que seu parâmetro é uma string e que não está vazia e lança uma ValueError se não for.
"""
def check_str(a):
    if type(a) is not str or a == "":
        raise ValueError()



dic_cores = {
    "brown": "marrom",
    "yellow": "amarelo",
    "blue": "azul",
    "pink": "rosa",
    "gray": "cinza",
    "purple": "roxo",
    "red": "vermelho",
    "white": "branco",
    "green": "verde",
    "black": "preto"
}

dic_tipos = {
    "normal": "normal",
    "fighting": "lutador",
    "flying": "voador",
    "poison": "veneno",
    "ground": "terra",
    "rock": "pedra",
    "bug": "inseto",
    "ghost": "fantasma",
    "steel": "aço",
    "fire": "fogo",
    "water": "água",
    "grass": "grama",
    "electric": "elétrico",
    "psychic": "psíquico",
    "ice": "gelo",
    "dragon": "dragão",
    "dark": "noturno",
    "fairy": "fada"
}

"""
1. Dado o número de um pokémon, qual é o nome dele?
"""
def nome_do_pokemon(numero: int):
    check_int(numero)
    response = requests.get(f'{site_pokeapi}/api/v2/pokemon/{numero}')
    status_code = response.status_code

    if status_code == 200:
        data = response.json()
        return data['name']
    else:
        raise PokemonNaoExisteException()

"""
2. Dado o nome de um pokémon, qual é o número dele?
"""
def numero_do_pokemon(nome: str):
    check_str(nome)
    response = requests.get(f'{site_pokeapi}/api/v2/pokemon/{nome.lower()}')
    status_code = response.status_code

    if status_code == 200:
        data = response.json()
        return data['id']
    else:
        raise PokemonNaoExisteException()
    
"""
3. Dado o nome ou número de um pokémon, qual é o nome da cor (em inglês) predominante dele?
"""
def color_of_pokemon(nome):
    if isinstance(nome, str): nome = nome.lower()

    pokemon = requests.get(f'{site_pokeapi}/api/v2/pokemon-species/{nome}')
    status_code = pokemon.status_code

    if status_code == 200:
        data_pokemon = pokemon.json()
        return data_pokemon['color']['name']
    else:
        raise PokemonNaoExisteException()
    
"""
4. Dado o nome de um pokémon, qual é o nome da cor (em português) predominante dele?
Os nomes de cores possíveis em português são "marrom", "amarelo", "azul", "rosa", "cinza", "roxo", "vermelho", "branco", "verde" e "preto".
No entanto, a pokeapi ainda não foi traduzida para o português! Como você pode dar um jeito nisso?
"""
def cor_do_pokemon(nome: str):
    check_str(nome)
    
    pokemon = requests.get(f'{site_pokeapi}/api/v2/pokemon-species/{nome.lower()}')
    status_code = pokemon.status_code

    if status_code == 200:
        data_species = pokemon.json()
        cor = data_species['color']['name']
        return dic_cores[cor]
    else:
        raise PokemonNaoExisteException()

"""
5. Dado o nome de um pokémon, quais são os tipos no qual ele se enquadra?
Os nomes dos tipos de pokémons em português são "normal", "lutador", "voador", "veneno", "terra", "pedra", "inseto", "fantasma", "aço", "fogo", "água", "grama", "elétrico", "psíquico", "gelo", "dragão", "noturno" e "fada".
Todo pokémon pode pertencer a um ou a dois tipos diferentes. Retorne uma lista contendo os tipos, mesmo que haja somente um.
Se houver dois tipos, a ordem não é importante.
"""

def tipos_do_pokemon(nome: str):
    check_str(nome)
    pokemon = requests.get(f'{site_pokeapi}/api/v2/pokemon-form/{nome.lower()}')
    status_code = pokemon.status_code

    if status_code == 200:
        data_pokemon = pokemon.json()

        types = []
        tipos = []
        c = 0
        for t in data_pokemon['types']:
            types.append(t['type']['name'])
            tipos.append(dic_tipos[types[c]])
            c += 1
        return tipos
    else:
        raise PokemonNaoExisteException()
    
"""
6. Dado o nome de um pokémon, liste de qual pokémon ele evoluiu.
Por exemplo, evolucao_anterior('venusaur') == 'ivysaur'
Retorne None se o pokémon não tem evolução anterior. Por exemplo, evolucao_anterior('bulbasaur') == None
"""
def evolucao_anterior(nome: str):
    check_str(nome)
    pokemon = requests.get(f'{site_pokeapi}/api/v2/pokemon-species/{nome.lower()}')
    status_code = pokemon.status_code

    if status_code == 200:
        data_pokemon = pokemon.json()
        
        if bool(data_pokemon['evolves_from_species']) == True:
            return data_pokemon['evolves_from_species']['name']
        else:
            return None
    else:
        raise PokemonNaoExisteException()

"""
7. A medida que ganham pontos de experiência, os pokémons sobem de nível.
É possível determinar o nível (1 a 100) em que um pokémon se encontra com base na quantidade de pontos de experiência que ele tem.
Entretanto, cada tipo de pokémon adota uma curva de level-up diferente (na verdade, existem apenas 6 curvas de level-up diferentes).
Assim sendo, dado um nome de pokémon e uma quantidade de pontos de experiência, retorne o nível em que este pokémon está.
Valores negativos de experiência devem ser considerados inválidos.
dica: na URL pokemon-species, procure growth rate
"""
def nivel_do_pokemon(nome, experiencia):
    check_str(nome)
    check_int(experiencia)
    if experiencia < 0: return 'invalid'

    response = requests.get(f'{site_pokeapi}/api/v2/pokemon-species/{nome.lower()}')

    if response.status_code == 200:
        value = response.json()
        response = requests.get(value['growth_rate']['url'])

        if response.status_code == 200:
            value = response.json()
            for xp in value['levels']:
                if experiencia == xp['experience'] or experiencia > xp['experience']: level = xp['level']
        else:
            raise PokemonNaoExisteException()
    else:
        raise PokemonNaoExisteException()

    return level