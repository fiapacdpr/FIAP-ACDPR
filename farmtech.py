"""FarmTech Solutions - gestão didática de plantios no Pará.

Projeto acadêmico FIAP. Os dados de insumos são estimativas demonstrativas e
não substituem análise de solo, receituário ou orientação de profissional
habilitado.
"""

from __future__ import annotations

import csv
import json
import math
from datetime import date
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_JSON = BASE_DIR / "dados_plantio.json"
ARQUIVO_CSV = BASE_DIR / "dados_plantio.csv"

CULTURAS = {
    "1": {
        "nome": "Açaí",
        "geometria": "Retângulo",
        "espacamento_ruas_m": 5.0,
        "espacamento_plantas_m": 5.0,
        "produto": "NPK 10-20-10",
        "dose_g_planta": 150.0,
    },
    "2": {
        "nome": "Mandioca",
        "geometria": "Trapézio",
        "espacamento_ruas_m": 1.0,
        "espacamento_plantas_m": 1.0,
        "produto": "NPK 10-28-20",
        "dose_g_planta": 20.0,
    },
}

CAMPOS_CSV = [
    "talhao",
    "cultura",
    "geometria",
    "comprimento_m",
    "largura_m",
    "base_maior_m",
    "base_menor_m",
    "altura_m",
    "area_m2",
    "area_ha",
    "espacamento_ruas_m",
    "espacamento_plantas_m",
    "numero_ruas",
    "numero_plantas",
    "produto",
    "dose_g_planta",
    "quantidade_insumo_kg",
    "data_registro",
]


def ler_float(mensagem: str, minimo: float = 0.0, padrao: float | None = None) -> float:
    """Lê número decimal positivo, aceitando vírgula como separador."""
    while True:
        sufixo = f" [{padrao:g}]" if padrao is not None else ""
        texto = input(f"{mensagem}{sufixo}: ").strip()
        if not texto and padrao is not None:
            return padrao
        try:
            valor = float(texto.replace(",", "."))
            if valor <= minimo:
                print(f"Digite um valor maior que {minimo:g}.")
                continue
            return valor
        except ValueError:
            print("Valor inválido. Use apenas números, por exemplo: 12,5.")


def ler_inteiro(mensagem: str, minimo: int, maximo: int) -> int:
    """Lê um inteiro dentro do intervalo indicado."""
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo <= valor <= maximo:
                return valor
        except ValueError:
            pass
        print(f"Opção inválida. Digite um número entre {minimo} e {maximo}.")


def calcular_area(cultura: str, dimensoes: dict[str, float]) -> float:
    """Calcula a área em m² conforme a geometria associada à cultura."""
    if cultura == "Açaí":
        return dimensoes["comprimento_m"] * dimensoes["largura_m"]
    if cultura == "Mandioca":
        return (
            (dimensoes["base_maior_m"] + dimensoes["base_menor_m"])
            * dimensoes["altura_m"]
            / 2
        )
    raise ValueError("Cultura não suportada.")


def calcular_ruas_e_plantas(
    cultura: str,
    dimensoes: dict[str, float],
    espacamento_ruas_m: float,
    espacamento_plantas_m: float,
) -> tuple[int, int]:
    """Estima ruas e plantas, considerando uma linha também na borda inicial."""
    if cultura == "Açaí":
        largura = dimensoes["largura_m"]
        comprimento_medio = dimensoes["comprimento_m"]
    elif cultura == "Mandioca":
        largura = dimensoes["altura_m"]
        comprimento_medio = (
            dimensoes["base_maior_m"] + dimensoes["base_menor_m"]
        ) / 2
    else:
        raise ValueError("Cultura não suportada.")

    numero_ruas = math.floor(largura / espacamento_ruas_m) + 1
    plantas_por_rua = math.floor(comprimento_medio / espacamento_plantas_m) + 1
    return numero_ruas, numero_ruas * plantas_por_rua


def montar_registro(
    talhao: str,
    cultura: str,
    geometria: str,
    dimensoes: dict[str, float],
    espacamento_ruas_m: float,
    espacamento_plantas_m: float,
    produto: str,
    dose_g_planta: float,
    data_registro: str | None = None,
) -> dict[str, Any]:
    """Cria um registro e recalcula todos os campos derivados."""
    area_m2 = calcular_area(cultura, dimensoes)
    numero_ruas, numero_plantas = calcular_ruas_e_plantas(
        cultura, dimensoes, espacamento_ruas_m, espacamento_plantas_m
    )
    return {
        "talhao": talhao,
        "cultura": cultura,
        "geometria": geometria,
        "dimensoes": dimensoes,
        "area_m2": round(area_m2, 2),
        "area_ha": round(area_m2 / 10_000, 4),
        "espacamento_ruas_m": espacamento_ruas_m,
        "espacamento_plantas_m": espacamento_plantas_m,
        "numero_ruas": numero_ruas,
        "numero_plantas": numero_plantas,
        "produto": produto,
        "dose_g_planta": dose_g_planta,
        "quantidade_insumo_kg": round(numero_plantas * dose_g_planta / 1_000, 3),
        "data_registro": data_registro or date.today().isoformat(),
    }


def carregar_registros(caminho: Path = ARQUIVO_JSON) -> list[dict[str, Any]]:
    """Carrega o vetor principal de registros do arquivo JSON."""
    if not caminho.exists():
        return []
    try:
        conteudo = json.loads(caminho.read_text(encoding="utf-8"))
        return conteudo if isinstance(conteudo, list) else []
    except (json.JSONDecodeError, OSError) as erro:
        print(f"Aviso: não foi possível carregar {caminho.name}: {erro}")
        return []


def salvar_registros(registros: list[dict[str, Any]], caminho: Path = ARQUIVO_JSON) -> None:
    """Persiste o vetor de registros em JSON."""
    caminho.write_text(
        json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def registro_para_linha(registro: dict[str, Any]) -> dict[str, Any]:
    """Converte um registro aninhado em linha plana para o CSV consumido pelo R."""
    linha = {campo: "" for campo in CAMPOS_CSV}
    for campo in CAMPOS_CSV:
        if campo in registro:
            linha[campo] = registro[campo]
    linha.update(registro.get("dimensoes", {}))
    return linha


def exportar_csv(
    registros: list[dict[str, Any]], caminho: Path = ARQUIVO_CSV
) -> None:
    """Exporta os vetores em CSV, mantendo cabeçalho mesmo se não houver dados."""
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV)
        escritor.writeheader()
        for registro in registros:
            escritor.writerow(registro_para_linha(registro))


def persistir(registros: list[dict[str, Any]]) -> None:
    salvar_registros(registros)
    exportar_csv(registros)


def escolher_cultura() -> tuple[str, dict[str, Any]]:
    print("\nCulturas disponíveis:")
    for codigo, dados in CULTURAS.items():
        print(f"  {codigo} - {dados['nome']} ({dados['geometria']})")
    codigo = str(ler_inteiro("Escolha a cultura: ", 1, len(CULTURAS)))
    return codigo, CULTURAS[codigo]


def ler_dimensoes(cultura: str) -> dict[str, float]:
    if cultura == "Açaí":
        return {
            "comprimento_m": ler_float("Comprimento do talhão (m)"),
            "largura_m": ler_float("Largura do talhão (m)"),
        }
    return {
        "base_maior_m": ler_float("Base maior do talhão (m)"),
        "base_menor_m": ler_float("Base menor do talhão (m)"),
        "altura_m": ler_float("Distância perpendicular entre as bases (m)"),
    }


def entrada_dados(registros: list[dict[str, Any]]) -> None:
    print("\n=== NOVO TALHÃO ===")
    talhao = input("Nome ou identificação do talhão: ").strip() or f"Talhão {len(registros)+1}"
    _, configuracao = escolher_cultura()
    cultura = configuracao["nome"]
    dimensoes = ler_dimensoes(cultura)
    espacamento_ruas = ler_float(
        "Espaçamento entre ruas (m)", padrao=configuracao["espacamento_ruas_m"]
    )
    espacamento_plantas = ler_float(
        "Espaçamento entre plantas (m)",
        padrao=configuracao["espacamento_plantas_m"],
    )
    produto = (
        input(f"Produto [{configuracao['produto']}]: ").strip()
        or configuracao["produto"]
    )
    dose = ler_float(
        "Dose por planta (g)", padrao=configuracao["dose_g_planta"]
    )
    registro = montar_registro(
        talhao,
        cultura,
        configuracao["geometria"],
        dimensoes,
        espacamento_ruas,
        espacamento_plantas,
        produto,
        dose,
    )
    registros.append(registro)
    persistir(registros)
    print("\nRegistro incluído com sucesso.")
    exibir_registro(len(registros) - 1, registro)


def formatar_dimensoes(registro: dict[str, Any]) -> str:
    d = registro["dimensoes"]
    if registro["cultura"] == "Açaí":
        return f"{d['comprimento_m']:g} m × {d['largura_m']:g} m"
    return (
        f"bases {d['base_maior_m']:g} m/{d['base_menor_m']:g} m; "
        f"altura {d['altura_m']:g} m"
    )


def exibir_registro(posicao: int, registro: dict[str, Any]) -> None:
    print(f"\n[{posicao}] {registro['talhao']} - {registro['cultura']}")
    print(f"    Geometria/dimensões: {registro['geometria']} - {formatar_dimensoes(registro)}")
    print(f"    Área: {registro['area_m2']:,.2f} m² ({registro['area_ha']:.4f} ha)")
    print(
        f"    Espaçamento: {registro['espacamento_ruas_m']:g} m entre ruas × "
        f"{registro['espacamento_plantas_m']:g} m entre plantas"
    )
    print(
        f"    Estimativa: {registro['numero_ruas']} ruas e "
        f"{registro['numero_plantas']:,} plantas"
    )
    print(
        f"    Insumo: {registro['produto']} - {registro['dose_g_planta']:g} g/planta "
        f"= {registro['quantidade_insumo_kg']:,.3f} kg"
    )


def saida_dados(registros: list[dict[str, Any]]) -> None:
    print("\n=== TALHÕES CADASTRADOS ===")
    if not registros:
        print("Nenhum registro cadastrado.")
        return
    for posicao, registro in enumerate(registros):
        exibir_registro(posicao, registro)
    print(f"\nTotal de registros no vetor: {len(registros)}")


def escolher_posicao(registros: list[dict[str, Any]], acao: str) -> int | None:
    if not registros:
        print("Não há registros para esta operação.")
        return None
    for posicao, registro in enumerate(registros):
        print(f"  [{posicao}] {registro['talhao']} - {registro['cultura']}")
    return ler_inteiro(
        f"Informe a posição do vetor que deseja {acao}: ", 0, len(registros) - 1
    )


def atualizar_dados(registros: list[dict[str, Any]]) -> None:
    print("\n=== ATUALIZAÇÃO ===")
    posicao = escolher_posicao(registros, "atualizar")
    if posicao is None:
        return
    atual = registros[posicao]
    print(
        "1 - Identificação do talhão\n"
        "2 - Produto\n"
        "3 - Dose por planta\n"
        "4 - Espaçamento entre ruas\n"
        "5 - Espaçamento entre plantas\n"
        "6 - Dimensões do talhão\n"
        "7 - Cultura (redefine todos os dados técnicos)"
    )
    campo = ler_inteiro("Campo a atualizar: ", 1, 7)

    if campo == 1:
        atual["talhao"] = input("Nova identificação: ").strip() or atual["talhao"]
    elif campo == 2:
        atual["produto"] = input("Novo produto: ").strip() or atual["produto"]
    elif campo == 3:
        atual["dose_g_planta"] = ler_float("Nova dose (g/planta)")
    elif campo == 4:
        atual["espacamento_ruas_m"] = ler_float("Novo espaçamento entre ruas (m)")
    elif campo == 5:
        atual["espacamento_plantas_m"] = ler_float("Novo espaçamento entre plantas (m)")
    elif campo == 6:
        atual["dimensoes"] = ler_dimensoes(atual["cultura"])
    else:
        _, configuracao = escolher_cultura()
        atual = montar_registro(
            atual["talhao"],
            configuracao["nome"],
            configuracao["geometria"],
            ler_dimensoes(configuracao["nome"]),
            configuracao["espacamento_ruas_m"],
            configuracao["espacamento_plantas_m"],
            configuracao["produto"],
            configuracao["dose_g_planta"],
            atual.get("data_registro"),
        )

    if campo != 7:
        atual = montar_registro(
            atual["talhao"],
            atual["cultura"],
            atual["geometria"],
            atual["dimensoes"],
            atual["espacamento_ruas_m"],
            atual["espacamento_plantas_m"],
            atual["produto"],
            atual["dose_g_planta"],
            atual.get("data_registro"),
        )
    registros[posicao] = atual
    persistir(registros)
    print(f"Posição {posicao} atualizada e campos calculados novamente.")
    exibir_registro(posicao, atual)


def deletar_dados(registros: list[dict[str, Any]]) -> None:
    print("\n=== EXCLUSÃO ===")
    posicao = escolher_posicao(registros, "excluir")
    if posicao is None:
        return
    registro = registros[posicao]
    confirmacao = input(
        f"Excluir '{registro['talhao']} - {registro['cultura']}'? (s/n): "
    ).strip().lower()
    if confirmacao == "s":
        removido = registros.pop(posicao)
        persistir(registros)
        print(f"Registro '{removido['talhao']}' removido do vetor.")
    else:
        print("Exclusão cancelada.")


def exibir_menu() -> None:
    print(
        "\n========================================\n"
        " FARMTECH SOLUTIONS - AGRICULTURA PARÁ\n"
        "========================================\n"
        "1 - Entrada de dados\n"
        "2 - Saída de dados\n"
        "3 - Atualizar posição do vetor\n"
        "4 - Deletar posição do vetor\n"
        "5 - Exportar dados para o R (CSV)\n"
        "6 - Sair do programa"
    )


def main() -> None:
    registros = carregar_registros()
    while True:
        exibir_menu()
        opcao = ler_inteiro("Escolha uma opção: ", 1, 6)
        if opcao == 1:
            entrada_dados(registros)
        elif opcao == 2:
            saida_dados(registros)
        elif opcao == 3:
            atualizar_dados(registros)
        elif opcao == 4:
            deletar_dados(registros)
        elif opcao == 5:
            exportar_csv(registros)
            print(f"Arquivo gerado: {ARQUIVO_CSV.name}")
        else:
            persistir(registros)
            print("Dados salvos. Até a próxima!")
            break


if __name__ == "__main__":
    main()
