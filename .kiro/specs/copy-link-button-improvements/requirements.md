# Requirements Document

## Introduction

Este documento define os requisitos para melhorias na experiência do usuário (UX) do botão "Copiar Link" na página de detalhes da empresa do sistema AMFRA. O sistema gerencia tokens individuais para colaboradores responderem questionários de avaliação clínica. Cada token possui um link único que pode ser copiado e distribuído. As melhorias visam fornecer feedback visual claro sobre o estado do botão e prevenir o uso de tokens já expirados.

## Glossary

- **Copy_Button**: O botão de interface que permite copiar o link único do token para a área de transferência
- **Token**: Identificador único gerado para cada colaborador que permite acesso individual ao questionário
- **Token_Table**: A tabela HTML que exibe a lista de tokens individuais na página admin_company_detail.html
- **Success_State**: Estado visual do botão após copiar com sucesso o link (verde com texto "✓ Copiado")
- **Disabled_State**: Estado visual do botão quando o token já foi usado (cinza, não clicável, texto "Link Expirado")
- **Clipboard**: Área de transferência do sistema operacional onde o link é copiado

## Requirements

### Requirement 1: Visual Feedback on Successful Copy

**User Story:** Como administrador do sistema, eu quero ver feedback visual claro quando copio um link de token, para que eu saiba que a operação foi bem-sucedida.

#### Acceptance Criteria

1. WHEN the user clicks the Copy_Button, THE Copy_Button SHALL copy the token URL to the Clipboard
2. WHEN the token URL is successfully copied to the Clipboard, THE Copy_Button SHALL change its background color to green (success color from CSS variables)
3. WHEN the token URL is successfully copied to the Clipboard, THE Copy_Button SHALL change its text content to "✓ Copiado"
4. WHILE the Copy_Button is in Success_State, THE Copy_Button SHALL maintain the green background and "✓ Copiado" text for exactly 2 seconds
5. WHEN 2 seconds have elapsed after entering Success_State, THE Copy_Button SHALL revert to its original appearance with "Copiar Link" text
6. WHEN 2 seconds have elapsed after entering Success_State, THE Copy_Button SHALL revert to its original background color

### Requirement 2: Disable Button for Used Tokens

**User Story:** Como administrador do sistema, eu quero que botões de tokens já usados sejam desabilitados, para que eu não tente copiar links que não funcionam mais.

#### Acceptance Criteria

1. WHEN a token has the property used equal to True, THE Copy_Button SHALL be rendered in Disabled_State
2. WHILE a Copy_Button is in Disabled_State, THE Copy_Button SHALL display the text "Link Expirado" instead of "Copiar Link"
3. WHILE a Copy_Button is in Disabled_State, THE Copy_Button SHALL have a gray background color
4. WHILE a Copy_Button is in Disabled_State, THE Copy_Button SHALL not respond to click events
5. WHILE a Copy_Button is in Disabled_State, THE Copy_Button SHALL display cursor style "not-allowed" on hover
6. WHILE a Copy_Button is in Disabled_State, THE Copy_Button SHALL not perform the hover transform animation
7. WHEN a token has the property used equal to False, THE Copy_Button SHALL be rendered in its normal interactive state

### Requirement 3: CSS Styling for Button States

**User Story:** Como desenvolvedor, eu quero estilos CSS bem definidos para os estados do botão, para que a implementação seja consistente e manutenível.

#### Acceptance Criteria

1. THE System SHALL define a CSS class for the Success_State with green background color using CSS variable --healthy or equivalent success color
2. THE System SHALL define a CSS class for the Disabled_State with gray background color and reduced opacity
3. THE System SHALL define a CSS class for the Disabled_State that sets cursor to "not-allowed"
4. THE System SHALL define a CSS class for the Disabled_State that removes hover effects and transform animations
5. WHEN the Copy_Button transitions to Success_State, THE System SHALL apply the success CSS class to the button element
6. WHEN the Copy_Button transitions from Success_State back to normal, THE System SHALL remove the success CSS class from the button element

### Requirement 4: Maintain Existing Functionality

**User Story:** Como administrador do sistema, eu quero que todas as funcionalidades existentes continuem funcionando, para que nenhuma regressão seja introduzida.

#### Acceptance Criteria

1. THE System SHALL preserve the existing token table layout and structure
2. THE System SHALL preserve the existing JavaScript event listeners for copy functionality
3. THE System SHALL preserve the existing token status badges (Disponível/Usado)
4. THE System SHALL preserve the existing employee name and usage date display logic
5. WHEN a token is not used, THE Token_Table SHALL display the Copy_Button in its normal interactive state
6. WHEN a token is used, THE Token_Table SHALL display "Link expirado" text in place of the Copy_Button (existing behavior) OR display the Copy_Button in Disabled_State (new behavior)
