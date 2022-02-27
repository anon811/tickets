const header = [
  {
    id: 'id',
    title: 'ID',
    sortable: true,
    sortType: 'number' 
  },
  {
    id: 'priority',
    title: 'Приоритет',
    sortable: true,
    sortType: 'string'
  },
  {
    id: 'created',
    title: 'Дата создания',
    sortable: true,
    sortType: 'string'
  },
  {
    id: 'description',
    title: 'Описание',
    sortable: false,
  },
  {
    id: 'device',
    title: 'Оборудование',
    sortable: false,
    template: data => {
      return `
      <div class="sortable-table__cell">
      ${data.title}
      </div>`;
    }
  },
  {
    id: 'device',
    title: 'Учреждение',
    sortable: true,
    sortType: 'string',
    template: data => {
      return `
      <div class="sortable-table__cell">
      ${data.department}
      </div>`;
    }
  },
];

export default header;
