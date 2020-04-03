import Axios from "axios";
import Cookies from 'js-cookie'

const http = Axios.create({
  baseURL: "/api/v1",
	headers: {'X-CSRFToken': Cookies.get('csrftoken')}
});

export default http;