import fetchJson from '../../utils/fetch-json'

const BACKEND_URL = process.env.BACKEND_URL;
const POSITIONS_URL = 'api/positions'


export default class ExpenditureForm {
  element;
  subElements;

  constructor() {
    this.render();
    this.initEventListeners();
  }

  render() {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = this.getTemplate();
    this.element = wrapper.firstElementChild;
    this.subElements = this.getSubElements();
    return this.element;
  }

  show() {
    // document.body.style.overflowY = 'hidden';
    let container = document.querySelector('.expenditure-form-container');
    container.style.display = "block";
  }

  getTemplate() {
    return `
    <div class="expenditure-form-container form-inline">
      <div class="expenditure-form">
        <form id="expenditure" class="form-grid" data-element="expenditureForm">

          <div class="form-group form-group__half_left">
            <fieldset>
              <label class="form-label">Позиция на складе</label>
              <input  class="form-control" autocomplete="off" list="positions" name="title" type="text" data-element="expenditureTitle">
            </fieldset>
          </div>

          <div class="form-group form-group__half_left">
            <fieldset>
              <label class="form-label">Количество</label>
              <input class="form-control" name="quantity" type="number" data-element="expenditureQt">
            </fieldset>
          </div>

          <div class="form-buttons">
            <button type="submit" name="save" class="button-primary-outline" data-element="btnSubmit">
              Добавить расход
            </button>

            <button type="submit" name="cancel" class="button-primary-outline" data-element="btnCancel">
              Отмена
            </button>
          </div>

          <datalist id="positions" data-element="positionsDatalist">
          </datalist>
          
        </form>
      </div>
    </div>
    `;
  }

  initEventListeners() {
    const {expenditureTitle, btnSubmit, btnCancel} = this.subElements;
    expenditureTitle.addEventListener('input', this.onInput);
    expenditureTitle.addEventListener('change', this.onChange);
    btnSubmit.addEventListener('click', this.onSubmit);
    btnCancel.addEventListener('click', this.onCancel);
  }

  removeEventLIsteners() {
    const {expenditureTitle, btnSubmit, btnCancel} = this.subElements;
    expenditureTitle.removeEventListener('click', this.onInput);
    btnSubmit.removeEventListener('click', this.onCancel);
    btnSubmit.removeEventListener('click', this.onSubmit);
  }

  onInput = async (event) => {
    const {expenditureTitle, positionsDatalist} = this.subElements;
    const data = await this.searchPosition(expenditureTitle.value);
    positionsDatalist.innerHTML =  data.map(item => {
     return `<option value="${item.title}" data-quantity="${item.quantity}">`
    }).join('');
  }

  onChange = event => {
    const {positionsDatalist, expenditureQt, expenditureTitle} = this.subElements;
    const title = event.target.value;
    const maxQuantity = positionsDatalist.querySelector(`[value="${title}"]`).dataset.quantity;
    expenditureQt.setAttribute('min', 1);
    expenditureQt.setAttribute('max', maxQuantity);
  }

  validateForm() {
    const {expenditureForm} = this.subElements;
    if (expenditureForm.checkValidity()){
      return true;
    } else {
      expenditureForm.reportValidity();
      return false;
    }
  }

  onSubmit = (event) => {
    event.preventDefault();

    if (this.validateForm()) {
      this.element.dispatchEvent(new CustomEvent('new-expenditure', {
        bubbles: true,
        detail: {
          title: this.subElements.expenditureForm.title.value,
          quantity: this.subElements.expenditureForm.quantity.value,
        },
      }));

      this.remove()
    }
  }

  async searchPosition(positionTitleContains) {
    const url = new URL(POSITIONS_URL, BACKEND_URL);
    url.searchParams.set('contains', positionTitleContains);
    const data =  await fetchJson(url);
    return data;
  }

  onCancel = (event) => {
    this.remove();
  }

  getSubElements() {
    const elements = this.element.querySelectorAll('[data-element]');

    return [...elements].reduce((accum, subElement) => {
      accum[subElement.dataset.element] = subElement;

      return accum;
    }, {});
  }

  remove() {
    this.removeEventLIsteners();
    this.element.remove();
  }

  destroy() {
    this.remove();
  }
}