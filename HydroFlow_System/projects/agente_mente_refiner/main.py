import os
import sys

def refine_air_prompt(input_path, output_path):
    print(f"Agente Mente: Refinando pedido de Bot AIR en {input_path}")
    
    if not os.path.exists(input_path):
        print("No hay pedidos pendientes de Bot AIR.")
        return

    # Leemos el "pedido" de Bot AIR
    with open(input_path, 'r', encoding='utf-8') as f:
        pedido = f.read()

    # Lógica de refinamiento (simulada por ahora con mejoras de keywords)
    prompt_refinado = f"""PROMPT REFINADO POR AGENTE_MENTE:
---
CONTEXTO: {pedido}
MEJORA: Agregando profundidad técnica, iluminación cinematográfica y estilo fractal.
RESULTADO: Cinematic shot, fractal patterns blending with {pedido}, hyper-realistic, 8k, golden hour lighting.
---"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prompt_refinado)
    
    print(f"Refinamiento completado. Resultado en {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
        
    in_p = sys.argv[1]
    out_p = sys.argv[2]
    
    refine_air_prompt(in_p, out_p)
    sys.exit(0)
