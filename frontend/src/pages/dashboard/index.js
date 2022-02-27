import RangePicker from '../../components/range-picker/index.js';
import SortableTable from '../../components/sortable-table/index.js';
import ColumnChart from '../../components/column-chart/index.js';
import header from './tickets-header.js';
import fetchJson from '../../utils/fetch-json.js';


export default class Page {
  element;
  subElements = {};
  components = {};

  async render () {
    const element = document.createElement('div');
    element.innerHTML = this.template;
    this.element = element.firstElementChild;

    this.subElements = this.getSubElements(this.element);

    await this.initComponents();

    this.renderComponents();
    this.initEventListeners();

    return this.element;
  }

  async initComponents () {
    const to = new Date();
    const from = new Date(to.getTime() - (30 * 24 * 60 * 60 * 1000));
    const [ticketsOpenedData, ticketsClosedData] = await this.getDataForColumnCharts(from, to);

    const rangePicker = new RangePicker({
      from,
      to
    });

    const sortableTable = new SortableTable(header, {
      url: `api/tickets/?status=1`,
      href: '/tickets',
      isSortLocally: true
    });

    const ticketsOpenedChart = new ColumnChart({
      data: ticketsOpenedData,
      label: 'Открыто заявок',
      value: Object.values(ticketsOpenedData).reduce((accum, item) => accum + item, 0),
      link: '/tickets'
    });

    const ticketsClosedChart = new ColumnChart({
      data: ticketsClosedData,
      label: 'Закрыто заявок',
      value: Object.values(ticketsClosedData).reduce((accum, item) => accum + item, 0),
      link: '/tickets'
    });

    this.components.sortableTable = sortableTable;
    this.components.rangePicker = rangePicker;
    this.components.ticketsOpenedChart = ticketsOpenedChart;
    this.components.ticketsClosedChart = ticketsClosedChart;
  }

  renderComponents () {
    Object.keys(this.components).forEach(component => {
      const root = this.subElements[component];
      const { element } = this.components[component];

      root.append(element);
    });
  }

  get template () {
    return `<div class="dashboard">
      <div class="content__top-panel">
        <h2 class="page-title">Сводка</h2>
        <!-- RangePicker component -->
        <div data-element="rangePicker"></div>
      </div>
      <div data-element="chartsRoot" class="dashboard__charts">
        <!-- column-chart components -->
        <div data-element="ticketsOpenedChart" class="dashboard__chart_opened"></div>
        <div data-element="ticketsClosedChart" class="dashboard__chart_close"></div>
      </div>

      <h3 class="block-title"></h3>

      <div data-element="sortableTable">
        <!-- sortable-table component -->
      </div>
    </div>`;
  }

  async getDataForColumnCharts (from, to) {
    const requests = [];
    const TICKETS_OPENED = `${process.env.BACKEND_URL}api/dashboard?date_gte=${from.toISOString()}
                            &date_lte=${to.toISOString()}&status=1`;
    const TICKETS_CLOSED = `${process.env.BACKEND_URL}api/dashboard?date_gte=${from.toISOString()}
                            &date_lte=${to.toISOString()}&status=0`;

    const ticketsOpenedResponse = await fetchJson(TICKETS_OPENED);
    const ticketsClosedResponse = await fetchJson(TICKETS_CLOSED);

    requests.push(ticketsOpenedResponse);
    requests.push(ticketsClosedResponse);

    return Promise.all(requests);
  }

  updateChartsComponents = async event => {
    const { from, to } = event.detail;
    const columnChartNames = [];
    const cssClassList = ["column-chart_loading"];
    this.updateCssClass(columnChartNames, "add", cssClassList);

    const [ticketsOpenedData, ticketsClosedData] = await this.getDataForColumnCharts(from, to);
    const ticketsOpenedTotal = Object.values(ticketsOpenedData).reduce((accum, item) => accum + item, 0);
    const ticketsClosedTotal = Object.values(ticketsClosedData).reduce((accum, item) => accum + item, 0);
    // Update charts

    this.components.ticketsOpenedChart.update({headerData: ticketsOpenedTotal , bodyData: ticketsOpenedData});
    this.components.ticketsClosedChart.update({headerData: ticketsClosedTotal, bodyData: ticketsClosedData});

    this.updateCssClass(columnChartNames, "remove", cssClassList);
  }

  updateCssClass(componentNamesList, action, classNameList) {
    for (const componentName of componentNamesList) {
      const {element} = this.components[componentName];

      for (const className of classNameList) {
        switch (action) {
          case "add":
            element.classList.add(className);
            break;
          case "remove":
            element.classList.remove(className);
            break;
        }
      }
    }
  }

  getSubElements ($element) {
    const elements = $element.querySelectorAll('[data-element]');

    return [...elements].reduce((accum, subElement) => {
      accum[subElement.dataset.element] = subElement;

      return accum;
    }, {});
  }

  initEventListeners () {
    this.components.rangePicker.element.addEventListener('date-select', this.updateChartsComponents);
  }

  removeEventListeners() {
    this.components.rangePicker.element.removeEventListener('date-select', this.updateChartsComponents);
  }

  destroy () {
    this.removeEventListeners();

    for (const component of Object.values(this.components)) {
      component.destroy();
    }

    this.element.remove();
  }
}
