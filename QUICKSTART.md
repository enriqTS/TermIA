# TermIA - Guia Rápido de Início 🚀

Este guia te ajudará a configurar e começar a trabalhar no projeto TermIA rapidamente.

## 📦 Passo 1: Clonar e Configurar

```bash
# Clone o repositório (ou crie a estrutura)
git clone https://github.com/seu-usuario/termia.git
cd termia

# OU crie a estrutura do zero
mkdir termia && cd termia
```

## 🏗️ Passo 2: Criar Estrutura de Diretórios

Execute estes comandos para criar toda a estrutura:

```bash
# Criar diretórios principais
mkdir -p src/{commands,ia,utils}
mkdir -p tests/fixtures
mkdir -p docs
mkdir -p examples

# Criar arquivos __init__.py
touch src/__init__.py
touch src/commands/__init__.py
touch src/ia/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

## 🐍 Passo 3: Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# OU ativar (Windows)
venv\Scripts\activate

# Verificar se ativou (deve mostrar (venv) no prompt)
which python  # Linux/Mac
where python  # Windows
```

## 📚 Passo 4: Instalar Dependências

Crie o arquivo `requirements.txt`:

```bash
cat > requirements.txt << EOF
# Core dependencies
ply==3.11

# IA Integration
openai==1.3.0
requests==2.31.0

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
colorama==0.4.6
prompt_toolkit==3.0.39

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0

# Development
black==23.11.0
flake8==6.1.0
mypy==1.7.0
EOF
```

Depois instale:

```bash
pip install -r requirements.txt
```

## 📝 Passo 5: Criar Arquivos Base

### 5.1 Arquivo `.gitignore`

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
.Python
*.egg-info/
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp

# TermIA
.termia_history
config.yaml
.env

# PLY
parser.out
parsetab.py

# Tests
.pytest_cache/
.coverage
htmlcov/
EOF
```

### 5.2 Arquivo `.env.example`

```bash
cat > .env.example << 'EOF'
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Ollama Configuration (alternative)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2

# TermIA Configuration
TERMIA_HISTORY_SIZE=100
TERMIA_DEBUG=false
EOF
```

## 💻 Passo 6: Copiar Código do Lexer

Copie o código do lexer para `src/lexer.py` (o código já foi fornecido anteriormente).

## ✅ Passo 7: Testar o Lexer

### 7.1 Copiar os testes

Copie o arquivo `test_lexer.py` para `tests/` (código já fornecido).

### 7.2 Executar testes

```bash
# Executar todos os testes
pytest tests/ -v

# Executar apenas testes do lexer
pytest tests/test_lexer.py -v

# Executar com cobertura
pytest tests/ --cov=src --cov-report=html
```

### 7.3 Testar manualmente

```bash
# Executar o lexer em modo debug
cd src
python lexer.py
```

## 🔧 Passo 8: Configurar Git

```bash
# Inicializar repositório
git init

# Adicionar arquivos
git add .

# Primeiro commit
git commit -m "feat: configuração inicial do projeto TermIA com lexer"

# Adicionar repositório remoto
git remote add origin https://github.com/seu-usuario/termia.git

# Push inicial
git branch -M main
git push -u origin main
```

## 📋 Checklist da Entrega Parcial (25/10)

Para a entrega parcial, você precisa ter:

- [ ] ✅ Estrutura de diretórios criada
- [ ] ✅ `requirements.txt` configurado
- [ ] ✅ Ambiente virtual funcionando
- [ ] ✅ `src/lexer.py` implementado e testado
- [ ] ✅ `tests/test_lexer.py` com testes passando
- [ ] ✅ `docs/commands_spec.md` (gramática definida)
- [ ] ✅ `.gitignore` configurado
- [ ] ✅ Repositório Git inicializado
- [ ] 🔄 `src/parser.py` implementado (próximo passo)
- [ ] 🔄 `tests/test_parser.py` com testes
- [ ] ✅ `README.md` com documentação básica

## 🎯 Próximos Passos (Semana 3)

Agora que o lexer está pronto, os próximos passos são:

1. **Implementar o Parser (src/parser.py)**
   - Usar PLY yacc
   - Definir regras gramaticais
   - Criar AST (Abstract Syntax Tree)

2. **Definir AST Nodes (src/ast_nodes.py)**
   - Classes para cada tipo de comando
   - Estrutura de dados para representar comandos

3. **Testes do Parser (tests/test_parser.py)**
   - Testar parsing de todos os comandos
   - Validar estrutura da AST

## 🐛 Resolução de Problemas Comuns

### Problema: PLY não está instalando

```bash
# Tente instalar explicitamente
pip install ply==3.11

# Verifique a versão do Python
python --version  # Deve ser 3.8+
```

### Problema: Testes não encontram o módulo src

```bash
# Execute os testes do diretório raiz
cd /caminho/para/termia
pytest tests/

# OU adicione o diretório ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest tests/
```

### Problema: Import errors no lexer

Certifique-se de que:
- O ambiente virtual está ativado
- PLY está instalado: `pip list | grep ply`
- Os arquivos `__init__.py` existem nos diretórios

## 📖 Recursos Úteis

### Documentação PLY
- [PLY Documentation](https://www.dabeaz.com/ply/ply.html)
- [PLY Tutorial](https://www.dabeaz.com/ply/PLY.pdf)

### Compiladores
- [Compilers: Principles, Techniques and Tools](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools)
- [Crafting Interpreters](https://craftinginterpreters.com/)

### Python Testing
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://realpython.com/pytest-python-testing/)

## 🎓 Dicas de Produtividade

### Use um Makefile

Crie um `Makefile` para automatizar tarefas:

```makefile
.PHONY: test install run clean

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=html

run:
	python main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "parser.out" -delete
	rm -rf .pytest_cache htmlcov

format:
	black src/ tests/

lint:
	flake8 src/ tests/
```

Uso:
```bash
make install  # Instalar dependências
make test     # Executar testes
make clean    # Limpar arquivos temporários
```

### Use VSCode com extensões

Extensões recomendadas:
- Python (Microsoft)
- Pylance
- Python Test Explorer
- GitLens
- Better Comments

## ✨ Comandos Úteis do Dia a Dia

```bash
# Ver status do Git
git status

# Criar nova branch para feature
git checkout -b feature/parser

# Executar testes específicos
pytest tests/test_lexer.py::TestTermIALexer::test_ls_simple -v

# Ver cobertura de testes
pytest tests/ --cov=src --cov-report=term-missing

# Formatar código
black src/ tests/

# Verificar estilo
flake8 src/

# Adicionar e commitar
git add .
git commit -m "feat: implementa parser básico"
```

## 💡 Exemplo de Sessão de Trabalho

```bash
# 1. Ativar ambiente
source venv/bin/activate

# 2. Criar branch
git checkout -b feature/minha-feature

# 3. Fazer modificações
# ... editar código ...

# 4. Testar
pytest tests/ -v

# 5. Formatar
black src/ tests/

# 6. Commit
git add .
git commit -m "feat: adiciona nova funcionalidade"

# 7. Push
git push origin feature/minha-feature
```

---

**Pronto!** 🎉 Agora você tem tudo configurado para começar a trabalhar no TermIA.

Dúvidas? Consulte o [README.md](README.md) ou a [documentação completa](docs/).