# 🤖 Bot de Subir App

Este projeto é um bot que automatiza o processo de subir e configurar um aplicativo. A estrutura é dividida em duas partes:

- `front-end`: Interface para interação com o usuário.
- `back-end`: Lógica de automação em Python para gerenciamento e publicação do app.

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- **Node.js** instalado (versão 16 ou superior recomendada)
- **Python 3.8+** instalado

---

### 🖥️ Rodando o Front-end

1. Abra o terminal.
2. Acesse a pasta do front-end:

   ```bash
   cd front-end
   ```

3. Instale as dependências (se for a primeira vez):

   ```bash
   npm install
   ```

4. Inicie a aplicação:

   ```bash
   npm run dev
   ```

5. Durante a execução, o sistema solicitará algumas informações:
   - **URL do app**: Exemplo: `https://inacio.ibsystem.com.br/app_corretor`
   - **google-services.json**: Será necessário mover este arquivo para a pasta correta do app após o build.
   - **Logo**: Caminho da imagem que será usada como logotipo do app.
   - **Pacote do app**: Formato: `com.ibsystem.nomedoapp`
   - **Nome do app**: Nome curto e sem espaços.

---

### ⚙️ Rodando o Back-end

1. Abra um novo terminal.
2. Acesse a pasta do back-end:

   ```bash
   cd back-end
   ```

3. Execute o script principal:

   ```bash
   python app.py
   ```

   ⚠️ **Importante:** O terminal pode solicitar uma confirmação (ex: "sim ou não"). Quando isso acontecer, apenas digite `sim` e pressione Enter.

---

## 🧩 Configurações Finais Após Execução

Depois que o app for gerado, siga os passos abaixo para finalizar a configuração:

1. Substitua as **imagens padrão** pelas imagens do seu app.
2. Adicione o **ícone de notificação**.
3. Execute o comando:

   ```bash
   eas init-id{o id do app criado na expo dev}
   ```

   Esse comando é essencial para configurar corretamente a identidade do app antes da publicação.

---

## 📁 Estrutura do Projeto

```
projeto-bot/
├── front-end/         # Interface em React ou Vite
├── back-end/          # Automação em Python
└── README.md          # Documentação
```

---

## 👨‍💻 Autor

Desenvolvido por **Inácio Santana**.

---

## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT. Veja os detalhes abaixo.

---

# Licença MIT (MIT License)

Copyright (c) 2025  
Inácio Santana

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in  
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN  
THE SOFTWARE.
