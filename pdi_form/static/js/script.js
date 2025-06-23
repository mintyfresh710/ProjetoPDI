document.addEventListener('DOMContentLoaded', function() {
    // 1. Validação do formulário
    const setupFormValidation = function() {
        const form = document.getElementById('pdi-form');
        if (!form) return;

        form.addEventListener('submit', function(event) {
            let isValid = true;

            const requiredFields = ['nome', 'ra', 'curso', 'perfil', 'competencias'];
            requiredFields.forEach(function(field) {
                const input = document.getElementById(field);
                const errorElement = document.getElementById(`${field}-error`);

                if (input && input.value.trim() === '') {
                    isValid = false;
                    input.classList.add('is-invalid');
                    if (errorElement) errorElement.textContent = 'Este campo é obrigatório';
                } else if (input) {
                    input.classList.remove('is-invalid');
                    if (errorElement) errorElement.textContent = '';
                }
            });

            const urlFields = ['linkedin', 'link_tcc'];
            urlFields.forEach(function(field) {
                const input = document.getElementById(field);
                const errorElement = document.getElementById(`${field}-error`);

                if (input && input.value.trim() !== '') {
                    try {
                        new URL(input.value);
                        input.classList.remove('is-invalid');
                        if (errorElement) errorElement.textContent = '';
                    } catch (e) {
                        isValid = false;
                        input.classList.add('is-invalid');
                        if (errorElement) errorElement.textContent = 'URL inválida';
                    }
                }
            });

            if (!isValid) {
                event.preventDefault();
                const firstError = document.querySelector('.is-invalid');
                if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    };

    // 2. Visualização prévia do PDF
    const setupPreviewButton = function() {
        const previewButton = document.getElementById('preview-pdf');
        const form = document.getElementById('pdi-form');

        if (!previewButton || !form) return;

        previewButton.addEventListener('click', function(event) {
            event.preventDefault();

            const requiredFields = ['nome', 'ra', 'curso'];
            let isValid = true;

            requiredFields.forEach(function(field) {
                const input = document.getElementById(field);
                if (input && input.value.trim() === '') isValid = false;
            });

            if (isValid) {
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
    };

    // 3. Expandir/colapsar seções
    const setupSectionToggles = function() {
        const sectionHeaders = document.querySelectorAll('.form-section h2');
        
        sectionHeaders.forEach(function(header) {
            header.addEventListener('click', function() {
                const section = this.parentElement;
                const content = section.querySelector('.section-content');

                if (content) {
                    content.style.display = (content.style.display === 'none') ? 'block' : 'none';
                    this.classList.toggle('collapsed');
                }
            });
        });
    };

    // 4. Gerenciamento de semestres
    const setupSemesters = function() {
        const semesterContainer = document.querySelector('.semester-container');
        if (!semesterContainer) return;

        const MAX_SEMESTRES = 10;

        const atualizarNumeracaoSemestres = function() {
            const boxes = semesterContainer.querySelectorAll('.semestre-box');
            boxes.forEach((box, index) => {
                const semestreNumero = index + 1;
                const label = box.querySelector('label');
                const input = box.querySelector('input');

                label.textContent = `${semestreNumero}º semestre`;
                label.setAttribute('for', `semestre-${semestreNumero}`);
                input.name = `pitch_${semestreNumero}_semestre`;
                input.id = `semestre-${semestreNumero}`;
            });
        };

        const pitchHeader = document.querySelector('.pitch-header');
        if (pitchHeader && !pitchHeader.querySelector('.btn-add-semestre')) {
            const addButton = document.createElement('button');
            addButton.type = 'button';
            addButton.className = 'btn-add-semestre';
            addButton.innerHTML = '+';
            addButton.style.marginLeft = '10px';

            addButton.addEventListener('click', function() {
                const currentSemestres = semesterContainer.querySelectorAll('.semestre-box').length;
                if (currentSemestres >= MAX_SEMESTRES) {
                    alert('Você só pode adicionar até 10 semestres.');
                    return;
                }

                const box = document.createElement('div');
                box.className = 'semestre-box';

                const label = document.createElement('label');
                const input = document.createElement('input');
                input.type = 'text';
                input.className = 'form-control';

                const removeBtn = document.createElement('button');
                removeBtn.type = 'button';
                removeBtn.className = 'btn-remove-semestre';
                removeBtn.innerHTML = 'X';
                removeBtn.addEventListener('click', () => {
                    box.remove();
                    atualizarNumeracaoSemestres();
                });

                box.appendChild(label);
                box.appendChild(input);
                box.appendChild(removeBtn);
                semesterContainer.appendChild(box);

                atualizarNumeracaoSemestres();
            });

            pitchHeader.appendChild(addButton);
        }

        atualizarNumeracaoSemestres();
    };

    // 5. Gerenciamento do campo TCC
    const setupTCCField = function() {
        const tccContainer = document.getElementById('tcc-container');
        const tccHeader = document.querySelector('.tcc-header');

        if (!tccHeader || tccHeader.querySelector('.btn-add-tcc')) return;

        const addTccBtn = document.createElement('button');
        addTccBtn.type = 'button';
        addTccBtn.className = 'btn-add-semestre';
        addTccBtn.innerHTML = '+';
        addTccBtn.style.marginLeft = '10px';
        addTccBtn.id = 'add-tcc-btn';

        addTccBtn.addEventListener('click', function() {
            if (tccContainer.querySelector('.tcc-box')) {
                alert('Você só pode adicionar um link do TCC.');
                return;
            }

            const box = document.createElement('div');
            box.className = 'tcc-box';

            const input = document.createElement('input');
            input.type = 'url';
            input.name = 'link_tcc';
            input.id = 'link_tcc';
            input.className = 'form-control';
            input.placeholder = 'https://...';

            const removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.className = 'btn-remove-semestre';
            removeBtn.innerHTML = 'X';
            
            removeBtn.addEventListener('click', function() {
                box.remove();
                const errorElement = document.getElementById('link_tcc-error');
                if (errorElement) errorElement.textContent = '';
            });

            input.addEventListener('input', function() {
                if (input.value.trim() !== '') {
                    try {
                        new URL(input.value);
                        input.classList.remove('is-invalid');
                        const errorElement = document.getElementById('link_tcc-error');
                        if (errorElement) errorElement.textContent = '';
                    } catch (e) {
                        input.classList.add('is-invalid');
                        const errorElement = document.getElementById('link_tcc-error');
                        if (errorElement) errorElement.textContent = 'URL inválida';
                    }
                } else {
                    input.classList.remove('is-invalid');
                    const errorElement = document.getElementById('link_tcc-error');
                    if (errorElement) errorElement.textContent = '';
                }
            });

            box.appendChild(input);
            box.appendChild(removeBtn);
            tccContainer.appendChild(box);
            input.focus();
        });

        tccHeader.appendChild(addTccBtn);
    };

    // Inicializa todas as funcionalidades
    setupFormValidation();
    setupPreviewButton();
    setupSectionToggles();
    setupSemesters();
    setupTCCField();
});
