import escapeHtml from '../../utils/escape-html.js';
import fetchJson from '../../utils/fetch-json.js';

const BACKEND_URL = process.env.BACKEND_URL;

export default class DeviceForm {
  element;
  editMode;
  deviceId;
  departments;
  devtypes;
  deviceData = null;
  devices = null;
  devicesUrl = 'api/devices';
  devtypesUrl = 'api/devtypes';
  departmentsUrl = 'api/departments';


  constructor(deviceId) {
    this.deviceId = deviceId;
    this.editMode = Boolean(this.deviceId);
  }

  async render() {
    const wrapper = document.createElement('div');

    [this.devtypes, this.departments, this.deviceData] = await this.getAllData(this.editMode);

    if (this.editMode) {
      wrapper.innerHTML = this.getEditDeviceFormTemplate(this.deviceData, this.devtypes, this.departments);
    } else {
      wrapper.innerHTML = this.getCreateDeviceFormTemplate(this.devtypes, this.departments);
    }

    const element = wrapper.firstElementChild;
    this.element = element;

    this.subElements = this.getSubElements();

    this.initEventListeners();

    return this.element;
  }

  async getAllData(editMode) {
    const requests = [];

    const devtypesRequest = this.getSingleData(this.devtypesUrl);
    const departmentsRequest = this.getSingleData(this.departmentsUrl);

    requests.push(devtypesRequest, departmentsRequest);

    if (editMode) {
      const deviceRequest = this.getSingleData(this.devicesUrl + '/' + this.deviceId);
      requests.push(deviceRequest);
    }

    return await Promise.all(requests);
  }

  async getSingleData(url, searchQueryParams) {
    const fetchUrl = this.getFetchUrl(url, searchQueryParams);
    const response = await fetchJson(fetchUrl);
    return response;
  }

  getFetchUrl(url, searchQueryParams) {
    const fetchUrl = new URL(url, BACKEND_URL);

    if (searchQueryParams) {
      for (let [param, val] of Object.entries(searchQueryParams)) {
        fetchUrl.searchParams.set(param, val);
      }
    }

    return fetchUrl;
  }

  getEditDeviceFormTemplate(deviceData, devtypes, departments) {
    return `
      <div class="device-form">
        <form data-element="deviceForm" class="form-grid">
          ${this.getInventoryNumberTemplate(deviceData)}
          ${this.getTitleTemplate(deviceData)}
          ${this.getDepartmentTemplate(departments, deviceData)}
          ${this.getDevtypeTemplate(devtypes, deviceData)}
          <div class="form-buttons">
            <button type="submit" name="save" class="button-primary-outline">
              Сохранить
            </button>
          </div>
        </form>
      </div>`;
  }

  getCreateDeviceFormTemplate(devtypes, departments) {
    return `
      <div class="device-form">
        <form data-element="deviceForm" class="form-grid">

          <div class="form-group form-group__wide">
            <label class="form-label">Инвентарный номер</label>
            <input required="" class="form-control" name="inv_num" data-element="deviceInventoryNumber" 
            placeholder="инвентарный номер" value="">
          </div>

          <div class="form-group form-group__wide">
            <label class="form-label">Название</label>
            <input required="" class="form-control" name="title" data-element="deviceTitle" 
              placeholder="название устройства" value="">
          </div>

          ${this.getDepartmentTemplate(departments)}
          ${this.getDevtypeTemplate(devtypes)}
          
          <div class="form-buttons">
            <button type="submit" name="save" class="button-primary-outline">
              Сохранить
            </button>
          </div>
        </form>
      </div>`;
  }

  getDepartmentTemplate(departments, deviceData) {
    if (deviceData) {
      return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Учреждение</label>
        <select class="form-control"  name="department">
        ${departments.map(department => {
          return `
            <option value="${department.id}" ${deviceData.department === department.title ? "selected" : ""}>
              ${department.title}
            </option>
          `;}).join('')}
        </select>
      </div>`;
    }
    return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Учреждение</label>
        <select class="form-control"  name="department">
        ${departments.map(department => {
          return `
            <option value="${department.id}">${department.title}</option>
          `;}).join('')}
        </select>
      </div>`;  
  }

  getDevtypeTemplate(devtypes, deviceData) {
    if (deviceData) {
      return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Тип устройства</label>
        <select class="form-control"  name="type">
        ${devtypes.map(devtype => {
          return `
            <option value="${devtype.id}" ${deviceData.devtype === devtype.title ? "selected" : ""}>
              ${devtype.title}
            </option>
          `;}).join('')}
        </select>
      </div>`;
    }
    return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Тип устройства</label>
        <select class="form-control"  name="type">
        ${devtypes.map(devtype => {
          return `
            <option value="${devtype.id}">${devtype.title}</option>
          `;}).join('')}
        </select>
      </div>`; 
  }

  getInventoryNumberTemplate({inv_num}) {
    return `
      <div class="form-group form-group__wide">
        <label class="form-label">Инвентарный номер</label>
        <input required="" class="form-control" name="inv_num" data-element="deviceInventoryNumber" 
        placeholder="инвентарный номер" value="${inv_num? escapeHtml(inv_num) : ''}">
      </div>`;
  }

  getTitleTemplate({title}) {
    return `
      <div class="form-group form-group__wide">
        <label class="form-label">Название</label>
        <input required="" class="form-control" name="title" data-element="deviceTitle" 
        placeholder="название устройства" value="${title? escapeHtml(title) : ''}">
      </div>`;
  }

  getSubElements(element = this.element) {
    const elements = element.querySelectorAll('[data-element]');

    return [...elements].reduce((accum, subElement) => {
      accum[subElement.dataset.element] = subElement;
      return accum;
    }, {});
  }

  onFormSubmit = (event) => {
    event.preventDefault();
    
    const key = localStorage.getItem('key');

    if (!key || key === 'null') {
      const customEventName = 'non-authorized';
      this.element.dispatchEvent(new CustomEvent(customEventName, {
        bubbles: true,
      }));
    } else {
      const {deviceForm} = this.subElements;
      const formData = new FormData(deviceForm);
      const data = {};

      const payloadFields = [
        'inv_num',
        'title',
        'department',
        'type',
      ];

      const indexToText = [
        'department',
        'type',
      ];

      for (let [name, value] of formData) {
        if (payloadFields.includes(name)) {
          data[name] = indexToText.includes(name) 
            ? deviceForm[name].options[deviceForm[name].selectedIndex].text
            : value;
        }
      }

      if (this.editMode) {
        data.id = parseInt(this.deviceId);
      }

      this.sendFormData(data);
    }
  }

  async sendFormData(data) {
    const fetchUrl = this.editMode 
      ? this.getFetchUrl(this.devicesUrl + '/' + this.deviceId + '/')
      : this.getFetchUrl(this.devicesUrl + '/');
    const key = localStorage.getItem('key');

    const requestParams = {
      method: this.deviceId ? 'PUT' : 'POST',
      headers:             {
        'Content-Type': 'application/json',
        'Authorization': `Token ${key}`,
      },
      body: JSON.stringify(data)
    }

    try {
      await fetchJson(fetchUrl, requestParams);

      const customEventName = (this.editMode) ? "device-updated" : "device-saved";
      this.element.dispatchEvent(new CustomEvent(customEventName, {
        bubbles: true,
      }));
    } catch(err) {
      const customEventName = 'device-error';
      this.element.dispatchEvent(new CustomEvent(customEventName, {
        bubbles: true,
      }));
    }
  }

  initEventListeners() {
    this.element.addEventListener('submit', this.onFormSubmit);
  }

  removeEventListeners() {
    this.element.removeEventListener('submit', this.onFormSubmit);
  }

  remove() {
    this,this.removeEventListeners();
    this.element.remove();
  }

  destroy() {
    this.remove();
  }
}