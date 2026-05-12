# G2_GREEDY_PA-26.1

Conteúdo da Disciplina: Algoritmos Ganaciosos

## Alunos
| Matrícula | Aluno |
| -- | -- |
| 231011533 | João Maurício Pilla Nascimento |
| 231035446 | Lucas Monteir Freitas |

## Sobre
O projeto é um gerenciador de tarefas que busca, via algortimos de *Interval Scheduling*, *Interval Partitioning* e *Minimize Lateness*, montar um plano semanal para maximizar sua entrega de tarefas.

No backend, o sistema pega o conjunto de tarefas a ele passado, aplica os algoritmos ganaciosos sobre eles e monta a agenda otimizada.

O frontend consome esses dados e exibe uma interface para visualizar uma agenda com a distribuição de tarefas maximizadas para maior "completude", respeitandos os *deadlines*.

## Screenshots
![Tela de chegada](x.png)
![Tela de pesquisa](y.png)
![Mapa de influencia](z.png)

## Instalação
Linguagem: Python e TypeScript
Framework: FastAPI e React + Vite

### Pré-requisitos

- Python 3.8 ou superior
- Node.js 20 ou superior
- npm 10 ou superior

### Backend

Na raiz do projeto, execute:

```bash
source venv/bin/activate
```

Seguido por:

```bash
pip install -r requirements.txt
```

E:

```bash
uvicorn src.api:app --reload
```

Esse comando:

- cria o ambiente virtual `venv`;
- instala as dependências do backend listadas em `requirements.txt`;
- e inicia a API FastAPI em `http://127.0.0.1:8000`.

### Frontend

Em outro terminal, execute:

```bash
cd frontend
npm install
npm run dev
```

O frontend ficará disponível no endereço informado pelo Vite, normalmente `http://127.0.0.1:5173`.

## Vídeo