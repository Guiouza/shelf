# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

import sqlite3 as sql
import os

BASE_DIR = __file__.removesuffix('\\shelf.py')
print(BASE_DIR)

DATABASE_FILE = os.path.join(BASE_DIR, 'db/data.db')
SCHEMAS_DIR = os.path.join(BASE_DIR, 'schemas')
DATA_FILE =  os.path.join(BASE_DIR, '.data/mangas')

HELP_MSG = """Commands:
    .a    ADD NEW MANGA TO DATABASE
    .b    BUILD DATABASE FROM A DATA FILE
    .c    CLEAR THE TERMINAL
    .q    QUIT SHELF TERMINAL
    .u    UPDATE MANGAS IN THE DATABASE
    .r    REMOVE A MANGA

As a shortcut for updating single mangas, you can just type its name if it doesn't start with a . (dot) character."""

class Manga:
    def __init__(self, n, c, s):
        self.nome = n
        self.cap = c
        self.status = s
        self.data = {
            'nome': self.nome,
            'capitulo': self.cap,
            'status': self.status
        }
    
    def check(self):
        if self.nome is not str or self.nome == '':
            return False
        if self.cap is not int or self.cap < 0:
            return False
        if self.status not in ['lendo', 'novo', 'terminado', 'dropado']:
            return False
        return True

def update(con, mangas=None):
    cur = con.cursor()

    if mangas is None:
        cur.execute('SELECT nome FROM mangas ORDER BY nome')
        mangas = cur.fetchall()

    i = 1
    for nome in mangas:
        print(f'\t{i}: {nome[0]}')
        i += 1
    
    while (indicie := input('Qual manga deseja atualizar: ')).isnumeric():
        indicie = int(indicie) - 1
        if indicie >= len(mangas) or indicie < 0:
            print('Erro de parâmetro! Selecione um dos mangas enumerados abaixo ou faça uma nova pesquisa:')
            i = 1
            for nome in mangas:
                print(f'\t{i}: {nome[0]}')
                i += 1
            continue

        cur.execute("SELECT * FROM mangas WHERE nome = ?", mangas[indicie])
        manga = cur.fetchall()[0]

        print(f'\tnome: {manga[0]}')
        print(f'\tcapitulo: {manga[1]}')
        print(f'\tstatus: {manga[2]}')

        nome = input('\t\tnome: ')
        capitulo = input('\t\tcapitulo: ')
        status = input('\t\tstatus: ')

        update = [nome, capitulo, status]
        if nome == '':
            update[0] = manga[0]
        if capitulo == '':
            update[1] = manga[1]
        if status == '':
            update[2] = manga[2]
        
        if update:
            cur.execute(
                "UPDATE mangas SET nome = ?, capitulo = ?, status =? WHERE nome = ?",
                update + [manga[0]]
            )
            con.commit()
        else:
            print('\t\tNada foi atualziado.')
    
    cur.close()

def ensure_tables_are_created(con: sql.Connection):
    for file in os.scandir(SCHEMAS_DIR):
        if file.is_file() and file.name.endswith('.sql'):
            with open(file.path) as f:
                con.executescript(f.read())

def build_database_from_datafile(con, data_file):    
    with open(data_file) as file:
        pattern = file.readline()
        sep, *labels = pattern.split()

        data = []
        for line in file:
            line = line.removesuffix('\n')
            content = line.split(sep)

            data_object = {}
            for key, value in zip(labels, content):
                data_object.setdefault(key,value)

            data.append(data_object)

    con.executemany('INSERT OR IGNORE INTO mangas (nome, capitulo) VALUES (:nome, :capitulo)', data)
    con.commit()

def remove(con, manga):
    pass

def main(con: sql.Connection):
    print("Use .<command> to run specific operations.\nHELP: .h\n")
    while True:
        res = input('>> ')

        if res == '.h':
            print(HELP_MSG)

        if res == '.b':
            filename = input('\tfile: ')
            build_database_from_datafile(con, filename)

        elif res == '.u':
            update(con)

        elif res == '.a':
            cur = con.cursor()

            while (input('Adicionar mangá à base de dados [y/N]? ') == 'y'):
                nome = input('\t\tnome: ')
                capitulo = int(input('\t\tcapitulo: '))
                status = input('\t\tstatus: ')

                manga = Manga(nome, capitulo, status)
                
                if manga.check():
                    cur.execute(
                        "INSERT OR IGNORE INTO mangas VALUES(:nome, :capitulo, :status)",
                        manga.data
                    )
                    con.commit()
                else:
                    print('\t\tNada foi adicionado')

            cur.close()

        elif res == '.q':
            break
        
        elif res == '.c':
            os.system('cls')
        
        elif res == '.r':
            print('\tRemove a manga from the database.')

        elif res: #search
            mangas = []
            cur = con.cursor()
            cur.execute('SELECT nome FROM mangas WHERE nome LIKE ? ORDER BY nome', ['%'+res+'%', ])
            mangas = cur.fetchall()
            cur.close()

            if len(mangas) == 0:
                print('\tNo manga find with this name.')
                continue
            update(con, mangas)

if __name__ == '__main__':
    con = sql.connect(DATABASE_FILE)

    ensure_tables_are_created(con)

    try:
        main(con)
    except Exception as e:
        raise e
    finally:
        con.close()
