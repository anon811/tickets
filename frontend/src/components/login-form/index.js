import fetchJson from '../../utils/fetch-json';

const BACKEND_URL = process.env.BACKEND_URL;

export default class LoginForm {
  loginUrl = 'auth/login/'
  element;
  subElements;

  constructor() {
    this.render();
    this.initEventListeners();
  }

  render() {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = this.getTemplate();
    this.element = wrapper.firstElementChild;
    this.subElements = this.getSubElements();
    return this.element;
  }

  show() {
    // document.body.style.overflowY = 'hidden';
    let container = document.querySelector('.login-form-container');
    container.style.display = "block";
  }

  getTemplate() {
    return `
    <div class="login-form-container form-inline">
      <div class="login-form">
        <form id="login-form" class="form-grid" data-element="loginForm">

          <div class="form-group form-group__half_left">
            <fieldset>
              <label class="form-label">Логин</label>
              <input  class="form-control" name="login" type="text" data-element="login">
            </fieldset>
          </div>

          <div class="form-group form-group__half_left">
            <fieldset>
              <label class="form-label">Пароль</label>
              <input class="form-control" name="password" type="password" data-element="password">
            </fieldset>
          </div>

          <div class="form-buttons">

            <button type="submit" name="save" class="button-primary-outline" data-element="btnSubmit">
              Войти
            </button>

            <button type="submit" name="cancel" class="button-primary-outline" data-element="btnCancel">
              Отмена
            </button>

          </div>         
        </form>
      </div>
    </div>
    `;
  }

  initEventListeners() {
      const {btnCancel, btnSubmit} = this.subElements;
      btnSubmit.addEventListener('click', this.onSubmit);
      btnCancel.addEventListener('click', this.onCancel);
  }

  removeEventListeners() {
    const {btnCancel, btnSubmit} = this.subElements;
    btnSubmit.removeEventListener('click', this.onSubmit);
    btnCancel.removeEventListener('click', this.onCancel);
  }

  onSubmit = async (event) => {
    event.preventDefault();
    const {loginForm} = this.subElements;
    const login = loginForm.login.value;
    const password = loginForm.password.value;
    await this.loginWithEmailAndPassword(login, password);
    this.remove();
  }

  loginWithEmailAndPassword = async (login, password) => {
    const fetchUrl = new URL(this.loginUrl, BACKEND_URL);

    const data = {
      'username': login,
      'password': password,
    };
    
    const requestParams = {
      method: 'POST',
      headers:             {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(data)
    };

    try {
      const responseData = await fetchJson(fetchUrl, requestParams);
      const {key} = responseData;
      this.element.dispatchEvent(new CustomEvent('authStateChanged', {
        detail: {
          user: login,
          key: key,
        },
        bubbles: true,
      }));
    } catch (error) {
      alert(error);
    }
  }

  onCancel = (event) => {
    event.preventDefault();
    this.remove();
  }

  getSubElements() {
    const elements = this.element.querySelectorAll('[data-element]');

    return [...elements].reduce((accum, subElement) => {
      accum[subElement.dataset.element] = subElement;

      return accum;
    }, {});
  }

  remove() {
    this.removeEventListeners();
    this.element.remove();
  }

  destroy() {
    this.remove();
  }

}