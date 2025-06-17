// Funcionalidades do 5W2H
let savedPlans = JSON.parse(localStorage.getItem('5w2h_plans')) || [];

// Função para salvar o planejamento 5W2H
function save5W2H() {
    const plan = {
        id: Date.now(),
        date: new Date().toLocaleDateString('pt-BR'),
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

    savedPlans.push(plan);
    localStorage.setItem('5w2h_plans', JSON.stringify(savedPlans));
    
    displaySavedPlans();
    showNotification('Planejamento salvo com sucesso!', 'success');
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
    // Por exemplo, usando jsPDF ou enviando os dados para o backend Django
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
                    <span class="plan-date">Salvo em: ${plan.date}</span>
                    <div class="plan-actions">
                        <button onclick="loadPlan(${index})" class="btn-load">Carregar</button>
                        <button onclick="deletePlan(${index})" class="btn-delete">Excluir</button>
                    </div>
                </div>
                <div class="plan-preview">
                    <strong>O que:</strong> ${plan.what.substring(0, 100)}${plan.what.length > 100 ? '...' : ''}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Função para carregar um plano salvo
function loadPlan(index) {
    if (confirm('Isso substituirá o conteúdo atual. Deseja continuar?')) {
        const plan = savedPlans[index];
        document.getElementById('what').value = plan.what;
        document.getElementById('why').value = plan.why;
        document.getElementById('who').value = plan.who;
        document.getElementById('when').value = plan.when;
        document.getElementById('where').value = plan.where;
        document.getElementById('how').value = plan.how;
        document.getElementById('howmuch').value = plan.howmuch;
        
        showNotification('Plano carregado com sucesso!', 'success');
    }
}

// Função para excluir um plano salvo
function deletePlan(index) {
    if (confirm('Tem certeza que deseja excluir este plano?')) {
        savedPlans.splice(index, 1);
        localStorage.setItem('5w2h_plans', JSON.stringify(savedPlans));
        displaySavedPlans();
        showNotification('Plano excluído!', 'info');
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
    displaySavedPlans();
    loadAutoSave();
    
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

