# CODIGO

## Windows

### Crear entorno virtual

```bash
python -m venv .venv
```

### Activar entorno virtual

```bash
.\.venv\Scripts\activate
```

> [!WARNING]
> Puedes necesitar ejecutar el siguiente comando en modo administrador para poder activar el entorno virtual: set-executionpolicy remotesigned

## Linux

### Crear entrono virtual

```bash
virtualenv .venv
```

### Activar entorno virtual

```bash
source .venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar aplicación

```bash
python main.py
```

## Ejecutar tests

```bash
python -m unittest -v
```