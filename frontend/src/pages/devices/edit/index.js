import DeviceForm from '../../../components/device-form/index.js';


export default class Page {
  element;
  deviceId;
  subElements = {};
  components = {};

  constructor(match) {
    [, this.deviceId] = match;
  }

  async initComponents () {
    const deviceForm = new DeviceForm(this.deviceId);
    await deviceForm.render();
    this.components.deviceForm = deviceForm;
  }

  get template () {
    return `
    <div class="device-edit">
      <div class="content__top-panel">
        <h1 class="page-title">
          <a href="/devices" class="link">Оборудование</a> / 
            ${this.deviceId? 'Редактировать' : 'Добавить'}
        </h1>
      </div>
      <div class="content-box">
        <div data-element="deviceForm">
          <!-- device-form component -->
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
