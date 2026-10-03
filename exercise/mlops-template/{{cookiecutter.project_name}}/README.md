# {{cookiecutter.project_name}}

Autor: {{cookiecutter.author_name}}

Projeto gerado como parte do exercício de modularização do curso de MLOps.

## Estrutura

```
{{cookiecutter.project_name}}/
├── data/
│   └── raw/
│       └── points.csv       # gerado pelo generate_data.py
├── src/
│   ├── data.py              # carregamento e preparação dos dados
│   ├── train.py             # treinamento do modelo
│   ├── evaluate.py          # avaliação do modelo
│   └── predict.py           # predição
├── outputs/
│   └── metrics.json         # gerado pelo main.py
├── generate_data.py
├── main.py
└── requirements.txt
```

## Como executar

1. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Gerar os dados:
   ```bash
   python generate_data.py
   ```

3. Implementar os módulos em `src/` (ver enunciado do exercício)

4. Executar o pipeline:
   ```bash
   python main.py
   ```

## Como subir no GitHub

Usando HTTP:

```bash
git init
git add .
git commit -m "exercicio de modularizacao"
git remote add origin https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

OU usando SSH:
```bash
git init
git add .
git commit -m "exercicio de modularizacao"
git remote add origin git@github.com:{{cookiecutter.github_username}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

O repositório deve ser **público** para que a correção automática funcione.
