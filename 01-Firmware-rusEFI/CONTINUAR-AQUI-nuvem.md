# Continuar o firmware em uma conversa nova (26/10/2026)

Plano: doc https://claude.ai/artifact/QKGpEtk1Px1L29Qsqju6w1, aba "Plano de trabalho · Mudanças no firmware".

## Onde paramos
- Fases 1 e 2 completas. Da fase 3, itens 10, 11 e 12 prontos e testados no Mac (1939/1939 testes, flash 87,24%).
- Último branch no Mac: `cam-sync-only-at-start` (commit 38af665e319), em rusefi (clone do rusEFI).
- Item 13 (tabelas 24×20 na placa F7) escrito, mas NÃO enviado ao Mac: patch em /mnt/project-files/firmware/item13/. Falta aplicar sobre `cam-sync-only-at-start` e checar o build proteus_f7 (tamanho da config e página do TunerStudio).
- Ordem da fase 3 (crescente, pedido do Carlos): 13, 16, 17, 20, 21, 22, 25, 26, 27, 30, 32, 34, 35, 36, 37, 38, 42, 43, 44, 45, 46, e depois os novos 53, 54, 55 (rede CAN referência) e 56 (LED RGB de status). Fase 4 (arrancada) por último.

## Atualização 26/10 à noite (conversa "Continuar firmware da fase 3")
- Itens 13, 16 e 20 aplicados e testados no Mac: 1946/1946 testes. Último branch: `closed-loop-shift-pause` (21e5ea86ae8). F4 flash 87,33%; F7 com tabelas 24×20: flash 92,5% (banco 0), config 28.284 B.
- Item 17 (sensores CAN) vai junto com o item 54.
- Clone da nuvem refeito em /home/claude/rusefi (upstream 1b0196058f6 + todos os patches na ordem). Próximo: item 21.

## Como trabalhamos
- O código é escrito no clone da nuvem (/home/claude/rusefi; se a conversa nova não tiver o clone, recriar a partir dos patches em /mnt/project-files/firmware/itemNN/, na ordem).
- Um branch por item, encadeados. `git format-patch` para /mnt/project-files/firmware/itemNN/.
- O patch vai ao Mac por Remote Control (pasta rusefi (clone do rusEFI)) em gzip+base64; lá: novo branch, `git am -3`, testes de unidade e build Proteus F4 (ver memória firmware-changes-progress).
- Nada é enviado para a internet (Carlos ainda não tem GitHub). Download no Mac só com OK do Carlos.

## Outras anotações do dia
- Rede CAN para painéis: manuais/analise-can-pro.md. módulo de referência: manuais/analise-módulo de referência.md.
- Placa: hardware/ideias-placa-pro.md. Decidido: 8 saídas individuais de injeção (fortes, ~10 A, até 4 bicos de alta impedância cada) e 8 de ignição, sequencial até 8 cilindros.

- 26/10 noite: itens 36, 37 e 38 (lenta) prontos no Mac, branch `idle-after-start-timing` (5d2d72b378a), 1957/1957 testes, flash F4 87,92%. Patch em item36-38/. Próximo: item 42.

## Pausa (2026-10-29)
- Carlos pediu para pausar depois do item 45. Item 46 NÃO foi começado no Mac.
- Rascunho do item 46 só na nuvem (branch `start-edit-password`, só o .h do módulo EcuPasswords): senhas fora do tune (registro de storage próprio), partida bloqueada até digitar a senha, edição bloqueada (escrita/burn) até digitar a senha, 3 erros = 30 s de bloqueio.
- Item 45 confirmado no Mac (2026-10-29): branch `odometer-hour-meter` 2b1d7974811 + 489ceaea6f7 (regenerados), 1966/1966 testes, F4 flash 88,34%. Parado aqui.

## Atualização 31/10/2026 (fim da conversa "Continuar firmware da fase 3")
- Carlos pediu para continuar numa conversa nova (esta ficou longa).
- Estado: pausado depois do item 45, a pedido do Carlos (29/10). Próximo, quando ele mandar seguir: item 46.
- Item 46: usar a ideia da outra-ecu (manuais/analise-outra-ecu-t20k.md): senha do preparador (bloqueia ler e gravar o mapa) + senha do usuário (libera só as funções escolhidas; a lista é do app) + senha de partida. Senhas guardadas fora do mapa. Rascunho só do .h no clone da nuvem (branch `start-edit-password`); o clone pode não existir na conversa nova.
- Depois do 46: 53, 54 (com 17), 55, 56, 22. Item 27 ainda espera a decisão do Carlos (recomendado: deixar para depois).
- Ao fim da fase 3: revisão final da lista inteira (Carlos pediu), incluindo os itens pequenos sugeridos da outra-ecu.
- Carlos aprovou (31/10) fazer a biblioteca de sensores do app com os dados da outra-ecu (pressão, temperatura, ~100 borboletas/pedais com pinagem). Isso é parte do app/interface.
- Próximo grande passo sugerido e ainda não decidido: interface primeiro (com o simulador da rusEFI no Mac), placa pronta para bancada (Nucleo STM32F767) e só depois a nossa placa.
- A conexão com o Mac (Remote Control) caiu em 30/10 com "extra_usage_unavailable"; abrir uma nova quando precisar, com aprovação do Carlos.
- No Mac também há uma passagem atualizada: CONTINUAR.md (cadeia de branches, último odometer-hour-meter 489ceaea6f7, regra dos enums regenerados). Cópia do manual da outra-ecu e notas em (manuais de referência, fora do repositório) e notas-outra-ecu.md.

## 31/10/2026 tarde (conversa "Continuar firmware a partir do item 46")
- Item 46 no padrão referência (escolha do Carlos): senha do usuário (bloqueia PC / menus / partida), do preparador (bloqueia mapas, alertas ficam livres) e de manutenção (odômetro). Fora do arquivo de tune, só sai com reset total. 3 erros = 30 s.
- Item 46 PRONTO no Mac: branch start-edit-password-ft (95ceacedd6c + regen 2a341cfa681), 1975/1975, flash F4 88,72%, config 22.680 B. Próximo: 53, 54 (com 17), 55, 56, 22.
- Testes de unidade agora rodam também na nuvem (instalar openjdk-11; make -o .ramdisk-sentinel).
- Item 53 PRONTO no Mac: branch ftcan-broadcast (8d14e6152af + regen 40f485213c8), 1978/1978, flash F4 88,92%. Patch em item53/. Próximo: 54 (receber FTCAN, junto com o 17).

### 31/10 noite: item 54 + 17 feito
- Ler módulos externos na CAN (WBO2 Nano/Slim, EGT-8/4, expansores) nos sensores da ECU. Patch firmware/item54/. Mac: branch ftcan-receive (ccda254dd53 + regen 30b7ac2a518), 1982/1982, Proteus F4 flash 89,12%.
- Próximo: item 55 (pacotes CAN personalizados estilo profissional), depois 56, 22.

### 31/10 noite: item 55 feito
- 8 pacotes CAN personalizados (4 valores de 16 bits, enviar ou receber). Patch firmware/item55/. Mac: branch can-custom-frames (fc7b4646166 + regen 25707b6bb95), 1985/1985, flash 89,24%, config 23.212 B.
- Próximo: item 56 (LED RGB de status), depois 22.

### 31/10 noite: itens 56 e 22 feitos, FASE 3 COMPLETA
- Item 56 (LED RGB de status, cores da módulo de referência): patch firmware/item56/, Mac branch rgb-status-led (67aaa7fde05), 1987/1987.
- Item 22 (lambda por cilindro, malha fechada que iguala os cilindros pelo lambda de cada cilindro da WBO2 referência na CAN): patch firmware/item22/, Mac branch cylinder-lambda-trim (3f64ffa1bde), 1989/1989, flash F4 89,46%, config 23.232 B.
- Cadeia de branches no Mac: ... start-edit-password-ft → ftcan-broadcast → ftcan-receive → can-custom-frames → rgb-status-led → cylinder-lambda-trim (ponta atual). Stashes regen-after-iNN guardam os gerados de cada item.
- Item 27 ainda espera o Carlos (recomendado deixar para depois).
- Próximo: revisão completa da lista de mudanças (pedido do Carlos), incluindo os itens pequenos do outra-ecu.

### 31/10 noite: revisão da lista (conversa "Revisar lista de mudanças do firmware")
- Revisão no doc do plano, aba "Revisão da lista · 31/10". 48 de 56 itens prontos; faltam 27 (recomendado depois) e fase 4.
- Lacunas: 41 sem alerta de subida da EGT (proposto 41b); 29/31 com 6 marchas (lista dizia 10, proposto manter 6); 44 sem taxa por canal (adiado); 54 sem Switchpad/Gear Controller (só se Carlos usar).
- outra-ecu: ventoinha PWM, log condicional, limite suave com ponto/combustível, borboleta no coasting e flex JÁ existem na rusEFI. Novos propostos: 57 (óleo, bloqueio da nova partida), 58 (seletor de mapas por tensão), 59 (blip da borboleta na redução, puxado da fase 4).
- Arrumação pendente: exportar do Mac a cadeia inteira (as correções do item 1 e do item 33 só existem lá).
- Esperando o OK do Carlos para a ordem 41b, 57, 58, 59.

### 31/10 noite: itens 41b, 57, 58, 59 feitos NA NUVEM (Carlos aprovou)
- Carlos: não usa Switchpad/Gear Controller; marchas ficam 6; item 27 no final.
- 41b subida da EGT (sensor de alerta 47), 57 óleo (tempo ajustável + bloqueio da nova partida, motivo de corte 26), 58 seletor de mapas por tensão (tuneSelectorChannel), 59 blip na redução (DownshiftBlip).
- Patches: firmware/item41b, item57, item58, item59 (um commit cada, aplicar nessa ordem sobre cylinder-lambda-trim; conferido que aplicam limpo). Testes na nuvem: 2009/2009.
- NÃO estão no Mac. Falta: aplicar no Mac, testes + build Proteus F4 (tamanho), só com OK do Carlos.
- Nuvem: clone em /home/claude/rusefi, branches egt-rise-alert → oil-restart-lock → tune-selector-voltage → downshift-blip; commits "LOCAL ONLY" (correções do item 1/33 e arquivos gerados) não vão para o Mac. Precisa openjdk-11 (apt-get update antes).
- 31/10 noite: itens 41b, 57, 58, 59 PRONTOS NO MAC, sem correção: egt-rise-alert 61e55a47152, oil-restart-lock 6206ae7331e, tune-selector-voltage eb14aff6208, downshift-blip 62f43ae78e0 + regen e9928ea720b (ponta atual). 2009/2009. F4 flash 89,68%, config 23.244 B, CCM livre 21.668 B, heap 35.744 B. Stash "regen antes items 41b-59". CONTINUAR.md atualizado.
- Próximo: item 27 fica para o fim; fase 4 (arrancada) ou interface (simulador). Carlos decide.
- 31/10 23h: Carlos encerrou a fase 3. Item 27 decidido: fica para o final, junto com a placa (eGates por driver externo tipo FT DPD, placa com saídas de comando; firmware de 2 para 4 motores DC). Próximo grande passo a escolher: fase 4 (arrancada) ou interface com o simulador.

## 01/11/2026: INTERFACE (conversa "Começar a interface com o simulador")
- Carlos escolheu app web TypeScript + Electron. Detalhes e decisões: memória interface-app.md.
- App v0.1 pronto e testado no simulador (nuvem): /mnt/project-files/app/ (ecu-app/, ecu-app-v0.1.tar.gz, LEIAME.md, prints/). Telas: Conexão, Painel, Mapa em ms (editar/gravar), Menu (12 menus, só Painel e Injeção ativos).
- Na nuvem: clone /home/claude/rusefi (branch ui-base = todos os patches + sim-fix) e app em /home/claude/ecu-app; pode não existir na conversa nova. Recriar: clonar rusEFI 1b0196058f6, aplicar patches na ordem (lista em interface-app.md / histórico), apt-get gcc-multilib g++-multilib openjdk-11, `make -j16 -o .ramdisk-sentinel` em simulator/. Simulador: ./build/rusefi_simulator (TS na porta 29001, scripts na 29002). Valores de sensores: `npx tsx test/sim-sensores.ts 5200`.
- Correções do firmware achadas: firmware/sim-fix/0001 e 0002. No Mac: branch sim-fix (75b8c94062d, 6e32994257d), 2009/2009.
- Mac: Node 22 em ~/.local/node; Carlos coloca a linha do PATH no ~/.zshrc. App em ecu-app, ponte em :8600 (`npx tsx src/bridge/main.ts`). Simulador NÃO roda no macOS (precisa Linux: VM UTM ou nuvem).
- Próximo: Electron (janela própria) + USB/serial, depois as demais telas do canvas (ignição, alertas, configuração do motor...), importar/exportar .ftm, biblioteca de sensores. Carlos pediu conversas novas mais curtas (esta ficou cara em tokens).

## 01/11/2026: itens 61 e 62 (thread "Polir menus do app")
- 61 lenta por TPS (curva ms por RPM, só com mapa ms por TPS e TPS abaixo de idlePidDeactivationTpsThreshold) e 62 compensação MAP/TPS (% na parte útil do pulso pelo sensor que o mapa não usa). Um commit, patch firmware/item61-62/ (+ .ini f407-discovery gerado). Bits unusedBit_Fancy26/27. Testes na nuvem: 2017/2017.
- Nuvem: /home/claude/rusefi refeito (1b0196058f6 + todos os patches até item60 + LOCAL ONLY item 33 título e item 1 unmock). Precisa JAVA_HOME=openjdk-11.
- NÃO aplicado no Mac ainda: aplicar sobre custom-firing-order, testes + build Proteus F4.

## PENDENTE para a próxima rodada de firmware (Carlos 01/11/2026)
Fazer tudo junto quando voltar a mexer no firmware:
- Shift light estilo profissional: RPM de troca por marcha, saída para lâmpada, canal ao vivo para o app piscar a tela / barra de LEDs.
- Injeção de água/metanol (WMI): bomba por duty × MAP (pode usar GPPWM) + nível/alerta; app com modelo pronto.
- Controle de tração: precisa sensores de velocidade das rodas (dianteira/traseira) e entradas na placa. Carlos 01/11: se possível, receber também as velocidades das rodas pela rede CAN (ex.: ABS do carro ou módulo referência).
- Itens 61-62 ainda não aplicados no Mac.
(Pit limit: Carlos não quer.)

## 01/11/2026 tarde: rodada shift light / WMI / tração (thread "Fazer rodada de firmware: shift light e tração")
- Escritos e testados NA NUVEM (2030/2030 testes, simulador compila). Um commit cada, aplicar nesta ordem sobre custom-firing-order:
  1. firmware/item61-62/ (lenta por TPS + comp. MAP/TPS)
  2. firmware/item03-fix/ limite do alerta virou float (alerta por RPM e valores acima de 3276 funcionam)
  3. firmware/item63/ shift light: shiftLightRpm1..7 (sem marcha + 1ª-6ª), shiftLightPreRpm (barra de LEDs), shiftLightPin + piscar (Hz); saídas ao vivo shiftLightTarget/Progress/On; módulo ShiftLight
  4. firmware/item64/ água/metanol: usa uma Saída PWM programável (wmiGppwmChannel), boia (wmiLevelPin + atraso), avanço/combustível proporcionais ao duty, sensor de alerta 48 "WMI fault"; saídas wmiDuty/wmiStatus; módulo WaterMethanol
  5. firmware/item65/ tração: tcWheelSource (fio: aux speed 1 = dianteira, 2 = traseira, dentes + perímetro do pneu; CAN: destinos 7-10 "Wheel speed FL/FR/RL/RR" na CAN personalizada / FTCAN), patinagem = eixo de tração / eixo livre -> sensor WheelSlipRatio que alimenta as 3 tabelas da rusEFI (ponto, corte, borboleta); chave opcional tcSwitchPin; sem VSS o eixo livre vira a velocidade; sensor de alerta 49 "Wheel slip %"; módulo TractionWheels
- .ini do simulador com tudo: firmware/item65/rusefi_f407-discovery.ini (assinatura traction-wheel-speeds.2026.11.01.f407-discovery.1874771930).
- Nuvem: clone /home/claude/rusefi, branches alert-limit-float -> shift-light -> water-methanol -> traction-wheel-speeds sobre ui-base (+ 2 commits LOCAL ONLY: título item 33 e .unmock() do item 1).
- Mac: pendente (Remote Control com OK do Carlos).
- 01/11 15:4x: APLICADO NO MAC sem correção: idle-tps-map-comp f0dafac54fe, alert-limit-float 902a72b48b5, shift-light a781f0f6244, water-methanol 834a3f7dbca, traction-wheel-speeds 105df94b35a + regen bfc1546a236 (ponta). 2030/2030. Proteus F4 flash 90,35% (680.932 B), config 23.584 B, CCM livre 21.548 B, heap 35.304 B. Stashes "regen antes/depois items 61-65". Patches no Mac em 01-Firmware-rusEFI/patches/items-61-65/.

## 01/11/2026: teste do app no simulador real (thread "Testar o app no simulador rusEFI")
- Nuvem: /home/claude/rusefi refeito (1b0196058f6 + todos os patches em ordem de data + LOCAL ONLY título do item 33), branch sim-test. Simulador compila e roda. Nenhuma mudança de firmware foi necessária; correções foram no app (v0.30).
- Comportamento a saber: cylindersCount diferente do tamanho da ordem de ignição = firmwareError (no simulador fecha o programa). O app agora muda os dois juntos.
