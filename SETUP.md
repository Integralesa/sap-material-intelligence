# Setup - Material Intelligence Agent

## Paso 1: Preparar el Repositorio Localmente

```bash
# Crear carpeta del proyecto
mkdir sap-material-intelligence
cd sap-material-intelligence

# Inicializar git
git init

# Crear estructura de carpetas
mkdir agent
mkdir data
mkdir examples
```

## Paso 2: Crear Estructura de Carpetas

```
sap-material-intelligence/
├── agent/
│   ├── __init__.py           # (copiar de agent_init.py → agent/__init__.py)
│   └── core.py               # (copiar de agent_core.py → agent/core.py)
├── main.py                   # (copiar archivo main.py)
├── requirements.txt          # (copiar archivo)
├── .env.example              # (copiar archivo)
├── .gitignore                # (copiar archivo)
├── LICENSE                   # (copiar archivo)
├── README.md                 # (copiar archivo)
└── SETUP.md                  # (copiar este archivo)
```

## Paso 3: Copiar Archivos

Copia los siguientes archivos a sus ubicaciones:

1. **agent/__init__.py** ← agent_init.py
2. **agent/core.py** ← agent_core.py
3. **main.py** ← main.py
4. **requirements.txt** ← requirements.txt
5. **.env.example** ← .env.example
6. **.gitignore** ← .gitignore
7. **LICENSE** ← LICENSE
8. **README.md** ← README.md

## Paso 4: Configurar .env Local

```bash
# Copiar template
cp .env.example .env

# Editar .env y agregar tu API key
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## Paso 5: Instalar Dependencias Locales

```bash
# Crear virtual environment
python -m venv venv

# Activar (en Windows)
venv\Scripts\activate

# Activar (en Mac/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Paso 6: Probar Localmente

```bash
# Ejecutar demo
python main.py

# Modo interactivo
python main.py --interactive
```

## Paso 7: Crear en GitHub

1. Ve a https://github.com/new
2. Nombre del repo: `sap-material-intelligence`
3. Descripción: "Agente de IA personalizado para validación de Master Data en SAP"
4. Public (para que otros lo vean)
5. NO marques "Initialize with README" (ya tenemos uno)
6. Create repository

## Paso 8: Push a GitHub

```bash
# Agregar archivos
git add .

# Commit inicial
git commit -m "Initial commit: Material Intelligence Agent framework"

# Agregar origen remoto
git remote add origin https://github.com/integralesa/sap-material-intelligence.git

# Push
git branch -M main
git push -u origin main
```

## Paso 9: Verificar en GitHub

Visita: https://github.com/integralesa/sap-material-intelligence

Deberías ver:
- README.md bonito
- Estructura de carpetas
- Archivo de licencia

## Paso 10: Compartir en LinkedIn

Post:

```
Acabo de publicar mi agente de validación de materiales en GitHub.

Es lo que creé para validar MDG en SAP.
Ahora lo estoy mejorando y ofreciendo a empresas.

Código abierto, funcional, personalizable.

Si trabajas con SAP, revisa cómo funciona.
Si buscas ayuda con validación, escribí.

https://github.com/integralesa/sap-material-intelligence
```

---

## Troubleshooting

### Error: "No module named 'anthropic'"
```bash
pip install anthropic
```

### Error: "ANTHROPIC_API_KEY not found"
```bash
# Verificar que .env existe y tiene la key
cat .env
```

### Error: "Permission denied" en Linux
```bash
chmod +x main.py
./main.py
```

### Error de git "failed to push"
```bash
# Asegurar que estás autenticado en GitHub
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

---

## Próximos Pasos

Una vez en GitHub:

1. ✅ Compartir link en LinkedIn
2. ✅ Mencionar en discovery calls
3. ✅ Usar en demos: "Acá está el código del agente"
4. ✅ Invitar a contribuir
5. ✅ Evolucionar según feedback de clientes
