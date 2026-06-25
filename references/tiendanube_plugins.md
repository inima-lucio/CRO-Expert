# TiendaNube App Stack — Referencia de Plugins CRO

## Cómo usar este archivo

Phase 8 usa esta referencia para generar **recomendaciones diagnósticas de apps** — no una lista estática, sino apps específicas activadas por hallazgos concretos del audit. Cada recomendación debe citar el callout ID o la métrica de datos que la justifica.

**Regla fundamental:** Nunca recomendar una app porque "sería útil". Siempre citar el gap concreto: `"PDP-SOCIAL-01 detectó < 5 reviews visibles → Judge.me resuelve esto en 1 hora con impacto directo en CVR"`.

---

## Orden de prioridad de implementación

Cuando hay múltiples gaps, seguir este orden de ROI típico × velocidad de impacto:

| Prioridad | Categoría | ROI típico | Tiempo al primer retorno |
|-----------|-----------|-----------|--------------------------|
| 1 | Carrito abandonado (Perfit) | 3–8× inversión | 1–2 semanas |
| 2 | Reviews (Judge.me) | 2–4× inversión | 4–8 semanas |
| 3 | WhatsApp Business button | 1.5–3× inversión | Inmediato |
| 4 | Pop-up de captura / exit intent | 2–5× inversión | 2–4 semanas |
| 5 | Urgency + scarcity widgets | 1.5–2.5× inversión | Inmediato |
| 6 | Búsqueda IA (Doofinder) | 2–4× inversión | 4–8 semanas |
| 7 | Loyalty / puntos (Smile.io) | 2–4× inversión | 3–6 meses |
| 8 | Upsell / cross-sell / bundles | 1.5–2× inversión | 4–8 semanas |

---

## CATEGORÍA 1 — Reviews & Prueba Social

**Trigger conditions (cualquiera de estas activa la recomendación):**
- Cialdini `social_proof` score < 2 en PDP
- Callout `PDP-SOCIAL-*` presente
- < 10 reviews visibles en el PDP auditado
- Reviews section ausente o fuera del primer scroll en desktop/mobile
- Benchmark: sectores como belleza, electrónica y productos de salud requieren mínimo 20 reviews recientes para conversión óptima

**Impacto típico en CVR:**
- Mostrar cualquier review vs. sin reviews: +15–30%
- Reviews con fotos vs. solo texto: +25–45%
- >50 reviews vs. <10: +35–65%
- Reviews con foto + video testimonial: +50–80% en PDP

---

### ✅ Reseñas nativas de TiendaNube
- **Costo:** Gratis (incluido en todos los planes TN)
- **Qué hace:** sistema básico de opiniones en producto, estrella simple, texto
- **Cuándo recomendar:** solo como punto de partida si no tienen absolutamente nada
- **Limitación:** sin fotos, sin importación masiva, sin widgets personalizables, sin Q&A
- **Instalación:** nativo — activar en Panel TN → Configuración → Reseñas

---

### ⭐ Judge.me — RECOMENDACIÓN PRINCIPAL DE REVIEWS
- **Costo:** Plan Free (widgets básicos) · Plan Pro $15 USD/mes
- **Qué hace:**
  - Recolección automática de reviews vía email post-compra
  - Reviews con fotos y video
  - Widget de display totalmente personalizable
  - Q&A pública en producto
  - Importación masiva desde CSV / AliExpress / otras plataformas
  - Rich snippets SEO (estrellas en Google)
  - Integración directa con TiendaNube
- **Impacto esperado:** +15–30% CVR en PDP en 60 días de acumulación
- **Por qué recomendar:** mejor relación precio/funcionalidad del mercado, instalación en < 1 hora, soporte en español
- **Instalación:** TN App Store → Judge.me → activar email automático post-compra
- **Tiempo de activación:** 1–2 horas

---

### Stamped.io
- **Costo:** Desde $19 USD/mes
- **Qué hace:** reviews + NPS + UGC + loyalty en un stack integrado
- **Cuándo recomendar:** tiendas con > 500 pedidos/mes que quieren UGC en escala y loyalty combinado
- **Instalación:** TN App Store / vía script
- **Tiempo de activación:** 2–4 horas

---

### Yotpo
- **Costo:** Desde $79 USD/mes
- **Qué hace:** reviews enterprise + loyalty + SMS + visual UGC
- **Cuándo recomendar:** tiendas con > $30K USD/mes revenue y presupuesto de stack tech
- **Nota:** implementación compleja — requiere onboarding dedicado

---

## CATEGORÍA 2 — Carrito Abandonado & Email Automation

**Trigger conditions:**
- Tasa de abandono TN > 70%
- Revenue perdido en abandono > 20% del revenue real (dato de Phase 4C)
- GA4 funnel: drop ATC→Checkout > 60%
- Sin secuencia de recuperación de carrito activa (verificar en Phase 2 HTML si hay pixel de email platform o script de abandonment)
- `tn_orders_abandoned_count` significativo en datos TiendaNube

**Impacto típico:**
- Email de carrito abandonado a 1h: recupera 5–10% de carritos
- Secuencia de 3 emails (1h, 6h, 24h): recupera 10–20% de carritos
- SMS + email combinados: recupera hasta 25%
- Retorno típico: por cada $1 invertido en la herramienta, recuperar $3–8 en revenue perdido

---

### ⭐ Perfit — RECOMENDACIÓN PRINCIPAL PARA LATAM
- **Costo:** Plan Free hasta 1.500 contactos · Planes pagos desde ~$15 USD/mes (escala con lista)
- **Web:** perfit.com.ar
- **Qué hace:**
  - Email marketing + SMS marketing en español
  - **Automatización de carrito abandonado** — trigger inmediato + secuencia 1h / 6h / 24h
  - Flujos automáticos: bienvenida, post-compra, reactivación de clientes dormidos
  - Segmentación por comportamiento: visitó producto, hizo ATC, compró, no compró en X días
  - Editor drag & drop en español con templates para e-commerce
  - Reportes de revenue recuperado en pesos o USD
  - Integración nativa con TiendaNube — sincronización de órdenes, productos y contactos en tiempo real
- **Por qué es la recomendación principal para LATAM:**
  - Integración TN más completa del mercado latinoamericano
  - Soporte en español, horario local (Argentina)
  - Pricing accesible para pymes (no requiere volumen mínimo)
  - Cumple con regulaciones LATAM de email marketing
- **Flujos a activar inmediatamente (en este orden):**
  1. **Carrito abandonado:** 3 emails (1h — "¿Te olvidaste algo?" · 6h — reminder con imagen del producto · 24h — oferta de recuperación 10% off)
  2. **Bienvenida:** secuencia 3 emails al nuevo suscriptor (bienvenida + propuesta de valor + bestsellers)
  3. **Post-compra:** agradecimiento + pedido de review (activar Judge.me si corresponde)
  4. **Reactivación:** clientes sin compra en 60–90 días ("te extrañamos" + oferta exclusiva)
  5. **Winback:** clientes con > 1 compra previa sin comprar en 6 meses (segmento "At Risk" de RFM)
- **Revenue típico recuperado:** 10–20% del valor de carritos abandonados; para una tienda con $5.000 USD/mes en abandono → $500–$1.000 USD/mes recuperados
- **Instalación:** TN App Store → Perfit → conectar cuenta → activar sincronización → configurar flujos
- **Tiempo de activación:** 2–4 horas (incluye setup de los 3 flujos básicos)

---

### Klaviyo
- **Costo:** Free hasta 250 contactos · Desde $20 USD/mes para más
- **Qué hace:** automation premium con segmentación predictiva, A/B testing de emails, CLV predictions, flows avanzados
- **Cuándo recomendar:** tiendas con > $20K USD/mes revenue que quieren automation sofisticada y tienen recursos para configurarlo
- **Vs. Perfit:** más potente, más caro, curva de aprendizaje mayor, interfaz en inglés
- **Instalación:** TN App Store / integración vía API
- **Tiempo de activación:** 4–8 horas (setup correcto lleva tiempo y requiere conocimiento de la herramienta)

---

### ActiveCampaign
- **Costo:** Desde $29 USD/mes
- **Qué hace:** CRM + email automation + scoring de leads + flujos multi-canal
- **Cuándo recomendar:** marcas que venden B2B o tienen ciclo de venta largo (no típico de e-commerce puro)
- **Nota:** menos optimizado para e-commerce puro que Perfit o Klaviyo

---

### Mailchimp
- **Costo:** Free hasta 500 contactos básicos · Desde $13 USD/mes
- **Cuándo recomendar:** SOLO si el cliente ya está en Mailchimp y no quiere migrar
- **Limitación:** integración TN menos profunda que Perfit, no soporta abandonment nativo en plan free

---

## CATEGORÍA 3 — Urgencia & Escasez

**Trigger conditions:**
- Cialdini `urgency` score < 1 en PDP
- Cialdini `scarcity` score < 1 en PDP
- Sin countdown timers ni stock alerts visibles en screenshots
- Callout `PDP-PROMO-*` sobre ausencia de urgencia

**⚠️ Regla crítica:** Recomendar urgencia y escasez SOLO con datos reales. Urgencia falsa (timers que se reinician, "quedan 3 unidades" cuando hay stock infinito) destruye la confianza cuando el usuario lo detecta. Siempre vincular a datos reales de stock o fechas reales de cierre.

**Impacto típico:**
- "Quedan X unidades" con stock real: +6–12% ATC rate
- Countdown timer con deadline real: +10–20% CVR en campaña
- Notificaciones de venta en tiempo real: +8–15% CVR

---

### Sales Pop / Prueba Social en Tiempo Real
- **Costo:** Apps desde gratis (Sales Pop, TrustPulse, Fomo)
- **Qué hace:** muestra notificaciones del tipo "Juan de Buenos Aires compró este producto hace 7 minutos"
- **Cuándo recomendar:** tiendas con > 20 ventas/día — con menos volumen las notificaciones parecen falsas
- **Advertencia:** con < 20 ventas/día la herramienta puede hacer más daño que bien. Mencionarlo en la recomendación.
- **Impacto esperado:** +8–15% CVR cuando los datos son reales y el volumen es creíble

---

### Countdown Timer (urgencia temporal)
- **Costo:** Desde gratis
- **Qué hace:** timer de cuenta regresiva visible en PDP para ofertas con fecha de cierre
- **Cuándo recomendar:** tiendas que hacen campañas temporales activas (Hot Sale, CyberMonday, Black Friday, liquidaciones)
- **Condición:** SOLO con fecha de cierre real. Si el timer se reinicia al recargar → dañino para confianza.
- **Impacto esperado:** +10–20% CVR durante la campaña activa

---

### Stock Scarcity Widget
- **Costo:** Nativo TN (mostrar stock) o apps específicas
- **Qué hace:** "Solo quedan X unidades disponibles" en PDP
- **Cuándo recomendar:** cuando hay stock real limitado de ese SKU — datos de TN disponibles en Phase 4C
- **Condición:** si el stock real es > 20 unidades, no activar. Solo stock genuinamente limitado.

---

## CATEGORÍA 4 — Chat & Soporte Pre-Compra

**Trigger conditions:**
- Nielsen H10 (help & documentation) score < 2
- Sin botón de WhatsApp visible en PDP o checkout (callout `PDP-TRUST-*` o `CO-TRUST-*`)
- Callout `CO-FORM-*` sobre fricción en checkout sin canal de soporte
- Productos de ticket alto (> $100 USD) o productos con dudas naturales (tallas, compatibilidad, custom)
- Bounce rate en PDP > 65% → puede indicar dudas sin respuesta

**Por qué es crítico para LATAM:**
WhatsApp es el canal de comunicación primario en Argentina, México, Brasil y Colombia. Un porcentaje significativo de usuarios latinoamericanos consulta por WhatsApp ANTES de comprar. Sin botón de WhatsApp visible, se pierden ventas que el usuario habría concretado con una respuesta de 2 minutos.

**Impacto típico:**
- WhatsApp button en PDP: +10–25% CVR en categorías con dudas (moda, electrónica, custom)
- Chat en vivo en checkout: -8–15% abandono de checkout
- Respuesta automática en < 5 minutos: +30% más conversiones por chat que con respuesta > 1 hora

---

### ⭐ WhatsApp Business Button — CRÍTICO PARA LATAM
- **Costo:** Gratis (botón básico vía snippet) · Con chatbot desde ~$15 USD/mes
- **Qué hace:** botón flotante de WhatsApp en todas las páginas, click abre conversación pre-cargada con contexto del producto
- **Integración TN:** snippet de código (< 5 min) o apps de TN App Store
- **Tip de implementación:** configurar mensaje pre-cargado con el nombre del producto visto: "Hola, me interesa [nombre del producto], ¿tienen disponibilidad?"
- **Placement óptimo:** visible en PDP near ATC button Y en checkout (reduce abandono por dudas de pago)
- **Impacto esperado:** +10–25% en ventas para productos con preguntas frecuentes
- **Tiempo de activación:** 30 minutos

---

### Tidio — Chat + Chatbot
- **Costo:** Plan free (live chat básico) · Desde $19 USD/mes (chatbot automático)
- **Qué hace:** live chat en web, chatbot de respuesta automática a preguntas frecuentes, integración con WhatsApp e Instagram
- **Integration:** TiendaNube plugin
- **Cuándo recomendar:** tiendas con equipo de soporte activo que puede responder chats en horario comercial
- **Impacto esperado:** -8–15% abandono de checkout cuando hay soporte activo

---

### JivoChat
- **Costo:** Desde gratis para 1 agente
- **Qué hace:** omnichannel — chat web + WhatsApp + Instagram + Telegram en un panel
- **Por qué para LATAM:** muy popular en Argentina y México, interfaz en español, soporte local
- **Integration:** TiendaNube vía código o app

---

## CATEGORÍA 5 — Búsqueda Inteligente

**Trigger conditions:**
- Callout `HOME-NAV-*` sobre buscador ausente o deficiente
- Catálogo detectado con > 100 SKUs y sin buscador con autocompletado visible
- Bounce rate en home > 60% (usuarios que no encuentran lo que buscan)
- Sesiones con 0 páginas vistas adicionales (entrada + salida en home = no encontraron nada)

**Por qué importa:**
Los usuarios que usan la búsqueda interna tienen 2–5× más intención de compra que los que navegan por categorías. Si la búsqueda falla (typos, nombres inexactos, sin sugerencias), se pierden los visitantes de más alta conversión.

**Impacto típico:**
- Búsqueda con autocompletado vs. búsqueda básica: +15–20% en revenue de sesiones con búsqueda
- Búsqueda con typo tolerance: -25–40% en tasa de resultado vacío

---

### Doofinder — Búsqueda IA
- **Costo:** Desde $35 USD/mes (trial 30 días gratis)
- **Qué hace:** motor de búsqueda IA con autocompletado inteligente, tolerancia a typos, sinónimos configurables, búsqueda por imagen, resultados personalizados por comportamiento
- **Integration:** TiendaNube app nativa — indexación automática del catálogo
- **Cuándo recomendar:** catálogos > 50 SKUs, bounce rate alto en home, presupuesto para herramienta
- **Impacto esperado:** +15–20% revenue de sesiones que usan búsqueda
- **Tiempo de activación:** 1–2 horas (instalación + configuración inicial del índice)

---

## CATEGORÍA 6 — Loyalty & Retención

**Trigger conditions:**
- Tasa de recompra < 20% (ecommerce-bi análisis #6)
- Cohorte de retención M1 < 15% (ecommerce-bi análisis #9)
- Cialdini `commitment` score < 1 (sin programa de fidelización visible)
- Sin menciones a puntos, cashback, o beneficios para clientes recurrentes

**Por qué importa:**
Adquirir un nuevo cliente cuesta 5–7× más que retener uno existente. Un programa de loyalty bien ejecutado puede aumentar la frecuencia de compra 20–30% y el CLV 2–4×.

---

### Smile.io
- **Costo:** Plan Free (básico) · Starter desde $49 USD/mes
- **Qué hace:** programa de puntos por compra, programa de referidos, tiers VIP con beneficios, widget embebido en PDP y carrito
- **Integration:** TiendaNube App Store
- **Cuándo recomendar:** tiendas con > 200 clientes repetidores/mes y ticket promedio > $40 USD
- **Impacto esperado:** +30–50% tasa de recompra con loyalty activo en 6 meses
- **Tiempo de activación:** 3–4 horas (configuración de estructura de puntos + widget)

---

## CATEGORÍA 7 — Pop-ups & Captura de Email/Leads

**Trigger conditions:**
- Sin email capture visible en home (callout `HOME-PROMO-*` o `HOME-CTA-*`)
- Bounce rate > 65% sin captura de lead → tráfico pagado desperdiciado
- Sin lista de emails activa para retargeting

**Impacto típico:**
- Pop-up con descuento de bienvenida: captura 5–8% de visitantes únicos
- Exit-intent pop-up: captura adicional 3–5% de los que iban a salir
- Quiz de captura: 8–15% (mayor calidad de lead + segmentación automática)

---

### Pop-up Nativo TiendaNube
- **Costo:** Incluido en planes TN
- **Qué hace:** pop-up de descuento o captura de email en primera visita o exit intent
- **Cuándo recomendar:** punto de partida si no tienen nada de captura
- **Limitación:** opciones de personalización limitadas

---

### Privy
- **Costo:** Plan Free limitado · Desde $30 USD/mes
- **Qué hace:** exit-intent pop-ups, slide-ins, banners, A/B testing de pop-ups, integración directa con Klaviyo/Mailchimp/Perfit
- **Integration:** TiendaNube vía script
- **Cuándo recomendar:** tiendas con > 1.000 visitas/mes que quieren captura optimizada con A/B testing
- **Impacto esperado:** +6–15% en captura de emails de visitantes únicos

---

## CATEGORÍA 8 — Upsell, Cross-sell & Bundles

**Trigger conditions:**
- AOV por debajo del benchmark de categoría (ver `references/benchmarks.md`)
- CART callouts sobre ausencia de cross-sell
- Market Basket analysis (ecommerce-bi #1) muestra combos con lift > 1.5
- Productos ancla identificados (ecommerce-bi #4) sin sección "compraron junto"

**Impacto típico:**
- Cross-sell relevante en PDP: +8–15% AOV
- Bundles con descuento: +15–25% AOV
- "Compradores también vieron" en cart: +5–10% AOV

---

### Bundles / Combos de Productos
- **Qué hace:** permite armar paquetes de productos con descuento por volumen o combinación
- **TN nativo:** TiendaNube tiene descuentos por volumen y promociones combo en su panel
- **Cuándo recomendar:** cuando market basket analysis detecta combinaciones frecuentes (ej: shampoo + acondicionador, cargador + funda, etc.)
- **Impacto esperado:** +15–25% AOV cuando el combo es relevante

---

### Frequently Bought Together (Cross-sell automático en PDP)
- **Qué hace:** sección "compradores también llevaron" en PDP y carrito, poblada automáticamente por algoritmo o manualmente
- **TN nativo:** sección de productos relacionados ya existe en TN — el gap suele ser en la configuración, no en la herramienta
- **Cuándo recomendar:** cuando la sección existe pero está vacía o mal configurada (callout `PDP-COPY-*` o `CART-CROSS-*`)
- **Impacto esperado:** +8–15% AOV con cross-sell relevante

---

## CATEGORÍA 9 — Pagos & Métodos de Pago

**Trigger conditions:**
- Sin métodos de pago locales LATAM visibles en PDP o checkout (callout `CO-PAYMENT-*`)
- Sin opción de cuotas visible para ticket promedio > $50 USD
- Sin Apple Pay / Google Pay para móvil
- Callout sobre PayU, MercadoPago, o métodos regionales ausentes

**Por qué crítico en LATAM:**
En Argentina, Brasil, México y Colombia, los métodos de pago locales son decisivos. Un usuario que llega al checkout y no ve su método preferido abandona inmediatamente. Las cuotas sin interés son el principal driver de conversión para tickets > $80 USD en Argentina.

---

### MercadoPago — CRÍTICO PARA ARGENTINA Y REGIÓN
- **Costo:** Comisión por transacción (3–4.99% según plan)
- **Qué hace:** acepta tarjetas crédito/débito, transferencias bancarias, QR, cuotas, billetera digital MP
- **Integration:** TiendaNube tiene integración nativa oficial
- **Cuándo recomendar:** cualquier tienda argentina o latinoamericana sin MercadoPago activo
- **Impacto:** crítico — es el método de pago preferido en Argentina (> 40% de las transacciones online)

---

### Cuotas sin interés (via MercadoPago o banco)
- **Qué hace:** permite pagar en 3, 6, 12 cuotas sin costo adicional para el comprador
- **Cuándo recomendar:** ticket promedio > $50 USD en Argentina — las cuotas pueden aumentar el ticket +30–50%
- **Nota:** mostrar el precio en cuotas en el PDP ("3 cuotas de $X sin interés") es uno de los cambios de mayor impacto inmediato en conversión para LATAM

---

### PayU (México, Colombia, Perú)
- **Qué hace:** gateway de pago regional para mercados fuera de Argentina
- **Integration:** TiendaNube
- **Cuándo recomendar:** tiendas con operación en México, Colombia, Perú que no tienen gateway local

---

## Contrato de datos — Plugin Recommendations JSON

Cada recomendación de app genera una entrada en `cro_plugins.json`:

```json
{
  "platform": "tiendanube",
  "generated_at": "ISO timestamp",
  "triggered_by": ["PDP-SOCIAL-01", "cialdini.social_proof: 1", "reviews_count: 3"],
  "recommendations": [
    {
      "rank": 1,
      "category": "cart_abandonment",
      "app": "Perfit",
      "reason": "La tasa de abandono detectada es 78% con $3.200 USD de revenue perdido mensual. Una secuencia automática de 3 emails de recuperación a 1h/6h/24h puede recuperar entre $320–640 USD/mes. ROI estimado: 5–10× el costo de la herramienta.",
      "triggered_by": ["tn_abandoned_rate: 78%", "tn_revenue_lost: 3200 USD/mes"],
      "expected_impact": "Recuperación del 10–20% del revenue abandonado",
      "roi_estimate": "5–10× inversión",
      "cost": "Desde $15 USD/mes",
      "install_time": "2–4 horas",
      "priority": "critical",
      "action": "Instalar desde TN App Store → activar flujo de carrito abandonado (1h / 6h / 24h) → conectar con Judge.me para pedir review post-compra"
    },
    {
      "rank": 2,
      "category": "reviews",
      "app": "Judge.me",
      "reason": "PDP-SOCIAL-01 detectó solo 3 reviews sin foto, todas de hace 8 meses. Para skincare premium con ticket $89, la prueba social es el principal driver de conversión. Judge.me automatiza la recolección de reviews con foto post-compra.",
      "triggered_by": ["PDP-SOCIAL-01", "cialdini.social_proof: 1"],
      "expected_impact": "+15–30% CVR en PDP en 8 semanas de acumulación",
      "roi_estimate": "2–4× inversión",
      "cost": "Gratis (plan Free) o $15 USD/mes (Pro)",
      "install_time": "1 hora",
      "priority": "high",
      "action": "Instalar Judge.me → activar email automático post-compra pidiendo review con foto → configurar widget de reviews near ATC button en PDP"
    }
  ]
}
```
