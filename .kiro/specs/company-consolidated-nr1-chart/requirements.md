# Requirements Document

## Introduction

Este documento especifica os requisitos para os gráficos consolidados profissionais NR-1 exibidos na página de relatório da empresa (admin_company_nr1.html). O sistema inclui dois gráficos principais: (1) um gráfico de barras horizontais mostrando a distribuição dos colaboradores nos 4 níveis de classificação de riscos psicossociais (Saudável, Atenção, Alerta, Crítico), e (2) um gráfico radar exibindo as médias das 7 dimensões HSE-IT. Ambos os gráficos utilizam a biblioteca Chart.js já presente no projeto.

## Glossary

- **NR1_Report_Page**: Página administrativa que exibe o relatório consolidado NR-1 de uma empresa (admin_company_nr1.html)
- **Consolidated_Chart**: Gráfico de barras horizontais que mostra a distribuição de colaboradores por nível de classificação
- **Radar_Chart**: Gráfico radar que mostra as médias das 7 dimensões HSE-IT em formato radial
- **Classification_Level**: Um dos 4 níveis de risco psicossocial: Saudável, Atenção, Alerta, ou Crítico
- **HSE_IT_Dimension**: Uma das 7 dimensões psicossociais avaliadas: DEMANDAS, CONTROLE, APOIO DA CHEFIA, APOIO DOS COLEGAS, RELACIONAMENTOS, CARGO, COMUNICAÇÃO E MUDANÇAS
- **Submission**: Resposta completa de um colaborador ao questionário NR-1 (35 perguntas)
- **Chart_Library**: Biblioteca Chart.js versão 4.4.2 já incluída no projeto
- **Company**: Entidade que representa uma empresa no sistema AMFRA
- **NR1_Agent**: Serviço que calcula e compila dados do estudo NR-1 para uma empresa

## Requirements

### Requirement 1: Exibir Gráfico Consolidado

**User Story:** Como administrador do sistema, eu quero visualizar um gráfico consolidado de distribuição de riscos, para que eu possa rapidamente entender a situação geral da empresa.

#### Acceptance Criteria

1. WHEN THE NR1_Report_Page is loaded, THE Consolidated_Chart SHALL be displayed at the top of the page before the employee list
2. THE Consolidated_Chart SHALL use horizontal bar chart format
3. THE Consolidated_Chart SHALL display all 4 Classification_Levels on the Y-axis in order: Saudável, Atenção, Alerta, Crítico
4. THE Consolidated_Chart SHALL display employee count on the X-axis
5. THE Consolidated_Chart SHALL use the same color scheme as individual charts: green (Saudável), yellow (Atenção), orange (Alerta), red (Crítico)

### Requirement 2: Calcular Dados de Distribuição

**User Story:** Como administrador do sistema, eu quero que o sistema calcule automaticamente a distribuição de colaboradores por nível, para que eu tenha dados precisos e atualizados.

#### Acceptance Criteria

1. WHEN THE NR1_Report_Page is requested, THE NR1_Agent SHALL query all Submissions for the Company
2. WHEN THE NR1_Agent processes Submissions, THE NR1_Agent SHALL count how many Submissions exist for each Classification_Level
3. WHEN THE NR1_Agent calculates distribution, THE NR1_Agent SHALL compute the percentage for each Classification_Level
4. THE NR1_Agent SHALL include distribution data in the report dictionary with keys for each Classification_Level
5. IF a Classification_Level has zero Submissions, THEN THE NR1_Agent SHALL include that level with count 0

### Requirement 3: Exibir Métricas no Gráfico

**User Story:** Como administrador do sistema, eu quero ver números absolutos e percentuais em cada barra, para que eu possa entender tanto a quantidade quanto a proporção de colaboradores em cada nível.

#### Acceptance Criteria

1. WHEN THE Consolidated_Chart renders a bar, THE Consolidated_Chart SHALL display the absolute count of employees inside or next to the bar
2. WHEN THE Consolidated_Chart renders a bar, THE Consolidated_Chart SHALL display the percentage of total employees inside or next to the bar
3. THE Consolidated_Chart SHALL format percentages with one decimal place
4. IF a Classification_Level has zero employees, THEN THE Consolidated_Chart SHALL display "0 (0.0%)"

### Requirement 4: Aplicar Design Profissional

**User Story:** Como administrador do sistema, eu quero que o gráfico tenha aparência profissional e consistente, para que o relatório mantenha qualidade visual uniforme.

#### Acceptance Criteria

1. THE Consolidated_Chart SHALL use the Chart_Library for rendering
2. THE Consolidated_Chart SHALL be responsive and adapt to mobile and desktop screen sizes
3. THE Consolidated_Chart SHALL display the title "Distribuição de Riscos Psicossociais - Visão Consolidada"
4. THE Consolidated_Chart SHALL use the same visual style as other charts in the system
5. THE Consolidated_Chart SHALL include a clear legend identifying each Classification_Level and its color

### Requirement 5: Integrar com Página Existente

**User Story:** Como desenvolvedor, eu quero integrar o gráfico na página existente sem quebrar funcionalidades, para que o sistema continue funcionando corretamente.

#### Acceptance Criteria

1. WHEN THE NR1_Report_Page is rendered, THE Consolidated_Chart SHALL appear before the "Níveis de Risco por Colaborador" section
2. THE NR1_Report_Page SHALL maintain all existing functionality after adding the Consolidated_Chart
3. THE Consolidated_Chart SHALL only display when report.status is "success"
4. IF report.status is "empty", THEN THE Consolidated_Chart SHALL not be displayed
5. THE Consolidated_Chart SHALL use data from the existing report.risk_distribution dictionary

### Requirement 6: Garantir Acessibilidade

**User Story:** Como usuário com necessidades especiais, eu quero que o gráfico seja acessível, para que eu possa compreender as informações independentemente de minhas limitações.

#### Acceptance Criteria

1. THE Consolidated_Chart SHALL include appropriate ARIA labels for screen readers
2. THE Consolidated_Chart SHALL use color combinations that meet WCAG AA contrast requirements
3. THE Consolidated_Chart SHALL include text labels in addition to color coding
4. THE Consolidated_Chart SHALL be keyboard navigable
5. THE Consolidated_Chart SHALL provide alternative text description of the data

### Requirement 7: Exibir Gráfico Radar das 7 Dimensões HSE-IT

**User Story:** Como administrador do sistema, eu quero visualizar um gráfico radar com as médias das 7 dimensões HSE-IT, para que eu possa rapidamente identificar os pontos fortes e fracos da empresa em cada dimensão psicossocial.

#### Acceptance Criteria

1. WHEN THE NR1_Report_Page is loaded, THE Radar_Chart SHALL be displayed in the "Análise Dimensional" section before the dimensional results table
2. THE Radar_Chart SHALL display all 7 HSE-IT dimensions: DEMANDAS, CONTROLE, APOIO DA CHEFIA, APOIO DOS COLEGAS, RELACIONAMENTOS, CARGO, COMUNICAÇÃO E MUDANÇAS
3. WHEN THE NR1_Agent calculates dimension averages, THE Radar_Chart SHALL display the average score for each dimension on a scale from 0 to 5
4. THE Radar_Chart SHALL use Chart.js radar type with blue color scheme (border: #2563eb, fill: rgba(37, 99, 235, 0.2))
5. THE Radar_Chart SHALL have a fixed height of 450px and be fully responsive across mobile and desktop devices
6. THE Radar_Chart SHALL display tooltips showing the exact average value and classification (BAIXO < 2.30, MÉDIO 2.30-3.69, ALTO ≥ 3.70) when hovering over data points
7. THE Radar_Chart SHALL include ARIA label "Gráfico radar mostrando as médias das 7 dimensões do HSE-IT" for screen reader accessibility
8. THE Radar_Chart SHALL be positioned after the horizontal bar chart and before the "Resultados por Dimensão" table
9. IF THE Radar_Chart fails to load, THEN THE system SHALL display an error message "Não foi possível carregar o gráfico radar"
10. THE Radar_Chart SHALL use data from report.dimension_analysis provided by the NR1_Agent
