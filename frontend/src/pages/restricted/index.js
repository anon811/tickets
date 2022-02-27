export default class {
  element;

  async render () {
    const element = document.createElement('div');

    element.innerHTML = `
      <div class="restricted">
        <h1 class="page-title">Неавторизованный пользователь</h1>
        <p>Возможность редактирования доступна только авторизованным пользователям, 
        необходимо войти. Воспользуйтесь формой входа на панели слева.</p>
      </div>
    `;

    this.element = element.firstElementChild

    return this.element;
  }
}
