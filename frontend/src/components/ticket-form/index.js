import escapeHtml from '../../utils/escape-html.js';
import fetchJson from '../../utils/fetch-json.js';
import ExpenditureForm from '../expenditure-form/index.js'

import DeleteHandle from './icon-trash.svg'

const BACKEND_URL = process.env.BACKEND_URL;

export default class TicketForm {
  element;
  inputElement;
  ticketData = null;
  worktypes = null;
  categories = null;
  priorities = null;
  users = null;
  devices = null;
  ticketUrl = 'api/tickets';
  worktypesUrl = 'api/worktypes';
  categoriesUrl = 'api/categories';
  prioritiesUrl = 'api/priorities';
  usersUrl = 'api/users';
  devicesUrl = 'api/devices';

  constructor(ticketId) {
    this.ticketId = ticketId;
    this.editMode = Boolean(this.ticketId);
  }

  async render() {
    const wrapper = document.createElement('div');

    [this.worktypes, this.categories, this.priorities, this.users, this.devices, this.ticketData] = await this.getAllData(this.editMode);

    if (this.editMode) {
      wrapper.innerHTML = this.getEditTicketFormTemplate(this.ticketData, this.worktypes, this.priorities, this.users, this.categories);
    } else {
      wrapper.innerHTML = this.getCreateTicketFormTemplate(this.users, this.worktypes, this.priorities, this.categories);
    }

    const element = wrapper.firstElementChild;

    this.element = element;

    this.subElements = this.getSubElements();

    this.initEventListeners();

    if (this.editMode) {
      this.ticketData.expenditures.map(expenditure => {
        const {position, quantity} = expenditure;
        this.addExpenditure(position, quantity);
      });
    }

    return this.element;
  }

  async getAllData(editMode) {
    const requests = [];

    const worktypesRequest = this.getSingleData(this.worktypesUrl);
    const categoriesRequest = this.getSingleData(this.categoriesUrl);
    const prioritiesRequest = this.getSingleData(this.prioritiesUrl);
    const usersRequest = this.getSingleData(this.usersUrl);
    const devicesRequest = this.getSingleData(this.devicesUrl);

    requests.push(worktypesRequest, categoriesRequest, prioritiesRequest, usersRequest, devicesRequest);

    if (editMode) {
      const ticketRequest = this.getSingleData(this.ticketUrl + '/' + this.ticketId);
      requests.push(ticketRequest);
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

  getEditTicketFormTemplate(ticketData, workTypes, priorities, users, categories) {
    return `
      <div class="ticket-form">
        <form data-element="ticketForm" class="form-grid">
          ${this.getCreatedTimeTemplate(ticketData)}
          ${this.getClosedTimeTemplate(ticketData)}
          ${this.getOwnerTemplate(users, ticketData)}
          ${this.getDescriptionTemplate(ticketData)}
          ${this.getDeviceTemplate(ticketData)}
          ${this.getWorkTypesTemplate(workTypes, ticketData)}
          ${this.getPriorityTemplate(priorities, ticketData)}
          ${this.getCategoryTemplate(categories, ticketData)}
          ${this.getExpenditureContainerTemplate()}
          ${this.getStatusTemplate(ticketData)}
          <div class="form-buttons">
            <button type="submit" name="save" class="button-primary-outline">
              Сохранить
            </button>
          </div>
        </form>
      </div>
    `;
  }

  getCreateTicketFormTemplate(users, workTypes, priorities, categories) {
    return `
      <div class="ticket-form">
        <form data-element="ticketForm" class="form-grid">
          <div class="form-group form-group__half_left">
            <fieldset>
              <label class="form-label">Дата создания:</label>
              <input required="" type="date" name="created" class="form-control" placeholder="Дата создания">
            </fieldset>
           </div>
           <div class="form-group form-group__half_left">
            <fieldset>
              <label class="form-label">Дата закрытия:</label>
              <input type="date" name="closed" class="form-control" placeholder="Дата закрытия">
            </fieldset>
          </div>
          ${this.getOwnerTemplate(users)}
          <div class="form-group form-group__wide">
            <label class="form-label">Описание</label>
            <textarea required="" class="form-control" name="description" data-element="ticketDescription"
            placeholder="Описание заявки"></textarea>
          </div>
          <div class="form-group form-group__half_left">
            <fieldset>
              <label class="form-label">Оборудование:</label>
              <input required="" list="devices" type="text" name="device" class="form-control" placeholder="оборудование" 
                autocomplete="off">
              <datalist id="devices" data-element="devicesDatalist">
                ${this.getDevicesDatalist()}
              </datalist>
            </fieldset>
          </div>
          ${this.getWorkTypesTemplate(workTypes)}
          ${this.getPriorityTemplate(priorities)}
          ${this.getCategoryTemplate(categories)}
          ${this.getExpenditureContainerTemplate()}
          <div class="form-group form-group__part-half">
            <label class="form-label">Статус</label>
            <select class="form-control" name="status">
              <option selected value="1">Активен</option>
              <option value="0">Неактивен</option>
            </select>
        </div>
        <div class="form-buttons">
        <button type="submit" name="save" class="button-primary-outline">
          Сохранить
        </button>
      </div>
    </form>
  </div>`;
  }

  getCreatedTimeTemplate({created}) {
    return `
      <div class="form-group form-group__half_left">
        <fieldset>
          <label class="form-label">Дата создания:</label>
          <input required="" type="date" name="created" class="form-control" placeholder="Дата создания" value="${created}">
        </fieldset>
      </div>
    `;
  }

  getClosedTimeTemplate({closed}) {
    return `
      <div class="form-group form-group__half_left">
        <fieldset>
          <label class="form-label">Дата закрытия:</label>
          <input type="date" name="closed" class="form-control" placeholder="Дата закрытия" 
          value="${closed? closed : ''}">
        </fieldset>
      </div>
    `;
  }

  getOwnerTemplate(users, ticketData) {
    if (ticketData) {
      return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Владелец</label>
        <select class="form-control"  name="owner">
        ${users.map(user => {
          return `
            <option value="${user.id}" ${ticketData.owner.includes(user.username) ? "selected" : ""}>${user.username}</option>
          `;}).join('')}
        </select>
      </div>`;
    }
    return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Владелец</label>
        <select class="form-control"  name="owner">
        ${users.map(user => {
          return `
            <option value="${user.id}">${user.username}</option>
          `;}).join('')}
        </select>
      </div>`; 
    
  }

  getDescriptionTemplate({description}) {
    return `
      <div class="form-group form-group__wide">
        <label class="form-label">Описание</label>
        <textarea required="" class="form-control" name="description" data-element="ticketDescription" placeholder="Описание заявки">${description? escapeHtml(description) : ''}</textarea>
      </div>
    `;
  }

  getDeviceTemplate({device}) {
    return `
      <div class="form-group form-group__half_left">
        <fieldset>
          <label class="form-label">Оборудование:</label>
          <input required="" list="devices" type="text" name="device" class="form-control" placeholder="оборудование" 
              value="${device.title},  инв. № ${device.inv_num}" autocomplete="off">
          <datalist id="devices" data-element="devicesDatalist">
            ${this.getDevicesDatalist()}
          </datalist>
        </fieldset>
      </div>
    `;
  }

  getDevicesDatalist() {
    return this.devices.map(device => {
      return ` <option value="${device.title},  инв. № ${device.inv_num}">`
    }).join('');
  }

  getWorkTypesTemplate(workTypes, ticketData) {
    if (ticketData) {
      return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Выполненные работы</label>
          <select multiple class="form-control multiple"  name="work_done">
          ${workTypes.map(worktype => {
            return `
              <option ${ticketData.work_done.includes(worktype.title) ? "selected" : ""} value="${worktype.id}">${worktype.title}</option>
            `;}).join('')}
          </select>
        </div>`;
    }
    return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Выполненные работы</label>
          <select multiple class="form-control multiple"  name="work_done">
          ${workTypes.map(worktype => {
            return `
              <option value="${worktype.id}">${worktype.title}</option>
            `;}).join('')}
          </select>
        </div>`;
  }

  getPriorityTemplate(priorities, ticketData) {
    if (ticketData) {
      return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Приоритет</label>
          <select class="form-control"  name="priority">
          ${priorities.map(priority => {
            return `
              <option ${ticketData.priority.includes(priority.title) ? "selected" : ""} value="${priority.number}">${priority.title}</option>
            `;}).join('')}
          </select>
        </div>`;
    }
    return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Приоритет</label>
          <select class="form-control"  name="priority">
          ${priorities.map(priority => {
            return `
              <option value="${priority.number}">${priority.title}</option>
            `;}).join('')}
          </select>
        </div>`;
  }

  getCategoryTemplate(categories, ticketData) {
    if (ticketData) {
      return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Категория</label>
          <select class="form-control"  name="category">
          ${categories.map(category => {
            return `
              <option ${ticketData.category === category.title ? "selected" : ""} value="${category.id}">${category.title}</option>
            `;}).join('')}
          </select>
        </div>`;
    }
    return `
      <div class="form-group form-group__half_left">
        <label class="form-label">Категория</label>
          <select class="form-control"  name="category">
          ${categories.map(category => {
            return `
              <option value="${category.id}">${category.title}</option>
            `;}).join('')}
          </select>
        </div>`;
  }

  getStatusTemplate({status}) {
    return `
      <div class="form-group form-group__part-half">
        <label class="form-label">Статус</label>
        <select class="form-control" name="status">
          <option ${(status === true) ? "selected" : ""} value="1">Активен</option>
          <option ${(status === false) ? "selected" : ""} value="0">Неактивен</option>
        </select>
      </div>
    `;
  }

  getExpenditureContainerTemplate() {
    return `
      <div class="form-group form-group__wide" data-element="expenditureContainer">
        <label class="form-label">Расход</label>
        <div data-element="expenditures"></div>
        <button type="button" name="addExpenditure" class="button-primary-outline"><span>Добавить расход</span></button>
      </div>
    `;
  }

  getSubElements(element = this.element) {
    const elements = element.querySelectorAll('[data-element]');

    return [...elements].reduce((accum, subElement) => {
      accum[subElement.dataset.element] = subElement;

      return accum;
    }, {});
  }

  showExpenditureForm = () => {
    const expenditureForm = new ExpenditureForm();
    const {element} = expenditureForm;
    document.body.append(element);
    expenditureForm.show();
  }

  getExpenditureTEmplate(title, quantity) {
    return `
    <div class="ticket-edit__expenditure-item" data-expenditure-title="${title}" data-expenditure-quantity="${quantity}">
      <span>
        ${title} 
      </span>
      <span>
        ${quantity} шт.
      </span>
      <button type="button">
        <img src="${DeleteHandle}" alt="delete" data-delete-handle>
      </button>
    </div>`;
  }

  newExpenditure = (event) => {
    const {title, quantity} = event.detail;
    this.addExpenditure(title, quantity);
  } 

  addExpenditure  = (title, quantity) => {
    const {expenditures} = this.subElements;
    const wrapper = document.createElement('div');
    wrapper.innerHTML = this.getExpenditureTEmplate(title, quantity);
    expenditures.append(wrapper.firstElementChild);
  }

  removeExpenditure = (event) => {
    const itemElement = event.target.closest('.ticket-edit__expenditure-item');
    if (itemElement){
      if (event.target.closest('[data-delete-handle]')) {
        itemElement.remove();
      }
    }
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
      const {ticketForm, expenditures} = this.subElements;
      const formData = new FormData(ticketForm);
      const data = {};

      const payloadFields = [
        'created',
        'closed',
        'description',
        'owner',
        'priority',
        'category',
        'status',
      ];

      const indexToText = [
        'owner',
        'priority',
        'category',
        'status',
      ];

      for (let [name, value] of formData) {
        if (name === 'closed' & !value) {
          value = null;
        }
        if (payloadFields.includes(name)) {
          data[name] = indexToText.includes(name) 
            ? ticketForm[name].options[ticketForm[name].selectedIndex].text
            : value;
        }
      }

      data.work_done = [...ticketForm.work_done.options].filter(option => option.selected).map(option => option.text);

      const deviceInventoryNumber = ticketForm.device.value.split(' ').pop();
      data.device = this.devices.find(device => device.inv_num === deviceInventoryNumber);

      const statusToBoolean = {
        'Активен': true,
        'Неактивен': false,
      }

      data.status = statusToBoolean[data.status];

      if (this.editMode) {
        data.id = parseInt(this.ticketId);
      }

      data.expenditures = [];

      const expenditureList = expenditures.querySelectorAll('.ticket-edit__expenditure-item');

      for (const expenditure of expenditureList) {
        data.expenditures.push({
          position: expenditure.dataset.expenditureTitle,
          quantity: parseInt(expenditure.dataset.expenditureQuantity),
        });
      }
      this.sendFormData(data);
    }
  }

  async sendFormData(data) {
    const fetchUrl = this.editMode 
      ? this.getFetchUrl(this.ticketUrl + '/' + this.ticketId + '/')
      : this.getFetchUrl(this.ticketUrl + '/');
    const key = localStorage.getItem('key');

    const requestParams = {
      method: this.ticketId ? 'PUT' : 'POST',
      headers:             {
        'Content-Type': 'application/json',
        'Authorization': `Token ${key}`,
      },
      body: JSON.stringify(data)
    }

    try {
      await fetchJson(fetchUrl, requestParams);
      const customEventName = (this.editMode) ? "ticket-updated" : "ticket-saved";
      this.element.dispatchEvent(new CustomEvent(customEventName, {
        bubbles: true,
      }));
    } catch(err) {
      const customEventName = 'ticket-error';
      this.element.dispatchEvent(new CustomEvent(customEventName, {
        bubbles: true,
      }));
    }
  }

  initEventListeners() {
    const addExpenditureButton = this.subElements["expenditureContainer"].lastElementChild;

    addExpenditureButton.addEventListener('click', this.showExpenditureForm);
    this.element.addEventListener('submit', this.onFormSubmit);
    this.element.addEventListener('click', this.removeExpenditure);
    document.addEventListener('new-expenditure', this.newExpenditure);
  }

  removeEventListeners() {
    const addExpenditureButton = this.subElements["expenditureContainer"].lastElementChild;

    addExpenditureButton.removeEventListener('click', this.showExpenditureForm);
    this.element.removeEventListener('submit', this.onFormSubmit);
    this.element.removeEventListener('click', this.removeExpenditure);
    document.removeEventListener('new-expenditure', this.newExpenditure);

  }

  remove() {
    this,this.removeEventListeners();
    this.element.remove();
  }

  destroy() {
    this.remove();
  }
}