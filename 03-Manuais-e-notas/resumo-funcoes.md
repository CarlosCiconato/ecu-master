# Nossa injeção (rusEFI + melhorias estilo profissional/outro módulo): resumo das funções

Atualizado em 31/10/2026. Branch mais recente: `downshift-blip`. Testes 2009/2009 OK.
Nada disso foi testado ainda em motor, bancada ou TunerStudio.

## Base (o que já vem da rusEFI)
- Motores de **1 a 12 cilindros** (4, 6, 8, 10, 12), 2 e 4 tempos, rotativo.
- Injeção sequencial, semissequencial, em lote ou "throttle body"; ignição individual, centelha perdida ou distribuidor.
- Carga por MAP (speed density), MAF, TPS (Alpha-N) ou mistura de ambos.
- Rodas fônicas: dezenas de padrões (60-2, 36-1, 36-2-2-2, Honda, Nissan, Mitsubishi, GM, etc.), até 4 sensores de comando.
- Comando variável (VVT) em admissão e escape, 2 bancadas.
- Até 2 borboletas eletrônicas (ETB), marcha lenta por borboleta, motor de passo ou válvula.
- Sonda wideband (analógica e por CAN), malha fechada de lambda curta e longa (LTFT), etanol/flex.
- Turbo: controle de pressão (boost), 2-step/launch, anti-lag, corte de giro.
- Até 8 EGT, sensores de pressão de óleo e combustível, nível de combustível, velocidade, marcha.
- Script Lua para funções personalizadas, CAN bus, log em cartão SD, TunerStudio.

## Melhorias que nós fizemos (em ordem)
**Injeção / combustível**
- Mapa principal em **tempo de injeção (ms)**, como nos módulos profissionais, com correção LTFT nesse mapa.
- Enriquecimento de aceleração maior com motor frio (curva por temperatura).
- Bico extra de partida a frio (pulsa durante a partida com motor frio).
- Enriquecimento pós-partida por segundos desde a partida.
- Combustível e ponto por marcha (tabelas RPM x marcha).
- Mais combustível com ar-condicionado ou ventoinhas ligadas.
- Desafogamento (flood clear) com posição da borboleta ajustável.

**Ignição**
- Ponto de partida pela temperatura do motor.
- Retardo de detonação **por cilindro**.
- Retardo de ponto e combustível após troca de marcha (marcha engatada x tempo).

**Malha fechada (sonda)**
- Só funciona entre um RPM mínimo e máximo.
- Pausa depois de uma troca de marcha.
- Limites de correção por MAP.
- **Lambda por cilindro**: malha fechada que iguala os cilindros.

**Turbo / largada**
- Pressão de boost para 2-step e anti-lag, posição de descanso da eGate.
- Alvo de boost por tempo depois da largada e por marcha x tempo depois da troca.
- Controle de boost com CO2 (válvulas de enchimento e alívio no domo da wastegate).
- Corte de giro progressivo (rampa de corte de centelha, estilo profissional).

**Borboleta eletrônica**
- Velocidade máxima da borboleta pela temperatura do motor.
- Posição máxima ajustável de 2 a 100%.
- Volta a funcionar sozinha depois de uma falha.
- **Blip na redução de marcha** (acelerada automática), estilo outro módulo.

**Marcha lenta**
- RPM extra depois da partida, degrau de ponto com carga e rampa de saída do ponto.

**Sensores e entradas**
- Sensor de rotação/fase VR ou Hall escolhido no software (pull-up interno).
- Decodificador de comando genérico com janela de detecção e conferência de dentes.
- Sensor de fase usado só para sincronizar na partida.
- Curva de 8 pontos para sensores de pressão não lineares.

**Alertas e proteções (motor de alertas estilo profissional, 3 ações + saída de alerta)**
- EGT 1 a 8, EGT mais quente e **subida rápida de EGT**.
- Pressão de combustível acima do MAP.
- Correção da malha fechada, rotação da turbina, MAP acima do boost máximo por etanol.
- Pressão mínima de óleo para o VTEC.
- **Pressão de óleo: tempo ajustável para formar pressão e trava de nova partida** depois de um corte por óleo.

**Saídas**
- 8 saídas PWM de uso geral (eram 4).
- Fonte de temperatura da ventoinha escolhível.
- LED RGB de status com as cores dos módulos profissionais.

**Ajustes (tunes) e segurança**
- 3 ajustes trocados por botão ou pelo aplicativo.
- **Chave seletora de ajuste numa entrada analógica** (por tensão), estilo outro módulo.
- Senhas estilo profissional: usuário (PC, menus, partida), preparador e manutenção.

**Rede CAN (referência CAN para painéis)**
- Transmite: nossa injeção aparece como uma módulo de referência ou módulo de referência para painéis e acessórios referência.
- Recebe: módulos externos na rede alimentam os sensores da injeção (pressão/temperatura de óleo, combustível, nível...).
- 8 frames CAN personalizados de 4 valores cada, para enviar ou receber.

**Registro e contadores**
- Log no cartão SD apaga os logs mais antigos para manter espaço e salva o ajuste junto com cada log.
- Odômetro e horímetro, total e parcial, guardados fora do ajuste.

**Placas**
- Proteus F4: configuração movida da CCM para a SRAM principal (mais espaço). Tabelas 16 x 16.
- Proteus F7: tabelas principais de 24 x 20.

## Números do firmware (Proteus F4, 31/10/2026)
Flash 89,68% usada, configuração 23.244 B, CCM ~21,2 KB livres, heap ~34,9 KB livres.
