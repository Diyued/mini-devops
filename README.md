# Mini proyecto DevOps — API Calculadora

API Flask minúscula para practicar el pipeline **push → test → docker → deploy**.

## Estructura
```
src/                 código (app.py, calculator.py)
tests/unit/          pruebas unitarias (pytest)
Dockerfile           imagen de producción (gunicorn, usuario no-root)
docker-compose.yml   se copia al servidor y levanta la imagen
.github/workflows/   pipeline CI/CD
```

## Local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest tests/unit/ --cov=src          # pruebas
python -m src.app                     # http://localhost:8000/health
curl "localhost:8000/calc/add?a=2&b=3"

docker compose up --build             # con Docker, en http://localhost
```

## Pipeline
| Job | Cuándo | Qué hace |
|---|---|---|
| build-and-test | push y PR | instala deps, pytest + cobertura (artifact) |
| docker-build | push a main/develop | build y push a ghcr.io |
| deploy | push a main/develop | SSH al servidor, `docker compose pull && up -d` |

`main` → environment **production**, `develop` → **staging**.

## Secrets (Settings → Secrets and variables → Actions)
- `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`
- `GHCR_PULL_TOKEN`: PAT con `read:packages` para que el servidor haga pull
- (`GITHUB_TOKEN` es automático)

## Preparar el servidor (una vez)
```bash
sudo mkdir -p /opt/app && sudo chown $USER /opt/app
# Docker + compose plugin instalados
```

## Probar el pipeline
1. Crea repo en GitHub y sube este proyecto a `main`.
2. Agrega los secrets y crea los environments `production` y `staging`.
3. Haz un cambio y push → mira la pestaña **Actions**.
4. Rompe un test a propósito: el pipeline se corta y no despliega.

## Rollback
Cada build queda con tag `sha-xxxxxxx`. Para volver atrás en el servidor:
`IMAGE=ghcr.io/<owner>/<repo>:sha-xxxxxxx docker compose up -d`
