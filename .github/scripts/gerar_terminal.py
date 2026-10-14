"""Gera o terminal.svg do perfil com a idade calculada automaticamente.

Uso:
    python .github/scripts/gerar_terminal.py              # usa a data de hoje (Sao Paulo)
    python .github/scripts/gerar_terminal.py 2026-10-17   # simula uma data (para testes)
"""

import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

NASCIMENTO = date(2007, 10, 17)
FUSO = ZoneInfo("America/Sao_Paulo")
SAIDA = Path(__file__).resolve().parents[2] / "terminal.svg"


def calcular_idade(hoje: date) -> int:
    idade = hoje.year - NASCIMENTO.year
    if (hoje.month, hoje.day) < (NASCIMENTO.month, NASCIMENTO.day):
        idade -= 1
    return idade


def data_de_hoje() -> date:
    if len(sys.argv) > 1:
        return date.fromisoformat(sys.argv[1])
    return datetime.now(FUSO).date()


def montar_linhas(idade: int):
    return [
        ("cmd", "whoami"),
        ("out", f"Lucas Massaroto, {idade} anos — Douradina, PR, Brasil"),
        ("out", "Desenvolvedor FullStack"),
        ("blank", ""),
        ("cmd", "cat sobre.txt"),
        ("out", "Sempre gostei de tecnologia e comecei a programar ainda criança, por"),
        ("out", "curiosidade. Fui aprendiz de T.I. na Gazin, onde aprendi muito na prática,"),
        ("out", "e hoje sigo na empresa atuando como desenvolvedor Full-Stack."),
        ("blank", ""),
        ("cmd", "ls stack/frontend"),
        ("out", "React.js  JavaScript  HTML5  CSS3  Bootstrap"),
        ("blank", ""),
        ("cmd", "ls stack/backend"),
        ("out", "Laravel  PHP  Node.js  MySQL  PostgreSQL"),
        ("blank", ""),
        ("cmd", "ls stack/ferramentas"),
        ("out", "Git  Docker  VSCode  Insomnia  npm"),
        ("blank", ""),
        ("cmd", "cat contato.txt"),
        ("out", "instagram : @lucasmassaroto17"),
        ("out", "tiktok    : @lucasmassaroto1"),
        ("out", "email     : lucasmassaroto17@gmail.com"),
        ("blank", ""),
        ("prompt", ""),
    ]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def gerar_svg(lines) -> str:
    font_size = 14
    line_height = 22
    pad_left = 24
    bar_height = 36
    top_padding = 18
    bottom_padding = 20
    width = 780
    height = bar_height + top_padding + len(lines) * line_height + bottom_padding

    green_cmd = "#B6FCB6"
    green_out = "#7FE58C"
    prompt_sym = "#7FE58C"

    p = []
    p.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" font-family="SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace">')
    p.append(f'<rect x="0" y="0" width="{width}" height="{height}" rx="10" fill="#0d1117"/>')
    p.append(f'<rect x="0" y="0" width="{width}" height="{bar_height}" rx="10" fill="#161b22"/>')
    p.append(f'<rect x="0" y="{bar_height-10}" width="{width}" height="10" fill="#161b22"/>')
    p.append('<circle cx="22" cy="18" r="6" fill="#ff5f56"/>')
    p.append('<circle cx="42" cy="18" r="6" fill="#ffbd2e"/>')
    p.append('<circle cx="62" cy="18" r="6" fill="#27c93f"/>')
    p.append(f'<text x="{width/2}" y="23" fill="#8b949e" font-size="12" text-anchor="middle">lucas@massaroto: ~</text>')

    y = bar_height + top_padding + font_size
    for kind, text in lines:
        if kind == "cmd":
            p.append(f'<text x="{pad_left}" y="{y}" font-size="{font_size}" xml:space="preserve"><tspan fill="{prompt_sym}" font-weight="bold">$ </tspan><tspan fill="{green_cmd}" font-weight="bold">{esc(text)}</tspan></text>')
        elif kind == "out":
            p.append(f'<text x="{pad_left}" y="{y}" font-size="{font_size}" fill="{green_out}" xml:space="preserve">{esc(text)}</text>')
        elif kind == "prompt":
            p.append(f'<text x="{pad_left}" y="{y}" font-size="{font_size}" xml:space="preserve"><tspan fill="{prompt_sym}" font-weight="bold">$ </tspan><tspan fill="{green_cmd}">_</tspan><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></text>')
        y += line_height

    p.append("</svg>")
    return "\n".join(p)


def main() -> None:
    hoje = data_de_hoje()
    idade = calcular_idade(hoje)
    SAIDA.write_text(gerar_svg(montar_linhas(idade)), encoding="utf-8")
    print(f"terminal.svg gerado: data={hoje} idade={idade}")


if __name__ == "__main__":
    main()
