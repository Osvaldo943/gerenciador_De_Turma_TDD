# Sistema de Rastreio de Parcelas - Dicionário de Dados

Este dicionário de dados descreve os principais termos usados no ***Sistema de Rastreio de Parcelas***. Ele serve como referência central para garantir que todos os envolvidos ***Desenvolvedores e Especialistas de domínio*** - compartilhem da mesma compreensão sobre os conceitos fundamentais do sistema.


| **Termo**         | **Descrição**           | **Atributos**           |
|-----------|---------------|----------------------|
| **Cliente** | Representa uma entidade que solicita a recolha de uma parecla através de uma ligação | Id, Nome, BI, Endereço, Telefone, E-mail|
| **Parcela** | Representa a menor unidade de carga que pode ser transportada. | Id_Parecela, Id_Cliente, Status, altura, comprimento, peso|
| **Ordem de Recolha** | Documento que garante a recolha da parcela | Id_ordem_recolha, Id_parcela, Id_cliente, Data_recolha, Data_emissão_da_ordem_recolha, Origem, Destino, Status|
| **Ordem de Entrega** | Documento que garante a entrega da parcela | Id_ordem_entrega, Id_parcela, Id_cliente, Data_entrega, Data_emissão_da_ordem_entrega, Origem, Destino, Status|
| **Nota de Recebimento** | Comprovativo de que a entrega da parcela foi realizada com sucesso | Id_nota_recebimento, Id_cliente, Id_parcela, Data_recolha, Data_entrega, Origem, Destino, Status|
| **Atendente**| É um funcionario vinculado a um posto de atendimento | Id_atendente, Nome, BI, Endereço, Telefone, E-mail|
| **Responsavel pela Coleta** | É um funcionario que recolha a parcela | Id_responsavel_pela_coleta, Nome, BI, Endereço, Telefone, E-mail|
| **Responsavel pela Entrega** | É um funcionario que entrega a parcela | Id_responsavel_pela_entrega, Nome, BI, Endereço, Telefone, E-mail|  

![**Representação**](/Imagem/Captura%20de%20ecrã%20de%202025-05-20%2023-30-40.png)

Este dicionário de dados é essencial para o desenvolvimento e manutenção do sistema. Ele promove a linguagem ubíqua entre os membros da equipe e garante que os conceitos do domínio estejam bem definidos e compreendidos por todos os envolvidos.