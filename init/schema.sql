CREATE TABLE "players" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "nome" TEXT NOT NULL,
    "nick" TEXT NOT NULL,
    "sobrenome" TEXT NOT NULL,
    "funcao" TEXT NOT NULL
);

CREATE TABLE "partidas" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "adversario" TEXT NOT NULL,
    "data" DATETIME NOT NULL,
    "resultado" TEXT NOT NULL,
    "campeonato" TEXT NOT NULL
);

CREATE TABLE "proximas_partidas" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "adversario" TEXT NOT NULL,
    "data" DATETIME NOT NULL,
    "campeonato" TEXT NOT NULL
);

CREATE TABLE "noticias" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "titulo" TEXT NOT NULL,
    "descricao" TEXT NOT NULL,
    "data" DATETIME NOT NULL
);

CREATE TABLE "campeonatos" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "nome" TEXT NOT NULL,
    "data_inicio" DATETIME NOT NULL,
    "data_fim" DATETIME NOT NULL,
    "status" TEXT NOT NULL
);