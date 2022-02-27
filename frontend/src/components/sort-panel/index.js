import RangePicker from '../range-picker/index.js';
import fetchJson from '../../utils/fetch-json.js';

const BACKEND_URL = process.env.BACKEND_URL;


export default class SortPanel {
  element;
  subElements = {};
  components = {};
  departmentUrl = 'api/departments';
  departments;

  constructor() {
    this.render();
    this.addDepartments();
  }


  get template () {
    return `
    <div class="content-box content-box_small">
      <form class="form-inline">
        <div class="form-group">
          <label class="form-label">Искать по:</label>
          <input type="text" data-element="filterDescription" class="form-control" placeholder="описанию заявки">
        </div>
        <div class="form-group">
          <input type="text" data-element="filterInventory" class="form-control" placeholder="инвентарному номеру">
        </div>
        <div data-element="rangePicker">
         <!-- range-picker component -->
        </div>
      <div class="form-group">
        <label class="form-label">Статус:</label>
        <select class="form-control" data-element="filterStatus">
          <option value="" selected="">Любой</option>
          <option value="1">Открыта</option>
          <option value="0">Закрыта</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Организация:</label>
        <select class="form-control" data-element="filterDepartment">
          <option value="" selected="">Любая</option>
        </select>
      </div>
    </form>
  </div>`;
  }

  render () {
    const element = document.createElement('div');
    element.innerHTML = this.template;
    this.element = element.firstElementChild;

    this.subElements = this.getSubElements(this.element);

    this.initComponents();
    
    this.renderComponents();

    return this.element;
  }

  initComponents() {
    const to = new Date();
    const from = new Date(to.getTime() - (30 * 24 * 60 * 60 * 1000));

    const rangePicker = new RangePicker({
      from,
      to
    });

    this.components.rangePicker = rangePicker;
  }

  renderComponents () {
    Object.keys(this.components).forEach(component => {
      const root = this.subElements[component];
      const { element } = this.components[component];

      root.append(element);
    });
  }

  async getDepartmentData() {
    const fetchUrl = this.getFetchUrl(this.departmentUrl);
    this.departments =  await fetchJson(fetchUrl);
  }

  async addDepartments() {
    await this.getDepartmentData();
    const { filterDepartment } = this.subElements;
    this.departments.map(department => {
      const option = new Option(department.title, department.id);
      filterDepartment.append(option);
    });
  }

  getFetchUrl(url) {
    const fetchUrl = new URL(url, BACKEND_URL);
    return fetchUrl;
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

