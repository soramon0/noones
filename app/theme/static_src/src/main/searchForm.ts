import { handleCountryChange, setCities } from "./utils";

document.addEventListener('DOMContentLoaded', () => {
	const countryField = document.querySelector<HTMLSelectElement>('#id_country')
	const cityField = document.querySelector('#id_city')
  const { value, text } = countryField.selectedOptions[0];
  
  setCities(value, text, cityField);
  handleCountryChange();
})

