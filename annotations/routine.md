# Rotina

**Módulos:**  
1. **Definição**
2. **Criação do repositório**
3. **Criação dos scripts**
4. **Criação da versão da rotina**
5. **Criação do fluxo da rotina** 

## Definição

O Dataform é uma ferramenta que permite gerenciar e automatizar o pipeline de dados dentro do BigQuery. As suas rotinas referem-se a scripts e processos que são automatizados para realizar transformações e cargas de dados.

Ou seja, é possível definir a frequência e o tempo de execução das rotinas, garantindo que as tabelas ou views sejam executadas em intervalos.

## Criação do repositório

Dentro do BigQuery, devemos entrar na aba do DataForm.

![DataForm](/annotations/images/dataform.png)

Uma vez dentro dele, criamos um repositório.

![Criação do repositório](/annotations/images/criarRepositorio.png)

## Criação dos scripts

Podemos criar, dentro do repositório, um espaço de trabalho para os scripts da rotina.

![Espaço de trabalho](/annotations/images/espacoTrabalho.png)

No espeço de trabalho, adicionamos nossos scripts SQLX dentro da pasta definitions.

![Pasta definitions](/annotations/images/definitions.png)

## Criação da versão da rotina

Depois de adicionados, realizamos o commit e push das alterações.

Voltamos para o repositório para entrar na aba de Versões e Progamação.

![Versões e Progamação](/annotations/images/versoes.png)

Agora, criamos um versão de rotina.

![Criar Versão](/annotations/images/criarVersao.png)

Já para configurar a versão, definimos as especificações dela. O sufixo do esquema e tabela aparecerá no BigQuery, para diferenciar dos outros datasets e tabelas/views.

![Configurar versão](/annotations/images/configVersao.png)

## Criação do fluxo da rotina

Uma vez criado a versão, devemos criar o fluxo de trabalho, que executará a rotina de fato.

![Criar fluxo de trabalho](/annotations/images/criarFluxo.png)

Da mesma forma que a versão, configuramos o fluxo. Nosso fluxo irá ser executado, no caso, a cada 5 minutos.

![Configurar fluxo de trabalho](/annotations/images/configFluxo.png)

Podemos escolher quais scripts do repositório o nosso fluxo executará. Em nosso caso, todos serão executados.

![Escolher execuções](/annotations/images/escolherExe.png)

Pronto, a partir do momento que a versão for executada, o fluxo será executado a cada 5 minutos. 

Porém, é possível também executar manualmente o fluxo.

![Executar agora](/annotations/images/executarAgora.png)

Feito isso, um novo dataset com as views dos scripts irá aparecer no BigQuery com o sufixo escolhido.

![BigQuery rotina](/annotations/images/rotinaBigquery.png)
