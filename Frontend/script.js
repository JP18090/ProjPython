// Base URL da API
const API_BASE = 'http://localhost:5000/api';

// Estado global da aplicação
let estadoGlobal = {
    veiculoSelecionado: null,
    calculoAtual: null,
    tarifas: {}
};

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    inicializarApp();
});

function inicializarApp() {
    carregarDashboard();
    carregarTarifas();
    
    // Atualizar dashboard a cada 30 segundos
    setInterval(carregarDashboard, 30000);
}

// === NAVEGAÇÃO ===
function mostrarSecao(secaoId) {
    // Esconder todas as seções
    document.querySelectorAll('.section').forEach(secao => {
        secao.classList.add('hidden');
    });
    
    // Mostrar seção selecionada
    document.getElementById(secaoId).classList.remove('hidden');
    
    // Carregar dados específicos da seção
    switch(secaoId) {
        case 'tarifas':
            carregarTarifas();
            break;
        case 'entrada':
            limparFormularioEntrada();
            break;
        case 'saida':
            limparFormularioSaida();
            break;
        case 'relatorios':
            carregarRelatorios();
            break;
        case 'veiculos':
            carregarVeiculosAtivos();
            break;
    }
}

function voltarMenu() {
    document.querySelectorAll('.section').forEach(secao => {
        secao.classList.add('hidden');
    });
    document.getElementById('menu-principal').classList.remove('hidden');
    carregarDashboard();
}

// === DASHBOARD ===
async function carregarDashboard() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const stats = await response.json();
        
        document.getElementById('total-vehicles').textContent = stats.totalVehicles || 0;
        document.getElementById('total-revenue').textContent = formatarMoeda(stats.totalRevenue || 0);
        document.getElementById('active-vehicles').textContent = stats.activeVehicles || 0;
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
    }
}

// === TARIFAS ===
async function carregarTarifas() {
    try {
        const response = await fetch(`${API_BASE}/tariffs`);
        const tarifas = await response.json();
        
        tarifas.forEach(tarifa => {
            estadoGlobal.tarifas[tarifa.vehicleType] = tarifa;
            preencherCamposTarifa(tarifa.vehicleType, tarifa);
        });
    } catch (error) {
        mostrarMensagem('Erro ao carregar tarifas', 'erro');
    }
}

function preencherCamposTarifa(tipo, tarifa) {
    const prefixo = tipo === 'carroGrande' ? 'carro-grande' : 
                   tipo === 'carroPequeno' ? 'carro-pequeno' : 'moto';
    
    document.getElementById(`${prefixo}-base`).value = tarifa.baseRate;
    document.getElementById(`${prefixo}-horas`).value = tarifa.fixedHours;
    document.getElementById(`${prefixo}-adicional`).value = tarifa.additionalHourRate;
}

async function salvarTarifas() {
    const tipos = ['carroGrande', 'carroPequeno', 'moto'];
    const prefixos = ['carro-grande', 'carro-pequeno', 'moto'];
    
    try {
        for (let i = 0; i < tipos.length; i++) {
            const tipo = tipos[i];
            const prefixo = prefixos[i];
            
            const dadosTarifa = {
                vehicleType: tipo,
                baseRate: document.getElementById(`${prefixo}-base`).value,
                fixedHours: document.getElementById(`${prefixo}-horas`).value,
                additionalHourRate: document.getElementById(`${prefixo}-adicional`).value
            };
            
            await fetch(`${API_BASE}/tariffs/${tipo}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dadosTarifa)
            });
        }
        
        mostrarMensagem('Tarifas atualizadas com sucesso!', 'sucesso');
        carregarTarifas();
    } catch (error) {
        mostrarMensagem('Erro ao salvar tarifas', 'erro');
    }
}

// === ENTRADA DE VEÍCULOS ===
function limparFormularioEntrada() {
    document.getElementById('form-entrada').reset();
    document.getElementById('ano').value = new Date().getFullYear();
}

async function registrarEntrada() {
    const dadosVeiculo = {
        vehicleType: document.getElementById('tipo-veiculo').value,
        plate: document.getElementById('placa').value.toUpperCase(),
        brand: document.getElementById('marca').value,
        model: document.getElementById('modelo').value,
        year: parseInt(document.getElementById('ano').value),
        color: document.getElementById('cor').value
    };
    
    // Validação básica
    if (!dadosVeiculo.vehicleType || !dadosVeiculo.plate || !dadosVeiculo.brand || 
        !dadosVeiculo.model || !dadosVeiculo.year || !dadosVeiculo.color) {
        mostrarMensagem('Preencha todos os campos', 'erro');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/vehicles`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dadosVeiculo)
        });
        
        if (response.ok) {
            mostrarMensagem('Veículo registrado com sucesso!', 'sucesso');
            limparFormularioEntrada();
        } else {
            const error = await response.json();
            mostrarMensagem(error.message || 'Erro ao registrar veículo', 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao registrar veículo', 'erro');
    }
}

// === SAÍDA DE VEÍCULOS ===
function limparFormularioSaida() {
    document.getElementById('busca-placa').value = '';
    document.getElementById('veiculo-encontrado').classList.add('hidden');
    document.getElementById('resumo-pagamento').classList.add('hidden');
    estadoGlobal.veiculoSelecionado = null;
    estadoGlobal.calculoAtual = null;
    
    // Definir hora atual como padrão
    const agora = new Date();
    const horaAtual = agora.toTimeString().slice(0, 5);
    document.getElementById('hora-saida').value = horaAtual;
}

async function buscarVeiculo() {
    const placa = document.getElementById('busca-placa').value.trim().toUpperCase();
    
    if (!placa) {
        mostrarMensagem('Digite uma placa', 'erro');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/vehicles/plate/${placa}`);
        
        if (response.ok) {
            const veiculo = await response.json();
            estadoGlobal.veiculoSelecionado = veiculo;
            exibirVeiculoEncontrado(veiculo);
        } else {
            mostrarMensagem('Veículo não encontrado ou já processado', 'erro');
            document.getElementById('veiculo-encontrado').classList.add('hidden');
        }
    } catch (error) {
        mostrarMensagem('Erro ao buscar veículo', 'erro');
    }
}

function exibirVeiculoEncontrado(veiculo) {
    const detalhes = `
        <div class="vehicle-details">
            <div class="vehicle-detail"><strong>Placa:</strong> ${veiculo.plate}</div>
            <div class="vehicle-detail"><strong>Tipo:</strong> ${obterLabelTipoVeiculo(veiculo.vehicleType)}</div>
            <div class="vehicle-detail"><strong>Veículo:</strong> ${veiculo.brand} ${veiculo.model}</div>
            <div class="vehicle-detail"><strong>Entrada:</strong> ${formatarDataHora(veiculo.entryTime)}</div>
            <div class="vehicle-detail"><strong>Cor:</strong> ${veiculo.color}</div>
            <div class="vehicle-detail"><strong>Ano:</strong> ${veiculo.year}</div>
        </div>
    `;
    
    document.getElementById('detalhes-veiculo').innerHTML = detalhes;
    document.getElementById('veiculo-encontrado').classList.remove('hidden');
    document.getElementById('resumo-pagamento').classList.add('hidden');
}

async function calcularValor() {
    if (!estadoGlobal.veiculoSelecionado) return;
    
    const horaSaida = document.getElementById('hora-saida').value;
    const formaPagamento = document.getElementById('forma-pagamento').value;
    
    if (!horaSaida) {
        mostrarMensagem('Defina a hora de saída', 'erro');
        return;
    }
    
    // Buscar tarifa para o tipo de veículo
    const tarifa = estadoGlobal.tarifas[estadoGlobal.veiculoSelecionado.vehicleType];
    if (!tarifa) {
        mostrarMensagem('Tarifa não encontrada para este tipo de veículo', 'erro');
        return;
    }
    
    // Calcular tempo estacionado
    const entryTime = new Date(estadoGlobal.veiculoSelecionado.entryTime);
    const exitTime = new Date();
    const [hours, minutes] = horaSaida.split(':');
    exitTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
    
    const diffMs = exitTime.getTime() - entryTime.getTime();
    const horasEstacionado = Math.max(0.1, diffMs / (1000 * 60 * 60));
    
    // Calcular valor
    const baseRate = parseFloat(tarifa.baseRate);
    const fixedHours = parseFloat(tarifa.fixedHours);
    const additionalHourRate = parseFloat(tarifa.additionalHourRate);
    
    let valorBase;
    if (horasEstacionado <= fixedHours) {
        valorBase = baseRate;
    } else {
        valorBase = baseRate + (horasEstacionado - fixedHours) * additionalHourRate;
    }    // Aplicar desconto PIX
    const desconto = formaPagamento === 'pix' ? valorBase * 0.05 : 0;
    const valorFinal = valorBase - desconto;
    
    estadoGlobal.calculoAtual = {
        horasEstacionado,
        valorBase,
        desconto,
        valorFinal,
        formaPagamento
    };
    
    exibirResumoPageamento();
}

function exibirResumoPageamento() {
    const calculo = estadoGlobal.calculoAtual;
    
    let resumoHtml = `
        <div class="payment-details">
            <div class="report-item">
                <span>Tempo estacionado:</span>
                <span>${calculo.horasEstacionado.toFixed(2)} horas</span>
            </div>
            <div class="report-item">
                <span>Valor base:</span>
                <span>${formatarMoeda(calculo.valorBase)}</span>
            </div>
    `;
    
    if (calculo.desconto > 0) {
        resumoHtml += `
            <div class="report-item" style="color: #16a34a;">
                <span>Desconto PIX (5%):</span>
                <span>-${formatarMoeda(calculo.desconto)}</span>
            </div>
        `;
    }
    
    resumoHtml += `
            <div class="report-item" style="border-top: 2px solid #e2e8f0; padding-top: 10px; font-weight: bold; font-size: 1.1rem;">
                <span>Total a Pagar:</span>
                <span style="color: #dc2626;">${formatarMoeda(calculo.valorFinal)}</span>
            </div>
        </div>
    `;
    
    document.getElementById('detalhes-pagamento').innerHTML = resumoHtml;
    document.getElementById('resumo-pagamento').classList.remove('hidden');
}

async function confirmarSaida() {
    if (!estadoGlobal.veiculoSelecionado || !estadoGlobal.calculoAtual) return;
    
    const horaSaida = document.getElementById('hora-saida').value;
    const exitTime = new Date();
    const [hours, minutes] = horaSaida.split(':');
    exitTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
    
    const dadosSaida = {
        exitTime: exitTime.toISOString(),
        paymentMethod: estadoGlobal.calculoAtual.formaPagamento,
        amountPaid: estadoGlobal.calculoAtual.valorFinal
    };
    
    try {
        const response = await fetch(`${API_BASE}/vehicles/${estadoGlobal.veiculoSelecionado.id}/exit`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dadosSaida)
        });
        
        if (response.ok) {
            mostrarMensagem(`Saída processada! Valor pago: ${formatarMoeda(estadoGlobal.calculoAtual.valorFinal)}`, 'sucesso');
            limparFormularioSaida();
        } else {
            mostrarMensagem('Erro ao processar saída', 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao processar saída', 'erro');
    }
}

// === RELATÓRIOS ===
async function carregarRelatorios() {
    await atualizarRelatorios();
}

async function atualizarRelatorios() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const stats = await response.json();
        
        // Estatísticas principais
        document.getElementById('rel-total-vehicles').textContent = stats.totalVehicles || 0;
        document.getElementById('rel-total-revenue').textContent = formatarMoeda(stats.totalRevenue || 0);
        document.getElementById('rel-active-vehicles').textContent = stats.activeVehicles || 0;
        
        // Ticket médio
        const ticketMedio = stats.totalRevenue && stats.totalVehicles > 0 
            ? stats.totalRevenue / (stats.totalVehicles - stats.activeVehicles)
            : 0;
        document.getElementById('rel-ticket-medio').textContent = formatarMoeda(ticketMedio);
        
        // Relatório por tipos
        exibirRelatorioTipos(stats);
        exibirRelatorioArrecadacao(stats);
        
    } catch (error) {
        mostrarMensagem('Erro ao carregar relatórios', 'erro');
    }
}

function exibirRelatorioTipos(stats) {
    const tipos = {
        'carroGrande': 'Carros Grandes',
        'carroPequeno': 'Carros Pequenos',
        'moto': 'Motos'
    };
    
    let html = '';
    Object.entries(tipos).forEach(([tipo, label]) => {
        html += `
            <div class="report-item">
                <span>${label}</span>
                <span>${stats.vehiclesByType?.[tipo] || 0}</span>
            </div>
        `;
    });
    
    document.getElementById('relatorio-tipos').innerHTML = html;
}

function exibirRelatorioArrecadacao(stats) {
    const tipos = {
        'carroGrande': 'Carros Grandes',
        'carroPequeno': 'Carros Pequenos',
        'moto': 'Motos'
    };
    
    let html = '';
    Object.entries(tipos).forEach(([tipo, label]) => {
        html += `
            <div class="report-item">
                <span>${label}</span>
                <span>${formatarMoeda(stats.revenueByType?.[tipo] || 0)}</span>
            </div>
        `;
    });
    
    document.getElementById('relatorio-arrecadacao').innerHTML = html;
}

// === VEÍCULOS ATIVOS ===
async function carregarVeiculosAtivos() {
    try {
        const response = await fetch(`${API_BASE}/vehicles/active`);
        const veiculos = await response.json();
        
        exibirListaVeiculos(veiculos);
    } catch (error) {
        mostrarMensagem('Erro ao carregar veículos ativos', 'erro');
    }
}

function exibirListaVeiculos(veiculos) {
    const container = document.getElementById('lista-veiculos');
    
    if (veiculos.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 40px; color: #6b7280;">Nenhum veículo no estacionamento</p>';
        return;
    }
    
    let html = '<div class="vehicle-list">';
    
    veiculos.forEach(veiculo => {
        const tempoEstacionado = calcularTempoEstacionado(veiculo.entryTime);
        
        html += `
            <div class="vehicle-item">
                <div class="vehicle-details">
                    <div class="vehicle-detail"><strong>Placa:</strong> ${veiculo.plate}</div>
                    <div class="vehicle-detail"><strong>Tipo:</strong> ${obterLabelTipoVeiculo(veiculo.vehicleType)}</div>
                    <div class="vehicle-detail"><strong>Veículo:</strong> ${veiculo.brand} ${veiculo.model}</div>
                    <div class="vehicle-detail"><strong>Entrada:</strong> ${formatarDataHora(veiculo.entryTime)}</div>
                    <div class="vehicle-detail"><strong>Tempo:</strong> ${tempoEstacionado}</div>
                </div>
                <button onclick="processarSaidaVeiculo('${veiculo.plate}')" class="btn btn-red" style="min-width: 120px;">
                    🚪 Processar Saída
                </button>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function processarSaidaVeiculo(placa) {
    mostrarSecao('saida');
    document.getElementById('busca-placa').value = placa;
    buscarVeiculo();
}

// === UTILITÁRIOS ===
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

function formatarDataHora(dataString) {
    const data = new Date(dataString);
    return data.toLocaleString('pt-BR');
}

function obterLabelTipoVeiculo(tipo) {
    switch (tipo) {
        case 'carroGrande': return 'Carro Grande';
        case 'carroPequeno': return 'Carro Pequeno';
        case 'moto': return 'Moto';
        default: return tipo;
    }
}

function calcularTempoEstacionado(entryTime) {
    const entrada = new Date(entryTime);
    const agora = new Date();
    const diffMs = agora.getTime() - entrada.getTime();
    const horas = Math.floor(diffMs / (1000 * 60 * 60));
    const minutos = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
    
    return `${horas}h ${minutos}m`;
}

function mostrarMensagem(texto, tipo = 'info') {
    const container = document.getElementById('mensagens');
    container.classList.remove('hidden');
    
    const mensagem = document.createElement('div');
    mensagem.className = `mensagem ${tipo}`;
    mensagem.textContent = texto;
    
    container.appendChild(mensagem);
    
    // Auto remover após 5 segundos
    setTimeout(() => {
        mensagem.remove();
        if (container.children.length === 0) {
            container.classList.add('hidden');
        }
    }, 5000);
}

// Permitir busca com Enter
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const target = e.target;
        if (target.id === 'busca-placa') {
            buscarVeiculo();
        }
    }
});