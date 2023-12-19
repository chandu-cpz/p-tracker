import { API_URLS } from "@/constants";
import axios from "axios";

const list = API_URLS.split(",");
const api = list[Math.floor(Math.random() * list.length)];
axios.get(`${api}/scrape`);
