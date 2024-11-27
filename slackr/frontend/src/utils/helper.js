/**
 * Clear all child of a DOM element
 * @param {*} child
 */
export function clearDom(child) {
  while(child.firstChild) child.removeChild(child.firstChild);
}

// Conver ISO string to time - date format
export function dataAndTime(iso) {
  const date = new Date(iso);
  
  const newDate = date.toLocaleDateString();
  const newTime = date.toLocaleTimeString();

  return `${newTime} - ${newDate}`
}