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

A saída esperada para esse programa é similar a: 
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
