"""Chat por consola (el script del reto 06/10, contenerizado).

    docker compose run --rm api python chat_cli.py
"""

import requests

import backend


def main():
    print(f"Backend {backend.modo()} → {backend.BACKEND_URL} · modelo {backend.MODEL}")
    print("Comandos: /nuevo, /salir\n")
    historial = [{"role": "system", "content": "Eres un asistente útil. Responde en español."}]
    while True:
        try:
            entrada = input("Tú › ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if entrada == "/salir":
            break
        if entrada == "/nuevo":
            historial = historial[:1]
            continue
        if not entrada:
            continue
        historial.append({"role": "user", "content": entrada})
        try:
            r = backend.chat(historial)
        except requests.RequestException as e:
            print(f"Error: {e}")
            historial.pop()
            continue
        historial.append({"role": "assistant", "content": r["respuesta"]})
        print(f"\nIA › {r['respuesta']}\n   [{r['tiempo_s']} s · {r['tokens']} tokens · {r['tok_s']} tok/s]\n")


if __name__ == "__main__":
    main()
