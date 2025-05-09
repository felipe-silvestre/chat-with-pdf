# 🧠 Chat com PDF — Atendente Virtual com Memória

Um app open-source onde você conversa com PDFs usando IA — com voz, contexto e uma atendente virtual animada.

## 📦 Tecnologias Utilizadas

- **Frontend**: HTML + JavaScript + Web Speech API
- **Backend**: FastAPI + LangChain + OpenAI + FAISS
- **Parsing de PDF**: PyPDF
- **Memória**: ConversationalRetrievalChain com LangChain

---

## 🚀 Como Rodar Localmente

### 🔁 Backend

1. Clone este repositório e entre na pasta do backend:

```bash
git clone https://github.com/seu-usuario/chat-with-pdf.git
cd chat-with-pdf/backend
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Copie o arquivo `.env.example` para `.env` e adicione sua chave da OpenAI:

```bash
cp .env.example .env
```

Conteúdo esperado do `.env`:
```env
OPENAI_API_KEY=sk-sua-chave-aqui
```

4. Rode o servidor:

```bash
uvicorn main:app --reload
```

O backend estará rodando em: `http://localhost:8000`

---

### 🎨 Frontend

1. Navegue até a pasta `frontend/`
2. Abra o arquivo `index.html` no navegador

> Recomendado usar Google Chrome para melhor suporte a voz (SpeechRecognition + SpeechSynthesis)

---

## 🧪 Recursos

- ✅ Upload de arquivos PDF
- ✅ Reconhecimento de fala (usuário fala com a atendente)
- ✅ Atendente responde com voz e balão de fala
- ✅ Memória de conversa entre perguntas

---

## 🤝 Contribuição

Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutirmos o que você gostaria de modificar.

---

## 🧑‍💻 Autor

Desenvolvido com ❤️ por Felipe Silvestre
Baseado em explorações com LangChain, FastAPI e OpenAI.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT — veja o arquivo LICENSE para mais detalhes.
