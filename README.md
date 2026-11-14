# Examen II Parcial — Programación de Negocios (UNICAH)

- **Estudiante:** Luis Medina
- **Número de cuenta:** 0806200300590

## Estructura del proyecto

1. **`tienda_unicah`** *(Partes 1 a 5)*:
   - Extensión de contactos (`res.partner`) con datos universitarios (`tipo_cliente`, `numero_cuenta`, `carrera`) en la pestaña **UNICAH** y validación de cuenta estudiantil.
   - Modelo de convenios de descuento (`tienda.convenio`) con reglas de acceso (`ir.access.csv`), convenios iniciales, vistas de lista/formulario y validaciones de porcentaje y vigencia.
   - Extensión de pedidos de venta (`sale.order`) con asignación automática de convenio vigente, botón **Aplicar convenio**, mensaje en el chatter, límite de unidades para estudiantes y cálculo de `monto_ahorro` con vistas de lista, filtro y agrupación.
2. **`unicah_becas`** *(Parte 6 — Propuesta propia para la universidad)*:
   - Gestión de solicitudes de becas estudiantiles (`unicah.beca`) con cálculo automático de porcentaje otorgado según el tipo de beca y el índice académico, descuento mensual y cuota neta a pagar.
   - Permisos en `security/ir.access.csv`, vistas de lista, formulario y búsqueda, menú **Becas UNICAH** en *Sales > Configuration*, herencia de `res.partner` para mostrar el historial de becas en la pestaña **UNICAH** del estudiante, y validaciones con `@api.constrains` y en la aprobación.
