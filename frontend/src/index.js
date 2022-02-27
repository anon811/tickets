import Router from './router/index.js';
import LoginForm from './components/login-form/index.js'
import tooltip from './components/tooltip/index.js';
import NotificationMessage from './components/notification/index.js'


// const URL_PATH = process.env.URL_PATH;
const URL_PATH = '';

class MainPage {
  element;

  constructor () {
    tooltip.initialize();
    this.router = Router.instance();
    this.render();
    this.getAuthMenu(this.user);
    this.addEventListeners();
    this.initialAuthStateCheck();
  }

  get template () {
    return `
      <main class="main">
      <div class="progress-bar">
        <div class="progress-bar__line"></div>
      </div>
      <aside class="sidebar">
        <h2 class="sidebar__title">
          <a href="/${URL_PATH}">TICKETS, PLEASE</a>
        </h2>
        <ul class="sidebar__nav sidebar__auth">
        </ul>
        <ul class="sidebar__nav">
          <li>
            <a href="/${URL_PATH}" data-page="dashboard">
              <i class="icon-dashboard"></i> <span>Сводка</span>
            </a>
          </li>
          <li>
            <a href="/${URL_PATH}tickets" data-page="tickets">
              <i class="icon-products"></i> <span>Заявки</span>
            </a>
          </li>
          <li>
            <a href="/${URL_PATH}devices" data-page="devices">
              <i class="icon-categories"></i> <span>Оборудование</span>
            </a>
          </li>
          <li>
            <a href="/${URL_PATH}positions" data-page="positions">
              <i class="icon-sales"></i> <span>Склад</span>
            </a>
          </li>
        </ul>
        <ul class="sidebar__nav sidebar__nav_bottom">
          <li>
            <button type="button" class="sidebar__toggler">
              <i class="icon-toggle-sidebar"></i> <span>Свернуть</span>
            </button>
          </li>
        </ul>
      </aside>
      <section class="content" id="content">
      </section>
    </main>
    `;
  }

  getAuthMenu (user) {
    user = user === 'null'? null : user;
    const root = this.element.querySelector('.sidebar__auth');
    root.innerHTML = this.authMenuTemplate(user);
  }

  authMenuTemplate(user) {
    return `
      <li>
        <a>
          <i class="user_icon"></i> <span>${user ? `${user}`: 'Гость'}</span>
        </a>
        <ul class="sidebar__nav">
          ${!user ? '<li><a data-element="login">Войти</a>':'<li><a data-element="logout">Выйти</a>'}
        </ul>
      </li>`;
  }

  render () {
    const element = document.createElement('div');
    element.innerHTML = this.template;

    this.element = element.firstElementChild;
    document.body.append(this.element);
  }

  initializeRouter() {
    this.router
    .addRoute(new RegExp(`^${URL_PATH}$`), 'dashboard')
    .addRoute(new RegExp(`^${URL_PATH}tickets$`), 'tickets/list')
    .addRoute(new RegExp(`^${URL_PATH}tickets/add$`), 'tickets/edit')
    .addRoute(new RegExp(`^${URL_PATH}tickets/([\\w()-]+)$`), 'tickets/edit')
    .addRoute(new RegExp(`^${URL_PATH}devices$`), 'devices/list')
    .addRoute(new RegExp(`^${URL_PATH}devices/add$`), 'devices/edit')
    .addRoute(new RegExp(`^${URL_PATH}devices/([\\w()-]+)$`), 'devices/edit')
    .addRoute(new RegExp(`^${URL_PATH}positions$`), 'positions/list')
    .addRoute(new RegExp(`^${URL_PATH}positions/add$`), 'positions/edit')
    .addRoute(new RegExp(`^${URL_PATH}positions/([\\w()-]+)$`), 'positions/edit')
    .addRoute(/404\/?$/, 'error404')
    .setNotFoundPagePath('error404')
    .listen();
  }

  onAuthStateChanged = event => {
    const {user, key} = event.detail;
    localStorage.setItem('key', key);
    localStorage.setItem('user', user)
    this.getAuthMenu(user);
  }

  initialAuthStateCheck() {
    const user = localStorage.getItem('user');
    const key = localStorage.getItem('key');
    this.element.dispatchEvent(new CustomEvent('authStateChanged', {
      detail: {
        user: user,
        key: key,
      },
      bubbles: true,
    }));

  }

  showNotificationMessage(message, {duration = 3000, type = 'success'} = {}) {
    const notificationMessage = new NotificationMessage(message, {
      duration: duration,
      type: type,
    });
    notificationMessage.show();
  }

  ticketSaved = event => {
    const message = 'Заявка создана';
    this.showNotificationMessage(message);
  }

  ticketUpdated = event => {
    const message = 'Заявка обновлена';
    this.showNotificationMessage(message);
  }

  positionSaved = event => {
    const message = 'Позиция сохранена';
    this.showNotificationMessage(message);
  }

  positionUpdated = event => {
    const message = 'Позиция обновлена';
    this.showNotificationMessage(message);
  }

  formError = event => {
    const message = 'Не удалось сохранить изменения';
    this.showNotificationMessage(message, {type: 'error'})
  }

  deviceSaved = event => {
    const message = 'Устройство добавлено';
    this.showNotificationMessage(message);
  }

  deviceUpdated = event => {
    const message = 'Устройство обновлено';
    this.showNotificationMessage(message);
  }

  nonAuthorized = event => {
    const message = 'Необходимо войти в систему';
    this.showNotificationMessage(message, {type: 'error'});
  }

  addEventListeners() {
    const sidebarToggle = this.element.querySelector('.sidebar__toggler');

    sidebarToggle.addEventListener('click', event => {
      event.preventDefault();
      document.body.classList.toggle('is-collapsed-sidebar');
    });

    document.addEventListener('click', event => {
      if (event.target.closest('[data-element="login"]')) {
        const loginForm = new LoginForm();
        const {element} = loginForm;
        document.body.append(element);
        loginForm.show();
      }
      if (event.target.closest('[data-element="logout"]')) {
        this.element.dispatchEvent(new CustomEvent('authStateChanged', {
          detail: {
            user: null,
            key: null,
          },
          bubbles: true,
        }));
      }

    });

    document.addEventListener('authStateChanged', this.onAuthStateChanged);
    document.addEventListener('ticket-saved', this.ticketSaved);
    document.addEventListener('ticket-updated', this.ticketUpdated);
    document.addEventListener('ticket-error', this.formError);
    document.addEventListener('device-saved', this.deviceSaved);
    document.addEventListener('device-updated', this.deviceUpdated);
    document.addEventListener('device-error', this.formError);
    document.addEventListener('position-saved', this.positionSaved);
    document.addEventListener('position-updated', this.positionUpdated);
    document.addEventListener('position-error', this.formError);
    document.addEventListener('non-authorized', this.nonAuthorized);
  }
}

const mainPage = new MainPage();

document.body.append(mainPage.element);

mainPage.initializeRouter();
