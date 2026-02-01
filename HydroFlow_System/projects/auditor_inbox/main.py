import os
import sys
import shutil

def audit_inbox(input_dir, output_dir):
    print(f"Auditor Inbox: Analizando {input_dir}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Lógica simple de auditoría: 
    # - Si el archivo es .md y tiene más de 100 caracteres, se considera "valioso"
    # - Si es muy corto, se queda en inbox por ahora (o se podría marcar para borrar)
    
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        
        if os.path.isfile(filepath) and filename.endswith('.md'):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if len(content) > 100:
                print(f"Aprobado: {filename} (Tamaño: {len(content)})")
                shutil.copy(filepath, os.path.join(output_dir, filename))
            else:
                print(f"Descartado/Pendiente: {filename} (Demasiado corto)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python main.py <input_dir> <output_dir>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        audit_inbox(input_path, output_path)
        sys.exit(0)
    except Exception as e:
        print(f"Error en auditoria: {e}")
        sys.exit(1)
