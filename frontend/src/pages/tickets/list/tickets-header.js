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
    sortable: false,
  },
  {
    id: 'owner',
    title: 'Исполнитель',
    sortable: true,
    sortType: 'string',
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
      ${data.title}, Инв. №${data.inv_num}
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
  {
    id: 'category',
    title: 'Категория',
    sortable: true,
    sortType: 'string'
  }
];

export default header;
