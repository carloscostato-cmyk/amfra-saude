# Explicação do Código: Gráfico Consolidado NR-1

## Visão Geral

Este documento explica como o código do gráfico consolidado funciona, linha por linha, para facilitar futuras manutenções.

---

## 1. Estrutura HTML

### Canvas Element

```html
<canvas id="consolidatedChart" 
        role="img" 
        aria-label="Gráfico de barras horizontais mostrando a distribuição de colaboradores por nível de risco psicossocial">
</canvas>
```

**Explicação:**
- `<canvas>`: Elemento HTML5 onde o Chart.js desenha o gráfico
- `id="consolidatedChart"`: Identificador único para o JavaScript encontrar
- `role="img"`: Informa screen readers que é uma imagem
- `aria-label`: Descrição para acessibilidade

### Descrição Oculta (Acessibilidade)

```html
<div id="chartDescription" style="position: absolute; left: -10000px; ...">
    Distribuição de riscos psicossociais: 
    BAIXO: 5 colaboradores (20.0%).
    MÉDIO: 12 colaboradores (48.0%).
    ALTO: 8 colaboradores (32.0%).
</div>
```

**Explicação:**
- Div posicionado fora da tela (mas não `display: none`)
- Screen readers conseguem ler o conteúdo
- Usuários visuais não veem (está a -10000px à esquerda)

---

## 2. CSS

### Container do Gráfico

```css
.nr1-chart-container {
    position: relative;
    height: 300px;
    margin: 1.5rem 0;
    padding: 1.5rem;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
}
```

**Explicação:**
- `position: relative`: Permite posicionamento absoluto dos filhos
- `height: 300px`: Altura fixa para o gráfico (Chart.js precisa disso)
- `margin`, `padding`: Espaçamento consistente com o design
- `background`, `border`, `border-radius`: Estilo visual

### Responsividade Mobile

```css
@media (max-width: 600px) {
    .nr1-chart-container { height: 250px; }
}
```

**Explicação:**
- Em telas < 600px (mobile), reduz altura para 250px
- Economiza espaço vertical em telas pequenas
- Gráfico permanece legível

---

## 3. JavaScript - Preparação de Dados

### Estrutura de Dados

```javascript
const chartData = {
    labels: ['BAIXO', 'MÉDIO', 'ALTO'],
    counts: [
        {{ report.risk_distribution.get('BAIXO', 0) }},
        {{ report.risk_distribution.get('MÉDIO', 0) }},
        {{ report.risk_distribution.get('ALTO', 0) }}
    ],
    colors: ['#ef4444', '#f59e0b', '#10b981'],
    borderColors: ['#dc2626', '#d97706', '#059669']
};
```

**Explicação:**
- `labels`: Nomes das barras (eixo Y)
- `counts`: Valores numéricos (eixo X)
- `{{ ... }}`: Sintaxe Jinja2 - substituído pelo backend
- `report.risk_distribution.get('BAIXO', 0)`: Pega valor do dict, default 0
- `colors`: Cores de preenchimento das barras
- `borderColors`: Cores das bordas (um tom mais escuro)

### Cálculo do Total

```javascript
const total = chartData.counts.reduce((a, b) => a + b, 0);
```

**Explicação:**
- `reduce()`: Soma todos os valores do array
- `(a, b) => a + b`: Função que soma dois números
- `, 0`: Valor inicial da soma
- Resultado: total de colaboradores (ex: 5 + 12 + 8 = 25)

---

## 4. JavaScript - Configuração do Chart.js

### Criação do Gráfico

```javascript
new Chart(ctx, {
    type: 'bar',
    data: { ... },
    options: { ... }
});
```

**Explicação:**
- `new Chart()`: Cria instância do gráfico
- `ctx`: Contexto do canvas (onde desenhar)
- `type: 'bar'`: Tipo de gráfico (barras)
- `data`: Dados a serem exibidos
- `options`: Configurações visuais e comportamentais

### Configuração: Barras Horizontais

```javascript
options: {
    indexAxis: 'y',
    // ...
}
```

**Explicação:**
- `indexAxis: 'y'`: Inverte os eixos
- Padrão: barras verticais (indexAxis: 'x')
- Com 'y': barras horizontais (o que queremos)

### Configuração: Responsividade

```javascript
responsive: true,
maintainAspectRatio: false,
```

**Explicação:**
- `responsive: true`: Gráfico se adapta ao tamanho do container
- `maintainAspectRatio: false`: Permite altura fixa (300px)
- Sem isso, Chart.js tentaria manter proporção 2:1

### Configuração: Legenda

```javascript
plugins: {
    legend: {
        display: false
    },
    // ...
}
```

**Explicação:**
- `legend.display: false`: Esconde a legenda padrão
- Não precisamos porque as cores são auto-explicativas
- Labels já identificam cada barra (BAIXO, MÉDIO, ALTO)

### Configuração: Tooltip

```javascript
tooltip: {
    enabled: true,
    callbacks: {
        label: function(context) {
            const value = context.parsed.x;
            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
            return `${value} colaboradores (${percentage}%)`;
        }
    }
}
```

**Explicação:**
- `enabled: true`: Ativa tooltips (aparecem ao passar o mouse)
- `callbacks.label`: Customiza o texto do tooltip
- `context.parsed.x`: Valor da barra (ex: 5)
- `((value / total) * 100).toFixed(1)`: Calcula percentual com 1 casa decimal
- `total > 0 ?`: Evita divisão por zero
- Resultado: "5 colaboradores (20.0%)"

### Configuração: Datalabels (Labels nas Barras)

```javascript
datalabels: {
    anchor: 'end',
    align: 'end',
    color: '#0f172a',
    font: {
        weight: 'bold',
        size: 13
    },
    formatter: function(value, context) {
        const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
        return `${value} (${percentage}%)`;
    }
}
```

**Explicação:**
- `anchor: 'end'`: Posiciona label no final da barra
- `align: 'end'`: Alinha label à direita
- `color`: Cor do texto (preto escuro)
- `font.weight: 'bold'`: Texto em negrito
- `font.size: 13`: Tamanho da fonte
- `formatter`: Função que formata o texto
- Resultado: "5 (20.0%)" aparece na barra

### Configuração: Eixo X (Horizontal)

```javascript
scales: {
    x: {
        beginAtZero: true,
        ticks: {
            stepSize: 1,
            precision: 0
        },
        title: {
            display: true,
            text: 'Número de Colaboradores',
            font: { size: 12, weight: 'bold' }
        }
    },
    // ...
}
```

**Explicação:**
- `beginAtZero: true`: Eixo começa em 0 (não em valor mínimo)
- `ticks.stepSize: 1`: Incrementos de 1 em 1 (0, 1, 2, 3...)
- `ticks.precision: 0`: Sem casas decimais (inteiros)
- `title.text`: Label do eixo ("Número de Colaboradores")
- `title.font`: Estilo do label

### Configuração: Eixo Y (Vertical)

```javascript
y: {
    title: {
        display: true,
        text: 'Nível de Risco',
        font: { size: 12, weight: 'bold' }
    }
}
```

**Explicação:**
- Similar ao eixo X
- `title.text`: Label do eixo ("Nível de Risco")
- Não precisa de `ticks` porque são labels categóricos (BAIXO, MÉDIO, ALTO)

---

## 5. Error Handling

### Try-Catch

```javascript
try {
    new Chart(ctx, { ... });
} catch (error) {
    console.error('Failed to initialize consolidated chart:', error);
    ctx.parentElement.innerHTML = '<p style="...">Não foi possível carregar o gráfico.</p>';
}
```

**Explicação:**
- `try { ... }`: Tenta executar o código
- `catch (error)`: Se houver erro, executa este bloco
- `console.error()`: Loga erro no console (para debug)
- `ctx.parentElement.innerHTML`: Substitui canvas por mensagem de erro
- Usuário vê mensagem amigável em vez de página quebrada

---

## 6. Renderização Condicional

### Jinja2 Template

```jinja2
{% if report.status == "success" %}
<script>
    // Código do gráfico aqui
</script>
{% endif %}
```

**Explicação:**
- `{% if ... %}`: Condicional do Jinja2
- `report.status == "success"`: Só renderiza se há dados
- Se `status == "empty"`: script não é incluído no HTML
- Evita erros quando não há dados para exibir

---

## 7. Fluxo de Dados Completo

### Backend → Template → JavaScript → Chart.js

```
1. Backend (Python):
   NR1StudyAgent.run_study()
   └─> return { "risk_distribution": {"BAIXO": 5, "MÉDIO": 12, "ALTO": 8} }

2. Template (Jinja2):
   {{ report.risk_distribution.get('BAIXO', 0) }}
   └─> Substituído por: 5

3. JavaScript:
   const chartData = { counts: [5, 12, 8] }
   └─> Array de números

4. Chart.js:
   new Chart(ctx, { data: { datasets: [{ data: [5, 12, 8] }] } })
   └─> Desenha barras no canvas
```

---

## 8. Exemplo de Dados Reais

### Input (Backend):

```python
report = {
    "status": "success",
    "total_respondents": 25,
    "risk_distribution": {
        "BAIXO": 5,
        "MÉDIO": 12,
        "ALTO": 8
    }
}
```

### Output (HTML Renderizado):

```html
<canvas id="consolidatedChart" ...></canvas>

<script>
const chartData = {
    labels: ['BAIXO', 'MÉDIO', 'ALTO'],
    counts: [5, 12, 8],
    colors: ['#ef4444', '#f59e0b', '#10b981'],
    borderColors: ['#dc2626', '#d97706', '#059669']
};

const total = 25; // 5 + 12 + 8

new Chart(ctx, {
    // ... configuração ...
});
</script>
```

### Output (Visual):

```
BAIXO   ████████ 5 (20.0%)
MÉDIO   ████████████████ 12 (48.0%)
ALTO    ████████ 8 (32.0%)
```

---

## 9. Manutenção Futura

### Como Mudar Cores:

```javascript
// Localizar esta linha:
colors: ['#ef4444', '#f59e0b', '#10b981'],

// Substituir por novas cores (formato hexadecimal):
colors: ['#ff0000', '#ffff00', '#00ff00'],
```

### Como Mudar Altura do Gráfico:

```css
/* Localizar esta linha: */
.nr1-chart-container { height: 300px; }

/* Mudar para nova altura: */
.nr1-chart-container { height: 400px; }
```

### Como Adicionar Mais Classificações:

1. **Backend:** Adicionar nova classificação em `CLASSIFICATION_RULES`
2. **Template:** Adicionar na lista de labels:
   ```javascript
   labels: ['BAIXO', 'MÉDIO', 'ALTO', 'NOVA_CLASSIFICACAO'],
   ```
3. **Template:** Adicionar na lista de counts:
   ```javascript
   counts: [
       {{ report.risk_distribution.get('BAIXO', 0) }},
       {{ report.risk_distribution.get('MÉDIO', 0) }},
       {{ report.risk_distribution.get('ALTO', 0) }},
       {{ report.risk_distribution.get('NOVA_CLASSIFICACAO', 0) }}
   ],
   ```
4. **Template:** Adicionar cor correspondente:
   ```javascript
   colors: ['#ef4444', '#f59e0b', '#10b981', '#3b82f6'],
   ```

### Como Mudar Formato dos Labels:

```javascript
// Localizar esta função:
formatter: function(value, context) {
    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
    return `${value} (${percentage}%)`;
}

// Mudar para novo formato (ex: só percentual):
formatter: function(value, context) {
    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
    return `${percentage}%`;
}
```

---

## 10. Debugging

### Console Logs Úteis:

```javascript
// Adicionar após const chartData = { ... }:
console.log('Chart Data:', chartData);
console.log('Total:', total);

// Adicionar dentro do formatter:
formatter: function(value, context) {
    console.log('Formatting value:', value, 'for label:', context.label);
    // ... resto do código
}
```

### Verificar se Chart.js Carregou:

```javascript
// Adicionar no início do script:
if (typeof Chart === 'undefined') {
    console.error('Chart.js not loaded!');
    return;
}
console.log('Chart.js version:', Chart.version);
```

### Verificar Dados do Backend:

```javascript
// Adicionar após const chartData = { ... }:
if (chartData.counts.every(c => c === 0)) {
    console.warn('All counts are zero! Check backend data.');
}
```

---

## 11. Referências

- **Chart.js Docs:** https://www.chartjs.org/docs/latest/
- **Datalabels Plugin:** https://chartjs-plugin-datalabels.netlify.app/
- **Canvas API:** https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- **Jinja2 Docs:** https://jinja.palletsprojects.com/

---

**Este documento deve ser atualizado sempre que o código for modificado!**
