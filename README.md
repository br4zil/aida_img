# AIDA IMG

Sistema desenvolvido na tese de doutorado **"Detecção Automatizada de Indícios de Desonestidade Acadêmica em MOOCs que utilizam Avaliações Baseadas no Envio de Imagens"** (UFRGS, 2025).

O **AIDA IMG** é uma ferramenta web que utiliza **visão computacional** e **inteligência artificial** para detectar **indícios de desonestidade acadêmica** em atividades de cursos online (MOOCs) baseadas no **envio de imagens**.

---

## Principais Funcionalidades
- Upload e análise automática de imagens enviadas por alunos.  
- Extração de características visuais com **CNN + OpenCV + CLIP**.  
- Comparação entre análise humana e automática.  
- Geração de gráficos e relatórios com indicadores de desonestidade acadêmica.  
- Integração com plataformas MOOC (ex: **Lúmina/UFRGS**).

---

## Tecnologias Utilizadas
- **Python 3**  
- **Django** (backend web)  
- **OpenCV**, **TensorFlow**, **Scikit-learn**, **CLIP (OpenAI)**  
- **Bootstrap + Chart.js** (frontend)  
- **SQLite / PostgreSQL**

---

## Citação
Santos, G. S. (2025). Detecção Automatizada de Indícios de Desonestidade Acadêmica em MOOCs que utilizam Avaliações Baseadas no Envio de Imagens.
Tese (Doutorado em Informática na Educação) – Universidade Federal do Rio Grande do Sul (UFRGS).

---

## Contato
Autor: Gilson Saturnino dos Santos
Instituições: IFMS – Campus Coxim | UFRGS – PPGIE
E-mail: gilson.santos@ifms.edu.br
Orientadora: Profa. Dra. Gabriela Trindade Perry

---

## Licença
Licença MIT — uso e modificação permitidos para fins acadêmicos e científicos, com citação da fonte.


---

## Instalação e Execução
```bash
# Clone o repositório
git clone https://github.com/<seu_usuario>/aida_img.git
cd aida_img

# Crie o ambiente virtual e instale dependências
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt

# Execute o servidor
python manage.py runserver
