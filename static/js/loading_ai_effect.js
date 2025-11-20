const form = document.getElementById('trip-form');
const loading = document.getElementById('loading');
const footer = document.querySelector('footer');
// savePlanContainer nie jest już potrzebny, bo wszystko jest w jednym bloku

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  loading.classList.remove('hidden');
  footer.innerHTML = '';

  const formData = new FormData(form);

  try {
    const response = await fetch("", {
      method: "POST",
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: formData
    });

    if (response.ok) {
      const html = await response.text();
      footer.innerHTML = html;
    } else {
      footer.innerHTML = `<div class="text-red-600">Błąd serwera. Spróbuj ponownie.</div>`;
    }

  } catch (err) {
    footer.innerHTML = `<div class="text-red-600">Coś poszło nie tak. Proszę spróbuj ponownie.</div>`;
  } finally {
    loading.classList.add('hidden');
  }
});