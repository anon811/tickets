import SortableTable from '../../../components/sortable-table/index.js';
import header from './positions-header.js';


export default class Page {
  element;
  components = {};
  subElements = {};

  render() {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = this.template;
    this.element = wrapper.firstElementChild;
    this.subElements = this.getSubElements(this.element);
    this.initComponents();
    this.renderComponents();
    return this.element;
  }

  get template() {
    return `
    <div class="position-details">
      <div class="positions-list">
          <div class="content__top-panel">
              <h1 class="page-title">Просмотр расходных материалов</h1>
              <a href="/positions/add" class="button-primary">Добавить позицию</a>
          </div>
          <div data-element="sortableTable">
              <!-- sortable-table component -->
          </div>
      </div>
    </div>`;
  }

  getSubElements(element) {
    const elements = element.querySelectorAll('[data-element]');
    
    return [...elements].reduce((accum, subElement) => {
      accum[subElement.dataset.element] = subElement;

      return accum;
    }, {});
  }

  initComponents() {
    const sortableTable = new SortableTable(header, {
      url: 'api/positions/',
      href: '/positions',
    });

    this.components.sortableTable = sortableTable;
  }

  renderComponents() {
    Object.keys(this.components).forEach(component => {
      const root = this.subElements[component];
      const {element} = this.components[component];
      root.append(element);
    })
  }

  destroy() {
    
    for (const component of Object.values(this.components)) {
      component.destroy();
    }

    this.element.remove();
  }
}