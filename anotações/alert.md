# Alertas

Existem duas maneiras de criar alertas: utilizando **logs** ou criando **métricas**. Abaixo estão os passos para cada método.

## 1. Criação de Alertas com Logs

1. Acesse a **análise de registros**:

   ![Análise de Registros](images/image.png)

2. Selecione a opção **Criar alerta**.

3. Uma nova aba lateral será exibida para a criação da política do novo alerta, onde você poderá inserir:
   - Nome do alerta
   - Nível de gravidade
   - Documentação opcional

   ![Configuração Inicial](images/image-1.png)

4. Defina os detalhes do alerta e insira as entradas de **logs** que serão monitoradas:

   ![Entradas de Logs](images/image-2.png)

5. (Opcional) Adicione **tags** no alerta para fornecer mais informações sobre o log que originou o alerta.

   ![Configuração de Tags](images/image-4.png)

6. Selecione o intervalo de tempo entre as notificações e o tempo de duração para o fechamento automático de incidentes:

   ![Intervalo de Notificações](images/image-5.png)

7. Escolha um **canal de notificação** previamente configurado para receber os alertas.

   ![Canal de Notificação](images/image-6.png)

8. Por fim, crie o alerta, que enviará notificações de acordo com os logs.

## 2. Criação de Alertas com Métricas

1. Acesse a **análise de registros** e, no menu lateral, selecione a opção **Alertas**:

   ![Acesso aos Alertas](images/image-7.png)

2. Na aba de alertas, selecione a opção **+ Create policy**:

   ![Criar Nova Política](images/image-8.png)

3. Uma nova janela de configuração será exibida. Comece definindo a **métrica** desejada para o alerta:

   ![Configuração de Métrica](images/image-9.png)

4. Após selecionar a métrica, você poderá:
   - Criar **filtros**
   - Definir **séries temporais**
   - Configurar a **função da janela**

   ![Configurações Avançadas](images/image-10.png)

5. Defina o comportamento do gatilho do alerta, como:
   - Passagem de um limite específico
   - Ausência de dados por um período

   ![Definição de Gatilho](images/image-11.png)

6. Configure o modo de **notificação** do alerta:

   ![Configuração de Notificação](images/image-12.png)

7. Defina o intervalo de notificações, insira a documentação e dê um nome para a política:

   ![Documentação e Nome](images/image-13.png)

8. Finalmente, revise a métrica e selecione a opção **Criar política**:

   ![Revisão e Criação](images/image-14.png)
