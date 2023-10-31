# BD2-Log-Undo

Uma **descrição detalhada do Projeto** pode ser conseguida [AQUI](descricao_TP2_log.pdf)!

## Alunos 

Lênisson Nasiloski Bebber - [GitHub](https://github.com/LenissonNasiloski)

Luiz Paulo Grafetti Terres - [GitHub](https://github.com/luizpgt)

# Execute esse código na sua máquina

## Preparando o ambiente local

Clone este repositório:
```
git clone https://github.com/luizpgt/BD2-Log-Undo.git
```

Habilite seu Ambiente Virtual Python:
```
python -m venv env && source env/bin/activate
```

Abra o diretório do repositório:
```
cd BD2-Log-Undo/
```

Instação das dependências com PIP
```
pip install -r requirements.txt
```

## Ajustando os arquivos de configuração

Altere as devidas informações de conexão com o PostgreSQL dentro no arquivo `database.ini`
```
vim database.ini
```
`ps:` o arquivo database.ini leva em consideração o PostgreSQL na porta padrão `5432`

`ps2:` confirme que o PostgreSQL esteja rodando. Em sistemas LINUX usando systemd pode-se usar o comando: `systemctl status postgresql`, e `systemctl start postgresql` o inicia, caso esteja desabilitado.

Crie o seu arquivo de variáveis de ambiente com base no exemplo disponibilizado
```
mv example.env .env
```

## Execute o código !

```
python main.py
```

Considerando alguns casos de entrada metadata.json possíveis:
```
{
    "table": {
        "id":[1,2],
        "A":[24,20],
        "B":[55,30]
    }
}
```

```
{
    "table": {
        "id":[1,2, 3],
        "A":[24, 20, 10],
        "B":[55, 30, 20],
	"C":["luiz", "paulo", "lenin"]
    }
}
```

```
{
    "table": {
        "id":[1,2, 3],
        "A":[24, null, 10],
        "B":[55, 30],
	"C":["luiz", "paulo", "lenin"]
    }
}
```

E o seguinte LOG para todos os metadata.json:
```
<start T1>
<T1,1, A,20>
<start T2>
<commit T1>
<START CKPT(T2)>
<T2,2, B,20>
<commit T2>
<END CKPT>
<start T3>
<start T4>
<T4,1, B,555>
```

As saídas esperadas são respectivamente:
```
"Transação T4 realizou UNDO"
"Transação T3 realizou UNDO"
{
    "t": {
        "id": [
            1,
            2
        ],
        "A": [
            24,
            20
        ],
        "B": [
            555,
            30
        ]
    }
}
```

```
"Transação T4 realizou UNDO"
"Transação T3 realizou UNDO"
{
    "t": {
        "id": [
            1,
            2,
            3
        ],
        "A": [
            24,
            20,
            10
        ],
        "B": [
            555,
            30,
            20
        ],
        "C": [
            "luiz",
            "paulo",
            "lenin"
        ]
    }
}

```

```
"Transação T4 realizou UNDO"
"Transação T3 realizou UNDO"
{
    "t": {
        "id": [
            1,
            2,
            3
        ],
        "A": [
            24,
            null,
            10
        ],
        "B": [
            555,
            30,
            null
        ],
        "C": [
            "luiz",
            "paulo",
            "lenin"
        ]
    }
}
```
