#%%
'''
            Mini-Proiect Inteligenta Artificiala

    Cerinta: Rezolvati problema 8-puzzle folosind un algoritm de cautare neinformata si un algoritm de cautare informata.

    Pentru cautarea neinformata, am ales algoritmul BFS (breadth-first search)

    Pentru cautarea informata, am ales algoritmul A*.
    
'''

#%%

    # Functiile de baza pentru puzzle


# find_empty(puzzle) gaseste spatiul liber din puzzle si returneaza pozitia acestuia

def find_empty(puzzle):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                return i, j

# fucntia gen_stari(puzzle) genereaza starile posibile pentru puzzle

def gen_stari(puzzle):

    # Functie aux pentru interschimbarea pozitiilor a doua piese in puzzle
    def swap_piese(puzzle, i1, j1, i2, j2):

        new_puzzle = [row[:] for row in puzzle]
        new_puzzle[i1][j1], new_puzzle[i2][j2] = new_puzzle[i2][j2], new_puzzle[i1][j1]

        return new_puzzle

    empty_i, empty_j = find_empty(puzzle)
    mutari = []

    mutari_posibile = [
        (empty_i - 1, empty_j),   # mutare in sus
        (empty_i + 1, empty_j),   # mutare in jos
        (empty_i, empty_j - 1),   # mutare la stanga
        (empty_i, empty_j + 1)    # mutare la dreapta
    ]

    for mutare in mutari_posibile:
        new_i, new_j = mutare
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            mutari.append(swap_piese(puzzle, empty_i, empty_j, new_i, new_j))

    return mutari
    
#%%

    # BFS

def bfs(stare_initiala, stare_scop):

    coada = [] 
    coada.append((stare_initiala, []))
    visited = set()
    visited.add(tuple(tuple(row) for row in stare_initiala))

    while coada:
        stare_curenta, drum = coada.pop(0)
        
        if stare_curenta == stare_scop:
            return drum
        
        mutari_urmatoare = gen_stari(stare_curenta)
        for mutare in mutari_urmatoare:
            mutare_tuple = tuple(tuple(row) for row in mutare)
            if mutare_tuple not in visited:
                visited.add(mutare_tuple)
                coada.append((mutare, drum + [mutare]))
    
    return None


#%%

    # Functiile euristice

'''
            Functia euristica Manhattan estimeaza costul minim pentru a ajunge de la o stare curenta catre
        starea finala, folosind suma distantelor de pe axa orizontala, respectiv axa verticala, intre
        pozitia fiecarui element si pozitia sa corecta

'''

def manhattan(stare_curenta, stare_scop):
    
    distanta = 0
    
    for i in range(len(stare_curenta)):  
        for j in range(len(stare_curenta[0])):
            if stare_curenta[i][j] != 0:
                piesa = stare_curenta[i][j]
                for linie in range(len(stare_scop)):
                    if piesa in stare_scop[linie]:
                        coloana = stare_scop[linie].index(piesa)
                        distanta += abs(linie - i) + abs(coloana - j)
    
    return distanta


'''
            Functia euristica a pieselor plasate gresit numara cate piese nu sunt in pozitia corecta in raport cu starea finala, 
        oferind o estimare a costului de mutare pentru a ajunge la starea dorita.

'''

def pozitie_gresita(stare_curenta, stare_scop):

    gresite = 0

    for i in range(len(stare_curenta)):
        for j in range(len(stare_curenta[0])):
            if stare_curenta[i][j] != stare_scop[i][j] and stare_curenta[i][j] != 0:
                gresite += 1

    return gresite
 


#%%

    # A*

def a_star(stare_initiala, stare_scop, euristica):

    open_set = [(euristica(stare_initiala, stare_scop), 0, stare_initiala, [])]
    closed_set = set()

    while open_set:
        _, cost, stare_curenta, drum = min(open_set)
        open_set.remove((euristica(stare_curenta, stare_scop) + cost, cost, stare_curenta, drum))
        closed_set.add(tuple(tuple(linie) for linie in stare_curenta))

        if stare_curenta == stare_scop:
            return drum

        mutari_urmatoare = gen_stari(stare_curenta)
        for mutare in mutari_urmatoare:
            if tuple(tuple(linie) for linie in mutare) not in closed_set:
                open_set.append((euristica(mutare, stare_scop) + cost + 1, cost + 1, mutare, drum + [mutare]))


    return None
        
#%%

    # Functia de afisare in consola a drumului parcurs

def afisare(puzzle, drum):

    mutari_dict = {
        (-1, 0) : 'Mutare in sus',
        (1, 0) : 'Mutare in jos',
        (0, -1) : 'Mutare la stanga',
        (0, 1) :  'Mutare la dreapta'
    }

    stare_curenta = puzzle[:]
    print("0.Stare initiala:")
    for l in stare_curenta:
        print(l)
    print()


    for i in range(len(drum)):
        stare_anterioara = stare_curenta[:]
        stare_curenta = drum[i][:]

        empty_i_curr, empty_j_curr = find_empty(stare_anterioara)
        empty_i_next, empty_j_next = find_empty(stare_curenta)

        diff_i = empty_i_next - empty_i_curr
        diff_j = empty_j_next - empty_j_curr 

        mutare = mutari_dict[(diff_i, diff_j)]

        print(f"{i+1}.{mutare}")
        for l in stare_curenta:
                print(l)
        print()

    print("Stare finala: ")
    for l in drum[-1]:
        print(l)

    

#%%

    # Stare scop

stare_scop1 = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]
            ]

stare_scop2 = [
                [1, 2, 3],
                [8, 0, 4],
                [7, 6, 5]
            ]

def alegere_stare_scop():
    optiune = input(f"Introduceți starea scop dorită, \n1 pentru:\n{stare_scop1}\n2 pentru:\n{stare_scop2}\nOptiune: ")
    return optiune

def alegere_algoritm():
    optiune = input(f"Introduceti algoritmul dorit: 1 pentru BFS, 2 pentru A*   ")
    return optiune

def alegere_euristica():
    
    optiune = input("Introduceti functia euristica dorita: 1 pentru Distanta Manhattan, 2 pentru Piese Plasate Gresit   ")
    return int(optiune)


#%%



def main():

    def input_puzzle():
        
        puzzle = []

        print("Introduceti puzzle-ul initial (cate o linie, cu elementele separate prin spatiu):")

        for _ in range(3):
            linie = list(map(int, input().split()))
            puzzle.append(linie)

        return puzzle
    
    puzzle = input_puzzle()
    
    alegere_scop = int(alegere_stare_scop())
    if alegere_scop == 1:
        stare_scop = stare_scop1
    else:
        stare_scop = stare_scop2

    alegere_algo = int(alegere_algoritm())
    
    if alegere_algo == 1:
        if bfs(puzzle, stare_scop): 
            print("BFS (breadth-first search): \n")
            drum_bfs = bfs(puzzle, stare_scop)
            afisare(puzzle, drum_bfs)
        else:
            print('Nu exista solutie')

    else:
        print("A*: ")

        alegere_eur = int(alegere_euristica())
        
        if alegere_eur == 1:
            
            print("Functia euristica aleasa: Distana Manhattan")
            if a_star(puzzle, stare_scop, manhattan):
                drum_astar = a_star(puzzle, stare_scop, manhattan)
                afisare(puzzle, drum_astar)
            else:
                print('Nu exista solutie')

        else:

            print("Functia euristica aleasa: Piese pozitionate gresit")
            if a_star(puzzle, stare_scop, pozitie_gresita):
                drum_astar = a_star(puzzle, stare_scop, pozitie_gresita)
                afisare(puzzle, drum_astar)
            else:
                print('Nu exista solutie')
            drum_astar = a_star(puzzle, stare_scop, pozitie_gresita)
            afisare(puzzle, drum_astar)
            

#%%
    # Rularea programului

main()
