"""test_tpi.py — Suite de pruebas automatizadas del TP Integrador."""

import pytest
from figuras import (
    Triangulo,
    Cuadrado,
    Pentagono,
    Hexagono,
    Lado,
    Etiqueta,
    Taller,
    FactoriaPoligonoRegular,
    Poligono,
    Exportable,
    exportar_todo,
)
from libreria_externa import PlanoCAD


def test_asociacion_lado_etiqueta():
    """Verifica asociación opcional 0..1 entre Lado y Etiqueta."""
    lado_sin_tag = Lado(5.0)
    assert lado_sin_tag.etiqueta is None

    tag = Etiqueta("Lado A")
    lado_con_tag = Lado(5.0, tag)
    assert lado_con_tag.etiqueta == tag
    assert lado_con_tag.etiqueta.texto == "Lado A"


def test_composicion_copia_defensiva_poligono():
    """Verifica que Poligono crea copias independientes de sus Lados."""
    l1 = Lado(3.0)
    lados = [l1, Lado(4.0), Lado(5.0)]
    t = Triangulo("T", "rojo", lados)

    # El objeto interno no es el mismo que el externo (composición pura)
    assert t.lados()[0] is not l1
    assert t.lados()[0].longitud == 3.0

    # Inmutabilidad de la tupla retornada
    assert isinstance(t.lados(), tuple)


def test_falla_temprana_poligono_abstracto_e_invariantes():
    """Verifica que instanciar Poligono directo falla y que se controlan los lados esperados."""
    with pytest.raises(TypeError):
        # Poligono es ABC sin lados_esperados implementado
        Poligono("Invalido", "blanco", [Lado(1.0), Lado(1.0), Lado(1.0)])  # type: ignore

    with pytest.raises(ValueError):
        # Cuadrado espera 4 lados, no 3
        Cuadrado("C", "azul", [Lado(2.0), Lado(2.0), Lado(2.0)])


def test_agregacion_taller_ciclo_de_vida():
    """Verifica que Taller agrega figuras y que su inventario es inmutable."""
    t = Triangulo("T", "rojo", [Lado(3), Lado(4), Lado(5)])
    c = Cuadrado("C", "azul", [Lado(2)] * 4)

    taller = Taller()
    taller.recibir(t)
    taller.recibir(c)

    inv = taller.inventario()
    assert len(inv) == 2
    assert isinstance(inv, tuple)

    # Si se destruye el taller, el triángulo sigue existiendo
    del taller
    assert t.perimetro() == 12.0


def test_protocol_exportable_con_tercero():
    """Verifica cumplimiento estructural de Exportable con PlanoCAD sin modificarlo."""
    plano = PlanoCAD("CAD-101", "1:100")
    t = Triangulo("T", "verde", [Lado(3), Lado(4), Lado(5)])

    assert isinstance(plano, Exportable)
    assert isinstance(t, Exportable)

    res = exportar_todo([t, plano])
    assert len(res) == 2
    assert "PlanoCAD[CAD-101 @ 1:100]" in res[1]


def test_factoria_poligono_regular():
    """Verifica el reemplazo de PoligonoRegular por Factory Method."""
    pentagono = FactoriaPoligonoRegular.crear("P", "amarillo", 4.0, 5)
    assert isinstance(pentagono, Pentagono)
    assert pentagono.lados_esperados() == 5
    assert pentagono.perimetro() == 20.0