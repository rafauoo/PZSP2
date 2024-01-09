function formatDate(dateString) {
  const options = {day: 'numeric', month: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric'};
  return new Date(dateString).toLocaleDateString('en-GB', options);
}

export default formatDate;