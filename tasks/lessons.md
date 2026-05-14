# Lecciones aprendidas — Orquestador

Actualizar después de cada corrección del usuario. Revisar al inicio de cada sesión relevante.
Si el mismo error ocurre dos veces → actualizar el protocolo en `orquestador/CLAUDE.md` directamente.

---

## Formato de entrada

```
### [YYYY-MM-DD] Lección: <título breve>
**Qué salió mal:** <descripción concisa>
**Causa raíz:** <por qué ocurrió>
**Regla nueva:** <qué hacer diferente la próxima vez>
**Aplica a:** [delegación / spec / síntesis / validación]
```

---

## Registro

### [2026-05-13] Lección: Recomendaciones ad-hoc fuera de contexto
**Qué salió mal:** En análisis directo de imágenes (modo ad-hoc sin ENTREGA formal), el orquestador generó recomendaciones derivadas del conocimiento general de Arauco/forestal en vez de los hallazgos específicos de las imágenes. Las recomendaciones sonaban correctas para el dominio pero no estaban ancladas a los datos reales analizados.
**Causa raíz:** El protocolo de síntesis formal (review skill con checklist Paso 3.5) solo se activa con ENTREGAs de agentes. En modo ad-hoc no había ningún freno que exigiera derivación desde evidencia.
**Regla nueva:** Cada recomendación en síntesis ad-hoc debe citar explícitamente la evidencia del insumo que la origina. Si no hay evidencia presente → no incluir la recomendación, usar bloque "Hipótesis a validar" en su lugar.
**Aplica a:** síntesis / validación
