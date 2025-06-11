document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('dark-mode-toggle');
  const isDark = localStorage.getItem('darkMode') === 'true';

  // Aplica o tema inicial
  if (isDark) {
    document.documentElement.classList.add('dark-theme');
    if (toggle) toggle.checked = true;
  }

  // Configura o evento de mudança
  if (toggle) {
    toggle.addEventListener('change', () => {
      // Alterna o tema visualmente
      document.documentElement.classList.toggle('dark-theme', toggle.checked);
      
      // Salva a preferência no localStorage
      localStorage.setItem('darkMode', toggle.checked);
    });
  }
});