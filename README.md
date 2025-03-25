# Sistema de Estacionamento

## Descrição
Este é um programa em Python desenvolvido como um **projeto escolar** para gerenciar um estacionamento, permitindo cadastrar tarifas, registrar entrada e saída de veículos, gerar relatórios diários e por tipo de veículo, e calcular o valor das tarifas baseando-se no tempo de permanência. O sistema também oferece um desconto de 5% para pagamentos via PIX.

## Funcionalidades
1. **Cadastrar Tarifas**: Define os valores das tarifas para diferentes tipos de veículos.
2. **Registrar Entrada de Veículo**: Registra a entrada de um veículo no estacionamento.
3. **Registrar Saída de Veículo**: Calcula a tarifa com base no tempo estacionado e o tipo do veículo.
4. **Gerar Relatório Diário**: Exibe o total arrecadado no dia.
5. **Gerar Relatório por Tipo de Veículo**: Mostra a quantidade e a receita gerada por cada tipo de veículo.
6. **Sair**: Encerra o programa.

## Estrutura das Tarifas
O programa trabalha com três categorias de veículos:
- **Carro Grande**: Tarifa fixa de R$15,00, com valor adicional de R$1,50 por hora extra após as 2 primeiras horas.
- **Carro Pequeno**: Tarifa fixa de R$10,00, com valor adicional de R$1,00 por hora extra após as 2 primeiras horas.
- **Moto**: Tarifa fixa de R$5,00, com valor adicional de R$0,50 por hora extra após as 2 primeiras horas.

## Forma de Pagamento
O sistema permite o pagamento por:
- Cartão de Crédito/Débito
- PIX (com desconto de 5%)
- Dinheiro

## Cálculo das Tarifas
O programa solicita ao usuário o tempo de permanência e o tipo de veículo. Se o tempo for menor ou igual ao tempo fixo (2 horas), a tarifa base é aplicada. Caso contrário, é adicionado um valor extra por cada hora adicional. Se o pagamento for via PIX, um desconto de 5% é aplicado ao valor total.

## Exemplo de Cálculo
Se um carro pequeno permaneceu por 4 horas e o pagamento for via PIX:
- Tarifa base: R$10,00
- Horas adicionais: 2 x R$1,00 = R$2,00
- Valor total sem desconto: R$12,00
- Com desconto PIX (5%): R$11,40

## Como Executar o Programa
1. Execute o script Python.
2. Escolha uma das opções do menu.
3. Para registrar uma saída, insira o tempo de permanência e selecione o tipo de veículo.
4. Escolha a forma de pagamento.
5. O programa calcula e exibe o valor final.

## Melhorias Futuras
- Implementação de um banco de dados para armazenar histórico de veículos.
- Interface gráfica para facilitar a interação.
- Opção de cadastramento automático da entrada via leitura de placas.

