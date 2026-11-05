"""Las decisiones metodológicas de la limpieza, con nombre y valor por defecto."""

from dataclasses import dataclass

from .imputacion import EstrategiaDeImputacion, estrategia_de_imputacion


@dataclass(frozen=True)
class PoliticaDeLimpieza:
    """Qué se considera atípico y cómo se imputa.

    Es inmutable a propósito: una política se decide una vez por corrida y
    ningún paso del proceso debería poder cambiarla por el camino.
    """

    percentil_atipicos: float = 0.99
    grupos_imputacion: tuple[str, ...] = ("area", "sexo")
    metodo_imputacion: str = "mediana"
    valor_fijo: float | None = None

    def __post_init__(self):
        if not 0 < self.percentil_atipicos <= 1:
            raise ValueError("percentil_atipicos debe estar entre 0 y 1")
        if not self.grupos_imputacion:
            raise ValueError("grupos_imputacion no puede estar vacío")
        # Construirla aquí hace que un nombre inválido falle al crear la política, no al imputar
        self.estrategia

    @classmethod
    def desde_dict(cls, valores: dict) -> "PoliticaDeLimpieza":
        """Construye la política a partir de un diccionario, como el que viene de un YAML o de JSON."""
        return cls(
            percentil_atipicos=float(valores.get("percentil_atipicos", cls.percentil_atipicos)),
            grupos_imputacion=tuple(valores.get("grupos_imputacion", cls.grupos_imputacion)),
            metodo_imputacion=str(valores.get("metodo_imputacion", cls.metodo_imputacion)),
            valor_fijo=valores.get("valor_fijo", cls.valor_fijo),
        )

    @property
    def estrategia(self) -> EstrategiaDeImputacion:
        return estrategia_de_imputacion(self.metodo_imputacion, self.valor_fijo)

    @property
    def descripcion(self) -> str:
        grupos = " x ".join(self.grupos_imputacion)
        return (
            f"{self.estrategia.descripcion} de ocupados por {grupos}; "
            f"atipicos recortados al percentil {self.percentil_atipicos:.0%}".replace("%", "")
        )
