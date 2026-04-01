# Mobile Button Overlap Fix - Bugfix Design

## Overview

Este documento especifica a correção técnica para o problema de sobreposição de botões na página de detalhes da empresa (`admin_company_detail.html`) em dispositivos móveis. O bug ocorre quando a tela tem largura ≤ 720px, fazendo com que os botões "Visualizar Estudo NR-1" e "Sair" apareçam sobrepostos ao nome da empresa.

A correção será implementada exclusivamente via CSS, sem alterações no HTML, garantindo que o layout desktop permaneça intacto enquanto o mobile é corrigido.

## Glossary

- **Bug_Condition (C)**: A condição que dispara o bug - quando a largura da viewport é ≤ 720px e os botões em `.admin-shell__actions` não se reorganizam adequadamente
- **Property (P)**: O comportamento desejado - botões devem aparecer abaixo do título sem sobreposição em telas mobile
- **Preservation**: O layout desktop (viewport > 720px) deve permanecer inalterado com botões alinhados à direita
- **`.admin-shell__header`**: Container flex que organiza o cabeçalho da página de detalhes da empresa
- **`.admin-shell__brand`**: Elemento que contém o título e descrição da empresa
- **`.admin-shell__actions`**: Container dos botões de ação que precisa de ajustes no mobile
- **Media Query @media (max-width: 720px)**: Breakpoint que define estilos para dispositivos móveis

## Bug Details

### Bug Condition

O bug se manifesta quando a página `admin_company_detail.html` é visualizada em dispositivos com largura de viewport ≤ 720px. O container `.admin-shell__header` usa `flex-direction: column` na media query mobile, mas os botões em `.admin-shell__actions` não recebem estilos adequados para se reorganizarem, causando sobreposição visual com o conteúdo do título.

**Formal Specification:**
```
FUNCTION isBugCondition(viewport)
  INPUT: viewport of type ViewportDimensions
  OUTPUT: boolean
  
  RETURN viewport.width <= 720
         AND page == 'admin_company_detail.html'
         AND buttonsOverlapTitle('.admin-shell__actions')
END FUNCTION
```

### Examples

- **Exemplo 1**: iPhone SE (375px width) - botões aparecem sobrepostos ao nome da empresa, tornando ambos ilegíveis
- **Exemplo 2**: iPad Mini em modo portrait (768px width) - layout funciona corretamente (não é bug, viewport > 720px)
- **Exemplo 3**: Samsung Galaxy S20 (360px width) - botões aparecem sobrepostos, texto do título fica parcialmente oculto
- **Edge Case**: Viewport exatamente 720px - deve aplicar os estilos mobile e exibir botões sem sobreposição

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- Layout desktop (viewport > 720px) deve continuar exibindo botões alinhados à direita horizontalmente
- Design visual de alta qualidade no desktop deve permanecer inalterado
- Outros elementos da página (tabela de tokens, lista de colaboradores) devem continuar funcionando normalmente
- Outras páginas que usam `.admin-shell__header` devem continuar funcionando corretamente em ambos os tamanhos de tela

**Scope:**
Todas as viewports com largura > 720px devem ser completamente não afetadas por esta correção. Isso inclui:
- Desktops (1920px, 1440px, 1366px, etc.)
- Tablets em modo landscape (1024px, 768px em landscape)
- Qualquer dispositivo com viewport > 720px

## Hypothesized Root Cause

Baseado na análise do código CSS e HTML, as causas mais prováveis são:

1. **Falta de Estilos Específicos para `.admin-shell__actions` no Mobile**: A media query `@media (max-width: 720px)` já aplica `flex-direction: column` ao `.admin-shell__header`, mas não define estilos específicos suficientes para `.admin-shell__actions`, fazendo com que os botões não se reorganizem adequadamente.

2. **Propriedades Flex Conflitantes**: Os botões podem estar herdando propriedades flex do desktop que causam comportamento inadequado no mobile (como `flex: 1 1 auto` sem `width: 100%`).

3. **Gap Insuficiente**: O espaçamento entre elementos pode não ser suficiente no mobile, contribuindo para a aparência de sobreposição.

4. **Min-width dos Botões**: A propriedade `min-width: fit-content` pode estar causando que os botões não quebrem adequadamente em telas pequenas.

## Correctness Properties

Property 1: Bug Condition - Mobile Button Layout

_For any_ viewport com largura ≤ 720px acessando a página admin_company_detail.html, o layout SHALL reorganizar os botões em `.admin-shell__actions` de forma que apareçam abaixo do título da empresa sem sobreposição, com todos os elementos visíveis e legíveis.

**Validates: Requirements 2.1, 2.2, 2.3**

Property 2: Preservation - Desktop Layout

_For any_ viewport com largura > 720px, o layout SHALL produzir exatamente o mesmo resultado visual que o código original, preservando o design horizontal com botões alinhados à direita e mantendo toda a qualidade visual do desktop.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

## Fix Implementation

### Changes Required

Assumindo que nossa análise de causa raiz está correta:

**File**: `app/static/css/style.css`

**Section**: `@media (max-width: 720px)` (linha ~1243)

**Specific Changes**:

1. **Confirmar Estilos Existentes**: Verificar que `.admin-shell__header` já tem `flex-direction: column` aplicado na media query mobile (já existe no código atual)

2. **Adicionar Estilos para `.admin-shell__actions`**: Dentro da media query `@media (max-width: 720px)`, adicionar regras específicas para `.admin-shell__actions`:
   - `display: flex` - garantir que é um container flex
   - `flex-wrap: wrap` - permitir que botões quebrem linha se necessário
   - `gap: 0.75rem` - espaçamento adequado entre botões
   - `width: 100%` - ocupar toda a largura disponível

3. **Ajustar Botões Individuais**: Adicionar regras para `.admin-shell__actions .button`:
   - `flex: 1 1 auto` - permitir que botões cresçam e encolham
   - `min-width: fit-content` - garantir que o texto do botão não quebre

4. **Verificar Ordem Visual**: Garantir que a ordem de exibição seja: título → descrição → botões (de cima para baixo)

5. **Testar Responsividade**: Validar em múltiplas larguras de viewport (320px, 375px, 414px, 720px) para garantir que não há quebras

**Nota**: O código CSS atual já contém parte desses estilos (linhas ~1250-1260), mas pode precisar de ajustes ou estar incompleto. A implementação deve verificar e corrigir conforme necessário.

## Testing Strategy

### Validation Approach

A estratégia de teste segue uma abordagem de duas fases: primeiro, demonstrar o bug no código não corrigido através de testes visuais em diferentes viewports, depois verificar que a correção funciona corretamente e preserva o comportamento desktop.

### Exploratory Bug Condition Checking

**Goal**: Demonstrar o bug ANTES de implementar a correção. Confirmar ou refutar a análise de causa raiz. Se refutarmos, precisaremos re-hipotizar.

**Test Plan**: Abrir a página `admin_company_detail.html` no navegador e usar as ferramentas de desenvolvedor para simular diferentes tamanhos de viewport. Observar o comportamento dos botões em relação ao título da empresa.

**Test Cases**:
1. **iPhone SE (375px)**: Verificar se botões aparecem sobrepostos ao título (deve falhar no código não corrigido)
2. **Samsung Galaxy S20 (360px)**: Verificar se botões aparecem sobrepostos ao título (deve falhar no código não corrigido)
3. **Viewport 720px (breakpoint exato)**: Verificar se botões aparecem sobrepostos (deve falhar no código não corrigido)
4. **Desktop 1920px**: Verificar se layout está correto com botões à direita (deve passar - não é afetado pelo bug)

**Expected Counterexamples**:
- Botões "Visualizar Estudo NR-1" e "Sair" aparecem sobrepostos ao nome da empresa em viewports ≤ 720px
- Possíveis causas: falta de estilos específicos para `.admin-shell__actions` no mobile, propriedades flex inadequadas, gap insuficiente

### Fix Checking

**Goal**: Verificar que para todas as viewports onde a condição de bug se aplica (largura ≤ 720px), o layout corrigido produz o comportamento esperado.

**Pseudocode:**
```
FOR ALL viewport WHERE isBugCondition(viewport) DO
  result := renderPage_fixed(viewport, 'admin_company_detail.html')
  ASSERT buttonsAppearBelowTitle(result)
  ASSERT noOverlap(result)
  ASSERT allElementsVisible(result)
END FOR
```

**Test Plan**: Após aplicar a correção CSS, testar em múltiplas viewports mobile para garantir que os botões aparecem corretamente abaixo do título sem sobreposição.

**Test Cases**:
1. **iPhone SE (375px)**: Botões devem aparecer abaixo do título, sem sobreposição, todos visíveis
2. **Samsung Galaxy S20 (360px)**: Botões devem aparecer abaixo do título, sem sobreposição, todos visíveis
3. **Viewport 720px**: Botões devem aparecer abaixo do título, sem sobreposição, todos visíveis
4. **Viewport 320px (menor comum)**: Botões devem aparecer abaixo do título, sem sobreposição, todos visíveis

### Preservation Checking

**Goal**: Verificar que para todas as viewports onde a condição de bug NÃO se aplica (largura > 720px), o layout corrigido produz exatamente o mesmo resultado que o código original.

**Pseudocode:**
```
FOR ALL viewport WHERE NOT isBugCondition(viewport) DO
  ASSERT renderPage_original(viewport) = renderPage_fixed(viewport)
END FOR
```

**Testing Approach**: Comparação visual lado a lado entre o código original e o código corrigido em viewports desktop. Usar ferramentas de screenshot para garantir que não há diferenças visuais.

**Test Plan**: Observar o comportamento no código NÃO CORRIGIDO primeiro para viewports desktop, depois escrever testes de regressão visual capturando esse comportamento.

**Test Cases**:
1. **Desktop 1920px**: Verificar que layout horizontal com botões à direita permanece idêntico
2. **Desktop 1440px**: Verificar que layout horizontal com botões à direita permanece idêntico
3. **iPad em landscape (1024px)**: Verificar que layout permanece idêntico
4. **Viewport 721px (logo acima do breakpoint)**: Verificar que layout desktop é aplicado corretamente

### Unit Tests

- Testar renderização da página em viewport 375px (mobile) e verificar ausência de sobreposição
- Testar renderização da página em viewport 1920px (desktop) e verificar layout horizontal
- Testar edge case de viewport exatamente 720px
- Testar que outros elementos da página (tabela, lista) não são afetados

### Property-Based Tests

- Gerar viewports aleatórias entre 320px e 720px e verificar que botões sempre aparecem abaixo do título
- Gerar viewports aleatórias entre 721px e 2560px e verificar que layout desktop é preservado
- Testar múltiplas combinações de tamanhos de texto e zoom do navegador

### Integration Tests

- Testar fluxo completo: acessar lista de empresas → clicar em empresa → verificar layout mobile correto
- Testar que botões são clicáveis e funcionais após a correção CSS
- Testar que a correção não afeta outras páginas que usam `.admin-shell__header`
- Testar em navegadores diferentes (Chrome, Firefox, Safari mobile)
