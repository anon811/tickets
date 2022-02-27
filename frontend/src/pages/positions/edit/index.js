import PositionForm from "../../../components/position-form";


export default class Page {
  element;
  positionId;
  subElements = {};
  components = {};

  constructor(match) {
    [, this.positionId] = match
  }

  async initComponents () {
    const positionForm = new PositionForm(this.positionId);
    await positionForm.render();
    this.components.positionForm = positionForm;
  }

  get template () {
    return `
    <div class="position-edit">
      <div class="content__top-panel">
        <h1 class="page-title">
          <a href="/positions" class="link">Склад</a> / ${this.positionId? 'Редактировать' : 'Добавить'}
        </h1>
      </div>
      <div class="content-box">
        <div data-element="positionForm">
          <!-- position-form component -->
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
