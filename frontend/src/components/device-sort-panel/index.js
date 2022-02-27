import fetchJson from '../../utils/fetch-json.js';

const BACKEND_URL = process.env.BACKEND_URL;


export default class SortPanel {
  element;
  subElements = {};
  departmentUrl = 'api/departments';
  devtypesUrl = 'api/devtypes'
  departments;
  devtypes;

  constructor() {
    this.render();
    this.populateForm();
  }

  get template () {
    return `
    <div class="content-box content-box_small">
        <form class="form-inline">
            <div class="form-group">
                <label class="form-label">Искать по:</label>
                <input type="text" data-element="filterInventory" class="form-control" placeholder="инвентарному номеру">
            </div>
            <div class="form-group">
                <input type="text" data-element="filterTitle" class="form-control" placeholder="названию устройства">
            </div>
            <div class="form-group">
                <label class="form-label">Организация:</label>
                <select class="form-control" data-element="filterDepartment">
                <option value="" selected="">Любая</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">Тип:</label>
                <select class="form-control" data-element="filterType">
                <option value="" selected="">Любой</option>
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

    return this.element;
  }

  async getSingleData(url, searchQueryParams){
    const fetchUrl = this.getFetchUrl(url, searchQueryParams);
    const response = fetchJson(fetchUrl);
    return response;
  }

  async getAllData() {
    const requests = [];
    const departmentRequest = this.getSingleData(this.departmentUrl);
    const devtypesRequest = this.getSingleData(this.devtypesUrl);
    requests.push(departmentRequest, devtypesRequest);
    return Promise.all(requests);
  }

  addDepartments() {
    const { filterDepartment } = this.subElements;
    this.departments.map(department => {
      const option = new Option(department.title, department.id);
      filterDepartment.append(option);
    });
  }

  addDevtypes() {
    const {filterType} = this.subElements;
    this.devtypes.map(devtype => {
      const option = new Option(devtype.title, devtype.id);
      filterType.append(option);
    });
  }

  async populateForm() {
    [this.departments, this.devtypes] = await this.getAllData();
    this.addDepartments();
    this.addDevtypes(); 
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
    this.element.remove();
  }
}