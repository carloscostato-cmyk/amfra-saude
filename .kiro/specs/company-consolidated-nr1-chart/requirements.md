# Requirements Document

## Introduction

Este documento especifica os requisitos para a criação de um gráfico consolidado profissional NR-1 que mostre a distribuição dos colaboradores da empresa nos 4 níveis de classificação de riscos psicossociais (Saudável, Atenção, Alerta, Crítico). O gráfico será exibido na página de relatório NR-1 da empresa (admin_company_nr1.html) e utilizará a biblioteca Chart.js já presente no projeto.

## Glossary

- **NR1_Report_Page**: Página administrativa que exibe o relatório consolidado NR-1 de uma empresa (admin_company_nr1.html)
- **Consolidated_Chart**: Gráfico de barras horizontais que mostra a distribuição de colaboradores por nível de classificação
- **Classification_Level**: Um dos 4 níveis de risco psicossocial: Saudável, Atenção, Alerta, ou Crítico
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
