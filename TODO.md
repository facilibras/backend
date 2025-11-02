# Sinais
## Modelo
- [ ] Funções de conveniência:
    - [ ] `depois_de(Configuracao)`
    - [ ] `configuracao_anterior(idx: int = -1)`
    - [ ] `igual_a(Configuracao)`

## Corrigir Sinais
- [ ] Letra K sem movimento atualmente

## Feedback antigo
- [ ] Polegar_dentro (BAIXO): *Falso negativo*
- [ ] Indicador_cima (LATERAL): *Falso negativo* comum nos sinais com orientação lateral
- [ ] Indicador_flexionado (BAIXO): *Falso positivo* quando p/ indicador para baixo
- [ ] Indicador_frente_90 (FRENTE): *Falso positivo* quando p/ indicador para baixo
- [ ] Medio_cima: **Funcional**, porém precisa refatorar
- [ ] Medio_enc_polegar: **Funcional**, porém pensar em uma forma melhor
- [ ] Medio_frente_45: **Funcional**, mas precisa deixar mais estrito
- [ ] Anelar_baixo (LATERAL): *Falso negativo* comum nos sinais com orientação lateral
- [ ] Anelar_enc_polegar: **Funcional**, porém pensar em uma forma melhor
- [ ] Minimo_baixo (BAIXO): **Funcional**, porém precisa refatorar

> [!IMPORTANT]
> Possivelmente inverter lógica da orientação lateral para lidar com falsos positivos relacionados a profundidade
