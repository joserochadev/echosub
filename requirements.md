# ✅ Requisitos do EchoSub

## 📦 Requisitos Funcionais (RF)

- [x] **RF01** – Permitir que o usuário informe o caminho de um arquivo de vídeo local.
- [x] **RF02** – Extrair automaticamente o áudio do vídeo informado.
- [ ] **RF03** – Transcrever o áudio utilizando o modelo Whisper.
- [ ] **RF04** – Gerar um arquivo de legendas no formato `.srt`.
- [ ] **RF05** – Nomear o arquivo `.srt` com base no nome do vídeo original.
- [ ] **RF06** – Permitir a escolha do idioma da transcrição.
- [ ] **RF07** – Informar ao usuário o progresso do processo (ex: extração, transcrição, geração).
- [ ] **RF08** – Validar se o arquivo de entrada é um vídeo válido.
- [ ] **RF09** – Gerar mensagens de erro claras em caso de falhas.

---

## 📌 Regras de Negócio (RN)

- [x] **RN01** – Aceitar apenas arquivos de vídeo com extensões válidas (`.mp4`, `.avi`, `.mkv`, `.mov`).
- [ ] **RN02** – Se já existir um `.srt` com o mesmo nome, sobrescrever ou salvar com sufixo numérico.
- [ ] **RN03** – O idioma da transcrição deve estar entre os suportados pelo Whisper.
- [ ] **RN04** – O tempo de cada legenda deve ser sincronizado com o áudio, seguindo o padrão SRT.
- [ ] **RN05** – O modelo Whisper deve ser selecionável conforme o desempenho desejado (`base`, `small`, `medium`, `large`).

---

## ⚙️ Requisitos Não Funcionais (RNF)

- [ ] **RNF01** – Executar em sistemas compatíveis com Python e FFMPEG (Linux, Windows, macOS).
- [ ] **RNF02** – Rodar localmente, sem necessidade de internet após instalação.
- [ ] **RNF03** – Utilizar Poetry para gerenciamento de dependências.
- [ ] **RNF04** – Ter tempo de resposta compatível com o tamanho do vídeo e modelo usado.
- [ ] **RNF05** – Utilizar recursos computacionais de forma eficiente.
- [ ] **RNF06** – Seguir boas práticas de organização e documentação do código.
