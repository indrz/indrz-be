export const getFormattedDate = (format = 'yyyy-mm-dd', separator = '-', date = new Date()) => {
  const dateObj = {};
  const position = format.split(separator);
  let dd = date.getDate();
  let mm = date.getMonth() + 1; // January is 0!

  dateObj.yyyy = date.getFullYear();

  if (dd < 10) {
    dd = '0' + dd;
  }
  if (mm < 10) {
    mm = '0' + mm;
  }
  dateObj.dd = dd;
  dateObj.mm = mm;

  return `${dateObj[position[0]]}${separator}${dateObj[position[1]]}${separator}${dateObj[position[2]]}`;
};
export const getGeomFromCoordinates = (coordinates) => {
  return `SRID=3857;MULTILINESTRING((${coordinates[0].join(' ')},${coordinates[1].join(' ')}))`;
};

export default {
  getFormattedDate,
  getGeomFromCoordinates
}
