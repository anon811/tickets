import escapeHtml from '../../utils/escape-html.js';
import fetchJson from '../../utils/fetch-json.js';

const BACKEND_URL = process.env.BACKEND_URL;

export default class PositionForm {
  positionId;
  editMode;
  element;
  positionData = null;
  positionUrl = 'api/positions';

  constructor(positionId) {
    this.positionId = positionId;
    this.editMode = Boolean(this.positionId);
  }

  async render() {
    if (this.editMode) {
      this.positionData = await this.getPositionData();
    } 

    const wrapper = document.createElement('div');
    wrapper.innerHTML = this.getPositionFormTemplate(this.positionData)
    const element = wrapper.firstElementChild;
    this.element = element;

    this.subElements = this.getSubElements();

    this.initEventListeners();

    return this.element;
  }

  async getPositionData() {
    const positionrequest = this.getSingleData(this.positionUrl + '/' + this.positionId);
    const data = await positionrequest;
    return data;
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

  getPositionFormTemplate(positionData) {
    console.log(positionData)
    return `
      <div class="position-form">
        <form data-element="positionForm" class="form-grid">
          ${this.getTitleTemplate(positionData? positionData.title : positionData)}
          ${this.getQuantityTemplate(positionData? positionData.quantity : positionData)}
          <div class="form-buttons">
            <button type="submit" name="save" class="button-primary-outline">
              Сохранить
            </button>
          </div>
        </form>
      </div>
    `;
  }

  getTitleTemplate(title) {
    return `
      <div class="form-group form-group__half_left">
        <fieldset>
          <label class="form-label">Наименование позиции:</label>
          <input required="" 
            name="title" 
            class="form-control" 
            data-element="positionTitle"
            value="${title? escapeHtml(title) : ''}" autocomplete="off">
        </fieldset>
      </div>
    `;
  }

  getQuantityTemplate(quantity) {
    return `
    <div class="form-group form-group__half_left">
      <label class="form-label">Количество</label>
      <input required="" 
        type="number" 
        class="form-control" 
        name="quantity"
        data-element="positionQuantity" 
        value="${quantity? quantity : ''}"
      </input>
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

  onFormSubmit = (event) => {
    event.preventDefault();

    const key = localStorage.getItem('key');

    if (!key || key === 'null') {
      const customEventName = 'non-authorized';
      this.element.dispatchEvent(new CustomEvent(customEventName, {
        bubbles: true,
      }));
    } else {
      const {positionForm} = this.subElements;
      const formData = new FormData(positionForm);
      const data = {};

      const payloadFields = [
        'title',
        'quantity',
      ];

      for (let [name, value] of formData) {
        if (payloadFields.includes(name)) {
          data[name] = value;
        }
      }

      if (this.editMode) {
        data.id = parseInt(this.positionId);
      }

      this.sendFormData(data);
    }
  }

  async sendFormData(data) {
    const fetchUrl = this.editMode 
      ? this.getFetchUrl(this.positionUrl + '/' + this.positionId + '/')
      : this.getFetchUrl(this.positionUrl + '/');
    const key = localStorage.getItem('key');

    const requestParams = {
      method: this.positionId ? 'PUT' : 'POST',
      headers:             {
        'Content-Type': 'application/json',
        'Authorization': `Token ${key}`,
      },
      body: JSON.stringify(data)
    }

    try {
      await fetchJson(fetchUrl, requestParams);
      const customEventName = (this.editMode) ? "position-updated" : "position-saved";
      this.element.dispatchEvent(new CustomEvent(customEventName, {
        bubbles: true,
      }));
    } catch(err) {
      const customEventName = 'position-error';
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
    this.removeEventListeners();
    this.element.remove();
  }

  destroy() {
    this.remove();
  }
}