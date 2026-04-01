# Visual Test Guide: Gráfico Consolidado NR-1

## Objetivo

Este guia ajuda a verificar visualmente se o gráfico consolidado está funcionando corretamente.

## Pré-requisitos

- Servidor rodando localmente (`python run.py`)
- Pelo menos uma empresa com respostas no banco de dados
- Navegador moderno (Chrome, Firefox, Safari, Edge)

## Teste 1: Verificação Básica

### Passos:

1. Abrir `http://localhost:5000/admin/login`
2. Fazer login
3. Clicar em uma empresa que tenha respostas
4. Clicar em "Ver Relatório NR-1"

### O que verificar:

- [ ] **Gráfico aparece** após a seção "Legenda"
- [ ] **Título da seção:** "Distribuição de Riscos Psicossociais"
- [ ] **Subtítulo:** "Visão Consolidada" (badge azul)
- [ ] **Gráfico é de barras horizontais** (não verticais)
- [ ] **3 barras visíveis:** BAIXO, MÉDIO, ALTO
- [ ] **Cores corretas:**
  - BAIXO: Vermelho (#ef4444)
  - MÉDIO: Amarelo/Laranja (#f59e0b)
  - ALTO: Verde (#10b981)

### Screenshot esperado:

```
┌─────────────────────────────────────────────────┐
│ [VISÃO CONSOLIDADA]                             │
│ Distribuição de Riscos Psicossociais           │
├─────────────────────────────────────────────────┤
│                                                 │
│ BAIXO   ████████ 5 (20.0%)                     │
│                                                 │
│ MÉDIO   ████████████████ 12 (48.0%)           │
│                                                 │
│ ALTO    ████████ 8 (32.0%)                     │
│                                                 │
│         0    5    10   15   20                  │
│         Número de Colaboradores                 │
└─────────────────────────────────────────────────┘
```

## Teste 2: Labels e Tooltips

### Passos:

1. Observar as barras do gráfico
2. Passar o mouse sobre cada barra

### O que verificar:

- [ ] **Labels nas barras** mostram formato: "N (X.X%)"
  - Exemplo: "5 (20.0%)"
- [ ] **Labels são legíveis** (não sobrepostos)
- [ ] **Tooltip aparece** ao passar o mouse
- [ ] **Tooltip mostra:** "N colaboradores (X.X%)"
- [ ] **Percentuais somam ~100%** (pode ter 0.1% de diferença por arredondamento)

## Teste 3: Responsividade Desktop

### Passos:

1. Redimensionar janela do navegador
2. Testar em diferentes larguras:
   - 1920px (desktop grande)
   - 1366px (laptop)
   - 1024px (tablet landscape)

### O que verificar:

- [ ] **Gráfico se adapta** à largura da janela
- [ ] **Labels permanecem legíveis** em todas as larguras
- [ ] **Não há scroll horizontal** desnecessário
- [ ] **Proporções mantidas** (barras não ficam distorcidas)

## Teste 4: Responsividade Mobile

### Passos:

1. Abrir DevTools (F12)
2. Ativar modo responsivo (Ctrl+Shift+M)
3. Selecionar dispositivo mobile:
   - iPhone 12 Pro (390px)
   - Samsung Galaxy S20 (360px)
   - iPad (768px)

### O que verificar:

- [ ] **Gráfico se adapta** à tela pequena
- [ ] **Altura reduz** para 250px (vs 300px no desktop)
- [ ] **Labels ainda legíveis** (não cortados)
- [ ] **Barras proporcionais** (não esmagadas)
- [ ] **Sem overflow horizontal**

## Teste 5: Acessibilidade

### Passos:

1. Abrir DevTools (F12)
2. Ir para aba "Elements"
3. Inspecionar o elemento `<canvas id="consolidatedChart">`

### O que verificar:

- [ ] **Atributo `role="img"`** presente
- [ ] **Atributo `aria-label`** presente e descritivo
- [ ] **Div oculto** com ID `chartDescription` existe
- [ ] **Descrição textual** contém dados do gráfico

### Teste com Screen Reader (Opcional):

1. Ativar NVDA (Windows) ou VoiceOver (Mac)
2. Navegar até o gráfico
3. Verificar que o screen reader lê a descrição

## Teste 6: Dados Corretos

### Passos:

1. Observar os números no gráfico
2. Comparar com a seção "Níveis de Risco por Colaborador" abaixo

### O que verificar:

- [ ] **Números no gráfico** = **Números na grid abaixo**
- [ ] **Soma das barras** = **Total de respondentes** (mostrado nos KPIs)
- [ ] **Percentuais corretos** (calcular manualmente se necessário)

### Exemplo de validação:

```
KPIs mostram: 25 respondentes

Gráfico mostra:
- BAIXO: 5 (20.0%)
- MÉDIO: 12 (48.0%)
- ALTO: 8 (32.0%)

Validação:
✅ 5 + 12 + 8 = 25 (correto)
✅ 20.0% + 48.0% + 32.0% = 100.0% (correto)
```

## Teste 7: Performance

### Passos:

1. Abrir DevTools (F12)
2. Ir para aba "Network"
3. Recarregar página (Ctrl+R)
4. Ir para aba "Console"

### O que verificar:

- [ ] **Chart.js carrega** (ver em Network)
- [ ] **Datalabels plugin carrega** (ver em Network)
- [ ] **Sem erros no console** (aba Console)
- [ ] **Página carrega rápido** (< 2 segundos)
- [ ] **Gráfico renderiza rápido** (< 500ms após page load)

## Teste 8: Casos Extremos

### Caso 1: Empresa sem respostas

**Passos:**
1. Acessar empresa sem respostas
2. Tentar ver relatório NR-1

**Esperado:**
- [ ] Mensagem "Dados Insuficientes" aparece
- [ ] **Gráfico NÃO aparece** (renderização condicional)

### Caso 2: Todos em um nível

**Passos:**
1. Criar empresa de teste com todos os colaboradores em BAIXO

**Esperado:**
- [ ] Barra BAIXO: 100%
- [ ] Barras MÉDIO e ALTO: 0 (0.0%)
- [ ] Sem erros de divisão por zero

### Caso 3: Distribuição desigual

**Passos:**
1. Empresa com 1 BAIXO, 1 MÉDIO, 98 ALTO

**Esperado:**
- [ ] Barra BAIXO muito pequena mas visível
- [ ] Barra ALTO domina o gráfico
- [ ] Labels ainda legíveis

## Teste 9: Print/PDF

### Passos:

1. Na página do relatório NR-1
2. Clicar em "Imprimir Relatório" (ou Ctrl+P)
3. Visualizar preview de impressão

### O que verificar:

- [ ] **Gráfico aparece** no preview
- [ ] **Cores preservadas** (não fica tudo preto)
- [ ] **Layout não quebra** (gráfico não corta)
- [ ] **Legível quando impresso** (testar imprimir em PDF)

## Teste 10: Navegadores Diferentes

### Testar em:

- [ ] **Chrome** (versão mais recente)
- [ ] **Firefox** (versão mais recente)
- [ ] **Safari** (Mac/iOS)
- [ ] **Edge** (Windows)

### O que verificar em cada:

- [ ] Gráfico renderiza corretamente
- [ ] Cores corretas
- [ ] Tooltips funcionam
- [ ] Sem erros no console
- [ ] Performance aceitável

## Checklist Final

Antes de considerar o teste completo:

- [ ] Todos os 10 testes acima passaram
- [ ] Sem erros no console em nenhum navegador
- [ ] Gráfico funciona em desktop e mobile
- [ ] Dados estão corretos (validados manualmente)
- [ ] Acessibilidade verificada
- [ ] Performance aceitável (< 2s page load)

## Problemas Comuns e Soluções

### Problema: Gráfico não aparece

**Possíveis causas:**
1. Chart.js não carregou (verificar Network)
2. JavaScript com erro (verificar Console)
3. Empresa sem dados (verificar status do report)

**Solução:**
- Recarregar página (Ctrl+F5)
- Verificar console para erros
- Testar com empresa diferente

### Problema: Labels sobrepostos

**Causa:** Muitos colaboradores, barras muito longas

**Solução:**
- Ajustar font size no datalabels config
- Usar `align: 'start'` em vez de `align: 'end'`

### Problema: Cores erradas

**Causa:** Mapeamento incorreto de classificação → cor

**Solução:**
- Verificar array `colors` no JavaScript
- Confirmar ordem: ['#ef4444', '#f59e0b', '#10b981']

### Problema: Percentuais não somam 100%

**Causa:** Arredondamento

**Solução:**
- Aceitável se diferença < 0.1%
- Se diferença > 0.1%, há bug no cálculo

## Relatório de Teste

Após completar todos os testes, preencher:

```
Data: _______________
Testador: _______________
Navegador: _______________
Resolução: _______________

Testes Passados: _____ / 10
Bugs Encontrados: _____
Severidade: [ ] Crítico [ ] Alto [ ] Médio [ ] Baixo

Observações:
_________________________________
_________________________________
_________________________________

Aprovado para produção: [ ] Sim [ ] Não
```

---

**Boa sorte com os testes! 🧪**
