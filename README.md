# GFSystem

Bem-vindo ao **GFSystem**, um sistema simples e eficiente desenvolvido em **Django** para gerenciar suas matérias e acompanhar suas faltas ao longo do período letivo. O sistema fornece relatórios visuais e alertas sobre o percentual de faltas, ajudando você a evitar reprovações por excesso de faltas.

---

## **Funcionalidades**

- **Cadastro de Matérias:**
  - Permite adicionar nome, descrição, carga horária, dias da semana e faltas iniciais.
  
- **Dashboard Intuitivo:**
  - Exibe todas as matérias com informações detalhadas, incluindo:
    - Nome da matéria.
    - Descrição (opcional).
    - Carga horária total.
    - Dias da semana.
    - Faltas registradas e seu percentual em relação ao limite permitido.
    - Status com alertas:
      - **Verde**: "Tá de boa" (baixo percentual de faltas).
      - **Amarelo**: "Melhor não faltar" (fique atento!).
      - **Laranja**: "Mais um reprova" (alto risco de reprovação).
      - **Vermelho**: "Reprovou mn" (acima do limite permitido).

- **Gestão de Faltas:**
  - Adicione faltas diretamente no dashboard com apenas um clique.

- **Edição e Exclusão de Matérias:**
  - Atualize ou remova informações de uma matéria existente.

- **Finalizar Período:**
  - Botão dedicado para excluir todas as matérias cadastradas e começar um novo período letivo.

---

## **Pré-requisitos**

Certifique-se de ter os seguintes itens instalados no seu ambiente:

- Python 3.8+
- Django 4.2+
- Banco de dados (SQLite ou outro configurado no Django).

---

## **Instalação**

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/Cromablue/GFSystem.git
   cd GFSystem
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realize as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

6. **Acesse o sistema:**
   - Abra o navegador e acesse: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## **Estrutura do Sistema**

- **Modelos:**
  - `Materia`: Gerencia os dados das matérias, cálculo do limite de faltas e validações.

- **Views:**
  - `dashboard`: Exibe a lista de matérias e as interações possíveis.
  - `adicionar_materia`: Página para criar novas matérias.
  - `editar_materia`: Atualizar os dados de uma matéria.
  - `adicionar_faltas`: Incrementa as faltas de uma matéria.
  - `remover_materia`: Remove uma matéria específica.
  - `finalizar_periodo`: Remove todas as matérias do usuário atual.

- **Templates:**
  - Arquivos HTML organizados para fácil manutenção e extensão.

---

## **Uso**

1. **Adicionar uma Matéria:**
   - Vá até o botão "Adicionar Matéria" no dashboard.
   - Preencha os campos necessários (nome, carga horária, etc.).
   - Clique em "Salvar".

2. **Acompanhar Faltas:**
   - No dashboard, visualize o percentual de faltas e os alertas correspondentes.

3. **Adicionar Faltas:**
   - Clique no botão vermelho **"Faltei :("** para incrementar as faltas.

4. **Editar ou Remover Matérias:**
   - Utilize os botões "Editar" e "Remover" na matéria correspondente.

5. **Finalizar Período:**
   - Clique no botão **"Finalizar Período"** para excluir todas as matérias e começar do zero.

---

## **Personalização**

- **Estilização:**
  - O sistema utiliza Bootstrap para estilização responsiva.
  - Edite os templates localizados em `templates/` para personalizar a aparência.

- **Mensagens de Status:**
  - Mensagens como "Tá de boa" ou "Reprovou mn" podem ser alteradas diretamente no arquivo de templates do dashboard.

---

## **Contribuição**

1. Faça um fork deste repositório.
2. Crie uma nova branch:
   ```bash
   git checkout -b feature/minha-nova-feature
   ```
3. Realize suas alterações e commit:
   ```bash
   git commit -m "Adiciona minha nova feature"
   ```
4. Envie as alterações:
   ```bash
   git push origin feature/minha-nova-feature
   ```
5. Abra um pull request.

---

## **Licença**

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

## **Contato**

- Desenvolvedor: [José Santo de Moura Neto](https://github.com/cromablue)
- Email: jsmoura.dev@gmail.com

---
