const data = {
  home: ['Welcome', 'Recent activity', 'Next action'],
  library: ['Saved item', 'Offline item', 'Shared item'],
  settings: ['Appearance', 'Accessibility', 'Notifications'],
};

const title = document.querySelector('#page-title');
const cards = document.querySelector('#cards');
const status = document.querySelector('#status');
const links = [...document.querySelectorAll('.primary-nav a')];

function render(destination, announce = false) {
  const key = data[destination] ? destination : 'home';
  title.textContent = key[0].toUpperCase() + key.slice(1);
  cards.replaceChildren(...data[key].map((label) => {
    const article = document.createElement('article');
    article.className = 'card';
    const heading = document.createElement('h3');
    heading.textContent = label;
    const body = document.createElement('p');
    body.textContent = 'Replace with product content.';
    article.append(heading, body);
    return article;
  }));
  for (const link of links) {
    if (link.hash === `#${key}`) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  }
  status.textContent = announce ? `${title.textContent} loaded` : '';
}

for (const link of links) {
  link.addEventListener('click', () => render(link.hash.slice(1), true));
}

const themeToggle = document.querySelector('#theme-toggle');
themeToggle.addEventListener('click', () => {
  const dark = document.documentElement.dataset.theme !== 'dark';
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  themeToggle.setAttribute('aria-pressed', String(dark));
  themeToggle.textContent = dark ? 'Use light theme' : 'Use dark theme';
});

render(location.hash.slice(1));
