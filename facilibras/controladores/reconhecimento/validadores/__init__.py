# ruff: noqa: F401, F811, I001

from facilibras.controladores.reconhecimento.validadores.validacao import (
    get_validador as get_validador,
)
from facilibras.controladores.reconhecimento.validadores.validacao import (
    registrar_validador as registrar_validador,
)

from facilibras.controladores.reconhecimento.validadores.validacao import (
    Invalido as Invalido,
)
from facilibras.controladores.reconhecimento.validadores.validacao import (
    Resultado as Resultado,
)
from facilibras.controladores.reconhecimento.validadores.validacao import (
    Valido as Valido,
)

# Inicializar os validadores

import facilibras.controladores.reconhecimento.validadores.mao as _
import facilibras.controladores.reconhecimento.validadores.posicao as _
import facilibras.controladores.reconhecimento.validadores.expressao as _
