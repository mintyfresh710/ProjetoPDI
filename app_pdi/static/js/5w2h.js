// Funcionalidades do 5W2H com integração Django
let savedPlans = [];

// Função para obter o token CSRF do Django
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return null;
}

// Função para fazer requisições AJAX
async function makeRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (method !== 'GET' && data) {
        options.body = JSON.stringify(data);
        // Adicionar token CSRF se necessário
        const csrfToken = getCSRFToken();
        if (csrfToken) {
            options.headers['X-CSRFToken'] = csrfToken;
        }
    }

    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        // Verificar se o usuário não está logado
        if (response.status === 401) {
            showNotification('Você precisa estar logado para usar esta funcionalidade', 'error');
            // Redirecionar para a página de login após 2 segundos
            setTimeout(() => {
                window.location.href = '/app_pdi/';
            }, 2000);
            return null;
        }
        
        return result;
    } catch (error) {
        console.error('Erro na requisição:', error);
        showNotification('Erro de conexão com o servidor', 'error');
        return null;
    }
}

// Função para carregar planos salvos do servidor
async function loadSavedPlans() {
    const result = await makeRequest('/app_pdi/api/w2h-plans/');
    if (result && result.plans) {
        savedPlans = result.plans;
        displaySavedPlans();
    }
}

// Função para salvar o planejamento 5W2H no servidor
async function save5W2H() {
    const plan = {
        what: document.getElementById('what').value,
        why: document.getElementById('why').value,
        who: document.getElementById('who').value,
        when: document.getElementById('when').value,
        where: document.getElementById('where').value,
        how: document.getElementById('how').value,
        howmuch: document.getElementById('howmuch').value
    };

    // Validar se pelo menos um campo está preenchido
    const hasContent = Object.values(plan).some(value => 
        typeof value === 'string' && value.trim() !== ''
    );

    if (!hasContent) {
        alert('Por favor, preencha pelo menos um campo antes de salvar.');
        return;
    }

    const result = await makeRequest('/app_pdi/api/w2h-plans/', 'POST', plan);
    
    if (result && result.success) {
        showNotification(result.message, 'success');
        loadSavedPlans(); // Recarregar a lista de planos
        clear5W2H(); // Limpar o formulário após salvar
    } else {
        showNotification(result ? result.message : 'Erro ao salvar plano', 'error');
    }
}

// Função para limpar todos os campos
function clear5W2H() {
    if (confirm('Tem certeza que deseja limpar todos os campos?')) {
        document.getElementById('what').value = '';
        document.getElementById('why').value = '';
        document.getElementById('who').value = '';
        document.getElementById('when').value = '';
        document.getElementById('where').value = '';
        document.getElementById('how').value = '';
        document.getElementById('howmuch').value = '';
        showNotification('Campos limpos!', 'info');
    }
}

// Função para exportar para PDF (simulação)
function export5W2H() {
    const plan = {
        what: document.getElementById('what').value,
        why: document.getElementById('why').value,
        who: document.getElementById('who').value,
        when: document.getElementById('when').value,
        where: document.getElementById('where').value,
        how: document.getElementById('how').value,
        howmuch: document.getElementById('howmuch').value
    };

    // Verificar se há conteúdo para exportar
    const hasContent = Object.values(plan).some(value => value.trim() !== '');
    
    if (!hasContent) {
        alert('Não há conteúdo para exportar. Preencha os campos primeiro.');
        return;
    }

    // Simular exportação (em um projeto real, isso seria implementado no backend)
    showNotification('Funcionalidade de exportação em desenvolvimento!', 'info');
    
    // Aqui você poderia implementar a geração real do PDF
    // Por exemplo, enviando os dados para uma view Django que gera PDF
}

// Função para exibir os planos salvos
function displaySavedPlans() {
    const container = document.getElementById('savedPlansList');
    
    if (savedPlans.length === 0) {
        container.innerHTML = '<p class="no-plans">Nenhum plano salvo ainda.</p>';
        return;
    }

    let html = '';
    savedPlans.forEach((plan, index) => {
        html += `
            <div class="saved-plan-item">
                <div class="plan-header">
                    <span class="plan-date">Salvo em: ${plan.created_at}</span>
                    <div class="plan-actions">
                        <button onclick="loadPlan(${plan.id})" class="btn-load">Carregar</button>
                        <button onclick="deletePlan(${plan.id})" class="btn-delete">Excluir</button>
                    </div>
                </div>
                <div class="plan-preview">
                    <strong>O que:</strong> ${plan.what ? plan.what.substring(0, 100) : 'Não preenchido'}${plan.what && plan.what.length > 100 ? '...' : ''}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Função para carregar um plano salvo do servidor
async function loadPlan(planId) {
    if (confirm('Isso substituirá o conteúdo atual. Deseja continuar?')) {
        const result = await makeRequest(`/app_pdi/api/w2h-plans/${planId}/`);
        
        if (result && result.plan) {
            const plan = result.plan;
            document.getElementById('what').value = plan.what || '';
            document.getElementById('why').value = plan.why || '';
            document.getElementById('who').value = plan.who || '';
            document.getElementById('when').value = plan.when || '';
            document.getElementById('where').value = plan.where || '';
            document.getElementById('how').value = plan.how || '';
            document.getElementById('howmuch').value = plan.howmuch || '';
            
            showNotification('Plano carregado com sucesso!', 'success');
            
            // Auto-resize dos textareas após carregar
            const fields = ['what', 'why', 'who', 'when', 'where', 'how', 'howmuch'];
            fields.forEach(field => {
                const element = document.getElementById(field);
                if (element) {
                    element.style.height = 'auto';
                    element.style.height = element.scrollHeight + 'px';
                }
            });
        } else {
            showNotification('Erro ao carregar plano', 'error');
        }
    }
}

// Função para excluir um plano salvo do servidor
async function deletePlan(planId) {
    if (confirm('Tem certeza que deseja excluir este plano?')) {
        const result = await makeRequest(`/app_pdi/api/w2h-plans/${planId}/`, 'DELETE');
        
        if (result && result.success) {
            showNotification(result.message, 'info');
            loadSavedPlans(); // Recarregar a lista de planos
        } else {
            showNotification(result ? result.message : 'Erro ao excluir plano', 'error');
        }
    }
}

// Função para mostrar notificações
function showNotification(message, type = 'info') {
    // Remover notificação existente
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Criar nova notificação
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Função para auto-salvar (salvar automaticamente a cada 30 segundos)
function autoSave() {
    const fields = ['what', 'why', 'who', 'when', 'where', 'how', 'howmuch'];
    const hasContent = fields.some(field => 
        document.getElementById(field).value.trim() !== ''
    );
    
    if (hasContent) {
        const autoSaveData = {};
        fields.forEach(field => {
            autoSaveData[field] = document.getElementById(field).value;
        });
        localStorage.setItem('5w2h_autosave', JSON.stringify(autoSaveData));
    }
}

// Função para carregar auto-save
function loadAutoSave() {
    const autoSaveData = JSON.parse(localStorage.getItem('5w2h_autosave'));
    if (autoSaveData) {
        Object.keys(autoSaveData).forEach(field => {
            const element = document.getElementById(field);
            if (element && autoSaveData[field]) {
                element.value = autoSaveData[field];
            }
        });
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    loadSavedPlans(); // Carregar planos do servidor
    loadAutoSave(); // Carregar auto-save local
    
    // Configurar auto-save a cada 30 segundos
    setInterval(autoSave, 30000);
    
    // Adicionar event listeners para os campos
    const fields = ['what', 'why', 'who', 'when', 'where', 'how', 'howmuch'];
    fields.forEach(field => {
        const element = document.getElementById(field);
        if (element) {
            element.addEventListener('input', function() {
                // Auto-resize textarea
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
        }
    });
});

// Limpar auto-save quando sair da página
window.addEventListener('beforeunload', function() {
    localStorage.removeItem('5w2h_autosave');
});

