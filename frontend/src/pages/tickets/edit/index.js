import TicketForm from '../../../components/ticket-form/index.js';


export default class Page {
  ticketId;
  element;
  subElements = {};
  components = {};

  constructor(match) {
    [, this.ticketId] = match;
  }

  async initComponents () {
    const ticketForm = new TicketForm(this.ticketId);
    await ticketForm.render();
    this.components.ticketForm = ticketForm;
  }

  get template () {
    return `
    <div class="ticket-edit">
      <div class="content__top-panel">
        <h1 class="page-title">
          <a href="/tickets" class="link">Заявки</a> / 
            ${this.ticketId? 'Редактировать' : 'Добавить'}
        </h1>
      </div>
      <div class="content-box">
        <div data-element="ticketForm">
          <!-- ticket-form component -->
        </div>
      </div>
    </div>`;
  }

  async render () {
    const element = document.createElement('div');

    element.innerHTML = this.template;

    this.element = element.firstElementChild;
    this.subElements = this.getSubElements(this.element);

    await this.initComponents();

    this.renderComponents();

    return this.element;
  }

  renderComponents () {
    Object.keys(this.components).forEach(component => {
      const root = this.subElements[component];
      const { element } = this.components[component];
      root.append(element);
    });
  }

  getSubElements ($element) {
    const elements = $element.querySelectorAll('[data-element]');

    return [...elements].reduce((accum, subElement) => {
      accum[subElement.dataset.element] = subElement;

      return accum;
    }, {});
  }

  destroy () {
    for (const component of Object.values(this.components)) {
      component.destroy();
    }

    this.element.remove();
  }
}
