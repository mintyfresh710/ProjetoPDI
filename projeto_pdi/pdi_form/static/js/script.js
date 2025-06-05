// Script para o formulário PDI
document.addEventListener('DOMContentLoaded', function() {
    // Validação do formulário
    const form = document.getElementById('pdi-form');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validar campos obrigatórios
            const requiredFields = ['nome', 'ra', 'curso', 'perfil', 'competencias', 'gaps', 'inicio_jornada', 'desenvolvimento_permanente'];
            
            requiredFields.forEach(function(field) {
                const input = document.getElementById(field);
                const errorElement = document.getElementById(`${field}-error`);
                
                if (input && input.value.trim() === '') {
                    isValid = false;
                    input.classList.add('is-invalid');
                    if (errorElement) {
                        errorElement.textContent = 'Este campo é obrigatório';
                    }
                } else if (input) {
                    input.classList.remove('is-invalid');
                    if (errorElement) {
                        errorElement.textContent = '';
                    }
                }
            });
            
            // Validar URLs
            const urlFields = ['linkedin', 'link_tcc'];
            
            urlFields.forEach(function(field) {
                const input = document.getElementById(field);
                const errorElement = document.getElementById(`${field}-error`);
                
                if (input && input.value.trim() !== '') {
                    try {
                        new URL(input.value);
                        input.classList.remove('is-invalid');
                        if (errorElement) {
                            errorElement.textContent = '';
                        }
                    } catch (e) {
                        isValid = false;
                        input.classList.add('is-invalid');
                        if (errorElement) {
                            errorElement.textContent = 'URL inválida';
                        }
                    }
                }
            });
            
            if (!isValid) {
                event.preventDefault();
                // Rolar até o primeiro campo com erro
                const firstError = document.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    }
    
    // Visualização prévia do PDF
    const previewButton = document.getElementById('preview-pdf');
    
    if (previewButton) {
        previewButton.addEventListener('click', function(event) {
            event.preventDefault();
            
            // Verificar se os campos obrigatórios estão preenchidos
            const requiredFields = ['nome', 'ra', 'curso'];
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                const input = document.getElementById(field);
                if (input && input.value.trim() === '') {
                    isValid = false;
                }
            });
            
            if (isValid) {
                // Submeter o formulário para visualização prévia
                const form = document.getElementById('pdi-form');
                const previewInput = document.createElement('input');
                previewInput.type = 'hidden';
                previewInput.name = 'preview';
                previewInput.value = 'true';
                form.appendChild(previewInput);
                form.submit();
            } else {
                alert('Por favor, preencha pelo menos os campos Nome, RA e Curso para visualizar o PDF.');
            }
        });
    }
    
    // Expandir/colapsar seções
    const sectionHeaders = document.querySelectorAll('.form-section h2');
    
    sectionHeaders.forEach(function(header) {
        header.addEventListener('click', function() {
            const section = this.parentElement;
            const content = section.querySelector('.section-content');
            
            if (content) {
                if (content.style.display === 'none') {
                    content.style.display = 'block';
                    this.classList.remove('collapsed');
                } else {
                    content.style.display = 'none';
                    this.classList.add('collapsed');
                }
            }
        });
    });
});
