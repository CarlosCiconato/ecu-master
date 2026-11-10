# Como continuar o projeto rusEFI (estilo profissional) numa nova conversa

Atualizado em 01/11/2026. Tudo está só neste Mac; nada foi enviado para a internet.

## Onde está tudo
- Código: `rusefi (clone do rusEFI)` (rusEFI com todas as melhorias, em branches locais).
- Branch mais recente (contém TODAS as melhorias): `traction-wheel-speeds` (bfc1546a236, itens 61-65 + regen).
- Patches aplicados: `01-Firmware-rusEFI/patches/`.
- Notas da placa (módulo de referência/550/700, sugestão de hardware): `notas-placa.md`.
- Manuais para analisar: `(manuais de referência, fora do repositório)` (referência: CAN Technical Guide, CAN para painéis, módulo de referência; outro módulo).
- Notas do manual outro módulo (dados de sensores, ideias de itens): `notas-outra-ecu.md`.

## Itens feitos (em ordem de aplicação)
1, 18, 2, 3+39, 4 (fase 1) → 5, 6, 7, 8, 9, 15, (config fora da CCM), 19, 23+24, 28, 29+31, 33, 40+41 → 10, 11, 12
→ 13, curva de sensor de pressão (8 pontos), pausa do malha fechada após troca de marcha, 21, 25, 26,
30+32, 34, 35, 36+37+38, 42, 43, 44, 45.
Números de 1 a 45 sem número na lista acima: veja o "Mapa item → branch" logo abaixo. A lista completa/fases está com o Claude do projeto.
Testes: 1966/1966 OK. Firmware Proteus F4: 88,34% da flash, CCM ~21,9 KB livres, heap ~37,7 KB,
config 22.656 B. Proteus F7 (só verificado no item 13): 92,5% flash0, config 28.284 B.
Parado após o item 45 a pedido do Carlos (29/10/2026).
Depois vieram 46, 53, 54 (+17), 55, 56, 22 (lambda por cilindro) e, em 31/10/2026, 41b, 57, 58, 59
(pacote 01-Firmware-rusEFI/patches/items-41b-59.mbox, sha256 1a8c81ab…663c).
Testes: 2009/2009 OK. Proteus F4 (31/10, ponta downshift-blip): 89,68% da flash (675.868 B de 736 KB),
config 23.244 B, CCM ~21,2 KB livres (21.668 B), heap ~34,9 KB (35.744 B). Sem erro de tamanho.

Item 60 (01/11/2026): ordem de ignição personalizada (FO_CUSTOM = 37, "Custom (type it)";
campo customFiringOrder[12], U08 1..12). Branch custom-firing-order (3165c5e0b82), patch em
01-Firmware-rusEFI/patches/item60/ (sha256 b71d7c16…f259). Testes 2015/2015 OK. Proteus F4: 89,73% da flash
(676.300 B), config 23.256 B. Arquivos gerados guardados no stash "regen antes item60".

Itens 61-65 (01/11/2026): pacote 01-Firmware-rusEFI/patches/items-61-65/ (b.txz sha256 e1841edf…9caa).
- idle-tps-map-comp (f0dafac54fe): itens 61+62, marcha lenta por TPS e compensação MAP/TPS no modo Injection time
- alert-limit-float (902a72b48b5): correção do item 03, limite de alerta float (RPM > 3276)
- shift-light (a781f0f6244): item 63, shift light por marcha
- water-methanol (834a3f7dbca): item 64, injeção de água/metanol
- traction-wheel-speeds (105df94b35a + bfc1546a236 regen items 61-65): item 65, velocidade das rodas (fio ou CAN) para o controle de tração
Testes 2030/2030 OK. Proteus F4: 90,35% da flash (680.932 B de 736 KB), config 23.584 B,
CCM 21.548 B livres, heap 35.304 B. Gerados: stash "regen antes items 61-65" (antes) e "regen depois items 61-65".

Mapa item → branch (correção conforme a lista do projeto, 31/10/2026):
| Item | O que é | Branch / situação |
|---|---|---|
| 16 | Curva de 8 pontos dos sensores de pressão | pressure-sensor-curve |
| 17 | Associar sensores CAN | feito junto com o 54 (ftcan-receive) |
| 20 | Pausa da malha fechada na troca de marcha | closed-loop-shift-pause |
| 22 | Lambda por cilindro | cylinder-lambda-trim (NÃO é o 52) |
| 52 | Blip na redução + pit limit (fase 4) | só o blip feito, como item 59 (downshift-blip); pit limit FALTA |
| — | Config fora da CCM (sem número de item) | config-out-of-ccm |
| 27 | Mais de 2 motores DC | DECIDIDO (31/10/2026): fica para o final, junto com a placa (saídas de controle para ponte H externa, ver notas-placa.md) |
| 14, 47–51 | Fase 4 | FALTAM |
FASE 3 ENCERRADA em 31/10/2026 (Carlos). O 27 foi decidido: fica para o final, com a placa.
Próxima: fase 4 (14, 47 a 51 e o pit limit do 52).

Cadeia de branches (cada uma em cima da anterior):
ms-injection-map → ltft-ms-map → progressive-rev-limiter → alert-engine → etb-speed-by-clt →
generic-cam-window → multiple-tunes → knock-per-cylinder → etb-max-position → hall-pullup-outputs →
gppwm-8-channels → config-out-of-ccm → closed-loop-rpm-window → boost-launch-egate →
cranking-timing-clt → gear-compensation → cold-accel-enrichment → fuel-pressure-egt-alerts →
cold-start-injector → etb-auto-recover → cam-sync-only-at-start → f7-bigger-tables →
pressure-sensor-curve → closed-loop-shift-pause → closed-loop-limits-by-map → boost-by-time →
dome-co2-control → shift-retard-enrichment → flood-clear-tps → afterstart-by-time →
idle-after-start-timing → extra-alert-sensors → fan-ac-vtec-options → sd-log-room-and-tune →
odometer-hour-meter → start-edit-password-ft (2a341cfa681) → ftcan-broadcast (40f485213c8) →
ftcan-receive (30b7ac2a518) → can-custom-frames (25707b6bb95) → rgb-status-led (67aaa7fde05) →
cylinder-lambda-trim (3f64ffa1bde) → egt-rise-alert (61e55a47152, item 41b) →
oil-restart-lock (6206ae7331e, item 57) → tune-selector-voltage (eb14aff6208, item 58) →
downshift-blip (62f43ae78e0 item 59 + e9928ea720b regen do enum GPPWM_EgtRiseRate) →
sim-fix (75b8c94062d + 6e32994257d) → custom-firing-order (3165c5e0b82, item 60) →
idle-tps-map-comp (f0dafac54fe) → alert-limit-float (902a72b48b5) → shift-light (a781f0f6244) →
water-methanol (834a3f7dbca) → traction-wheel-speeds (105df94b35a + bfc1546a236 regen)

## Procedimento para cada item novo
1. `cd rusefi (clone do rusEFI)`; `git stash push -u` (guarda arquivos regenerados);
   apagar sentinelas: `find firmware unit_tests -maxdepth 1 \( -name .config-sentinel -o -name .docsenums-sentinel -o -name .tooljars-sentinel -o -name .target-sentinel \) -delete`
2. `git checkout -b <novo-branch> <branch-anterior>`; `git am -3 <patch>` (conferir sha256 antes).
3. Testes: `export PATH=$HOME/.local/bin:$PATH; cd unit_tests; perl -e 'alarm 900; exec @ARGV' make -j8 -o .ramdisk-sentinel; perl -e 'alarm 900; exec @ARGV' ./build/rusefi_test`
4. Firmware Proteus F4 (compilador do STM32CubeIDE + gmake):
   ST=/Applications/STM32CubeIDE.app/Contents/Eclipse/plugins/com.st.stm32cube.ide.mcu.externaltools.gnu-tools-for-stm32.14.3.rel1.macos64_1.0.100.202602081740/tools/bin
   `cd firmware; rm -rf build; PATH=$ST:$HOME/.local/bin:$PATH bash -c 'source config/boards/common_script_read_meta_env.inc config/boards/proteus/meta-info-proteus_f4.env && gmake -j8 -r -o .ramdisk-sentinel build/rusefi.elf'`
5. Erros comuns já vistos: título de dado de log > 34 letras; tipo `custom` declarado depois do uso;
   `bit` com comentário precisa de `,"sim","não"`.
6. Arquivos de enum regenerados e versionados (auto_generated_commonenum.cpp, auto_generated_enginetypes.cpp,
   java_console/.../enums/*.java): commitar sozinhos num segundo commit. O auto_generated_commonenum.h fica FORA do git.
7. Payload em base64 vindo do projeto: conferir o sha256 do .patch; se o gzip disser "truncated" mas o hash bater, está ok.

## Ferramentas instaladas (sem senha)
- `~/.local/bin`: gmake (GNU make 4.4.1), flock e realpath (substitutos).
- `~/.local/arm-gnu-toolchain`: ARM 14.2 (NÃO funciona neste Mac Intel; pode apagar, ~1 GB).
- Java 17 (Temurin) instalado pelo Carlos.

## Pendências
- Fase 3 encerrada (31/10/2026). Próxima: fase 4 (14, 47–51, pit limit do 52); lista com o Claude do projeto.
- Item 27 (mais de 2 motores DC): fazer no final, junto com o projeto da placa.
- Depois: revisão final de todos os branches para ver se não faltou nada.
- Próximo passo sugerido: interface primeiro, testada com o simulador (`rusefi (clone do rusEFI)/simulator`, ainda não
  compilado neste Mac) + TunerStudio; depois placa pronta (Nucleo F767 ou Proteus F7); por último a nossa placa.
  Falta o Carlos dizer se "interface" é a tela do painel ou o programa de ajuste.
- Analisar os manuais referência (rede CAN / CAN para painéis, módulo de referência). outro módulo já resumido em notas-outra-ecu.md.
- Limpar os stashes de arquivos regenerados (`git stash list`), se o Carlos quiser.
- Nada testado ainda em ECU real, bancada ou TunerStudio.
