import os

def list_files(startpath):
    ignore_dirs = [
        '.vscode', 
        'media', 
        'nutri_venv', 
        # 'templates', 
        'migrations',
        '__pycache__',
        '.git',
        'datagrid',
        'formplugins',
        'json-path-picker',
        'miscellaneous',
        'notifications',
        'skins',
        'statistics',
        'themes'

    ]
    
    with open('estrutura_projeto.txt', 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            
            # Ignorar diretórios não desejados
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            # Se você quiser ignorar mais diretórios, pode adicioná-los à lista ignore_dirs
            
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            f.write(f'{indent}{os.path.basename(root)}/\n')
            
            # Listando apenas arquivos .py, excluindo arquivos de migração e iniciadores
            py_files = [file for file in files if file.endswith('.py') and not file in ['__init__.py', '0001_initial.py', '0002_categoria_ordem.py', '0003_categoria_capa.py', '0004_categoria_descricao.py', '0002_infosapp_nome_reduzido.py', '0003_alter_infosapp_nome_reduzido.py']]
            
            subindent = ' ' * 4 * (level + 1)
            for file in py_files:
                f.write(f'{subindent}{file}\n')
# Substitua 'caminho/do/seu/projeto' pelo caminho real do seu projeto Django
list_files(r'C:\Users\cristian.torres\GitHub\Portal-Bruna-Nutricionista')
