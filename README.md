# Snake Single Player

Jogo da cobrinha single-player em Python com Pygame.

## Como executar

```bash
pip install -r requirements.txt
python main.py
```

## Controles

- W ou seta para cima: mover para cima
- S ou seta para baixo: mover para baixo
- A ou seta para esquerda: mover para esquerda
- D ou seta para direita: mover para direita
- ENTER: reiniciar depois do game over
- ESC: sair

## Arquitetura

```text
client/
  game.py       controla o loop principal
  controls.py   transforma teclado em comandos
  renderer.py   desenha o jogo na tela

core/
  config.py     guarda configuracoes globais
  commands.py   define comandos e direcoes
  entities.py   define Snake, Food e Position
  world.py      contem as regras principais do jogo
```

O `core` concentra as regras do jogo e o estado da partida.
O `client` concentra entrada do usuario, janela, renderizacao e loop principal.
