import SortableTable from '../../../components/sortable-table/index.js';
import SortPanel from '../../../components/sort-panel/index.js';
import header from './tickets-header.js';
import fetchJson from '../../../utils/fetch-json.js';

const BACKEND_URL = process.env.BACKEND_URL;
const TICKETS_URL = "api/tickets";


export default class Page {
  element;
  components = {};
  subElements = {};

  render() {
    const wrapper = document.createElement('div')
    wrapper.innerHTML = this.template;
    this.element = wrapper.firstElementChild;
    this.subElements = this.getSubElements(this.element);
    this.initComponents();
    this.renderComponents();
    this.modifyEmptyPlaceholder();
    this.initEventListeners();
    return this.element;
  }

  get template () {
    return `
    <div class="details">
      <div class="tickets-list">
        <div class="content__top-panel">
          <h1 class="page-title">Просмотр заявок</h1>
          <a href="/tickets/add" class="button-primary">Создать заявку</a>
        </div>
        <div data-element="sortPanel">
          <!-- sort-panel component -->
        </div>
        <div data-element="sortableTable">
          <!-- sortable-table component -->
        </div>
      </div>
    </div>`;
  }

  getSubElements (element) {
    const elements = element.querySelectorAll('[data-element]');

    return [...elements].reduce((accum, subElement) => {
      accum[subElement.dataset.element] = subElement;

      return accum;
    }, {});
  }

  initComponents() {
    const sortPanel = new SortPanel();
    const sortableTable = new SortableTable(header, {
      url: 'api/tickets/',
      href: '/tickets',
    });

    this.components.sortableTable = sortableTable;
    this.components.sortPanel = sortPanel;
  }

  renderComponents() {

    Object.keys(this.components).forEach(component => {
      const root = this.subElements[component];
      const { element } = this.components[component];
      root.append(element);
    })

  }

  modifyEmptyPlaceholder() {
    const { subElements } = this.components.sortableTable;
    const { emptyPlaceholder } = subElements;
    emptyPlaceholder.innerHTML = `
      <div>
        <p>Не найдено заявок, удовлетворяющих выбранному критерию</p>
        <button type="button" class="button-primary-outline">Очистить фильтры</button>
      </div>
    `;
  }

  initEventListeners() {
    const { subElements } = this.components.sortPanel;
    const { filterDescription ,filterInventory, filterStatus, filterDepartment } = subElements;

    const resetFiltersButton = this.element.querySelector(".button-primary-outline");

    for (const element of [filterDescription, filterInventory, filterStatus, filterDepartment]) {
      element.addEventListener("input", this.filterTickets);
    }

    resetFiltersButton.addEventListener("click", this.resetFilters);

    this.element.addEventListener('date-select', this.filterTickets);
  }

  removeEventListeners() {
    const { subElements } = this.components.sortPanel;
    const { filterDescription ,filterInventory, filterStatus } = subElements;

    const resetFiltersButton = this.element.querySelector(".button-primary-outline");

    for (const element of [filterDescription, filterInventory, filterStatus]) {
      element.removeEventListener("input", this.filterTickets);
    }

    resetFiltersButton.removeEventListener("click", this.resetFilters);

    this.element.removeEventListener('date-select', this.filterTickets);

  }

  filterTickets = async (event) => {
    const { type, detail } = event;

    if (type === "date-select") {
      const { from, to } = detail;
      this.dateFrom = from.toISOString();
      this.dateTo = to.toISOString();
    }
    
    // reset these values each time a filter is added or changed
    // in order to load data with filter each time from the beginning
    this.components.sortableTable.start = 0;
    this.components.sortableTable.end = 1 + this.components.sortableTable.step;
    
    const { sorted, start, end, element: sortableTableElem } = this.components.sortableTable;
    const { id, order } = sorted;
    
    sortableTableElem.classList.add("sortable-table_loading");
    
    const { subElements } = this.components.sortPanel;
    const { filterDescription, filterInventory, filterStatus, filterDepartment } = subElements;
    const { value: filterDescriptionValue } = filterDescription;
    const { value: filterInventoryValue} = filterInventory;
    const { value: filterStatusValue } = filterStatus;
    const filterDepartmentValue = filterDepartment.options[filterDepartment.selectedIndex].text

    const url = new URL(TICKETS_URL, BACKEND_URL);

    url.searchParams.set("date_gte", this.dateFrom);
    url.searchParams.set("date_lte", this.dateTo);

    url.searchParams.set("description_like", filterDescriptionValue);
    url.searchParams.set("inventory_like", filterInventoryValue);

    url.searchParams.set("status", filterStatusValue);
    url.searchParams.set("department", filterDepartmentValue);

    url.searchParams.set('sort', id);
    url.searchParams.set('order', order);
    url.searchParams.set('start', start);
    url.searchParams.set('end', end);
    
    this.components.sortableTable.filtered = {
      "date_gte": this.dateFrom,
      "date_lte": this.dateTo,
      "description_like": filterDescriptionValue,
      "inventory_like": filterInventoryValue,
      "status": filterStatusValue
    }

    const data = await fetchJson(url);
    this.components.sortableTable.addRows(data);

    sortableTableElem.classList.remove("sortable-table_loading");
  }

  resetFilters = (event) => {
    event.preventDefault();

    const { subElements } = this.components.sortPanel;
    const { filterDescription, filterInventory, filterStatus, filterDepartment } = subElements;


    filterDescription.value = "";
    filterInventory.value = "";
    filterStatus.value = "";
    filterDepartment.value = "";

    this.components.sortableTable.filtered = null;


    this.filterTickets(event);
  }

  destroy() {
    this.removeEventListeners();

    for (const component of Object.values(this.components)) {
      component.destroy();
    }

    this.element.remove();
  }
  
}