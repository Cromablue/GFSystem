
# GFSystem

Bem-vindo ao **GFSystem**, um sistema simples e eficiente desenvolvido em **Django** para gerenciar suas matérias e acompanhar suas faltas ao longo do período letivo. O sistema fornece relatórios visuais e alertas sobre o percentual de faltas, ajudando você a evitar reprovações por excesso de faltas.

---

## 🚀 Funcionalidades

- **📘 Cadastro de Matérias:**  
  - Adicione nome, descrição, carga horária, dias da semana e faltas iniciais.

- **📊 Dashboard Intuitivo:**  
  - Exibe todas as matérias com informações detalhadas:
    - Nome da matéria.
    - Descrição (opcional).
    - Carga horária total.
    - Dias da semana.
    - Faltas registradas e seu percentual.
    - Status com alertas coloridos:
      - 🟢 **Verde**: "Tá de boa"
      - 🟡 **Amarelo**: "Melhor não faltar"
      - 🟠 **Laranja**: "Mais um reprova"
      - 🔴 **Vermelho**: "Reprovou mn"

- **➕ Gestão de Faltas:**  
  - Adicione faltas diretamente no dashboard com um clique.

- **✏️ Edição e 🗑️ Exclusão de Matérias:**  
  - Atualize ou remova informações de matérias.

- **🔁 Finalizar Período:**  
  - Limpe todos os dados e comece um novo período letivo.

---

## ✅ Pré-requisitos

- Python 3.8+  
- Django 4.2+  
- MariaDB (preferencialmente em cluster Galera)  
- Linux com scripts de deploy para master/slaves (opcional)

---

## ⚙️ Instalação e Deploy Automatizado

### 1. Clonar o Repositório

```bash
git clone https://github.com/Cromablue/GFSystem.git
cd GFSystem
```

### 2. Criar e Ativar Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Deploy do Cluster (Opcional)

```bash
cd deploy
chmod +x deploy.sh deploy_master.sh deploy_slave.sh
sudo ./deploy.sh
```

- Escolha o tipo de nó: Master, Slave 1 ou Slave 2.
- O script configurará IP fixo, Galera, Bind9, firewall e Django.

### 5. Rodar o Servidor Django

```bash
cd ..
source venv/bin/activate
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Acesse no navegador pelo IP do nó master na porta 8000.

---

## 🧱 Estrutura do Sistema

- **Modelos:**
  - `Materia`: armazena dados da disciplina, faltas e lógica de alerta.

- **Views:**
  - `dashboard`, `adicionar_materia`, `editar_materia`, `adicionar_faltas`, `remover_materia`, `finalizar_periodo`

- **Templates:**
  - HTMLs organizados para fácil manutenção.

---

## 💡 Como Usar

1. **Adicionar Matéria:** Clique em "Adicionar Matéria" no dashboard.
2. **Visualizar Alertas:** Veja alertas de faltas no dashboard.
3. **Registrar Faltas:** Use o botão **"Faltei :("**.
4. **Editar ou Remover:** Use os botões correspondentes.
5. **Finalizar Período:** Reseta tudo e começa do zero.

---

## 🎨 Personalização

- **Estilo:** Usa Bootstrap (responsivo).
- **Textos e Alertas:** Editáveis nos templates.

---

## 🤝 Contribuindo

```bash
git checkout -b feature/minha-nova-feature
git commit -m "Adiciona minha nova feature"
git push origin feature/minha-nova-feature
```

Abra um **pull request** com sua proposta.

---

## 📄 Licença

MIT — Veja o arquivo `LICENSE` para detalhes.

---

## 📬 Contato

- Desenvolvedor: [José Santo de Moura Neto](https://github.com/cromablue)  
- Email: jsmoura.dev@gmail.com