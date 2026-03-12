CREATE TABLE IF NOT EXISTS mangas(
    nome TEXT UNIQUE,
    capitulo TEXT,
    status TEXT CHECK (status IN ('lendo', 'hiato', 'terminado', 'novo', 'dropado')) DEFAULT 'lendo'
);