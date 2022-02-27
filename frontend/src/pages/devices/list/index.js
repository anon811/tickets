import SortableTable from '../../../components/sortable-table/index.js';
import header from './devices-header.js';
import fetchJson from '../../../utils/fetch-json.js';
import SortPanel from '../../../components/device-sort-panel/index.js';

const BACKEND_URL = process.env.BACKEND_URL;
const DEVICES_URL = "api/devices";


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
    <div class="device-details">
      <div class="devices-list">
          <div class="content__top-panel">
              <h1 class="page-title">Просмотр оборудования</h1>
              <a href="/devices/add" class="button-primary">Добавить устройство</a>
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
      url: 'api/devices/',
      href: '/devices',
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
        <p>Не найдено устройств, удовлетворяющих выбранному критерию</p>
        <button type="button" class="button-primary-outline">Очистить фильтры</button>
      </div>
    `;
  }

  initEventListeners() {
    const { subElements } = this.components.sortPanel;
    const { filterInventory, filterTitle, filterDepartment, filterType } = subElements;

    const resetFiltersButton = this.element.querySelector(".button-primary-outline");

    for (const element of [filterInventory, filterTitle, filterType, filterDepartment]) {
      element.addEventListener("input", this.filterDevices);
    }
    
    resetFiltersButton.addEventListener("click", this.resetFilters);
  }

  removeEventListeners() {
    const { subElements } = this.components.sortPanel;
    const { filterTitle, filterInventory,  filterDepartment, filterType} = subElements;

    const resetFiltersButton = this.element.querySelector(".button-primary-outline");

    for (const element of [filterTitle, filterInventory,  filterDepartment, filterType]) {
      element.removeEventListener("input", this.filterDevices);
    }

    resetFiltersButton.removeEventListener("click", this.resetFilters);

    return;
  }

  filterDevices = async (event) => {
    const { type, detail } = event;

    // reset these values each time a filter is added or changed
    // in order to load data with filter each time from the beginning
    this.components.sortableTable.start = 0;
    this.components.sortableTable.end = 1 + this.components.sortableTable.step;
    
    const { sorted, start, end, element: sortableTableElem } = this.components.sortableTable;
    const { id, order } = sorted;
    
    sortableTableElem.classList.add("sortable-table_loading");
    
    const { subElements } = this.components.sortPanel;
    const { filterInventory, filterTitle, filterDepartment, filterType } = subElements;
    const { value: filterInventoryValue } = filterInventory;
    const { value: filterTitleValue} = filterTitle;
    const filterDepartmentValue = filterDepartment.options[filterDepartment.selectedIndex].text
    const filterTypeValue = filterType.options[filterType.selectedIndex].text

    const url = new URL(DEVICES_URL, BACKEND_URL);

    url.searchParams.set("title_like", filterTitleValue);
    url.searchParams.set("inventory_like", filterInventoryValue);

    url.searchParams.set("type", filterTypeValue);
    url.searchParams.set("department", filterDepartmentValue);

    url.searchParams.set('sort', id);
    url.searchParams.set('order', order);
    url.searchParams.set('start', start);
    url.searchParams.set('end', end);
    
    // preserve this for server side sorting and for onscroll loading
    this.components.sortableTable.filtered = {
      "title_like": filterTitleValue,
      "inventory_like": filterInventoryValue,
      "type": filterTypeValue,
      "department": filterDepartmentValue,
    }

    const data = await fetchJson(url);
    this.components.sortableTable.addRows(data);

    sortableTableElem.classList.remove("sortable-table_loading");
  }

  resetFilters = (event) => {
    event.preventDefault();

    const { subElements } = this.components.sortPanel;
    const { filterInventory, filterTitle, filterType, filterDepartment} = subElements;


    filterInventory.value = "";
    filterTitle.value = "";
    filterType.value = "";
    filterDepartment.value = "";

    this.components.sortableTable.filtered = null;


    this.filterDevices(event);
    return;
  }

  destroy() {
    this.removeEventListeners();

    for (const component of Object.values(this.components)) {
      component.destroy();
    }

    this.element.remove();
  }
  
}