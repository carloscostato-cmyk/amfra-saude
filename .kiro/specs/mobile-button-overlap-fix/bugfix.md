# Bugfix Requirements Document

## Introduction

No sistema AMFRA de avaliação clínica, a página de detalhes da empresa (`admin_company_detail.html`) apresenta um problema de layout em dispositivos móveis. Os botões de ação "Visualizar Estudo NR-1" e "Sair" aparecem sobrepostos ao nome da empresa quando a tela tem largura máxima de 720px, tornando o conteúdo ilegível e prejudicando a experiência do usuário mobile.

Este bug afeta apenas a visualização mobile, enquanto o desktop funciona perfeitamente e não deve ser alterado.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN a página admin_company_detail.html é visualizada em dispositivos com largura de tela ≤ 720px THEN os botões "Visualizar Estudo NR-1" e "Sair" aparecem sobrepostos ao nome da empresa

1.2 WHEN o usuário acessa a página no mobile THEN o layout do header fica quebrado e o conteúdo fica ilegível

1.3 WHEN a media query @media (max-width: 720px) é aplicada THEN os botões em `.admin-shell__actions` não se reorganizam adequadamente abaixo do título

### Expected Behavior (Correct)

2.1 WHEN a página admin_company_detail.html é visualizada em dispositivos com largura de tela ≤ 720px THEN os botões "Visualizar Estudo NR-1" e "Sair" SHALL aparecer abaixo do nome da empresa sem sobreposição

2.2 WHEN o usuário acessa a página no mobile THEN o layout do header SHALL estar bem organizado com todos os elementos visíveis e legíveis

2.3 WHEN a media query @media (max-width: 720px) é aplicada THEN os botões em `.admin-shell__actions` SHALL se reorganizar em layout vertical ou horizontal responsivo sem causar sobreposição

### Unchanged Behavior (Regression Prevention)

3.1 WHEN a página é visualizada em dispositivos com largura de tela > 720px (desktop) THEN o sistema SHALL CONTINUE TO exibir o layout horizontal com botões alinhados à direita

3.2 WHEN o CSS é modificado para corrigir o mobile THEN o sistema SHALL CONTINUE TO manter o design de alta qualidade no desktop sem alterações visuais

3.3 WHEN outros elementos da página (tabela de tokens, lista de colaboradores) são renderizados THEN o sistema SHALL CONTINUE TO funcionar normalmente sem regressões

3.4 WHEN outras páginas do sistema que usam `.admin-shell__header` são acessadas THEN o sistema SHALL CONTINUE TO exibir o layout correto tanto no mobile quanto no desktop
