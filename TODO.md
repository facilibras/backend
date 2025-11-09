# Sinais
## Corrigir Sinais
- [ ] Letra K sem movimento atualmente

## Validadores
- [x] Posição
- [x] Rosto
- [ ] Mão
    - [x] Alfabeto
    - [x] Números
    - [ ] Restante

 > [!IMPORTANT]
 > Considerar utilizar lógica equivalente do `MINIMO + Orientacao(BAIXO)` para outros dedos

## Feedback antigo
- [ ] Polegar_dentro (BAIXO): *Falso negativo*
- [ ] Indicador_cima (LATERAL): *Falso negativo* comum nos sinais com orientação lateral
- [ ] Indicador_flexionado (BAIXO): *Falso positivo* quando p/ indicador para baixo
- [ ] Indicador_frente_90 (FRENTE): *Falso positivo* quando p/ indicador para baixo
- [ ] Medio_enc_polegar: **Funcional**, porém pensar em uma forma melhor
- [ ] Medio_frente_45: **Funcional**, mas precisa deixar mais estrito
- [ ] Anelar_baixo (LATERAL): *Falso negativo* comum nos sinais com orientação lateral
- [ ] Anelar_enc_polegar: **Funcional**, porém pensar em uma forma melhor

# Pontos Fracos
- [ ] Sinal X: Por causa dos validadores PROXIMO_AO_CORPO e DISTANTE_AO_CORPO
