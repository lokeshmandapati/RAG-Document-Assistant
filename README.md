📚 # RAG-Document-Assistant
An intelligent Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions from them using AI.

Built with Streamlit + LangChain + Groq + ChromaDB, this project enables fast and accurate document-based question answering.

🚀 Features
📄 Supports multiple file formats:

PDF

TXT

DOCX

CSV

🧠 AI-powered question answering using:

Vector embeddings

Semantic search

LLM (Groq)

⚡ Fast retrieval with Chroma Vector Database

🔄 Two AI response styles:

🤖 System AI → structured, precise, formal

🧑 Human AI → friendly, conversational, easy to understand

📊 Smart document chunking & retrieval using MMR (Maximal Marginal Relevance)

🧠 How It Works
Upload File → Chunking → Embeddings → Vector DB (Chroma)
                                      ↓
User Query → Retrieval → Context → Groq LLM → Answer
🛠️ Tech Stack
Frontend: Streamlit

LLM: Groq (LLaMA models)

Embeddings: HuggingFace (all-MiniLM-L6-v2)

Vector DB: ChromaDB

Framework: LangChain

📂 Project Structure
RAG-File-Assistant/
│
├── app.py
├── chroma_db/        # (auto-generated, ignored in Git)
├── .env              # API keys (ignored)
├── .gitignore
├── requirements.txt
└── README.md
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/RAG-File-Assistant.git
cd RAG-File-Assistant
2️⃣ Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Add environment variables
Create .env file:

GROQ_API_KEY=your_groq_api_key
▶️ Run the App
streamlit run app.py
📌 Usage
Upload a document (PDF, TXT, DOCX, CSV)

Click "Create Vector Database"

Choose AI mode:

System AI (structured)

Human AI (friendly)

Ask questions about the document

🧪 Example
Input:
"What is the leave policy?"

Output:
Relevant extracted context

AI-generated answer based only on document

⚡ Optimization Features
Efficient chunking using RecursiveCharacterTextSplitter

Semantic search using MMR

Fast inference using Groq API

Persistent vector storage using ChromaDB

🔒 Security Best Practices
.env file is ignored (API keys protected)

chroma_db/ is ignored (prevents data leakage)

No hardcoded credentials

📈 Future Improvements
🔹 Add user authentication

🔹 Cloud deployment (Streamlit Cloud / AWS)

🔹 Support for image & multimodal RAG

🔹 Use faster embeddings (OpenAI / GPU)

🔹 Add chat history memory

🌟 Key Highlights (For Resume)
Built a RAG-based AI system for document Q&A

Integrated LLM + Vector Database + Retrieval pipeline

Implemented multi-format document processing

Designed dual AI persona system (System vs Human AI)

Optimized retrieval using MMR search strategy

🤝 Contributing
Feel free to fork this repo and improve it.

📜 License
This project is for educational and demonstration purposes.

👨‍💻 Author
Lokesh Mandapati
AI & Data Enthusiast 🚀

⭐ If you like this project
Give it a ⭐ on GitHub!

