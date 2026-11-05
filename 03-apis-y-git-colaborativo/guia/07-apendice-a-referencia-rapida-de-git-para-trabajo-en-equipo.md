# Apéndice A — Referencia rápida de Git para trabajo en equipo

| Quiero... | Comando |
|----|----|
| Actualizar main | `git switch main` · `git pull` |
| Crear mi rama desde main | `git switch -c feature/etapa-N-nombre-yo` |
| Ver qué cambié | `git status` · `git diff` |
| Guardar un cambio | `git add ruta` · `git commit -m "tipo(alcance): descripción"` |
| Subir mi rama por primera vez | `git push -u origin feature/...` |
| Subir cambios posteriores | `git push` |
| Traer main a mi rama | `git fetch origin` · `git rebase origin/main` |
| Continuar / abortar un rebase | `git rebase --continue` · `git rebase --abort` |
| Subir después de un rebase | `git push --force-with-lease` |
| Ver la historia | `git log --oneline --graph --all` |
| Guardar cambios a medias | `git stash` · `git stash pop` |
| Descartar cambios de un archivo | `git restore ruta` |
| Traer la rama de un compañero para revisar | `git fetch origin` · `git switch feature/su-rama` |
| Borrar mi rama ya mezclada | `git switch main` · `git branch -d feature/...` |
| Ver dónde estuvo HEAD (rescate) | `git reflog` |

### Convención de mensajes de commit

```text
feat(etapa-N): ...      funcionalidad nueva
fix(etapa-N): ...       corrección
refactor(etapa-N): ...  reorganización sin cambio de comportamiento
docs(...): ...          documentación
test(...): ...          pruebas
chore(...): ...         mantenimiento (dependencias, configuración)
```

### Convención de ramas

```text
feature/etapa-N-nombre-tunombre     trabajo en una etapa
contrato/descripcion-corta          cambio al contrato (revisa todo el equipo)
docs/descripcion-corta              solo documentación
```
