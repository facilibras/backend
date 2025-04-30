# Sinais
## Geral
- [ ] Corrigir sinal da letra K (Orientacao.FRENTE -> Orientacao.LATERAL)
- [ ] Corrigir sinal da letra P (Orientacao.LATERAL -> Orientacao.TRAS) ???
- [ ] Variações de Sinais

## Corrigir Sinais
- [ ] Letra Ç: Reconhece ambos sinais na lateral.
- [ ] Letra O: Funciona mas dependendo do ângulo da mão não é instantâneo.
- [ ] Letra X: Movimento

## Melhorar
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

# Reconhecimento
## Geral
- [ ] Refatorar para uma classe de reconhecimento

## Movimentos
- [ ] Usar ponto de referência dependendo do sinal

## Validadores
- [ ] Integrar rotação matricial para verificar inclinação
- [ ] Se não der certo, utilizar atan2 para verificar inclinações
- [ ] Utilizar profundidade nas validações
- [ ] Modularizar validadores em pacotes para cada dedo

