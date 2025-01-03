# 📄 DocsTalker - Analisador de PDFs

Ferramenta interativa para análise e conversação com documentos PDF utilizando modelos de linguagem avançados e interface Streamlit.

## 🎯 Funcionalidades
- Carregamento e análise de múltiplos PDFs
- Interface conversacional intuitiva
- Processamento de texto avançado com IA
- Extração inteligente de informações

## ⚙️ Pré-requisitos
- Python 3.9 ou superior
- Conta na OpenAI com chave de API
- Conexão com internet

## 🚀 Instalação
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/docsTalker.git
cd docsTalker
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
    - Copie o arquivo `.env.example` para `.env`
    - Adicione sua chave da API OpenAI e outras configurações necessárias

## 💻 Uso
1. Inicie a aplicação:
```bash
streamlit run Home.py
```

2. Acesse através do navegador (geralmente http://localhost:8501)
3. Faça upload dos PDFs desejados
4. Comece a interagir com seus documentos!

## 📁 Estrutura do Projeto
```
docsTalker/
├── Home.py            # Aplicação principal
├── pages/            # Páginas adicionais
├── utils/            # Utilitários e configurações
├── requirements.txt  # Dependências
└── .env             # Configurações locais
```

## 🤝 Contribuindo
Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas features
- Enviar pull requests

## 📝 Licença
Este projeto está sob a licença MIT.
