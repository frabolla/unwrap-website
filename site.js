var systemDark = window.matchMedia('(prefers-color-scheme: dark)');
var titleElement = document.querySelector('title');
var italianTitle = titleElement.textContent;

function setLang(lang) {
  document.documentElement.lang = lang;
  updateLangControls();
  try { localStorage.setItem('unwrap-lang', lang); } catch (e) {}
}
// Il testo visibile dipende da <html lang>, impostato già nell'<head> di ogni pagina.
function updateLangControls() {
  var lang = document.documentElement.lang;
  document.getElementById('btn-it').classList.toggle('active', lang === 'it');
  document.getElementById('btn-en').classList.toggle('active', lang === 'en');
  document.title = (lang === 'en' && titleElement.dataset.en) || italianTitle;
  updateThemeButton();
}

function setTheme(theme) {
  if (theme) {
    document.documentElement.setAttribute('data-theme', theme);
  } else {
    document.documentElement.removeAttribute('data-theme');
  }
  updateThemeButton();
  try { localStorage.setItem('unwrap-theme', theme || ''); } catch (e) {}
}
function isDark() {
  var theme = document.documentElement.getAttribute('data-theme');
  return theme ? theme === 'dark' : systemDark.matches;
}
// Se il tema scelto coincide con quello di sistema, si torna a seguire il sistema.
function toggleTheme() {
  var dark = !isDark();
  setTheme(dark === systemDark.matches ? null : (dark ? 'dark' : 'light'));
}
function updateThemeButton() {
  var en = document.documentElement.lang === 'en';
  var label = isDark()
    ? (en ? 'Switch to light theme' : 'Passa al tema chiaro')
    : (en ? 'Switch to dark theme' : 'Passa al tema scuro');
  var button = document.getElementById('theme-toggle');
  if (button) {
    button.title = label;
    button.setAttribute('aria-label', label);
  }
}

updateLangControls();
systemDark.addEventListener('change', updateThemeButton);

function openFaqFromHash() {
  if (location.hash) {
    try {
      var target = document.querySelector(location.hash);
      if (target) {
        if (target.tagName && target.tagName.toLowerCase() === 'details') {
          target.open = true;
        } else {
          var parentDetails = target.closest('details');
          if (parentDetails) parentDetails.open = true;
        }
        setTimeout(function() {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 60);
      }
    } catch (e) {}
  }
}
window.addEventListener('DOMContentLoaded', openFaqFromHash);
window.addEventListener('hashchange', openFaqFromHash);
if (document.readyState === 'interactive' || document.readyState === 'complete') {
  openFaqFromHash();
}
