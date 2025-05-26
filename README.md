# Tarefa08

Essa tarefa consiste na implementação do algoritmo para detecção de ataques sanduíches  em DeFi discutido na aula sobre “front running”.

# 🚀 Detector de Ataques Sanduíche na Blockchain Ethereum

Este projeto, desenvolvido em Python, analisa blocos da blockchain Ethereum utilizando a API Infura para detectar automaticamente ataques do tipo sanduíche — uma prática maliciosa comum em exchanges descentralizadas (DEXs), onde um invasor insere duas transações antes e depois da vítima para manipular o mercado.

## ✅ Funcionalidades
- Consulta blocos da Ethereum via API Infura.
- Analisa sequências de transações para identificar padrões de ataques sanduíche.
- Gera automaticamente um relatório com os ataques detectados.

## 🛠️ Tecnologias Utilizadas
- Python 3
- Biblioteca `requests`
- API Infura

## ▶️ Como Executar
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Jaelma02/TAREFA08.git
   cd TAREFA08
2. Instale as dependências: pip install requests
3. Configure a variável INFURA_URL no código com sua chave de API da Infura (ou utilize a chave padrão).
4. Execute o script: python sand02.py
✒️ Autores
Lemuel Cavalcante
Jaelma Barbosa
Erick Macgregor
