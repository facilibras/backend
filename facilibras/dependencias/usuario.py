from typing import Annotated, Any

from fastapi import Depends

from facilibras.controladores.autenticacao import usuario_autenticado, usuario_opcional

T_Usuario = Annotated[dict[str, Any], Depends(usuario_autenticado)]
T_UsuarioOpcional = Annotated[dict[str, Any], Depends(usuario_opcional)]
