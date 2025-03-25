# José Pedro Bitetti Tkatchuk 
# Magno Rogerio de Oliveira Junior
# Andreas Caycedo Martinez
tcg = 15.00 # Tarifa carro grande
hfcg = 2.00 # Hora fixa carro grande
hacg = 1.50 # Horas adicionais carro grande
tcp = 10.00 # Tarifa carro pequeno
hfcp = 2.00 # Hora fixa carro pequeno
hacp = 1.00 # Horas adicionais carro pequeno
tm = 5.00 # Tarifa moto
hfm = 2.00 # Hora fixa moto
ham = 0.50 # Horas adicionais moto
tarifa = 0  # Valor padrão da tarifa inicializado
quantidade_veiculos_dia = 0 # Quantidade de veiculos que entraram no estacionamento 
valor_total_arrecadado_dia = 0 # Valor diario total arrecadado 
quantidade_carro_grande = 0 # Quantidade de carros grandes
quantidade_carro_pequeno = 0 # Quantidade de carros pequenos
quantidade_moto = 0 # Quantidade de motos
valor_total_carro_grande = 0 # valor total de carros grandes
valor_total_carro_pequeno = 0 # valor total de carros pequenos 
valor_total_moto = 0 # valor total de moto 
valor_medio = 0 # valr medio de cada veiculo 

while True:
    print('1. Cadastrar Tarifas')
    print('2. Registrar Entrada de Veículo')
    print('3. Registrar Saída de Veículo')
    print('4. Gerar Relatório diário')
    print('5. Gerar Relatório por tipo de veículo')
    print('6. Sair')
    op = int(input('Escolha uma opção:'))
    if op == 6:
        break
    elif op == 1:
        print('Processamento para cadastrar as tarifas')
        while True:
            print('1. Ver/Atualizar tarifas')
            print('2. Voltar para o menu inicial')
            op = int(input('Escolha uma opçao:'))
            if op == 1:
                if op == 1:
                    print('1. Carro Grande')
                    print('2. Carro Pequeno ')
                    print('3. Moto')
                    op = int(input('Escolha uma opçao:'))
                    if op == 1:
                        print(f'A tarifa está no valor de {tcg} por hora com {hfcg} horas fixas + {hacg} de horas adicionais')
                        print('1. Alterar valores')
                        print('2. voltar para o menu anterior')
                        op = int(input('Escolha uma opçao:'))
                        if op == 1:
                            tcg = float(input('Digite o novo valor da tarifa:'))
                            hfcg = float(input('Digite um novo periodo de horas fixas:'))
                            hacg = float(input('Digite um novo periodo de horas adicionais:'))
                            print(f'As tafifas de carros grandes foram atualizadas para {tcg} por hora com {hfcg} horas fixas + {hacg} de horas adicionais.')
                        if op == 2:
                            continue 
                        elif op not in [1, 2]:
                            print('Opção Invalida')
                    if op == 2:
                        print(f'A tarifa está no valor de {tcp} por hora com {hfcp} horas fixas + {hacp} de horas adicionais')
                        print('1. Alterar valores')
                        print('2. voltar para o menu anterior')
                        op = int(input('Escolha uma opçao:'))
                        if op == 1:
                            tcp = float(input('Digite o novo valor da tarifa:'))
                            hfcp = float(input('Digite um novo periodo de horas fixas:'))
                            hacp = float(input('Digite um novo periodo de horas adicionais:'))
                            print(f'As tafifas de carros grandes foram atualizadas para {tcp} por hora com {hfcp} horas fixas + {hacp} de horas adicionais.')
                        if op == 2:
                            continue 
                        elif op not in [1, 2]:
                            print('Opção Invalida')
                    if op == 3:
                        print(f'A tarifa está no valor de {tm} por hora com {hfm} horas fixas + {ham} de horas adicionais')
                        print('1. Alterar valores')
                        print('2. voltar para o menu anterior')
                        op = int(input('Escolha uma opçao:'))
                        if op == 1:
                            tm = float(input('Digite o novo valor da tarifa:'))
                            hfm = float(input('Digite um novo periodo de horas fixas:'))
                            ham = float(input('Digite um novo periodo de horas adicionais:'))
                            print(f'As tafifas de carros grandes foram atualizadas para {tm} por hora com {hfm} horas fixas + {ham} de horas adicionais.')
                        if op == 2:
                            continue 
                        elif op not in [1, 2]:
                            print('Opção Invalida')
                    elif op not in [1, 2, 3]:
                        print('Opção Invalida')
            if op == 2:
                break
            elif op not in [1, 2]:
                print('Opção Invalida')
    elif op == 2:
        print('Processamento para registrar Entrada de Veículo:')
        from datetime import datetime
        cont = 0
        while cont < 10:
            print('1. Carro Grande')
            print('2. Carro Pequeno')
            print('3. Moto')
            print('4.Voltar para o menu inicial')
            op = int(input("Escolha uma opção: "))
            if op == 1:
                data = input("Data da entrada do veiculo (DD/MM/AAAA):")
                hora = input("Horario de entrada (HH:MM):")
                marca = input("Marca do veículo: ")
                placa = input("Placa do veículo:")
                modelo = input("Modelo do veículo:")
                ano = input("Ano do veículo:")
                cor = input('Cor do Veiculo:')
                hora_entrada_segundos = datetime.strptime(hora, "%H:%M").hour * 3600 + datetime.strptime(hora, "%H:%M").minute * 60
                hora_atual = datetime.now().timestamp()
                print('O veículo cadastrado foi:',marca,modelo,'placa:', placa,',', ano, ',', cor,'em',data,'as',hora)
                veiculo = [data, hora, marca, placa, modelo, ano, cor,]
                cont += 1
                quantidade_carro_grande += 1
            elif op == 2: 
                data = input("Data da entrada do veiculo (DD/MM/AAAA):")
                hora = input("Horario de entrada (HH:MM):")
                marca = input("Marca do veículo: ")
                placa = input("Placa do veículo:")
                modelo = input("Modelo do veículo:")
                ano = input("Ano do veículo:")
                cor = input('Cor do Veiculo:')
                hora_entrada_segundos = datetime.strptime(hora, "%H:%M").hour * 3600 + datetime.strptime(hora, "%H:%M").minute * 60
                hora_atual = datetime.now().timestamp()
                print('O veículo cadastrado foi:',marca,modelo,'placa:', placa,',', ano, ',', cor,'em',data,'as',hora)
                veiculo = [data, hora, marca, placa, modelo, ano, cor,]
                cont += 1
                quantidade_carro_pequeno += 1
            elif op == 3:
                data = input("Data da entrada do veiculo (DD/MM/AAAA):")
                hora = input("Horario de entrada (HH:MM):")
                marca = input("Marca do veículo: ")
                placa = input("Placa do veículo:")
                modelo = input("Modelo do veículo:")
                ano = input("Ano do veículo:")
                cor = input('Cor do Veiculo:')
                hora_entrada_segundos = datetime.strptime(hora, "%H:%M").hour * 3600 + datetime.strptime(hora, "%H:%M").minute * 60
                hora_atual = datetime.now().timestamp()
                print('O veículo cadastrado foi:',marca,modelo,'placa:', placa,',', ano, ',', cor,'em',data,'as',hora)
                veiculo = [data, hora, marca, placa, modelo, ano, cor,]
                cont += 1
                quantidade_moto += 1
            elif op == 4:
                break
            else:
                print("Opção Invalida")
        quantidade_veiculos_dia += 1
    elif op == 3:
            print('Processamento para registrar saída de veículo')
            print('1. Mostrar veículos')
            print('2. Voltar para o menu inicial')
            op_saida = int(input("Escolha uma opção: "))
            if op_saida == 1:
                print("Veículos cadastrados:")
                print(veiculo)
                print('1. Seguir para o pagamento')
                print('2. Voltar para o menu anterior')
                op_pagamento = int(input("Escolha uma opção: "))
                if op_pagamento == 1:
                    def calcular_tempo_permanencia(hora_entrada, hora_saida):
                        entrada_minutos = int(hora_entrada.split(':')[0]) * 60 + int(hora_entrada.split(':')[1])
                        saida_minutos = int(hora_saida.split(':')[0]) * 60 + int(hora_saida.split(':')[1])
                        diferenca_minutos = saida_minutos - entrada_minutos
                        horas = diferenca_minutos // 60
                        minutos = diferenca_minutos % 60   
                        return horas, minutos
                    hora_saida = input("Digite a hora de saída (formato HH:MM): ")
                    horas, minutos = calcular_tempo_permanencia(veiculo[1], hora_saida)
                    print(f"O tempo de permanência do veículo {veiculo} foi de {horas:.0f} horas e {minutos:.0f} minutos.")
                    print('Qual a forma de pagamento desejada?')
                    print('1. Cartão de Crédito ou Débito')
                    print('2. Pix')
                    print('3. Dinheiro')
                    op_pagamento = int(input("Escolha uma opção: "))
                    if op_pagamento == 2: 
                        horas_estacionado = float(input("Digite o tempo de permanência do carro em horas: "))
                        print('Selecione o tipo do veículo para calcular o preço')
                        print('1. Carro Grande')
                        print('2. Carro Pequeno')
                        print('3. Moto')
                        op_veiculo = int(input("Escolha uma opção: ")) 
                        if op_veiculo == 1:
                            if horas_estacionado <= hfcg:
                                tarifa = tcg
                            else:
                                tarifa = tcg + (horas_estacionado - hfcg) * hacg
                            tarifa_com_desconto = tarifa - (tarifa * 5/100)
                            valor_total_carro_grande += tarifa_com_desconto
                        elif op_veiculo == 2:
                            if horas_estacionado <= hfcp:
                                tarifa = tcp
                            else: 
                                tarifa = tcp + (horas_estacionado - hfcp) * hacp
                            tarifa_com_desconto = tarifa - (tarifa * 5/100)
                            valor_total_carro_pequeno += tarifa_com_desconto
                        elif op_veiculo == 3:
                            if horas_estacionado <= hfm:
                                tarifa = tm
                            else: 
                                tarifa = tm + (horas_estacionado - hfm) * ham
                            tarifa_com_desconto = tarifa - (tarifa * 5/100)
                            valor_total_moto += tarifa_com_desconto
                        valor_total_arrecadado_dia += tarifa_com_desconto
                        print(f"O valor da tarifa a ser paga é R${tarifa:.2f} com desconto de PIX vai para {tarifa_com_desconto:.2f} reais")
                        print('1. Excluir algum veículo')
                        print('2. Voltar para o menu anterior')
                        op = int(input("Escolha uma opção: "))
                        if op == 1:
                            print(f'Saída do veículo {veiculo} foi concluída')
                        if op == 2:
                            continue
                        elif op not in [1, 2]:
                            print('Opção Inválida')
                    elif op_pagamento == 1 or op_pagamento == 3:  
                        horas_estacionado = float(input("Digite o tempo de permanência do carro em horas: "))
                        print('Selecione o tipo do veículo para calcular o preço')
                        print('1. Carro Grande')
                        print('2. Carro Pequeno')
                        print('3. Moto')
                        op_veiculo = int(input("Escolha uma opção:"))
                        if op_veiculo == 1:
                            if horas_estacionado <= hfcg:
                                tarifa = tcg
                            else:
                                tarifa = tcg + (horas_estacionado - hfcg) * hacg
                            valor_total_carro_grande += tarifa_com_desconto
                        elif op_veiculo == 2:
                            if horas_estacionado <= hfcp:
                                tarifa = tcp
                            else: 
                                tarifa = tcp + (horas_estacionado - hfcp) * hacp
                            valor_total_carro_pequeno += tarifa_com_desconto
                        elif op_veiculo == 3:
                            if horas_estacionado <= hfm:
                                tarifa = tm
                            else:   
                                tarifa = tm + (horas_estacionado - hfm) * ham
                            valor_total_moto += tarifa_com_desconto
                        valor_total_arrecadado_dia += tarifa  
                        print(f"O valor da tarifa a ser paga é R${tarifa:.2f} por {horas_estacionado:.0f} horas")
                        print('1. Excluir algum veículo')
                        print('2. Voltar para o menu anterior')
                        op = int(input("Escolha uma opção: "))
                        if op == 1:
                            print(f'Saída do veículo {veiculo} foi concluída')
                        if op == 2:
                            continue
                    elif op not in [1, 2, 3]:
                        print('Opção Inválida')
                elif op not in [1, 2, 3]:
                    print('Opção Inválida')                 
            if op == 2:
                break
            elif op not in [1, 2]:
                print('Opção Invalida')     
    elif op == 4:
        print('Processamento para gerar relatório diário')
        print(f'Quantidade de veículos que entraram hoje: {quantidade_veiculos_dia}')
        print(f'Valor total arrecadado hoje: R${valor_total_arrecadado_dia:.2f}')
    elif op == 5:
        print('Processamento para gerar relatório por tipo de veículo')
        tipos_veiculos = ['carro_grande', 'carro_pequeno', 'moto']
        for tipo in tipos_veiculos:
            if tipo == 'carro_grande':
                quantidade = quantidade_carro_grande
                valor_total = valor_total_carro_grande
            elif tipo == 'carro_pequeno':
                quantidade = quantidade_carro_pequeno
                valor_total = valor_total_carro_pequeno
            elif tipo == 'moto':
                quantidade = quantidade_moto
                valor_total = valor_total_moto
            valor_medio = valor_total / quantidade if quantidade > 0 else 0
            print(f'Tipo: {tipo.capitalize()}')
            print(f'Quantidade: {quantidade}')
            print(f'Valor total: R${valor_total:.2f}')
            print(f'Valor médio: R${valor_medio:.2f}')
            print('-----------------------------')
    else:
        print('Opção inválida')
